#!/usr/bin/env python3
"""One registry for controller execution, help and shell shortcuts."""
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

import yaml

from controller_i18n import cli_args, language, tr

ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r'^[a-z0-9][a-z0-9-]*$')
BUILTINS = {'help', 'help-all', 'list', 'shell-init', 'alias-names', 'local-help', 'modules-check'}


def inside(path):
    p = (ROOT / path).resolve()
    if not p.is_relative_to(ROOT) or Path(path).is_absolute():
        raise ValueError(tr('control.invalid_path', path=path))
    return p


def registry():
    commands, aliases = {}, {}
    for path in sorted((ROOT / 'bin/control.d').glob('*.json')):
        data = json.loads(path.read_text())
        if data.get('schema') != 1 or not isinstance(data.get('commands'), list) or len(data['commands']) != 1:
            raise ValueError(tr('control.invalid_module', file=path.name))
        for command in data['commands']:
            name = command['name']
            if not NAME.fullmatch(name) or name in commands or name in BUILTINS:
                raise ValueError(tr('control.invalid_command', name=name))
            if path.stem != name:
                raise ValueError(tr('control.bad_filename', file=path.name))
            inside(command['handler'])
            for requirement in command.get('requires', []):
                inside(requirement)
            commands[name] = command
    for name, command in commands.items():
        for shortcut in command.get('aliases', []):
            alias = shortcut['name']
            if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9-]*', alias) or alias in aliases or alias in BUILTINS:
                raise ValueError(tr('control.bad_alias', name=alias))
            if alias in commands and alias != name:
                raise ValueError(tr('control.alias_conflict', name=alias))
            if not all(isinstance(a, str) for a in shortcut.get('args', [])):
                raise ValueError(tr('control.alias_args'))
            aliases[alias] = (name, shortcut.get('args', []))
    return commands, aliases


def truth(value):
    return value is True or isinstance(value, str) and value.lower() in {'yes', 'on', 'true', '1'}


def state(command):
    missing = [p for p in [command['handler'], *command.get('requires', [])] if not inside(p).is_file()]
    if missing:
        return False, tr('control.missing', paths=', '.join(missing))
    feature = command.get('feature')
    if not feature:
        return True, tr('control.ready')
    path = command.get('settings', 'group_vars/all/settings.yml')
    try:
        data = yaml.safe_load(inside(path).read_text()) or {}
        value = data
        for key in command.get('setting_path', ['features', feature]):
            value = value[key]
    except KeyError:
        return (True, tr('control.default_ready')) if command.get('feature_default') is True else (False, tr('control.unset', name=feature))
    except (OSError, TypeError, yaml.YAMLError):
        return False, tr('control.unreadable', name=feature)
    return (True, tr('control.ready')) if truth(value) else (False, tr('control.disabled', name=feature))


def available(commands):
    return {name: command for name, command in commands.items() if state(command)[0]}


def command_title(name, command):
    path = ROOT / "descriptions" / "commands" / (name + ".md")
    if (path.resolve() != path or not path.is_file()
            or path.stat().st_size > 2 * 1024 * 1024):
        return command["description"]
    block = re.search(r"^```json\s*\n(.*?)\n```", path.read_text(), re.M | re.S)
    if block:
        try:
            contract = json.loads(block[1])
            title = contract.get("i18n", {}).get(language(), {}).get("title")
            if isinstance(title, str) and title.strip():
                return title
        except (ValueError, AttributeError):
            pass
    return command["description"]


def help_text(commands, all_commands=False):
    print(tr('control.usage'))
    for name, command in sorted(commands.items()):
        enabled, why = state(command)
        if enabled or all_commands:
            shortcuts = [a['name'] for a in command.get('aliases', []) if a['name'] != name]
            suffix = (tr('control.aliases', names=', '.join(shortcuts))) if shortcuts else ''
            if not enabled:
                suffix += ' [' + why + ']'
            print(f'  {name:<27} {command_title(name, command)}{suffix}')
    print(tr('control.modules_help'))


def local_help(commands):
    # Local helpers remain functions. Command aliases are printed from the registry.
    path = ROOT / 'config/shell_aliases.sh'
    text = path.read_text()
    localized = {
        'control': tr('control.local.control'),
        'ansible-cd': tr('control.local.ansible_cd'),
        'ansible-status': tr('control.local.ansible_status'),
        'host-info': tr('control.local.host_info'),
        'group-show': tr('control.local.group_show'),
        'log-show': tr('control.local.log_show'),
        'ansible-run': tr('control.local.ansible_run'),
        'myhelp': tr('control.local.myhelp'),
        'audit-crons': tr('control.local.audit_crons'),
        'reload': tr('control.local.reload'),
        'edit-alias': tr('control.local.edit_alias'),
        'git-save': tr('control.local.git_save'),
        'bashrc-install': tr('control.local.bashrc_install'),
        'my-help': tr('control.local.my_help'),
    }
    pattern = r'^# help: ([^\n]+)\n([a-zA-Z0-9_-]+)\(\)\s*\{(.*?)^\}'
    for description, name, body in re.findall(pattern, text, re.M | re.S):
        target = re.search(r'^\s+control ([a-z0-9-]+)', body, re.M)
        if target and target[1] not in {'help', 'graph', 'last-log'} and target[1] not in available(commands):
            continue
        print(f'  {name:<28} {localized.get(name, description)}')
    for description, name, value in re.findall(r'^# help: (.+)\nalias ([a-zA-Z0-9_-]+)=(.+)$', text, re.M):
        if not re.match(r"[\"']control ", value):
            print(f'  {name:<28} {localized.get(name, description)}')


def main():
    args = cli_args(sys.argv[1:], root=ROOT)
    commands, aliases = registry()
    name = args.pop(0) if args else 'help'
    if name in {'help', '-h', '--help', 'help-all'}:
        help_text(commands, name == 'help-all')
        return 0
    if name == 'list':
        print('\n'.join(sorted(available(commands))))
        return 0
    if name == 'alias-names':
        names = set(aliases)
        # Include obsolete literal aliases for safe cleanup during shell reload.
        path = ROOT / 'config/control/legacy_alias_names.json'
        if path.exists():
            names.update(json.loads(path.read_text()))
        print('\n'.join(sorted(names)))
        return 0
    if name == 'shell-init':
        enabled = available(commands)
        for alias, (command, fixed) in sorted(aliases.items()):
            if command in enabled:
                value = shlex.join(['control', command, *fixed])
                print('alias ' + shlex.quote(alias + '=' + value))
        return 0
    if name == 'local-help':
        local_help(commands)
        return 0
    if name == 'modules-check':
        for command, entry in sorted(commands.items()):
            enabled, why = state(entry)
            print(f'{command}: {why}')
        return 0
    if name in aliases and name not in commands:
        name, fixed = aliases[name]
        args = fixed + args
    if name not in commands:
        print(tr('control.unknown', name=name), file=sys.stderr)
        return 2
    command = commands[name]
    enabled, why = state(command)
    if not enabled:
        print(name + ': ' + why, file=sys.stderr)
        return 2
    # Handler sources shared helpers and preserves original command arguments.
    env = dict(os.environ, CONTROL_PROJECT_ROOT=str(ROOT))
    result = subprocess.run(['bash', str(inside(command['handler'])), *args], cwd=ROOT, env=env)
    return result.returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(tr('control.error', detail=exc), file=sys.stderr)
        raise SystemExit(2)
