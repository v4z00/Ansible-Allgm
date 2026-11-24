#!/usr/bin/env python3
"""Update only known managed code in the existing controller directory."""

import argparse
from contextlib import redirect_stdout
import fcntl
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time

import check
import local_extensions
import staging_manifest as manifest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import github_https
import install_controller as install

SHA = re.compile(r"[0-9a-f]{64}\Z")


def show_versions(root):
    try:
        rows = install.read_versions(root / install.VERSIONS)
    except (OSError, ValueError):
        print("versions.txt fehlt, ist unlesbar oder enthält einen ungültigen Eintrag.", file=sys.stderr)
        return 1
    for name, (version, _, _) in rows.items():
        print(name, version)
    if any(name.casefold() in ("tui", "ansible-tui") for name in rows):
        return 0
    search_path = os.pathsep.join((os.environ.get("PATH", os.defpath),
                                   str(Path.home() / ".local/bin")))
    tui = shutil.which("ansible-tui", path=search_path)
    if tui:
        try:
            value = subprocess.run([tui, "--version"], capture_output=True, timeout=5, check=True)
            match = re.fullmatch(rb"(?:ansible-tui|Ansible TUI) (s?[0-9]+\.[0-9]+\.[0-9]+(?:[-+][a-zA-Z0-9.-]+)?)",
                                 value.stdout.strip())
        except (OSError, subprocess.SubprocessError):
            match = None
        if not match:
            print("Ansible-TUI: Version nicht lesbar.", file=sys.stderr)
            return 1
        print("Ansible-TUI", match[1].decode("ascii"))
    elif not rows:
        print("Keine installierten Module gefunden.")
    return 0


def private_file(path):
    info = path.lstat()
    install.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid()
                    and not info.st_mode & 0o077, f"Private Datei mit Modus 0600 erforderlich: {path.name}")


def checkout(scratch, name, row, controller, branch):
    _, url, token_file = row
    install.require(not github_https.legacy_https(url),
                    f"{name}: SSH-Eintrag über den Installer auf HTTPS umstellen")
    if name == "NXTS3":
        install.require(token_file, f"{name}: Token-Dateipfad in versions.txt fehlt")
    else:
        install.require(not token_file, f"{name} wird anonym geladen. Viertes Feld in versions.txt leeren.")
    root = scratch / name
    github_https.clone_branch(url, root, branch, token_file, controller)
    entries = manifest.verify(root, name)
    files = {rel: root / rel for rel in entries}
    for rel, path in files.items():
        install.require(path.is_file() and not path.is_symlink()
                        and install.sha(path) == entries[rel]["sha256"],
                        f"{name}: SHA-256-Abweichung in Arbeitskopie: {rel}")
        path.chmod(int(entries[rel]["mode"], 8))
    return root, {rel: path for rel, path in files.items() if rel not in {"VERSION.txt", "controller-overlay.json", "install-controller", "install.sh"}}


def managed_baseline(root):
    # A local receipt is the last successfully installed content, not a desired state.
    if install.receipt_hash(root) is not None:
        data = manifest.load(root / install.RECEIPT)
        install.require(data.get("schema") == 1 and isinstance(data.get("files"), dict),
                        "Installationsnachweis ungültig")
        receipt = {rel: value for rel, value in data["files"].items()
                   if manifest.ship(rel) and manifest.allowed(rel)
                   and isinstance(value, str) and SHA.fullmatch(value)}
        return data.get("profile"), data.get("source"), receipt
    # Existing controllers with the previous checker already carry a verified code list.
    directory = root / "update_check"
    legacy = {}
    release = directory / "release.json"
    if release.is_file() and (directory / "integrity.json").is_file():
        seal = manifest.load(directory / "integrity.json")["files"]
        install.require(install.sha(release) == seal.get("release.json"),
                        "Bisheriges Prüfmanifest stimmt nicht mit lokaler Integrität überein")
        doc = manifest.load(release)
        for rel in doc["manifests"]:
            source = check.guarded(directory, rel)
            install.require(install.sha(source) == seal.get(rel),
                            "Bisheriges Komponentenmanifest ist verändert")
            legacy.update(manifest.load(source)["files"])
        for ext in (directory / "extensions").glob("*/manifest.json"):
            if not ext.resolve().is_relative_to(directory) or ext.parent.is_symlink():
                continue
            if install.sha(ext) == manifest.load(ext.parent / "integrity.json").get("manifest_sha256"):
                legacy.update(manifest.load(ext)["files"])
        return None, None, legacy
    return None, None, legacy


def guards(root, combined, temporary, local_files=()):
    stage = temporary / "prospective"
    stage.mkdir()
    install.copy_code(combined, stage)
    here = stage / "update_check"
    contract = check.load_json(here / "settings_contract.json")
    variables = check.check_settings(root, contract, code_root=stage, report_unknown=False, check_links=False)
    issues = [{"key": row["key"], "status": row["status"]} for row in variables["fields"]
              if row["severity"] == "error" or row["required"] and row["severity"] == "warning"]
    issues.extend({k: row[k] for k in ("key", "path", "status") if k in row} for row in variables["errors"])
    release = check.load_json(here / "release.json")
    registry_issues = check.check_registry(stage, release.get("feature_defaults"), settings_root=root)["issues"]
    local_conflicts = [row["path"] for row in local_files if row["status"] == "OK"
                       and local_extensions.overlaps_base(stage, row["path"])]
    return issues, registry_issues, local_conflicts


def prune(root, days):
    backup_dir = install.backup_home(root)
    if not backup_dir.is_dir():
        return
    items = sorted(item for item in backup_dir.iterdir() if install.BACKUP_ID.fullmatch(item.name)
                   and not item.is_symlink() and item.is_dir() and (item / "plan.json").is_file())
    cutoff = time.time() - days * 86400
    for item in items[:-1]:
        if item.stat().st_mtime < cutoff:
            shutil.rmtree(item)


def rollout(root, args, local_files=()):
    marker = root / install.VERSIONS
    private_file(marker)
    rows = install.read_versions(marker)
    branch = "staging" if args.staging else "main"
    saved_profile, previous_branch, baseline = managed_baseline(root)
    nxts3 = (root / "roles/nxts3").is_dir()
    homelab = (root / "roles/openwrt_operations").is_dir()
    install.require(not (nxts3 and homelab), "Homelab und NXTS3 sind getrennte Controller")
    profile = "NXTS3" if nxts3 else "Homelab" if homelab else "Allgm"
    install.require(saved_profile in (None, profile.lower()),
                    "Installationsnachweis und vorhandenes System passen nicht zusammen")
    with tempfile.TemporaryDirectory(prefix=f"ansible-{branch}-") as tmp:
        folder = Path(tmp).resolve()
        names = ["Allgm", profile] if profile != "Allgm" else ["Allgm"]
        install.require(all(name in rows and rows[name][1] for name in names),
                        "GitHub-URL für installierte Module in versions.txt eintragen")
        allgm, combined = checkout(folder, "Allgm", rows["Allgm"], root, branch)
        sources = {"Allgm": allgm}
        if profile != "Allgm":
            overlay, extension = checkout(folder, profile, rows[profile], root, branch)
            sources[profile] = overlay
            combined = install.merge_overlay(combined, extension,
                                             manifest.load(overlay / "controller-overlay.json"), profile)
        variable_issues, registry_issues, local_conflicts = guards(root, combined, folder, local_files)
        combined[install.VERSIONS] = install.version_source(root, sources, folder, branch=branch)
        candidates = install.update_files(combined)
        retired = set()
        if saved_profile and (branch == "staging" or previous_branch == "staging"):
            retired = {rel for rel in install.update_files(baseline)
                       if rel not in combined and install.is_code(rel)}
        plan, token = install.update_plan(root, candidates, profile.lower(), retired)
        changes = plan["files"]
        conflicts = [
            rel for rel, row in changes.items()
            if rel != install.VERSIONS and (
                (row["before"] is not None and row["before"] != baseline.get(rel))
                or (row["before"] is None and rel in baseline)
            )
        ]
        result = {"profile": profile, "branch": branch,
                  "versions": {name: install.version_for(source, branch) for name, source in sources.items()},
                  "changes": sorted(changes), "conflicts": conflicts,
                  "variables": variable_issues, "registry": registry_issues,
                  "local_conflicts": local_conflicts, "applied": False}
        if variable_issues or registry_issues or conflicts or local_conflicts:
            return 1, result
        if args.apply or args.auto:
            if changes or saved_profile is None or previous_branch != branch:
                # The shared controller lock remains held through preflight and writes.
                with redirect_stdout(io.StringIO()) as details:
                    install.update_controller(root, combined, profile.lower(), token, receipt_source=branch, retired=retired)
                result["applied"] = True
                result["result"] = details.getvalue().splitlines()
            if args.auto:
                prune(root, args.retention_days)
        return 0, result


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument("--remote", action="store_true", help="Branch prüfen und Änderungen anzeigen (Standard: main)")
    modes.add_argument("--apply", action="store_true", help="Geprüften Code des gewählten Branches übernehmen")
    modes.add_argument("--auto", action="store_true", help="main nichtinteraktiv per Cron übernehmen")
    modes.add_argument("--rollback", metavar="BACKUP", help="Gesicherten Codewechsel zurücknehmen")
    ap.add_argument("--staging", action="store_true", help="Für diesen Aufruf staging statt main prüfen oder übernehmen")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--retention-days", type=int, choices=(3, 4), default=4)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.staging and (args.auto or args.rollback):
        ap.error("--staging lässt sich nur zur Vorschau oder mit --apply verwenden. --auto verwendet main.")
    if not (args.staging or args.remote or args.apply or args.auto or args.rollback):
        ap.error("Update-Modus fehlt")
    branch = "staging" if args.staging else "main"
    os.umask(0o077)
    try:
        install.require(not args.root.is_symlink(), "Projektroot darf kein Symlink sein")
        root = args.root.resolve()
        install.require((root / "bin/control").is_file(), "Ansible-Controller mit bin/control erforderlich")
        lock = root.parent / f".{root.name}.controller-lock"
        fd = os.open(lock, os.O_CREAT | os.O_NOFOLLOW | os.O_RDWR, 0o600)
        with os.fdopen(fd, "r+"):
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if args.rollback:
                install.rollback_controller(root, args.rollback)
                return 0
            local = local_extensions.inspect(root)
            if not args.json:
                local_extensions.display(local)
            if not local_extensions.passed(local):
                if args.json:
                    print(json.dumps({"branch": branch, "applied": False, "local_extensions": local}))
                else:
                    print(f"Update aus {branch} wegen der lokalen SHA-Prüfung blockiert.")
                return 1
            status, result = rollout(root, args, local["files"])
            result["local_extensions"] = local
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"{result['profile']} {branch} · {len(result['changes'])} Änderungen")
            for module, version in result["versions"].items():
                print(f"  {module} {version}")
            for label, field in (("Codepfad", "changes"), ("Lokaler Konflikt", "conflicts"),
                                 ("Variable", "variables"), ("Registry", "registry"),
                                 ("Pfadkonflikt mit lokaler Erweiterung", "local_conflicts")):
                for value in result[field]:
                    print(label, value if isinstance(value, str) else " ".join(value.values()))
            for line in result.get("result", ()):
                print(line)
            print("Update blockiert." if status else "Prüfung erfolgreich.")
        return status
    except BlockingIOError:
        print("Ein Controller-Update läuft bereits.", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, check.AuditError,
            subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        print(f"Update abgebrochen: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
