#!/usr/bin/env python3
"""Prepare the Windows resolver; never open private account settings/secrets."""
import argparse
import datetime
import hashlib
import os
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
KNOWN_RESOLVERS = frozenset({
    '1ac2489081cba24348ad5ba5050dd21da4d2ba255a42d118d9e40e9574bff264',
    '41d0abf0e1b347c64ad3fd322e3c030c12654bd5fff0b2d39a01566f22c1aa6d',
})


def prepare(root, apply=False, upgrade_known=False):
    source=root/'templates/windows/access.yml.example'
    target=root/'group_vars/all_windows_systems/access.yml'
    exists=target.exists() or target.is_symlink()
    previous=None
    if exists:
        if target.is_symlink() or not target.is_file() or not upgrade_known or target.stat().st_size>65536:
            print('Existing Windows access file retained: '+str(target));return False
        previous=target.read_bytes()
        if previous==source.read_bytes():
            print('Windows resolver already current: '+str(target));return False
        if hashlib.sha256(previous).hexdigest() not in KNOWN_RESOLVERS:
            print('Unknown or locally edited Windows resolver retained: '+str(target));return False
    if not apply:
        print(('Would upgrade known resolver: ' if exists else 'Would create: ')+str(target));return True
    contents=source.read_text(encoding='utf-8')
    target.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    if previous is None:
        # Exclusive creation protects an existing file from replacement.
        with target.open('x',encoding='utf-8') as output:
            os.chmod(target,0o600);output.write(contents)
    else:
        # Only a byte-identical released resolver is eligible. Never adopt local edits.
        if target.is_symlink() or target.read_bytes()!=previous:
            raise ValueError('Resolver changed after preview')
        backup=root/'x/backups/windows-access'
        backup.mkdir(mode=0o700,parents=True,exist_ok=True)
        stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        saved=backup/(stamp+'.yml')
        with saved.open('xb') as output:os.chmod(saved,0o600);output.write(previous)
        with tempfile.NamedTemporaryFile(dir=target.parent,delete=False,mode='w',encoding='utf-8') as output:
            temporary=Path(output.name)
            try:
                os.fchmod(output.fileno(),0o600);output.write(contents);output.flush();os.fsync(output.fileno())
                if target.is_symlink() or target.read_bytes()!=previous:raise ValueError('Resolver changed before replacement')
                os.replace(temporary,target)
            finally:temporary.unlink(missing_ok=True)
        print('Resolver backup: '+str(saved))
    print(('Upgraded: ' if exists else 'Created: ')+str(target));return True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',type=Path,default=ROOT)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--upgrade-known-resolver',action='store_true')
    args=parser.parse_args();os.umask(0o077)
    prepare(args.project.resolve(),args.apply,args.upgrade_known_resolver)
    print('Keep windows_access.user/password together in the EXISTING private secrets.yml.')
    print('Connection settings: templates/windows/settings.example.yml; do not replace existing private files.')
    print('Enabled features.kerberos requires Kerberos, UPN, DNS/time and the Kerberos runtime; no NTLM fallback.')
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError):
        print('Windows access preparation failed; no account settings/secrets were read.',file=sys.stderr);sys.exit(1)
