#!/usr/bin/env python3
"""Create the missing private Windows resolver without reading account settings."""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def prepare(root, apply=False):
    """Never open settings.yml or overwrite a pre-existing connection resolver."""
    source = root / 'templates/windows/access.yml.example'
    target = root / 'group_vars/all_windows_systems/access.yml'
    if target.exists() or target.is_symlink():
        print('Existing Windows access file retained: ' + str(target))
        return False
    if not apply:
        print('Would create: ' + str(target))
        return True
    contents = source.read_text(encoding='utf-8')
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Exclusive creation also prevents a race from replacing an existing file.
    with target.open('x', encoding='utf-8') as output:
        os.chmod(target, 0o600)
        output.write(contents)
    print('Created: ' + str(target))
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=ROOT)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    os.umask(0o077)
    prepare(args.project.resolve(), args.apply)
    print('Add windows_access.user/password to the EXISTING private settings.yml.')
    print('Neutral fields: templates/windows/settings.example.yml; do not replace settings.yml.')
    print('Group Windows hosts under all_windows_systems; then run windows-check --limit HOST.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError):
        print('Windows access preparation failed; no settings values were read.', file=sys.stderr)
        sys.exit(1)
