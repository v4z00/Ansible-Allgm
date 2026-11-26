"""Read-only SHA-256 inventory of separately installed controller extensions."""
import hashlib
import json
import os
import sys
from pathlib import Path
import re
import stat

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from controller_i18n import status_text, tr

HEX = re.compile(r"[0-9a-f]{64}\Z")
IDENT = re.compile(r"[a-f0-9]{32}\Z")
PART = re.compile(r"[a-zA-Z0-9_-][a-zA-Z0-9._-]*\Z")
KEEP = "behalten"
ONCE = "nach-erfolg-archivieren"


def require(condition, message):
    if not condition:
        raise ValueError(message)


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
    return controller.with_name(controller.name + "-local")


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
    require(isinstance(register, dict) and register.get("schema") == 1
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
            require(isinstance(entry, dict) and isinstance(entry.get("sha256"), str) and HEX.fullmatch(entry["sha256"])
                    and entry.get("cleanup") in (KEEP, ONCE), tr("extension.invalid_file"))
            if "supplement" in entry:
                row["supplement"] = supplement_name(entry["supplement"])
            row["approved_sha256"] = entry["sha256"]
            if "archive" in entry:
                archive_proof(root, name, entry)
                status = "ARCHIVIERT" if name not in actual else "ARCHIVIERUNG_OFFEN"
            elif name not in actual:
                status = "FEHLT"
            else:
                row["measured_sha256"] = sha(path)
                status = "OK" if row["measured_sha256"] == entry["sha256"] else "SHA_ABWEICHUNG"
        if status == "OK" and controller and overlaps_base(controller, name):
            status = "BASIS_KONFLIKT"
        row["status"] = status
        rows.append(row)
    return {"status": "OK" if all(row["status"] in ("OK","ARCHIVIERT") for row in rows) else "PRUEFBEDARF",
            "files": rows}


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
        return scan(root, identifier, controller)
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
    if "error" in report:
        print(" ", report["error"])
