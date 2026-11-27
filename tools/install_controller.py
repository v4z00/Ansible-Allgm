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
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from controller_i18n import preload_for_update, tr
from staging_manifest import public_library
import controller_addons as addon
import controller_transaction as transaction
import local_extensions

CODE_ROOTS = {
    "bin", "config", "descriptions", "examples", "lib",
    "playbooks", "roles", "scripts", "templates", "tools", "update_check",
}
BASE_FILES = {
    "README.md", "configure_server_BASE.sh", "controller-base.json", "controller-addons-v1.json",
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
        name = {"allgm": "Allgm", "homelab": "Homelab"}.get(name.casefold(), name)
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


def version_source(dest, sources, scratch, *, token_file=None, prompt=False, branch=None,
                   addons=None, urls=None, tokens=None):
    addons, urls, tokens = addons or {}, urls or {}, tokens or {}
    lines = version_lines(dest / VERSIONS, optional=True)
    rows = {name.casefold(): row for name, row in parse_versions(lines).items()}
    changes = {}
    for name, path in sources.items():
        _, url, saved_path = rows.get(name.casefold(), ("", "", ""))
        key = name.casefold()
        override = urls.get(key)
        require(not override or not url or github_https.https_url(override) == url,
                f"Existing source for {name} differs from requested URL")
        url = override or url
        migrated = github_https.legacy_https(url)
        if migrated:
            url, saved_path = migrated, ""  # An SSH key can never serve as a token.
        url = url or remote_for(path)
        if not url and name in addons:
            raise ValueError(f"Explicit --addon-url {name}=HTTPS_URL required for an offline checkout")
        url = url or module_url(name)
        if name not in addons and url.lower().removesuffix(".git") == f"https://github.com/v4z00/{name}".lower():
            url = module_url(name)
        if url:
            github_https.https_url(url)
        access = "anonymous"
        if name in addons:
            access = addons[name][1].get("authentication", "anonymous")
        elif name.casefold() not in {"allgm", "homelab"}:
            metadata = read_json(path / "controller-overlay.json")
            access = metadata.get("authentication", "token-file")
            require(access in {"anonymous", "token-file"}, "Unbekannte Authentifizierung im Overlay")
        if access == "token-file":
            supplied = tokens.get(key) if name in addons else token_file
            selected = supplied if supplied is not None else saved_path
            if not selected and prompt:
                try:
                    with open("/dev/tty") as tty_in, open("/dev/tty", "w") as tty_out:
                        print("Pfad zur lokalen Token-Datei (0600): ", end="", file=tty_out, flush=True)
                        selected = tty_in.readline().strip()
                except OSError:
                    pass
            require(selected, "Der private Installer benötigt --token-file PFAD zur lokalen Token-Datei")
            github_https.read_token(selected, dest, *sources.values())
        else:
            supplied = tokens.get(key) if name in addons else token_file if name.casefold() != "allgm" else None
            require(not saved_path and not supplied, f"{name} wird anonym geladen. Viertes Feld in versions.txt leeren.")
            selected = ""
        changes[name.casefold()] = "|".join((name, version_for(path, branch), url, selected))
    output = [] if VERSION_HEADER in lines else [VERSION_HEADER, VERSION_HINT]
    for line in lines:
        output.append(changes.pop(line.partition("|")[0].casefold(), line))
    registered = addon.registrations(lines)
    output.extend(f"# addon={name}" for name in addons if name.casefold() not in registered)
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


def code_files(checkout, overlay=False):
    """Walk only deliverable directories in an offline checkout."""
    roots = CODE_ROOTS | ({"configure_server_BASE.sh"} if overlay else BASE_FILES | {"artifacts"})
    directories = CODE_ROOTS | {"examples/inventory"}
    if not overlay:
        directories |= {
            "artifacts", "artifacts/script-library", "artifacts/script-library/bin",
            "artifacts/script-library/lib", "artifacts/script-library/lib/common",
            "artifacts/script-library/lib/data", "artifacts/script-library/lib/python",
        }
    files = {}
    pending = [checkout / name for name in sorted(roots) if os.path.lexists(checkout / name)]
    while pending:
        candidate = pending.pop()
        rel = candidate.relative_to(checkout).as_posix()
        if rel not in directories and not is_code(rel, overlay):
            continue
        mode = candidate.lstat().st_mode
        require(not stat.S_ISLNK(mode), f"Link in Codequelle: {rel}")
        if stat.S_ISDIR(mode):
            pending.extend(candidate.iterdir())
        else:
            require(stat.S_ISREG(mode) and rel not in directories, f"Sonderdatei in Codequelle: {rel}")
            files[rel] = candidate
    return files


def merge_overlay(base, extension, meta, name):
    require(meta.get("schema") == 1 and isinstance(meta.get("profile"), str)
            and meta["profile"].casefold() == name.casefold(),
            "Overlay-Profil stimmt nicht mit der Quelle überein")
    allowed = set(meta["replaces"])
    actual = {rel for rel in extension.keys() & base.keys() if sha(extension[rel]) != sha(base[rel])}
    require(actual <= allowed, f"Nicht freigegebene Overlay-Kollision: {', '.join(sorted(actual - allowed))}")
    combined = {**base, **extension}
    require(len({p.casefold() for p in combined}) == len(combined), "Overlay-Dateinamen kollidieren")
    return combined


def copy_code(files, dest):
    for rel, src in files.items():
        file = dest / rel
        file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, file)


def first_install_language(requested, interactive=True):
    if requested:
        return requested
    locale = next((os.environ[key] for key in ("LC_ALL", "LC_MESSAGES", "LANG")
                   if os.environ.get(key)), "")
    suggestion = "de" if re.split(r"[_@.-]", locale.lower())[0] == "de" else "en"
    if not interactive:
        return suggestion
    try:
        with open("/dev/tty", "r") as reader, open("/dev/tty", "w") as writer:
            while True:
                print(f"Controller language / Sprache [de/en, Enter = {suggestion}]: ",
                      end="", file=writer, flush=True)
                reply = reader.readline()
                if not reply:
                    break
                choice = reply.strip().lower() or suggestion
                if choice in {"de", "en"}:
                    return choice
    except OSError:
        pass
    return suggestion


def initialize(dest, files, language=None, interactive=True):
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
    settings = dest / "group_vars/all/settings.yml"
    chosen = first_install_language(language, interactive)
    starter, count = re.subn(r"^controller_lang: (?:de|en)$", "controller_lang: " + chosen,
                             settings.read_text(), flags=re.MULTILINE)
    require(count <= 1, "Duplicate language setting in the first-run template")
    if not count:
        # Earlier templates omitted the optional language key.
        from configure import set_field
        import yaml
        starter = set_field(starter, "controller_lang", chosen, yaml.SafeLoader)
    settings.write_text(starter)
    (dest / "host_vars").mkdir(mode=0o700)
    for name in ("host_vars", "group_vars"):
        (dest / "inventory" / name).symlink_to(f"../{name}", target_is_directory=True)


def write_receipt(root, profile, hashes, source=None, layout=None):
    receipt = {"schema": 1, "profile": profile, "files": {rel: value for rel, value in hashes.items() if rel != VERSIONS}}
    if layout is not None:
        receipt.update(schema=2, modules=layout["modules"],
                       owners={p: layout["owners"][p] for p in receipt["files"]})
    if source:
        receipt["source"] = source
    (root / RECEIPT).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")


def require_safe(root, rel, file_required=False):
    require(is_code(rel), f"Ungültiger Codepfad: {rel}")
    path = root / rel
    require(all(not p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)),
            f"Link im Controllerpfad: {rel}")
    require(all(not parent.exists() or parent.is_dir() for parent in path.parents
                if parent.is_relative_to(root)), f"Not a controller directory: {rel}")
    if file_required:
        require(path.is_file(), f"Verwaltete Datei fehlt: {rel}")
    return path


def load_addons(paths, profile, dest):
    loaded = {}
    names = {"allgm", "homelab", profile.casefold()}
    for path in paths:
        require(not path.is_symlink() and path.is_dir(), "Invalid add-on checkout")
        path = path.resolve()
        require(not dest.resolve().is_relative_to(path), "Controller must be outside the source directory")
        # Only the name is read before verification, solely to select the expected manifest.
        name = read_json_from_git(path, "controller-addon.json").get("name")
        require(isinstance(name, str) and VERSION_NAME.fullmatch(name) and name.casefold() not in names,
                "Invalid or duplicate add-on name")
        metadata, mapping = addon.descriptor(path, name)
        loaded[name] = (path, metadata, mapping)
        names.add(name.casefold())
    return loaded


def read_json_from_git(root, rel):
    result = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"],
                            capture_output=True, check=True)
    return json.loads(result.stdout)


def local_sources(overlay, name, addons):
    files = code_files(BASE)
    owners = dict.fromkeys(files, "Allgm")
    sources = {"Allgm": BASE}
    if overlay:
        extension = code_files(overlay, overlay=True)
        files = merge_overlay(files, extension, read_json(overlay / "controller-overlay.json"), name)
        owners.update(dict.fromkeys(extension, name))
        sources[name] = overlay
    files, owners = addon.combine(files, owners, addons)
    sources.update({n: entry[0] for n, entry in addons.items()})
    return files, sources, {"owners": owners,
                            "modules": addon.module_info(sources, addons, version_for)}


def inspect_addon_install(dest, base, files, layout, previous, baseline):
    import check
    return addon.installation_guards(dest, base, files, layout["owners"], layout["modules"],
                                     previous, baseline, sha, require_safe, check.global_settings)


def existing_install(dest, files, layout, profile, previous, baseline, retired):
    require(previous and previous.get("profile") in {"allgm", profile},
            "Migrate an existing controller through the reviewed --update plan")
    module_names = set(previous.get("modules", {}))
    if previous.get("schema") == 1:
        module_names.add("Allgm")
        module_names.update(n for n in layout["modules"] if n.casefold() == previous["profile"])
    additions = set(layout["modules"]) - module_names
    candidates = update_files(files)
    for rel, old_hash in baseline.items():
        require(sha(require_safe(dest, rel, file_required=True)) == old_hash,
                f"Local change in managed file: {rel}")
    if previous["profile"] != profile:
        require(previous["profile"] == "allgm", "An installed profile cannot be replaced")
        # A profile may replace only the exact base revision the operator already installed.
        reference = code_files(BASE)
        for rel, digest in baseline.items():
            if previous.get("owners", {}).get(rel, "Allgm") == "Allgm" and rel in reference:
                require(sha(reference[rel]) == digest, "First update the base release")
    else:
        for rel, src in candidates.items():
            if rel == VERSIONS:
                continue
            owner = layout["owners"][rel]
            if owner not in additions:
                require(baseline.get(rel) == sha(src), "Use --update to change an installed release")
        require(all(rel in files or rel in retired for rel in update_files(baseline)),
                "Use --update to retire managed files")
    for rel in candidates:
        if rel != VERSIONS and rel not in baseline:
            require(not require_safe(dest, rel).exists(), f"Local file collides with installation: {rel}")
    updated_layout = {"owners": {p: n for p, n in layout["owners"].items() if p in candidates},
                      "modules": layout["modules"]}
    plan, token = update_plan(dest, candidates, profile, retired, updated_layout)
    previous_owners = {p: n for p, n in previous.get("owners", {}).items() if p in candidates}
    if (plan["files"] or previous.get("schema") != 2
            or previous.get("modules") != layout["modules"]
            or previous_owners != updated_layout["owners"]):
        update_controller(dest, files, profile, token, previous.get("source"), retired, updated_layout)


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


def update_plan(dest, files, profile, retired=(), layout=None):
    data = {"schema": 1, "target": str(dest.resolve()), "profile": profile,
            "previous_receipt": receipt_hash(dest), "files": {}}
    if layout is not None:
        data["layout_sha256"] = hashlib.sha256(json.dumps(layout, sort_keys=True).encode()).hexdigest()
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


def transaction_path(root, rel):
    if rel == RECEIPT:
        path = root / RECEIPT
        require(not root.is_symlink() and not path.is_symlink(), "Unsafe receipt path")
        return path
    return require_safe(root, rel)


def put_files(dest, pending, restore, validate=None):
    preload_for_update()
    transaction.apply(dest, backup_home(dest, create=True), pending, restore,
                      transaction_path, validate)


def restore_capability(root, original_tree, changed, prior_hash, prior_receipt_hash=None):
    """Read the pre-update descriptor from a verified backup, or the unchanged live receipt."""
    rel = "controller-base.json"
    if changed:
        if prior_hash is None:
            return {}
        source = require_safe(original_tree, rel, file_required=True)
    else:
        source = require_safe(root, rel)
        receipt = transaction_path(root, RECEIPT)
        if prior_receipt_hash is not None:
            # A partially applied transaction can already have replaced the live receipt.
            receipt = transaction_path(original_tree, RECEIPT)
            require(receipt.is_file() and sha(receipt) == prior_receipt_hash, tr("extension.unverified_target"))
        prior_hash = addon.receipt(receipt).get("files", {}).get(rel)
        if prior_hash is None and not source.exists():
            return {}
    require(prior_hash and sha(source) == prior_hash, tr("extension.unverified_target"))
    return read_json(source)


def check_local_restore(report, metadata, changes, *, recovering=False):
    restored = {rel for rel, row in changes.items() if row["before"] is not None}
    conflicts = [row["path"] for row in report["files"]
                 if row["status"] in ("OK", "BASIS_KONFLIKT")
                 and local_extensions.overlaps_managed(restored, row["path"])]
    require(not conflicts, tr("extension.prospective_conflict", paths=", ".join(conflicts)))
    if recovering and report["status"] == "PRUEFBEDARF":
        # A half-applied write may itself be shadowing an approved local file.
        # Only the verified journal undoing that write may bypass this transient overlap.
        removed = set(changes) - restored
        issues = [row for row in report["files"] if row["status"] not in ("OK", "ARCHIVIERT")]
        if issues and all(row["status"] == "BASIS_KONFLIKT"
                          and row["approved_sha256"] == row["measured_sha256"]
                          and local_extensions.overlaps_managed(removed, row["path"]) for row in issues):
            status = local_extensions.MIGRATION_REQUIRED if report["schema"] == 1 else "OK"
            report = {**report, "status": status, "integrity_status": "OK"}
    local_extensions.require_compatible(report, metadata, rollback=True)


def recover_transaction(dest, local=None):
    if not dest.is_dir():
        return
    backups = backup_home(dest)
    interrupted = backups / ".transaction"
    if interrupted.exists() and not interrupted.is_symlink():
        report = local if local is not None else local_extensions.inspect(dest)
        if report["status"] != "NICHT_EINGERICHTET":
            journal = local_extensions.read_json(local_extensions.path_in(interrupted, "journal.json"))
            entries = journal["files"]
            rel = "controller-base.json"
            before = entries[rel]["before"] if rel in entries else None
            prior_receipt = entries.get(RECEIPT, {}).get("before")
            metadata = restore_capability(dest, interrupted / "original", rel in entries,
                                          before[0] if before else None, prior_receipt[0] if prior_receipt else None)
            check_local_restore(report, metadata, entries, recovering=True)
    if interrupted.exists() or interrupted.is_symlink():
        # Recovery can itself replace or remove the active translation catalogs.
        # A previous process may already have removed a catalog. The verified
        # journal can restore it; only a fresh exchange requires a full preload.
        try:
            preload_for_update()
        except FileNotFoundError:
            pass
    transaction.recover(dest, backups, transaction_path)


def inspect_before_change(dest, *, write, rollback=False):
    """Never recover code automatically while an installed schema 1 register awaits migration."""
    report = local_extensions.inspect(dest)
    journal = backup_home(dest) / ".transaction"
    if not journal.exists() and not journal.is_symlink():
        return report
    if report.get("schema") == 1 and not rollback:
        return report
    require(write, tr("update.interrupted"))
    recover_transaction(dest, report)
    return local_extensions.inspect(dest)


def installed_profile(dest):
    """Resolve the installer receipt and markers left by older overlay installers."""
    profiles = set()
    if receipt_hash(dest) is not None:
        receipt = read_json(dest / RECEIPT)
        name = receipt.get("profile")
        require(receipt.get("schema") in (1, 2) and isinstance(name, str) and VERSION_NAME.fullmatch(name),
                "Ungültiger Profilname im Installationsnachweis")
        profiles.add(name.casefold())
    if ((dest / "bin/control.d/.versions/homelab.json").is_file()
            or (dest / "roles/openwrt_operations").is_dir()):
        profiles.add("homelab")
    recorded_addons = set(addon.installed(addon.receipt(dest / RECEIPT)))
    for marker in (dest / "update_check/extensions").glob("*/manifest.json"):
        name = marker.parent.name
        if name.casefold() not in recorded_addons and VERSION_NAME.fullmatch(name) and (dest / "roles" / name).is_dir():
            profiles.add(name.casefold())
    if not profiles:
        for name in parse_versions(version_lines(dest / VERSIONS, optional=True)):
            if (dest / "roles" / name.casefold()).is_dir():
                profiles.add(name.casefold())
    require(len(profiles) <= 1, "Installationsnachweis und vorhandene Profilmarker widersprechen sich")
    return next(iter(profiles), "allgm")


def update_controller(dest, all_files, profile, accepted, receipt_source=None, retired=(), layout=None):
    require(dest.is_dir() and (dest / "bin/control").is_file(),
            "Update erwartet einen vorhandenen Ansible-Controller mit bin/control")
    require(installed_profile(dest) in {"allgm", profile}, "Für diesen Bestand den passenden Overlay-Installer verwenden")
    files = update_files(all_files)
    plan, token = update_plan(dest, files, profile, retired, layout)
    changed = plan["files"]
    if not changed and not receipt_source and layout is None:
        print(tr("update.current"))
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
        require(update_plan(dest, files, profile, retired, layout)[1] == token, "Bestand wurde während der Vorbereitung geändert")
        write_receipt(new, profile, {rel: sha(src) for rel, src in files.items()}, receipt_source, layout)
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
        transaction.sync_files(saved)
        os.rename(saved, backups / name)
        transaction.sync_directory(backups)
        put_files(dest, {rel: new / rel if rel in files or rel == RECEIPT else None for rel in (*changed, RECEIPT)},
                  {rel: restore / rel for rel in old}, verify_installed)
    print(tr("update.installed", count=len(changed), backup=backups / name))
    print(tr("update.undo", name=name))


def rollback_controller(dest, name, local=None):
    require(BACKUP_ID.fullmatch(name), "Ungültige Sicherungskennung")
    backups = backup_home(dest)
    backup = backups / name
    require(backup.is_dir() and not backup.is_symlink(), "Sicherung fehlt")
    plan = read_json(backup / "plan.json")
    require(plan["schema"] == 1 and plan["target"] == str(dest.resolve())
            and receipt_hash(dest) == plan["installed_receipt"],
            "Diese Sicherung passt nicht zum aktuellen Codewechsel")
    report = local if local is not None else local_extensions.inspect(dest)
    if report["status"] != "NICHT_EINGERICHTET":
        rel = "controller-base.json"
        changes = plan["files"]
        metadata = restore_capability(dest, backup, rel in changes, changes.get(rel, {}).get("before"),
                                      plan["previous_receipt"])
        check_local_restore(report, metadata, changes)
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
    print(tr("update.roll_back", name=name))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--lang", choices=("en", "de"), help="Language for a new controller")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--skip-runtime", action="store_true", help="Nur Code und lokale Startvorlagen kopieren")
    action.add_argument("--export-code", action="store_true", help="Nur Code für einen Offline-Releasebaum ausgeben")
    action.add_argument("--update", action="store_true", help="Bestehenden Controller prüfen und Update planen")
    action.add_argument("--rollback", metavar="BACKUP", help="Einen bestätigten Codewechsel zurücksetzen")
    parser.add_argument("--apply", metavar="PLAN_SHA256", help="Den exakt geprüften Updateplan einspielen")
    parser.add_argument("--addon", action="append", type=Path, default=[], metavar="CHECKOUT")
    parser.add_argument("--addon-url", action="append", default=[], metavar="NAME=HTTPS_URL")
    parser.add_argument("--addon-token-file", action="append", default=[], metavar="NAME=PATH")
    name = os.environ.get("ANSIBLE_STAGING_OVERLAY")
    if name and name.casefold() not in {"allgm", "homelab"}:
        parser.add_argument("--token-file", metavar="PFAD", help="Lokale Fine-Grained-Token-Datei (0600)")
    args = parser.parse_args()
    if args.apply and not args.update:
        parser.error("--apply setzt --update voraus")
    os.umask(0o077)
    try:
        target = args.target.absolute()
        require(target.name and not target.is_symlink(), "Eigenen Zielordner ohne Symlink angeben")
        require(not target.resolve().is_relative_to(BASE), "Ziel muss außerhalb der Quellablage liegen")
        require(name is None or VERSION_NAME.fullmatch(name) and name.casefold() != "allgm", "Ungültiger Installer-Aufruf")
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
            local = None if args.export_code else inspect_before_change(
                target, write=not args.update or bool(args.apply), rollback=bool(args.rollback))
            if local and not args.rollback:
                require(local_extensions.passed(local), local.get("migration_command") or tr("package.local_digest"))
            if args.rollback:
                rollback_controller(target, args.rollback, local)
                return 0
            profile = name.lower() if name else "allgm"
            addons = load_addons(args.addon, profile, target)
            urls, tokens = addon.assignments(args.addon_url), addon.assignments(args.addon_token_file)
            require(urls.keys() | tokens.keys() <= {n.casefold() for n in addons},
                    "URL or token supplied for undeclared add-on")
            files, sources, layout = local_sources(overlay, name, addons)
            if not args.export_code:
                descriptor = files.get("controller-base.json")
                local_extensions.require_compatible(local, read_json(descriptor) if descriptor else {})
                registered = addon.registrations(version_lines(target / VERSIONS, optional=True))
                require(registered.keys() <= {n.casefold() for n in addons},
                        "Provide checkouts of all registered add-ons or use update-check")
                files[VERSIONS] = version_source(target, sources, scratch, addons=addons, urls=urls, tokens=tokens,
                                                 token_file=getattr(args, "token_file", None), prompt=True)
            contains_files = target.exists() and (not target.is_dir() or any(target.iterdir()))
            if contains_files and not args.export_code:
                previous = addon.receipt(target / RECEIPT)
                import rollout
                _, _, baseline = rollout.managed_baseline(target)
                conflicts, retired = inspect_addon_install(target, BASE, files, layout, previous, baseline)
                require(not conflicts, "Add-on migration blocked: " + ", ".join(conflicts))
                local_conflicts = local_extensions.prospective_conflicts(files, local["files"])
                require(not local_conflicts, tr("extension.prospective_conflict", paths=", ".join(local_conflicts)))
                if addons:
                    variables, registry, overlaps = rollout.guards(target, files, scratch, local["files"])
                    require(not (variables or registry or overlaps), "Prospective module validation failed")
                if args.update:
                    update_controller(target, files, profile, args.apply, retired=retired, layout=layout)
                    return 0
                existing_install(target, files, layout, profile, previous, baseline, retired)
            else:
                require(not args.update, "--update requires an existing controller")
                require(not args.export_code or not target.exists(), "Exportziel existiert bereits")
                prepared = scratch / "controller"
                prepared.mkdir()
                if args.export_code:
                    copy_code(files, prepared)
                else:
                    initialize(prepared, files, args.lang, interactive=not args.skip_runtime)
                    if addons:
                        import check
                        issues = check.check_registry(prepared)
                        require(not issues["issues"], "Add-on registry conflicts")
                    hashes = {rel: sha(src) for rel, src in files.items()}
                    write_receipt(prepared, profile, hashes, layout=layout)
                transaction.sync_files(prepared)
                if args.export_code:
                    target.mkdir(mode=0o700)
                    try:
                        os.replace(prepared, target)
                    except OSError:
                        target.rmdir()
                        raise
                else:
                    os.rename(prepared, target)
                transaction.sync_directory(target.parent)
            if not (args.skip_runtime or args.export_code):
                subprocess.run(["bash", str(target / "bin/setup-runtime")], check=True)
        print(f"Controller {profile}: {target}")
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Controllerinstallation: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
