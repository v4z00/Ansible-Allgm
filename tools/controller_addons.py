"""Declarative Git add-on registration, verified path mapping and ownership."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess

import staging_manifest as manifest

NAME = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")
HEX = re.compile(r"[0-9a-f]{64}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def registrations(lines):
    """Other comments and four-field module rows are passive legacy state."""
    names = {}
    for line in lines:
        stripped = line.strip()
        if not re.match(r"^#\s*addon\s*=", stripped):
            continue
        name = stripped.split("=", 1)[1].strip()
        require(NAME.fullmatch(name) and name.casefold() not in names,
                "Invalid or duplicate # addon=NAME registration")
        names[name.casefold()] = name
    return names


def assignments(values):
    result = {}
    for value in values:
        name, equals, setting = value.partition("=")
        key = name.casefold()
        require(equals and NAME.fullmatch(name) and setting and key not in result,
                "Expected a single NAME=VALUE for each add-on")
        result[key] = setting
    return result


def receipt(path):
    if not path.exists() and not path.is_symlink():
        return {}
    require(path.is_file() and not path.is_symlink(), "Invalid controller receipt")
    data = manifest.load(path)
    require(isinstance(data, dict) and data.get("schema") in (1, 2)
            and isinstance(data.get("files"), dict), "Invalid controller receipt")
    if data["schema"] == 2:
        owners, modules = data.get("owners"), data.get("modules")
        require(isinstance(owners, dict) and set(owners) == set(data["files"])
                and isinstance(modules, dict) and "Allgm" in modules
                and all(isinstance(owner, str) and owner in modules for owner in owners.values()),
                "Malformed controller module ownership")
        for name, meta in modules.items():
            require(NAME.fullmatch(name) and isinstance(meta, dict)
                    and meta.get("kind") in ("base", "profile", "addon")
                    and isinstance(meta.get("version"), str), "Invalid installed module")
    return data


def installed(receipt_data):
    return {n.casefold(): n for n, meta in receipt_data.get("modules", {}).items()
            if meta["kind"] == "addon"}


def checked_path(value):
    require(isinstance(value, str), "Add-on paths must be strings")
    path = PurePosixPath(value)
    require(path.parts and not path.is_absolute() and path.as_posix() == value
            and all(p not in {".", ".."} and manifest.PART.fullmatch(p)
                    and not p.startswith(".") for p in path.parts), "Invalid add-on path")
    return value


def reserve(path, paths, directories):
    """Reject exact, case-only and file/directory collisions, including parent aliases."""
    key = path.casefold()
    require(key not in paths and key not in directories, f"Module path collision: {path}")
    for parent in PurePosixPath(path).parents:
        if parent == PurePosixPath("."):
            break
        spelling = parent.as_posix()
        folded = spelling.casefold()
        require(folded not in paths and directories.get(folded, spelling) == spelling,
                f"Module directory collision: {path}")
        directories[folded] = spelling
    paths.add(key)


def descriptor(source, name):
    entries = manifest.verify_addon(source, name)
    for rel, entry in entries.items():
        path = source / rel
        require(not any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(source))
                and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
                and bool(path.stat().st_mode & stat.S_IXUSR) == (entry["mode"] == "0755"),
                f"Add-on working tree differs from Git: {rel}")
    require("controller-addon.json" in entries and "VERSION.txt" in entries, "Missing add-on metadata")
    meta = manifest.load(source / "controller-addon.json")
    require(isinstance(meta, dict) and meta.get("schema") == 1 and meta.get("kind") == "addon"
            and meta.get("name") == name and meta.get("replaces") == []
            and meta.get("authentication", "anonymous") in {"anonymous", "token-file"},
            "Invalid add-on descriptor or module name")
    payload, exports = meta.get("payload"), meta.get("exports", {})
    require(isinstance(payload, list) and isinstance(exports, dict), "Invalid payload/exports")
    prefix = meta.get("mount_prefix", "")
    if prefix:
        checked_path(prefix)
        require(prefix.partition("/")[0] in {"playbooks", "roles"} and "/" in prefix,
                "An add-on mount needs a dedicated playbook or role directory")
    mapping = {}
    for value in payload:
        require(isinstance(value, str), "Invalid add-on payload entry")
        directory = value.endswith("/")
        path = checked_path(value[:-1] if directory else value)
        matches = [r for r in entries if r.startswith(path + "/")] if directory else [path]
        require(matches, f"Empty add-on payload directory: {path}")
        for rel in matches:
            require(rel in entries and rel not in mapping and not rel.startswith(".")
                    and rel not in {"controller-addon.json", "VERSION.txt"}, "Invalid or duplicate payload")
            target = prefix + "/" + rel if prefix else rel
            require(target.partition("/")[0] in {"playbooks", "roles"}
                    and manifest.allowed(target), f"Invalid mounted code path: {target}")
            mapping[rel] = target
    for rel, target in exports.items():
        checked_path(rel)
        checked_path(target)
        require(rel in entries and rel not in mapping and (
                re.fullmatch(r"bin/control\.d/[A-Za-z0-9_-]+\.(json|sh|py)", target)
                or re.fullmatch(r"descriptions/(commands|configurations|playbooks|roles)/[A-Za-z0-9_.-]+\.md", target)
            ) and manifest.allowed(target), "Invalid registry or description export")
        mapping[rel] = target
    require(mapping, "Empty add-on")
    return meta, mapping


def combine(base_files, base_owners, addons):
    combined, owners = dict(base_files), dict(base_owners)
    occupied, directories = set(), {}
    for target in combined:
        reserve(target, occupied, directories)
    for name, (root, _, mapping) in addons.items():
        for rel, target in mapping.items():
            reserve(target, occupied, directories)
            combined[target], owners[target] = root / rel, name
    return combined, owners


def module_info(sources, addons, version, branch=None):
    result = {}
    for name, source in sources.items():
        commit = None
        if (source / ".git").exists():
            cmd = subprocess.run(["git", "-C", str(source), "rev-parse", "--verify", "HEAD"],
                                 capture_output=True, text=True, check=True)
            commit = cmd.stdout.strip()
        result[name] = {"kind": "addon" if name in addons else "base" if name == "Allgm" else "profile",
                        "version": version(source, branch), "commit": commit}
    return result


def legacy_paths(base, combined, owners):
    file = base / "update_check/legacy_sss.json"
    if not file.is_file():
        return None, set()
    spec = manifest.load(file)
    require(spec.get("schema") == 1 and isinstance(spec.get("files"), list)
            and NAME.fullmatch(spec["module"]) and NAME.fullmatch(spec["feature"]),
            "Invalid legacy migration metadata")
    retired = set()
    for rel in spec["files"]:
        checked_path(rel)
        require(manifest.allowed(rel), "Invalid legacy migration path")
        if rel not in combined or owners.get(rel) == spec["module"]:
            retired.add(rel)
    return spec, retired


def installation_guards(dest, base, combined, owners, modules, previous, baseline,
                        sha, safe_path, settings):
    """Only attested old paths may change hands. Never adopt an unowned path."""
    active = {n for n, meta in modules.items() if meta["kind"] == "addon"}
    spec, legacy = legacy_paths(base, combined, owners)
    prior = installed(previous)
    require(set(prior) <= {name.casefold() for name in active},
            "An installed add-on is missing from the update. Restore its registration and source.")
    old_owners = previous.get("owners", {})
    conflicts = []
    retired = set()
    if legacy and spec["module"].casefold() not in prior and spec["module"] not in active:
        values, errors = settings(dest)
        features = values.get("features", {})
        if (errors and legacy.intersection(baseline) or not isinstance(features, dict)
                or features.get(spec["feature"], False) is not False):
            conflicts.append(f"Active or unresolved legacy feature: register {spec['module']} before updating")
    for rel in legacy | {p for p, n in owners.items() if n in active}:
        path = safe_path(dest, rel)
        if path.exists() and not path.is_file():
            conflicts.append(rel)
            continue
        exists = path.is_file()
        old = baseline.get(rel)
        old_owner = old_owners.get(rel)
        owner = owners.get(rel)
        legacy_owner = old_owner in (None, "Allgm")
        if rel in legacy and legacy_owner:
            if exists and (old is None or sha(path) != old) or not exists and old is not None:
                conflicts.append(rel)
            elif rel not in combined and old is not None:
                retired.add(rel)
            continue
        if owner in active and (exists or old is not None):
            if old_owner != owner or old is None or not exists or sha(path) != old:
                conflicts.append(rel)
    for rel, old_owner in old_owners.items():
        if old_owner not in prior.values():
            continue
        if rel in combined and owners[rel] != old_owner:
            conflicts.append(rel)
        elif rel not in combined:
            path = safe_path(dest, rel)
            if not path.is_file() or sha(path) != baseline.get(rel):
                conflicts.append(rel)
            else:
                retired.add(rel)
    return sorted(set(conflicts)), retired
