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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from controller_i18n import cli_args, error_text, machine_report, status_text, tr

import check
import local_extensions
import staging_manifest as manifest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import github_https
import install_controller as install

SHA = re.compile(r"[0-9a-f]{64}\Z")


def show_versions(root):
    try:
        lines = install.version_lines(root / install.VERSIONS)
        rows = install.parse_versions(lines)
        requested = install.addon.registrations(lines)
        receipt = install.addon.receipt(root / install.RECEIPT)
        recorded = {name.casefold(): (name, meta["version"])
                    for name, meta in receipt.get("modules", {}).items()}
    except (OSError, ValueError):
        print(tr("update.bad_versions"), file=sys.stderr)
        return 1
    for name, (version, _, _) in rows.items():
        if name.casefold() in recorded:
            print(*recorded.pop(name.casefold()))
        elif name.casefold() in requested:
            print(name, tr("update.pending"))
        else:
            print(name, version)
    for name, version in recorded.values():
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
            print(tr("update.unreadable_tui"), file=sys.stderr)
            return 1
        print("Ansible-TUI", match[1].decode("ascii"))
    elif not rows:
        print(tr("update.no_modules"))
    return 0


def private_file(path):
    info = path.lstat()
    install.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid()
                    and not info.st_mode & 0o077, tr("update.private_mode", file=path.name))


def checkout(scratch, name, row, controller, branch, *, addon=False):
    _, url, token_file = row
    install.require(not github_https.legacy_https(url),
                    tr("update.https_row", module=name))
    if name.casefold() in {"allgm", "homelab"}:
        install.require(not token_file, tr("update.public_token", module=name))
    root = scratch / name
    github_https.clone_branch(url, root, branch, token_file, controller)
    if addon:
        meta, mapping = install.addon.descriptor(root, name)
        return root, meta, mapping
    entries = manifest.verify(root, name)
    files = {rel: root / rel for rel in entries}
    for rel, path in files.items():
        install.require(path.is_file() and not path.is_symlink()
                        and install.sha(path) == entries[rel]["sha256"],
                        tr("update.checkout_hash", module=name, path=rel))
        path.chmod(int(entries[rel]["mode"], 8))
    return root, {rel: path for rel, path in files.items() if rel not in {"VERSION.txt", "controller-overlay.json", "install-controller", "install.sh"}}


def managed_baseline(root):
    # A local receipt is the last successfully installed content, not a desired state.
    if install.receipt_hash(root) is not None:
        data = install.addon.receipt(root / install.RECEIPT)
        install.require(data.get("schema") in (1, 2) and isinstance(data.get("files"), dict),
                        tr("update.bad_receipt"))
        receipt = {rel: value for rel, value in data["files"].items()
                   if manifest.ship(rel) and manifest.allowed(rel)
                   and isinstance(value, str) and SHA.fullmatch(value)}
        previous_branch = data.get("source")
        if not previous_branch and data.get("schema") == 2:
            installed_version = data["modules"]["Allgm"]["version"]
            if install.STAGING_VERSION.fullmatch(installed_version):
                previous_branch = "staging"
        return data.get("profile"), previous_branch, receipt
    # Existing controllers with the previous checker already carry a verified code list.
    directory = root / "update_check"
    legacy = {}
    release = directory / "release.json"
    if release.is_file() and (directory / "integrity.json").is_file():
        seal = manifest.load(directory / "integrity.json")["files"]
        install.require(install.sha(release) == seal.get("release.json"),
                        tr("update.original_release_hash"))
        doc = manifest.load(release)
        for rel in doc["manifests"]:
            source = check.guarded(directory, rel)
            install.require(install.sha(source) == seal.get(rel),
                            tr("update.original_component_hash"))
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
    local_conflicts = local_extensions.prospective_conflicts(combined, local_files)
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


def rollout(root, args, local_report):
    marker = root / install.VERSIONS
    private_file(marker)
    lines = install.version_lines(marker)
    rows = install.parse_versions(lines)
    registrations = install.addon.registrations(lines)
    previous = install.addon.receipt(root / install.RECEIPT)
    branch = "staging" if args.staging else "main"
    saved_profile, previous_branch, baseline = managed_baseline(root)
    profile_id = install.installed_profile(root)
    profile = next((name for name in rows if name.casefold() == profile_id), None)
    install.require(profile is not None, tr("update.profile_url"))
    with tempfile.TemporaryDirectory(prefix=f"ansible-{branch}-") as tmp:
        folder = Path(tmp).resolve()
        names = ["Allgm", profile] if profile != "Allgm" else ["Allgm"]
        by_key = {n.casefold(): n for n in rows}
        install.require(registrations.keys() <= by_key.keys()
                        and registrations.keys().isdisjoint(n.casefold() for n in names),
                        tr("update.addon_row"))
        install.require(install.addon.installed(previous).keys() <= registrations.keys(),
                        tr("update.restore_registration"))
        install.require(all(name in rows and rows[name][1] for name in names),
                        tr("update.module_url"))
        allgm, combined = checkout(folder, "Allgm", rows["Allgm"], root, branch)
        descriptor = combined.get("controller-base.json")
        metadata = manifest.load(descriptor) if descriptor else {}
        local_extensions.require_compatible(local_report, metadata)
        capability = metadata.get("addon_contract", 0)
        install.require(type(capability) is int and capability in (0, 1),
                        tr("update.unsupported_contract"))
        install.require(capability == 1 or not registrations,
                        tr("update.target_addons"))
        sources = {"Allgm": allgm}
        owners = dict.fromkeys(combined, "Allgm")
        if profile != "Allgm":
            overlay, extension = checkout(folder, profile, rows[profile], root, branch)
            sources[profile] = overlay
            combined = install.merge_overlay(combined, extension,
                                             manifest.load(overlay / "controller-overlay.json"), profile)
            owners.update(dict.fromkeys(extension, profile))
        addons = {}
        for key in registrations:
            name = by_key[key]
            addons[name] = checkout(folder, name, rows[name], root, branch, addon=True)
            sources[name] = addons[name][0]
        combined, owners = install.addon.combine(combined, owners, addons)
        layout = {"owners": owners,
                  "modules": install.addon.module_info(sources, addons, install.version_for, branch)}
        migration_issues, retired = install.inspect_addon_install(root, allgm, combined, layout,
                                                                  previous, baseline)
        variable_issues, registry_issues, local_conflicts = guards(root, combined, folder, local_report["files"])
        combined[install.VERSIONS] = install.version_source(root, sources, folder, branch=branch, addons=addons)
        candidates = install.update_files(combined)
        if saved_profile and (branch == "staging" or previous_branch == "staging"):
            retired |= {rel for rel in install.update_files(baseline)
                       if rel not in combined and install.is_code(rel)}
        # An older checker must be able to read the receipt after switching back.
        target_layout = layout if capability == 1 else None
        if target_layout:
            metadata_changed = (previous.get("modules") != layout["modules"]
                                or previous.get("owners") != layout["owners"])
        else:
            metadata_changed = previous.get("schema") != 1
        plan, token = install.update_plan(root, candidates, profile.lower(), retired, target_layout)
        changes = plan["files"]
        conflicts = [
            rel for rel, row in changes.items()
            if rel != install.VERSIONS and (
                (row["before"] is not None and row["before"] != baseline.get(rel))
                or (row["before"] is None and rel in baseline)
            )
        ]
        conflicts = sorted(set(conflicts) | set(migration_issues))
        result = {"profile": profile, "branch": branch,
                  "versions": {name: install.version_for(source, branch) for name, source in sources.items()},
                  "changes": sorted(changes), "conflicts": conflicts,
                  "variables": variable_issues, "registry": registry_issues,
                  "local_conflicts": local_conflicts, "applied": False}
        if variable_issues or registry_issues or conflicts or local_conflicts:
            return 1, result
        if args.apply or args.auto:
            if changes or saved_profile is None or previous_branch != branch or metadata_changed:
                # The shared controller lock remains held through preflight and writes.
                with redirect_stdout(io.StringIO()) as details:
                    install.update_controller(root, combined, profile.lower(), token, receipt_source=branch, retired=retired, layout=target_layout)
                result["applied"] = True
                result["result"] = details.getvalue().splitlines()
            if args.auto:
                prune(root, args.retention_days)
        return 0, result


def main(argv=None):
    argv = cli_args(argv, Path(__file__).resolve().parents[1])
    ap = argparse.ArgumentParser(description=tr("update.description"))
    ap.add_argument("--lang", choices=("de", "en"), help=tr("cli.lang"))
    modes = ap.add_mutually_exclusive_group()
    modes.add_argument("--remote", action="store_true", help=tr("update.preview_help"))
    modes.add_argument("--apply", action="store_true", help=tr("update.apply_help"))
    modes.add_argument("--auto", action="store_true", help=tr("update.auto_help"))
    modes.add_argument("--rollback", metavar="BACKUP", help=tr("update.rollback_help"))
    ap.add_argument("--staging", action="store_true", help=tr("update.staging_help"))
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--retention-days", type=int, choices=(3, 4), default=4)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.staging and (args.auto or args.rollback):
        ap.error(tr("update.branch_guard"))
    if not (args.staging or args.remote or args.apply or args.auto or args.rollback):
        ap.error(tr("update.missing_mode"))
    branch = "staging" if args.staging else "main"
    os.umask(0o077)
    try:
        install.require(not args.root.is_symlink(), tr("update.root_link"))
        root = args.root.resolve()
        install.require((root / "bin/control").is_file(), tr("update.missing_controller"))
        lock = root.parent / f".{root.name}.controller-lock"
        fd = os.open(lock, os.O_CREAT | os.O_NOFOLLOW | os.O_RDWR, 0o600)
        with os.fdopen(fd, "r+"):
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            local = install.inspect_before_change(root, write=bool(args.apply or args.auto or args.rollback),
                                                  rollback=bool(args.rollback))
            if not args.json:
                local_extensions.display(local)
            rollback_legacy = args.rollback and local["status"] == local_extensions.MIGRATION_REQUIRED
            if not local_extensions.passed(local) and not rollback_legacy:
                if args.json:
                    print(json.dumps(machine_report({"branch": branch, "applied": False, "local_extensions": local})))
                else:
                    print(tr("update.local_block", branch=branch))
                return 1
            if args.rollback:
                install.rollback_controller(root, args.rollback, local)
                return 0
            status, result = rollout(root, args, local)
            result["local_extensions"] = local
        if args.json:
            print(json.dumps(machine_report(result), ensure_ascii=False, indent=2))
        else:
            print(tr("update.change_count", profile=result["profile"], branch=branch, count=len(result["changes"])))
            for module, version in result["versions"].items():
                print(f"  {module} {version}")
            for label, field in ((tr("update.code_path"), "changes"), (tr("update.conflict"), "conflicts"),
                                 (tr("update.variable"), "variables"), (tr("update.registry"), "registry"),
                                 (tr("update.local_path_conflict"), "local_conflicts")):
                for value in result[field]:
                    print(label, error_text(value) if isinstance(value, str) else " ".join(status_text(v) if k == "status" else v for k, v in value.items()))
            for line in result.get("result", ()):
                print(line)
            print(tr("update.blocked") if status else tr("update.success"))
        return status
    except BlockingIOError:
        print(tr("update.locked"), file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, check.AuditError,
            subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        print(tr("update.aborted", error=error_text(error)), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
