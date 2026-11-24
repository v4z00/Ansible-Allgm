#!/usr/bin/env python3
"""Install the Allgm codebase and an optional, explicitly compatible overlay."""

import argparse
from datetime import datetime, timezone
from contextlib import nullcontext
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

import github_https

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "update_check"))
from staging_manifest import public_library

CODE_ROOTS = {
    "bin", "config", "descriptions", "examples", "lib",
    "playbooks", "roles", "scripts", "templates", "tools", "update_check",
}
BASE_FILES = {
    "README.md", "configure_server_BASE.sh", "controller-base.json",
    "requirements-controller.txt", "requirements.yml", "requirements-extra.yml",
}
LOCAL_NAMES = {
    "ansible.cfg", "inventory", "inventory_config.yml", "group_vars", "host_vars",
    "secrets.yml", "host_credentials.yml", "settings.yml", "99_readme",
    "agents.md", "regeln.txt", "control_modules_rules.txt", "state", "reports",
}
RECEIPT = ".controller-install.json"
VERSIONS = "versions.txt"
VERSION_HEADER = "# Modul|Version|Repo-URL|Token-Dateipfad"
VERSION_HINT = "# HTTPS: öffentlich mit leerem vierten Feld, privat mit absolutem Token-Dateipfad (0600)."
VERSION_VALUE = re.compile(r"[0-9]+(?:\.[0-9]+)+(?:[-+][A-Za-z0-9.-]+)?\Z")
STAGING_VERSION = re.compile(r"s[0-9]+\.[0-9]+\.[0-9]+\Z")
VERSION_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")


def version_lines(path, optional=False):
    if not path.exists() and optional and not path.is_symlink():
        return []
    require(not path.is_symlink() and path.is_file(), f"{VERSIONS} muss eine lokale Datei sein")
    return path.read_text().splitlines()


def parse_versions(lines):
    rows = {}
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("|")
        require(len(parts) == 4 and VERSION_NAME.fullmatch(parts[0])
                and (VERSION_VALUE.fullmatch(parts[1]) or STAGING_VERSION.fullmatch(parts[1])), f"Ungültige Zeile in {VERSIONS}")
        name, version, url, token_file = parts
        name = {"allgm": "Allgm", "homelab": "Homelab", "nxts3": "NXTS3"}.get(name.casefold(), name)
        require(name.casefold() not in {n.casefold() for n in rows}, f"Doppeltes Modul in {VERSIONS}")
        rows[name] = (version, url, token_file)
    return rows


def read_versions(path):
    return parse_versions(version_lines(path))


def module_url(name):
    return f"https://github.com/v4z00/Ansible-{name}.git"


def version_for(source, branch=None):
    value = (source / "VERSION.txt").read_text().strip()
    require(VERSION_VALUE.fullmatch(value), "VERSION.txt enthält keine gültige Version")
    if branch is None and (source / ".git").exists():
        ref = subprocess.run(["git", "-C", str(source), "symbolic-ref", "-q", "HEAD"], capture_output=True)
        branch = "staging" if ref.stdout.strip() == b"refs/heads/staging" else "main"
    if branch == "staging":
        require(STAGING_VERSION.fullmatch("s" + value), "Staging benötigt eine dreiteilige Version x.x.x")
        return "s" + value
    return value


def remote_for(source):
    # Read the literal origin without Git's global insteadOf rewrites.
    result = subprocess.run(["git", "-C", str(source), "config", "--local", "--get", "remote.origin.url"],
                            capture_output=True, text=True)
    url = result.stdout.strip()
    if result.returncode or not url or (Path(url).is_absolute() or url.startswith("file://")):
        return ""
    return github_https.legacy_https(url) or github_https.https_url(url)


def version_source(dest, sources, scratch, *, token_file=None, prompt=False, branch=None):
    lines = version_lines(dest / VERSIONS, optional=True)
    rows = parse_versions(lines)
    changes = {}
    for name, path in sources.items():
        _, url, saved_path = rows.get(name, ("", "", ""))
        migrated = github_https.legacy_https(url)
        if migrated:
            url, saved_path = migrated, ""  # An SSH key can never serve as a token.
        url = url or remote_for(path) or module_url(name)
        if url.lower().removesuffix(".git") == f"https://github.com/v4z00/{name}".lower():
            url = module_url(name)
        if url:
            github_https.https_url(url)
        if name == "NXTS3":
            selected = token_file if token_file is not None else saved_path
            if not selected and prompt and sys.stdin.isatty():
                try:
                    selected = input("Pfad zur lokalen Token-Datei (0600): ").strip()
                except EOFError:
                    selected = ""
            require(selected, "Der private Installer benötigt --token-file PFAD zur lokalen Token-Datei")
            github_https.read_token(selected, dest, *sources.values())
        else:
            require(not saved_path, f"{name} wird anonym geladen. Viertes Feld in versions.txt leeren.")
            selected = ""
        changes[name.casefold()] = "|".join((name, version_for(path, branch), url, selected))
    output = [] if VERSION_HEADER in lines else [VERSION_HEADER, VERSION_HINT]
    for line in lines:
        output.append(changes.pop(line.partition("|")[0].casefold(), line))
    output.extend(changes.values())
    result = scratch / VERSIONS
    result.write_text("\n".join(output) + "\n")
    result.chmod(0o600)
    return result


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(file):
    data = json.loads(file.read_text())
    require(isinstance(data, dict), "JSON-Objekt erwartet")
    return data


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_code(rel, overlay=False):
    parts = PurePosixPath(rel).parts
    if not parts or rel != PurePosixPath(rel).as_posix():
        return False
    if public_library(rel):
        return not overlay
    if len(parts) == 1:
        return rel == "configure_server_BASE.sh" if overlay else rel in BASE_FILES | {VERSIONS}
    if parts[0] not in CODE_ROOTS:
        return False
    inventory_example = (
        len(parts) == 3 and parts[:2] == ("examples", "inventory")
        and parts[2].endswith((".example.yml", ".yml.example"))
    )
    return all(
        (part.lower() not in LOCAL_NAMES or inventory_example and index == 1)
        and part != "__pycache__"
        and (not part.startswith(".") or part == ".versions" and parts[:2] == ("bin", "control.d"))
        and not part.lower().endswith((".pyc", ".bak", ".pem", ".key", ".token", ".pfx", ".p12", ".keytab"))
        for index, part in enumerate(parts)
    )


def code_files(root, overlay=False):
    files = {}
    for candidate in root.rglob("*"):
        rel = candidate.relative_to(root).as_posix()
        if rel == VERSIONS or not is_code(rel, overlay):
            continue
        require(not candidate.is_symlink(), f"Link in Codequelle: {rel}")
        if candidate.is_dir():
            continue
        require(candidate.is_file(), f"Sonderdatei in Codequelle: {rel}")
        files[rel] = candidate
    return files


def merge_overlay(base, extension, meta, name):
    require(meta.get("schema") == 1 and meta.get("profile") == name,
            "Overlay-Profil stimmt nicht mit der Quelle überein")
    allowed = set(meta["replaces"])
    actual = {rel for rel in extension.keys() & base.keys() if sha(extension[rel]) != sha(base[rel])}
    require(actual <= allowed, f"Nicht freigegebene Overlay-Kollision: {', '.join(sorted(actual - allowed))}")
    combined = {**base, **extension}
    require(len({p.casefold() for p in combined}) == len(combined), "Overlay-Dateinamen kollidieren")
    return combined


def compose(overlay, name=None):
    base = code_files(BASE)
    if overlay is None:
        return base
    return merge_overlay(base, code_files(overlay, overlay=True),
                         read_json(overlay / "controller-overlay.json"), name)


def copy_code(files, dest):
    for rel, src in files.items():
        file = dest / rel
        file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, file)


def initialize(dest, files):
    copy_code(files, dest)
    local = {
        "ansible.cfg": "ansible.cfg.example",
        "inventory/10_static.yml": "inventory.yml.example",
        "inventory_config.yml": "inventory_config.yml.example",
        "group_vars/all/settings.yml": "settings.yml.example",
        "group_vars/all/access.yml": "access.yml.example",
    }
    for rel, example in local.items():
        path = dest / rel
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        shutil.copyfile(dest / "examples/first_run" / example, path)
        path.chmod(0o600)
    (dest / "host_vars").mkdir(mode=0o700)
    for name in ("host_vars", "group_vars"):
        (dest / "inventory" / name).symlink_to(f"../{name}", target_is_directory=True)


def write_receipt(root, profile, hashes, source=None):
    receipt = {"schema": 1, "profile": profile, "files": {rel: value for rel, value in hashes.items() if rel != VERSIONS}}
    if source:
        receipt["source"] = source
    (root / RECEIPT).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")


def require_safe(root, rel, file_required=False):
    require(is_code(rel), f"Ungültiger Codepfad: {rel}")
    path = root / rel
    require(all(not p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)),
            f"Link im Controllerpfad: {rel}")
    if file_required:
        require(path.is_file(), f"Verwaltete Datei fehlt: {rel}")
    return path


def add_overlay(dest, files, hashes, profile, scratch):
    record = dest / RECEIPT
    require(record.is_file() and not record.is_symlink(),
            "Ziel enthält keine mit diesem Installer erstellte Installation")
    previous = read_json(record)
    require(previous.get("schema") == 1 and previous.get("profile") in {"allgm", "homelab", "nxts3"},
            "Unbekannter Installationsnachweis")
    old = previous["files"]
    for rel, expected in old.items():
        require(sha(require_safe(dest, rel, file_required=True)) == expected,
                f"Lokale Änderung im Codepfad: {rel}")
    if previous["profile"] == profile:
        require(old == {rel: value for rel, value in hashes.items() if rel != VERSIONS}, "Neue Codeversion über den Update-Weg einspielen")
        state = dest / VERSIONS
        if (not state.exists() or sha(state) != hashes[VERSIONS]
                or stat.S_IMODE(state.stat().st_mode) != 0o600):
            os.replace(files[VERSIONS], dest / VERSIONS)
        return
    require(previous["profile"] == "allgm" and profile in {"homelab", "nxts3"},
            "Profilwechsel benötigt eine frische Installation")
    base = code_files(BASE)
    require(old == {rel: sha(path) for rel, path in base.items()},
            "Zuerst den passenden Allgm-Quellstand verwenden")
    changed = {rel: files[rel] for rel, value in hashes.items() if old.get(rel) != value}
    for rel in changed:
        path = require_safe(dest, rel)
        require(rel == VERSIONS or rel in old or not path.exists(), f"Lokaler Pfad kollidiert mit Overlay: {rel}")
        for parent in path.parents:
            if parent == dest:
                break
            require(not parent.exists() or parent.is_dir(), f"Zielordner kollidiert mit Datei: {parent.name}")
    new, saved = scratch / "new", scratch / "saved"
    new.mkdir()
    saved.mkdir()
    copy_code(changed, new)
    copy_code({rel: dest / rel for rel in changed if (dest / rel).is_file()}, saved)
    write_receipt(new, profile, hashes)
    installed = []
    try:
        for rel in sorted(changed):
            path = dest / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            os.replace(new / rel, path)
            installed.append(rel)
        os.replace(new / RECEIPT, record)
    except OSError:
        for rel in reversed(installed):
            if (saved / rel).is_file():
                os.replace(saved / rel, dest / rel)
            else:
                (dest / rel).unlink()
        raise


BACKUP_ID = re.compile(r"[0-9]{8}T[0-9]{12}Z-[0-9a-f]{12}")


def update_files(files):
    # First-run examples never become part of an established controller.
    return {rel: path for rel, path in files.items()
            if not rel.startswith("examples/") and rel != "README.md"}


def receipt_hash(dest):
    path = dest / RECEIPT
    require(not path.is_symlink() and (not path.exists() or path.is_file()),
            "Installationsnachweis ist keine reguläre Datei")
    return sha(path) if path.exists() else None


def update_plan(dest, files, profile, retired=()):
    data = {"schema": 1, "target": str(dest.resolve()), "profile": profile,
            "previous_receipt": receipt_hash(dest), "files": {}}
    for rel in sorted(files.keys() | set(retired)):
        src = files.get(rel)
        location = require_safe(dest, rel)
        require(not location.exists() or location.is_file(),
                f"Codepfad kollidiert mit lokaler Ablage: {rel}")
        before = sha(location) if location.exists() else None
        if src is None and before is None:
            continue
        after = sha(src) if src is not None else None
        before_mode = stat.S_IMODE(location.stat().st_mode) if before is not None else None
        after_mode = stat.S_IMODE(src.stat().st_mode) if src is not None else None
        if before != after or before_mode is None or (before_mode ^ after_mode) & (0o777 if rel == VERSIONS else 0o100):
            data["files"][rel] = {
                "before": before, "after": after,
                "before_mode": before_mode, "after_mode": after_mode,
            }
    token = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    return data, token


def backup_home(dest, create=False):
    state = dest / ".local"
    backups = state / "controller-updates"
    for directory in (state, backups):
        require(not directory.is_symlink() and (not directory.exists() or directory.is_dir()),
                f"Backup-Pfad ist kein Verzeichnis: {directory}")
        if create:
            directory.mkdir(mode=0o700, exist_ok=True)
    return backups


def put_files(dest, pending, restore, validate=None):
    installed = []
    try:
        for rel, source in pending.items():
            target = dest / rel
            if source is None:
                target.unlink()
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(source, target)
            installed.append(rel)
        if validate:
            validate()
    except (OSError, ValueError):
        for rel in reversed(installed):
            source = restore.get(rel)
            if source is None:
                (dest / rel).unlink(missing_ok=True)
            else:
                os.replace(source, dest / rel)
        raise


def update_controller(dest, all_files, profile, accepted, receipt_source=None, retired=()):
    require(dest.is_dir() and (dest / "bin/control").is_file(),
            "Update erwartet einen vorhandenen Ansible-Controller mit bin/control")
    require(profile == "nxts3" or not (dest / "roles/nxts3").is_dir(),
            "NXTS3-Bestand braucht den eigenen NXTS3-Installer")
    require(profile == "homelab" or not (
        (dest / "bin/control.d/.versions/homelab.json").exists()
        or (dest / "roles/openwrt_operations").exists()),
        "Homelab-Bestand benötigt beim Update die geprüfte Homelab-Erweiterung")
    files = update_files(all_files)
    plan, token = update_plan(dest, files, profile, retired)
    changed = plan["files"]
    if not changed and not receipt_source:
        print("Der verwaltete Code entspricht bereits dem Staging-Stand.")
        return
    if not accepted:
        for rel, hashes in changed.items():
            before = hashes["before"]
            if hashes["after"] is None:
                print(f"ENTFERNEN {rel}  {before[:12]}")
            elif before is None:
                print(f"NEU       {rel}")
            else:
                print(f"ERSETZEN  {rel}  {before[:12]} → {hashes['after'][:12]}  {hashes['before_mode']:04o} → {hashes['after_mode']:04o}")
        print(f"{len(changed)} Codepfade. Nach Prüfung --update --apply {token} verwenden.")
        return
    require(accepted == token, "Staging oder Bestand hat sich geändert. Vorschau erneut ausführen.")
    backups = backup_home(dest, create=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    name = f"{stamp}-{token[:12]}"
    with tempfile.TemporaryDirectory(dir=backups, prefix=".prepare-") as tmp:
        work = Path(tmp)
        saved, new, restore = (work / directory for directory in ("backup", "new", "restore"))
        for directory in (saved, new, restore):
            directory.mkdir()
        old = {rel: dest / rel for rel, hashes in changed.items() if hashes["before"] is not None}
        if plan["previous_receipt"] is not None:
            old[RECEIPT] = dest / RECEIPT
        copy_code(old, saved)
        copy_code(old, restore)
        copy_code({rel: files[rel] for rel in changed if rel in files}, new)
        for rel, hashes in changed.items():
            if hashes["after"] is not None:
                require(sha(new / rel) == hashes["after"]
                        and stat.S_IMODE((new / rel).stat().st_mode) == hashes["after_mode"],
                        f"Kopie weicht vom Updateplan ab: {rel}")
            if hashes["before"] is not None:
                require(sha(saved / rel) == hashes["before"],
                        f"Datei hat sich während der Vorbereitung geändert: {rel}")
        require(update_plan(dest, files, profile, retired)[1] == token, "Bestand wurde während der Vorbereitung geändert")
        write_receipt(new, profile, {rel: sha(src) for rel, src in files.items()}, receipt_source)
        def verify_installed():
            for rel, hashes in changed.items():
                target = dest / rel
                if hashes["after"] is None:
                    require(not target.exists() and not target.is_symlink(), f"Datei noch vorhanden: {rel}")
                    continue
                require(sha(target) == hashes["after"]
                        and stat.S_IMODE(target.stat().st_mode) == hashes["after_mode"],
                        f"Kontrolle nach Installation fehlgeschlagen: {rel}")
        plan["installed_receipt"] = sha(new / RECEIPT)
        (saved / "plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
        os.rename(saved, backups / name)
        put_files(dest, {rel: new / rel if rel in files or rel == RECEIPT else None for rel in (*changed, RECEIPT)},
                  {rel: restore / rel for rel in old}, verify_installed)
    print(f"Aktualisiert: {len(changed)} Codepfade. Sicherung: {backups / name}")
    print(f"Rückweg: --rollback {name}")


def rollback_controller(dest, name):
    require(BACKUP_ID.fullmatch(name), "Ungültige Sicherungskennung")
    backups = backup_home(dest)
    backup = backups / name
    require(backup.is_dir() and not backup.is_symlink(), "Sicherung fehlt")
    plan = read_json(backup / "plan.json")
    require(plan["schema"] == 1 and plan["target"] == str(dest.resolve())
            and receipt_hash(dest) == plan["installed_receipt"],
            "Diese Sicherung passt nicht zum aktuellen Codewechsel")
    with tempfile.TemporaryDirectory(dir=backups, prefix=".restore-") as tmp:
        work = Path(tmp)
        saved, revert = work / "saved", work / "revert"
        saved.mkdir()
        revert.mkdir()
        current = {}
        original = {}
        for rel, hashes in plan["files"].items():
            target = require_safe(dest, rel)
            if hashes["after"] is None:
                require(not target.exists(), f"Datei seit Update wieder angelegt: {rel}")
            else:
                require(target.is_file() and sha(target) == hashes["after"]
                        and stat.S_IMODE(target.stat().st_mode) == hashes["after_mode"],
                        f"Datei seit Update verändert: {rel}")
                current[rel] = target
            if hashes["before"] is not None:
                source = require_safe(backup, rel, file_required=True)
                require(sha(source) == hashes["before"]
                        and stat.S_IMODE(source.stat().st_mode) == hashes["before_mode"],
                        f"Backup weicht ab: {rel}")
                original[rel] = source
        current[RECEIPT] = dest / RECEIPT
        if plan["previous_receipt"] is not None:
            source = backup / RECEIPT
            require(source.is_file() and not source.is_symlink() and sha(source) == plan["previous_receipt"],
                    "Gesicherter Installationsnachweis stimmt nicht")
            original[RECEIPT] = source
        copy_code(current, revert)
        copy_code(original, saved)
        put_files(dest, {rel: saved / rel if rel in original else None for rel in (*plan["files"], RECEIPT)},
                  {rel: revert / rel for rel in current})
    print(f"Controller-Code aus {name} zurückgesetzt.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--skip-runtime", action="store_true", help="Nur Code und lokale Startvorlagen kopieren")
    action.add_argument("--export-code", action="store_true", help="Nur Code für einen Offline-Releasebaum ausgeben")
    action.add_argument("--update", action="store_true", help="Bestehenden Controller prüfen und Update planen")
    action.add_argument("--rollback", metavar="BACKUP", help="Einen bestätigten Codewechsel zurücksetzen")
    parser.add_argument("--apply", metavar="PLAN_SHA256", help="Den exakt geprüften Updateplan einspielen")
    name = os.environ.get("ANSIBLE_STAGING_OVERLAY")
    if name == "NXTS3":
        parser.add_argument("--token-file", metavar="PFAD", help="Lokale Fine-Grained-Token-Datei (0600)")
    args = parser.parse_args()
    if args.apply and not args.update:
        parser.error("--apply setzt --update voraus")
    os.umask(0o077)
    try:
        target = args.target.absolute()
        require(target.name and not target.is_symlink(), "Eigenen Zielordner ohne Symlink angeben")
        require(not target.resolve().is_relative_to(BASE), "Ziel muss außerhalb der Quellablage liegen")
        require(name in (None, "Homelab", "NXTS3"), "Ungültiger Installer-Aufruf")
        overlay = Path(os.environ["ANSIBLE_STAGING_SOURCE"]).resolve() if name else None
        if overlay:
            require(not target.resolve().is_relative_to(overlay), "Ziel muss außerhalb der Overlay-Quelle liegen")
        target.parent.mkdir(parents=True, exist_ok=True)
        lock = target.parent / f".{target.name}.controller-lock"
        lock_context = nullcontext() if args.export_code else os.fdopen(
            os.open(lock, os.O_CREAT | os.O_NOFOLLOW | os.O_RDWR, 0o600), "r+")
        with lock_context as handle, tempfile.TemporaryDirectory(dir=target.parent, prefix=".controller-") as tmp:
            if handle is not None:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scratch = Path(tmp)
            if args.rollback:
                rollback_controller(target, args.rollback)
                return 0
            files = compose(overlay, name)
            if not args.export_code:
                sources = {"Allgm": BASE, **({name: overlay} if name else {})}
                files[VERSIONS] = version_source(target, sources, scratch,
                                                 token_file=getattr(args, "token_file", None), prompt=True)
            profile = name.lower() if name else "allgm"
            if args.update:
                update_controller(target, files, profile, args.apply)
                return 0
            hashes = {rel: sha(path) for rel, path in files.items()}
            contains_files = target.exists() and (not target.is_dir() or any(target.iterdir()))
            if contains_files and not args.export_code:
                add_overlay(target, files, hashes, profile, scratch)
            else:
                require(not args.export_code or not target.exists(), "Exportziel existiert bereits")
                prepared = scratch / "controller"
                prepared.mkdir()
                if args.export_code:
                    copy_code(files, prepared)
                else:
                    initialize(prepared, files)
                    write_receipt(prepared, profile, hashes)
                if args.export_code:
                    target.mkdir(mode=0o700)
                    try:
                        os.replace(prepared, target)
                    except OSError:
                        target.rmdir()
                        raise
                else:
                    os.rename(prepared, target)
            if not (args.skip_runtime or args.export_code):
                subprocess.run(["bash", str(target / "bin/setup-runtime")], check=True)
        print(f"Controller {profile}: {target}")
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Controllerinstallation: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
