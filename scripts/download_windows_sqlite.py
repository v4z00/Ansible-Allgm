#!/usr/bin/env python3
"""Fetch the pinned official SQLite CLI; no executable is stored in Git."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import urllib.request
import zipfile

VERSION='3.54.1'
URL='https://www.sqlite.org/2026/sqlite-tools-win-x64-3540100.zip'
SHA3='e171f3993a992edf076746926dd52b5e2ebfabaee38818e74987e1d8112ab987'
ROOT=Path(__file__).resolve().parents[1]


def download(output):
    with urllib.request.urlopen(URL,timeout=60) as response:data=response.read(32*1024*1024+1)
    if len(data)>32*1024*1024 or hashlib.sha3_256(data).hexdigest()!=SHA3:
        raise ValueError('Official SQLite archive checksum mismatch')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        matches=[name for name in archive.namelist() if Path(name).name=='sqlite3.exe']
        if len(matches)!=1:raise ValueError('Expected exactly one SQLite executable')
        if archive.getinfo(matches[0]).file_size>64*1024*1024:raise ValueError('SQLite executable too large')
        binary=archive.read(matches[0])
    digest=hashlib.sha256(binary).hexdigest()
    output.mkdir(parents=True,exist_ok=True,mode=0o700)
    destination=output/'sqlite3.exe'
    if destination.is_symlink():raise ValueError('Executable symlink refused')
    if destination.exists():
        if destination.read_bytes()!=binary:raise ValueError('Different existing executable retained; choose a new artifact directory')
    else:
        with destination.open('xb') as handle:handle.write(binary)
        destination.chmod(0o600)
    metadata={'version':VERSION,'url':URL,'archive_sha3_256':SHA3,'executable_sha256':digest}
    (output/'source.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print('Verified SQLite '+VERSION+' prepared: '+str(destination))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'artifacts/sqlite/windows')
    parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    if not args.apply:print('Would fetch pinned SQLite '+VERSION+' to '+str(args.output));return 0
    os.umask(0o077);download(args.output);return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError):print('SQLite artifact download failed; no host was contacted.',file=sys.stderr);sys.exit(1)
