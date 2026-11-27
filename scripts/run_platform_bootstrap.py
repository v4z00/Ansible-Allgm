#!/usr/bin/env python3
"""Keep the established SSH bootstrap and select Windows only when requested."""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(arguments):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--platform', choices=['linux', 'windows'], default='linux')
    options, forwarded = parser.parse_known_args(arguments)
    if options.platform == 'linux':
        return [sys.executable, str(ROOT / 'scripts/run_bootstrap.py'), *forwarded]
    selection = None
    for position, value in enumerate(forwarded):
        if value in ('--limit', '-l'):
            selection = forwarded[position + 1] if position + 1 < len(forwarded) else ''
        elif value.startswith('--limit='):
            selection = value.split('=', 1)[1]
        elif value.startswith('-l') and not value.startswith('--'):
            selection = value[2:]
    if not selection or not selection.strip() or selection.startswith('-'):
        parser.error('Windows bootstrap requires --limit HOST_OR_GROUP')
    return ['ansible-playbook', 'playbooks/windows/bootstrap.yml', *forwarded]


def main():
    os.chdir(ROOT)
    args = command(sys.argv[1:])
    os.execvp(args[0], args)


if __name__ == '__main__':
    main()
