#!/usr/bin/env python3
"""Select inventory targets without limiting localhost or dynamic bootstrap hosts."""

import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from controller_i18n import cli_args, tr


ROOT = Path(__file__).resolve().parents[1]
LINUX_PATTERN = "all_linux_systems:!opnsense_firewall"


class BootstrapError(Exception):
    pass


def split_options(args):
    """A legacy --limit is a selection suggestion, never an Ansible limit."""
    forwarded = []
    selection = None
    index = 0
    while index < len(args):
        value = args[index]
        if value in ("--limit", "-l", "--target"):
            index += 1
            if index >= len(args):
                raise BootstrapError(tr('bootstrap.missing_target', value=value))
            target = args[index]
        elif value.startswith(("--limit=", "--target=")):
            target = value.split("=", 1)[1]
        elif value.startswith("-l") and not value.startswith("--") and len(value) > 2:
            target = value[2:]
        else:
            if value in ("-i", "--inventory", "--inventory-file") or value.startswith(
                ("--inventory=", "--inventory-file=")
            ) or (value.startswith("-i") and not value.startswith("--") and len(value) > 2):
                raise BootstrapError(tr('bootstrap.inventory_option'))
            if value in ("--check", "-C"):
                raise BootstrapError(tr('bootstrap.check_mode'))
            if value == "--":
                raise BootstrapError(tr('bootstrap.separator'))
            forwarded.append(value)
            index += 1
            continue
        if selection is not None:
            raise BootstrapError(tr('bootstrap.one_selection'))
        if not target.strip() or target.startswith("-"):
            raise BootstrapError(tr('bootstrap.invalid_selection'))
        selection = target.strip()
        index += 1
    return selection, forwarded


def inventory_data(root):
    result = subprocess.run(
        ["ansible-inventory", "-i", "inventory", "--list"],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if result.returncode:
        # Never print captured inventory output: it can contain credentials.
        raise BootstrapError(tr('bootstrap.inventory_error'))
    try:
        data = json.loads(result.stdout)
    except (ValueError, TypeError) as error:
        raise BootstrapError(tr('bootstrap.invalid_json')) from error
    if not isinstance(data, dict):
        raise BootstrapError(tr('bootstrap.inventory_shape'))
    return data


def group_members(data, group, seen=None):
    seen = set() if seen is None else seen
    if group in seen:
        return set()
    seen.add(group)
    entry = data.get(group, {})
    members = set(entry.get("hosts", []))
    for child in entry.get("children", []):
        members.update(group_members(data, child, seen))
    return members


def expand_selection(selection, candidates):
    if selection.lower() in ("all", "alle"):
        return LINUX_PATTERN
    parts = []
    for item in selection.split(","):
        item = item.strip()
        if not item:
            raise BootstrapError(tr('bootstrap.empty_entry'))
        if item.isdecimal():
            number = int(item)
            if not 1 <= number <= len(candidates):
                raise BootstrapError(tr('bootstrap.unknown_number', item=item))
            item = candidates[number - 1]
        parts.append(item)
    return ",".join(parts)


def resolve_targets(root, pattern, candidates):
    result = subprocess.run(
        ["ansible", "-i", "inventory", LINUX_PATTERN, "--list-hosts", "--limit", pattern],
        cwd=root, capture_output=True, text=True, check=False,
    )
    # Refuse partial matches as well: a misspelled name must not be ignored.
    warnings = result.stderr.lower()
    if result.returncode or "could not match supplied host pattern" in warnings:
        raise BootstrapError(tr('bootstrap.unmatched'))
    expected = set(candidates)
    targets = sorted({line.strip() for line in result.stdout.splitlines() if line.strip() in expected})
    if not targets:
        raise BootstrapError(tr('bootstrap.no_targets'))
    return targets


def ask(prompt, default):
    answer = input(f"{prompt} [{default}]: ").strip()
    return answer or str(default)


def build_profiles(data, targets):
    hostvars = data.get("_meta", {}).get("hostvars", {})
    profiles = []
    for name in targets:
        values = hostvars.get(name, {})
        if not values.get("ansible_host"):
            raise BootstrapError(tr('bootstrap.missing_address', name=name))
        existing = values.get("bootstrap_targets", []) or []
        configured = next((item for item in existing if item.get("name") == name), {})
        access = (values.get("managed_host_access", {}) or {}).get(name, {})
        default_user = configured.get("user") or access.get("user") or values.get("managed_access_default_user") or "root"
        default_port = configured.get("port") or access.get("port") or values.get("managed_access_default_port") or 22
        print(tr('bootstrap.first_access', name=name, address=values['ansible_host']))
        user = ask(tr('bootstrap.user'), default_user)
        if not user or user.startswith("-") or any(char.isspace() for char in user):
            raise BootstrapError(tr('bootstrap.invalid_user', name=name))
        port_text = ask(tr('bootstrap.port'), default_port)
        try:
            port = int(port_text)
        except ValueError as error:
            raise BootstrapError(tr('bootstrap.numeric_port', name=name)) from error
        if not 1 <= port <= 65535:
            raise BootstrapError(tr('bootstrap.port_range', name=name))
        method = "direct"
        if user != "root":
            default_method = configured.get("become_method") or access.get("become_method") or "auto"
            if default_method not in ("auto", "sudo", "su"):
                default_method = "auto"
            method = ask(tr('bootstrap.escalation'), default_method).lower()
            if method not in ("auto", "sudo", "su"):
                raise BootstrapError(tr('bootstrap.invalid_escalation', name=name))
        profile = {"name": name, "user": user, "port": port, "become_method": method}
        for key in ("password_env", "become_password_env"):
            if configured.get(key):
                profile[key] = configured[key]
        profiles.append(profile)
    return profiles


def run_playbook(root, profiles, forwarded):
    log_dir = root / "logs"
    log_dir.mkdir(exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    log = log_dir / f"bootstrap-{stamp}.log"
    print(tr('bootstrap.log', log=log), flush=True)
    payload = {"bootstrap_target": "all", "bootstrap_targets": profiles}
    # mkstemp creates mode 0600. Credentials remain in Ansible's original
    # resolver; this file contains only the selected, non-secret profiles.
    descriptor, path = tempfile.mkstemp(prefix="ansible-bootstrap-", suffix=".json")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        env = os.environ.copy()
        env["ANSIBLE_LOG_PATH"] = str(log)
        return subprocess.run(
            ["ansible-playbook", "-i", "inventory", "playbooks/bootstrap.yml",
             *forwarded, "-e", "@" + path],
            cwd=root, env=env, check=False,
        ).returncode
    finally:
        Path(path).unlink(missing_ok=True)


def main(args=None, root=ROOT):
    args = cli_args(sys.argv[1:] if args is None else args, root=root)
    if any(arg in ("--help", "-h") for arg in args):
        print(tr('bootstrap.help'))
        return 0
    if "--syntax-check" in args:
        return subprocess.run(
            ["ansible-playbook", "-i", "inventory", "playbooks/bootstrap.yml", "--syntax-check"],
            cwd=root, check=False,
        ).returncode
    suggestion, forwarded = split_options(args)
    if not sys.stdin.isatty():
        raise BootstrapError(tr('bootstrap.tty'))
    data = inventory_data(root)
    candidates = sorted(group_members(data, "all_linux_systems") - group_members(data, "opnsense_firewall") - {"localhost"})
    if not candidates:
        raise BootstrapError(tr('bootstrap.empty_group'))
    hostvars = data.get("_meta", {}).get("hostvars", {})
    print(tr('bootstrap.select_hosts'))
    for number, name in enumerate(candidates, 1):
        print(f"{number:3}) {name} ({hostvars.get(name, {}).get('ansible_host', tr('bootstrap.no_address'))})")
    print(tr('bootstrap.selection_help'))
    selection = input(f"{tr('bootstrap.prompt')}{f' [{suggestion}]' if suggestion else ''}: ").strip() or suggestion
    if not selection or selection.lower() in ("q", "quit", "abbruch"):
        print(tr('bootstrap.cancelled'))
        return 0
    targets = resolve_targets(root, expand_selection(selection, candidates), candidates)
    print(tr('bootstrap.selected', count=len(targets)))
    for name in targets:
        print(f"  {name} ({hostvars.get(name, {}).get('ansible_host', tr('bootstrap.no_address'))})")
    if "--list-hosts" in forwarded:
        print(tr('bootstrap.preview'))
        return 0
    if input(tr('bootstrap.confirm')).strip() != "YES":
        print(tr('bootstrap.cancelled'))
        return 0
    profiles = build_profiles(data, targets)
    print(tr('bootstrap.key_first'))
    return run_playbook(root, profiles, forwarded)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BootstrapError, FileNotFoundError) as error:
        print(tr('bootstrap.error', error=error), file=sys.stderr)
        raise SystemExit(2)
    except (EOFError, KeyboardInterrupt):
        print(tr('bootstrap.abort'), file=sys.stderr)
        raise SystemExit(130)
