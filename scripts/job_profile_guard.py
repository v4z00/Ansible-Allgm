#!/usr/bin/env python3
"""Check destination types and ancestors without reading script/unit contents."""
import json
from pathlib import Path
import sys


def check(paths):
    for kind, value in paths:
        path = Path(value)
        if not path.is_absolute() or '..' in path.parts:raise ValueError('Invalid destination')
        for candidate in [path, *path.parents]:
            if candidate.is_symlink():raise ValueError('Destination link refused')
            if candidate != path and candidate.exists() and not candidate.is_dir():raise ValueError('Non-directory destination ancestor')
        if path.exists() and ((kind == 'directory' and not path.is_dir()) or (kind == 'file' and not path.is_file())):
            raise ValueError('Conflicting destination type')


if __name__ == '__main__':
    try:check(json.loads(sys.argv[1]));print('{"ok":true}')
    except (ValueError, OSError, IndexError, TypeError):sys.exit('Profile destination check failed; no content inspected.')
