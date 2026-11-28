"""Plan explicitly reviewed PowerShell deployments on the Ansible controller."""

import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from ansible.errors import AnsibleFilterError


PROFILE_NAME = re.compile(r"[a-z][a-z0-9-]{0,47}")
COMPONENT = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_. -]{0,95}")
WINDOWS_DEVICE = re.compile(r"(?:CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(?:\.|$)", re.I)
CODE_SUFFIXES = {".ps1", ".psm1", ".psd1", ".ps1xml"}
PRIVATE_NAMES = {"secrets", "credentials", "config", "private", "state", "logs", "archive", "old", "x"}


def require(condition, message):
    if not condition:
        raise AnsibleFilterError(message)


def regular_file(path):
    require(not any(p.is_symlink() for p in (path, *path.parents)) and path.is_file(),
            "Profile sources must be regular files without symlink ancestors.")
    return path


def code_path(value):
    require(isinstance(value, str), "Relative PowerShell path required.")
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix() == value and len(path.parts) <= 8,
            "Relative PowerShell path required.")
    require(path.suffix.lower() in CODE_SUFFIXES, "Only PowerShell code can be deployed.")
    for part in path.parts:
        require(COMPONENT.fullmatch(part) and not part.endswith((".", " "))
                and not WINDOWS_DEVICE.match(part) and part.split(".")[0].lower() not in PRIVATE_NAMES,
                "Unsafe or private PowerShell path.")
    return path


def read_files(source):
    manifest = regular_file(source / "deployment.json")
    require(manifest.stat().st_size <= 256 * 1024, "Profile manifest exceeds the size limit.")
    try:
        document = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise AnsibleFilterError("Invalid profile manifest.") from None
    require(isinstance(document, dict) and set(document) == {"schema", "files"}
            and type(document["schema"]) is int and document["schema"] == 1,
            "Expected a schema 1 manifest.")
    require(isinstance(document["files"], list) and 1 <= len(document["files"]) <= 200,
            "Manifest requires an explicit list of 1 to 200 files.")
    files = []
    paths = set()
    total_size = 0
    for entry in document["files"]:
        require(isinstance(entry, dict) and set(entry) == {"path", "sha256"},
                "Each manifest entry requires path and sha256.")
        path = code_path(entry["path"])
        key = str(path).lower()
        require(key not in paths, "Case-insensitive file collision in profile.")
        paths.add(key)
        file = regular_file(source / path)
        size = file.stat().st_size
        total_size += size
        require(size <= 8 * 1024**2 and total_size <= 32 * 1024**2, "Profile exceeds the code size limit.")
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        require(digest == entry["sha256"], f"Approved source hash changed for {path}.")
        files.append({"path": str(path), "source": str(file), "sha256": digest})
    directory_paths = {str(parent).lower() for row in files
                       for parent in PurePosixPath(row["path"]).parents if parent != PurePosixPath(".")}
    require(not paths & directory_paths, "A profile directory collides with a file.")
    return sorted(files, key=lambda row: row["path"])


def scheduled_task(spec, files):
    fields = {"script", "triggers", "enabled", "multiple_instances", "record_job", "principal",
              "on_demand", "additional_profiles"}
    require(isinstance(spec, dict) and set(spec) <= fields,
            "Unsupported scheduled task field.")
    script = code_path(spec.get("script"))
    require(script.suffix.lower() == ".ps1" and str(script) in {row["path"] for row in files},
            "Scheduled entrypoint must be a PS1 from the approved manifest.")
    triggers = spec.get("triggers", [])
    enabled = spec.get("enabled", True)
    instances = spec.get("multiple_instances", 2)
    record = spec.get("record_job", True)
    principal = spec.get("principal", "")
    on_demand = spec.get("on_demand", False)
    additional = spec.get("additional_profiles", [])
    require(type(enabled) is bool and type(record) is bool and type(instances) is int and instances in range(4),
            "Invalid scheduler settings.")
    require(isinstance(principal, str) and (not principal or PROFILE_NAME.fullmatch(principal)),
            "Invalid private principal reference.")
    require(type(on_demand) is bool and isinstance(triggers, list)
            and all(isinstance(t, dict) for t in triggers) and bool(triggers) != on_demand,
            "Only scheduled tasks require triggers. On-demand profiles must omit them.")
    require(isinstance(additional, list) and len(additional) <= 31
            and all(isinstance(name, str) and PROFILE_NAME.fullmatch(name) for name in additional)
            and len(additional) == len(set(additional)), "Invalid additional task profiles.")
    require(not on_demand or (record and not additional and not principal),
            "On-demand tasks use the calling task's principal and require job recording.")
    require(not additional or record, "Additional task profiles require job recording.")
    return {"script": str(script), "triggers": triggers, "enabled": enabled,
            "multiple_instances": instances, "record_job": record, "principal": principal,
            "on_demand": on_demand, "additional_profiles": additional}


def plan(profiles, selected, source_root, mode):
    require(isinstance(profiles, dict) and isinstance(selected, list)
            and all(isinstance(n, str) and PROFILE_NAME.fullmatch(n) for n in selected),
            "Use a mapping of profiles and an explicit list of valid profile names.")
    require(len(selected) == len(set(selected)) and mode in ("local", "sysvol"),
            "Duplicate profiles or invalid deployment mode.")
    root = Path(source_root)
    require(root.is_absolute() and ".." not in root.parts, "An absolute controller source root is required.")
    result = []
    on_demand_profiles = set()
    for name in selected:
        spec = profiles.get(name)
        require(isinstance(spec, dict) and set(spec) <= {"scope", "task"},
                f"Invalid or unknown Windows profile {name}.")
        scope = spec.get("scope", "local")
        require(scope in ("local", "sysvol"), f"Invalid scope for profile {name}.")
        require(scope != "sysvol" or "task" not in spec, "SYSVOL profiles only contain files.")
        if scope != mode:
            continue
        files = read_files(root / name)
        task = scheduled_task(spec["task"], files) if "task" in spec else {}
        require(set(task.get("additional_profiles", [])) <= on_demand_profiles,
                f"Additional jobs for {name} must follow their on-demand profiles in the selection.")
        if task.get("on_demand"):
            on_demand_profiles.add(name)
        identity = json.dumps([(row["path"], row["sha256"]) for row in files])
        release = hashlib.sha256(identity.encode()).hexdigest()
        dirs = {str(parent) for row in files for parent in PurePosixPath(row["path"]).parents
                if parent != PurePosixPath(".")}
        result.append({"name": name, "files": files, "task": task, "release": release,
                       "directories": sorted(dirs, key=lambda p: (p.count("/"), p))})
    return result


def windows_path(path, root):
    return root if path == "." else root + "\\" + path.replace("/", "\\")


def windows_paths(paths, root):
    return [windows_path(path, root) for path in paths]


class FilterModule:
    def filters(self):
        return {
            "windows_script_profile_plan": plan,
            "windows_script_profile_path": windows_path,
            "windows_script_profile_paths": windows_paths,
        }
