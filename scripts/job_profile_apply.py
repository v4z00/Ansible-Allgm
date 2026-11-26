#!/usr/bin/env python3
"""Apply only explicit service lifecycle settings; query status properties only."""
import argparse
import json
import re
import subprocess
import sys


def command(arguments):
    result = subprocess.run(['systemctl', '--no-pager', *arguments], capture_output=True, text=True, timeout=180)
    if result.returncode:raise ValueError('Systemd action failed')
    return result.stdout


def apply(entries, reload=False):
    # Validate the entire action list before the first mutation.
    if not isinstance(entries, list):raise ValueError('Explicit action list required')
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) - {'unit', 'enabled', 'state'}:raise ValueError('Invalid action fields')
        if not isinstance(entry.get('unit'), str) or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.:@-]*\.service', entry['unit']):raise ValueError('Invalid unit name')
        if 'enabled' in entry and type(entry['enabled']) is not bool:raise ValueError('Invalid enabled flag')
        if 'state' in entry and entry['state'] not in ('started', 'stopped', 'restarted', 'reloaded'):raise ValueError('Invalid service state')
    changed = False
    if reload:command(['daemon-reload']);changed = True
    for entry in entries:
        if 'enabled' not in entry and 'state' not in entry:continue
        raw = command(['show', entry['unit'], '--property=LoadState,ActiveState,UnitFileState'])
        values = {key: value for line in raw.splitlines() for key, sep, value in [line.partition('=')]
                  if sep and key in ('LoadState', 'ActiveState', 'UnitFileState')}
        if values.get('LoadState') != 'loaded' or values.get('UnitFileState') in ('masked', 'masked-runtime'):
            raise ValueError('Unit missing, masked or unavailable; no automatic unmask')
        if 'enabled' in entry:
            state = values.get('UnitFileState')
            if state not in ('enabled', 'enabled-runtime', 'disabled', 'static', 'indirect', 'linked', 'linked-runtime', 'alias'):
                raise ValueError('Unknown enable state')
            if entry['enabled'] and state != 'enabled':command(['enable', entry['unit']]);changed = True
            elif not entry['enabled'] and state in ('enabled', 'enabled-runtime'):
                command(['disable', entry['unit']]);changed = True
        action = entry.get('state')
        if action == 'started' and values.get('ActiveState') not in ('active', 'reloading'):action = 'start'
        elif action == 'stopped' and values.get('ActiveState') not in ('inactive', 'failed'):action = 'stop'
        elif action in ('restarted', 'reloaded'):action = {'restarted': 'restart', 'reloaded': 'reload'}[action]
        else:action = None
        if action:command([action, entry['unit']]);changed = True
    return {'changed': changed}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('entries');parser.add_argument('--reload', action='store_true');args = parser.parse_args()
    try:print(json.dumps(apply(json.loads(args.entries), args.reload)))
    except (ValueError, OSError, TypeError, subprocess.TimeoutExpired):sys.exit('Systemd profile action failed; raw diagnostics suppressed.')
