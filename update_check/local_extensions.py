"""Read-only SHA-256 inventory of separately installed controller extensions."""
import hashlib
import json
import os
import shlex
import sys
from pathlib import Path
import re
import stat

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from controller_i18n import status_text, tr

HEX = re.compile(r"[0-9a-f]{64}\Z")
IDENT = re.compile(r"[a-f0-9]{32}\Z")
PART = re.compile(r"[a-zA-Z0-9_-][a-zA-Z0-9._-]*\Z")
KEEP = "keep"
ONCE = "archive-after-success"
LEGACY_CLEANUP = {"behalten": KEEP, "nach-erfolg-archivieren": ONCE}
MIGRATION_REQUIRED = "MIGRATION_REQUIRED"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalize_cleanup(value, schema=None):
    require(isinstance(value, str), tr("extension.invalid_file"))
    if schema in (None, 1) and value in LEGACY_CLEANUP:
        return LEGACY_CLEANUP[value]
    require(schema in (None, 2) and value in (KEEP, ONCE), tr("extension.invalid_file"))
    return value


def policy(path):
    with regular(path).open("rb") as stream:
        first = stream.readline(256).strip()
        marker = stream.readline(256).strip() if first == b"---" or first.startswith(b"#!") else first
        cleanup = stream.readline(256).strip()
    markers = {b"# manuell-integriert: ja": (b"# bereinigung: ", 1),
               b"# manually-integrated: yes": (b"# cleanup: ", 2)}
    require(marker in markers, tr("extension.marker_required"))
    prefix, schema = markers[marker]
    require(cleanup.startswith(prefix), tr("extension.cleanup_header"))
    value = cleanup[len(prefix):].decode("ascii", errors="replace")
    return normalize_cleanup(value, schema)


def migration_hint(controller):
    tool = controller / "tools/migrate_local_extensions.py"
    if not tool.is_file() or tool.is_symlink():
        # During the first upgrade the installed controller may not yet ship the migrator.
        tool = Path(__file__).resolve().parents[1] / "tools/migrate_local_extensions.py"
    return shlex.join(["python3", str(tool), "--controller", str(controller), "--check"])


def require_compatible(report, metadata, *, rollback=False):
    if report["status"] == "NICHT_EINGERICHTET":
        return
    require(isinstance(metadata, dict), tr("extension.target_schema"))
    if report.get("layout") == "internal":
        require("internal" in metadata.get("local_extension_layouts", []), tr("extension.target_layout"))
    supported = metadata.get("local_extension_schema", 1)
    require(type(supported) is int and supported in (1, 2), tr("extension.target_schema"))
    if (rollback and report["status"] == MIGRATION_REQUIRED and report.get("integrity_status") == "OK"
            and supported == 1):
        return
    require(passed(report), report.get("migration_command") or tr("package.local_digest"))
    require(supported == report.get("schema"), tr("extension.rollback_register"))


def supplement_name(value):
    require(isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9-]{0,63}", value),
            tr("extension.invalid_name"))
    return value


def path_in(root, relative):
    require(isinstance(relative, str) and all(PART.fullmatch(p) for p in relative.split("/")),
            tr("extension.invalid_path"))
    current = root
    require(not root.is_symlink(), tr("extension.root_link"))
    for part in relative.split("/"):
        current = current / part
        require(not current.is_symlink(), tr("extension.linked_entry"))
    return current


def regular(path):
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, tr("extension.regular_file"))
    return path


def sha(path):
    digest = hashlib.sha256()
    with regular(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path):
    def unique(pairs):
        result = dict(pairs)
        require(len(result) == len(pairs), tr("extension.duplicate_key"))
        return result
    return json.loads(regular(path).read_text(encoding="utf8"), object_pairs_hook=unique)


def location(controller):
    legacy = controller.with_name(controller.name + "-local")
    internal = controller / ".local/extensions"
    if internal.exists() or internal.is_symlink():
        require(not legacy.exists() and not legacy.is_symlink(), tr("extension.ambiguous_location"))
        return internal
    return legacy


def marker(controller):
    directory = controller / ".local"
    require(not directory.is_symlink(), tr("extension.state_link"))
    return directory / "local-extension-id"


def checksum_line(value):
    return value + "  datei\n"


def archive_proof(root, name, entry):
    history = entry["archive"]
    require(isinstance(history, str) and IDENT.fullmatch(history), tr("extension.archive_id"))
    directory = path_in(root, "archiv/" + history)
    proof = read_json(path_in(directory, "BELEG.json"))
    expected = entry["sha256"]
    require(proof["path"] == name and proof["approved_sha256"] == proof["archived_sha256"] == expected
            and proof["run"]["sha256"] == expected and proof["run"]["exit_code"] == 0
            and proof["run"]["path"] == name, tr("extension.wrong_receipt"))
    require(regular(path_in(directory, "SHA256SUMS")).read_text() == checksum_line(expected)
            and sha(path_in(directory, "datei")) == expected, tr("extension.archive_digest"))
    return proof


def overlaps_managed(paths, local_name):
    """Compare the candidate's code paths without opening any site files."""
    local = tuple(local_name.casefold().split("/"))
    reserved = [local]
    if "roles" in local[:-1]:
        reserved.append(("roles", local[local.index("roles") + 1]))
    for path in paths:
        candidate = tuple(path.casefold().split("/"))
        for name in reserved:
            common = min(len(name), len(candidate))
            if name[:common] == candidate[:common]:
                return True
    return False


def prospective_conflicts(paths, local_files):
    return [row["path"] for row in local_files if row["status"] == "OK"
            and overlaps_managed(paths, row["path"])]


def overlaps_base(controller, name):
    parts = Path(name).parts
    if "roles" in parts[:-1]:
        # Ansible also finds roles relative to a playbook. A role owns its whole directory.
        role = controller / "roles" / parts[parts.index("roles") + 1]
        if role.exists() or role.is_symlink():
            return True
    target = controller / name
    return target.exists() or target.is_symlink()


def scan(root, expected_id=None, controller=None, *, delivery=False):
    register = read_json(path_in(root, "register.json"))
    require(isinstance(register, dict) and type(register.get("schema")) is int
            and register["schema"] in (1, 2)
            and isinstance(register.get("id"), str) and IDENT.fullmatch(register["id"])
            and isinstance(register.get("files"), dict), tr("extension.invalid_register"))
    require(expected_id in (None, register["id"]), tr("extension.wrong_register"))
    if "supplement" in register:
        supplement_name(register["supplement"])
    code = path_in(root, "code")
    require(code.is_dir(), tr("extension.missing_code"))
    actual = set()
    def fail(error):
        raise error
    for current, dirs, names in os.walk(code, onerror=fail):
        for item in dirs + names:
            path = Path(current) / item
            if delivery and item == ".DS_Store" and item in names:
                regular(path)  # Finder metadata is never copied into the registered code.
                continue
            rel = path.relative_to(code).as_posix()
            path_in(code, rel)
            if item in names:
                actual.add(rel)
    rows = []
    for name in sorted(actual | set(register["files"])):
        path = path_in(code, name)
        entry = register["files"].get(name)
        row = {"path": name}
        status = "NICHT_REGISTRIERT"
        if name in register["files"]:
            require(isinstance(entry, dict) and isinstance(entry.get("sha256"), str) and HEX.fullmatch(entry["sha256"]),
                    tr("extension.invalid_file"))
            cleanup = normalize_cleanup(entry.get("cleanup"), register["schema"])
            if "supplement" in entry:
                row["supplement"] = supplement_name(entry["supplement"])
            row["approved_sha256"] = entry["sha256"]
            if "archive" in entry:
                archive_proof(root, name, entry)
                require(cleanup == ONCE, tr("extension.invalid_file"))
                status = "ARCHIVIERT" if name not in actual else "ARCHIVIERUNG_OFFEN"
            elif name not in actual:
                status = "FEHLT"
            else:
                row["measured_sha256"] = sha(path)
                status = "OK" if row["measured_sha256"] == entry["sha256"] else "SHA_ABWEICHUNG"
                if status == "OK" and policy(path) != cleanup:
                    status = "POLICY_MISMATCH"
        if status == "OK" and controller and overlaps_base(controller, name):
            status = "BASIS_KONFLIKT"
        row["status"] = status
        rows.append(row)
    integrity = "OK" if all(row["status"] in ("OK", "ARCHIVIERT") for row in rows) else "PRUEFBEDARF"
    report = {"status": integrity, "integrity_status": integrity, "schema": register["schema"], "files": rows}
    if controller is not None and not delivery and register["schema"] == 1:
        report["migration_command"] = migration_hint(controller)
        if integrity == "OK":
            report["status"] = MIGRATION_REQUIRED
    return report


def inspect(controller):
    try:
        root = location(controller)
        pin = marker(controller)
        if not root.exists() and not root.is_symlink() and not pin.exists() and not pin.is_symlink():
            return {"status": "NICHT_EINGERICHTET", "files": []}
        for path in (root, regular(pin), regular(path_in(root, "register.json"))):
            attributes = path.lstat()
            require(attributes.st_uid == os.geteuid() and not (attributes.st_mode & 0o022),
                    tr("extension.permissions"))
        identifier = regular(pin).read_text().strip()
        require(IDENT.fullmatch(identifier), tr("extension.invalid_registration"))
        report = scan(root, identifier, controller)
        report["layout"] = "internal" if root == controller / ".local/extensions" else "sibling"
        return report
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        return {"status": "FEHLER", "error": str(error), "files": []}


def passed(report):
    return report["status"] in ("OK", "NICHT_EINGERICHTET")


def display(report):
    print(tr("extension.heading"), status_text(report["status"]))
    for row in report["files"]:
        origin = tr("extension.supplement", name=row["supplement"]) if "supplement" in row else ""
        print(" ", status_text(row["status"]), row["path"] + origin)
        if row["status"] == "SHA_ABWEICHUNG":
            print(tr("extension.expected"), row["approved_sha256"], tr("extension.actual"), row["measured_sha256"])
    if "migration_command" in report:
        print(" ", report["migration_command"])
    if "error" in report:
        print(" ", report["error"])
