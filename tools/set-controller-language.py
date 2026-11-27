#!/usr/bin/env python3
"""Set just the local controller language. Run with the controller's Python."""
import argparse
import fcntl
import os
from pathlib import Path
import re
import stat
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("/root/ansible"))
    parser.add_argument("--lang", choices=("de", "en"), default="de")
    parser.add_argument("--check", action="store_true", help="preview without writing")
    args = parser.parse_args()
    root = args.root.absolute()
    path = root / "group_vars/all/settings.yml"
    if not (root / "controller-base.json").is_file() or path.resolve() != path:
        parser.exit(1, "Expected an installed controller with a direct settings path.\n")
    sys.path.insert(0, str(root / "update_check"))
    import check
    import configure
    import yaml

    os.umask(0o077)
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > 1024 * 1024:
                parser.exit(1, "Expected a regular local settings file.\n")
            raw = stream.read()
            crlf = b"\r\n" in raw and b"\n" not in raw.replace(b"\r\n", b"")
            text = raw.decode("utf-8").replace("\r\n", "\n") if crlf else raw.decode("utf-8")
            before = configure._parse(text, check.UniqueLoader)
            if before.get("controller_lang") == args.lang and re.search(
                rf"""^controller_lang[ \t]*:[ \t]+(['"]?){args.lang}\1(?:[ \t]+\#[^\n]*|[ \t]*)$""", text, re.M
            ):
                print(f"controller_lang: {args.lang} (already set)")
                return
            updated = configure.set_field(text, "controller_lang", args.lang, check.UniqueLoader)
            if (configure._parse(updated, check.UniqueLoader) != {**before, "controller_lang": args.lang}
                    or not re.search(rf"^controller_lang[ \t]*:[ \t]+{args.lang}(?:[ \t]+\#[^\n]*|[ \t]*)$", updated, re.M)):
                parser.exit(1, "Settings need manual review.\n")
            if args.check:
                print(f"Would set controller_lang: {args.lang}")
                return
            backup_root = root / "x/backups/update_check"
            if backup_root.resolve() != backup_root:
                parser.exit(1, "Expected a direct local backup path.\n")
            payload = (updated.replace("\n", "\r\n") if crlf else updated).encode()
            backup = configure._transaction(root, [(path, payload, False)], {path: raw})
            print(f"controller_lang: {args.lang}\nBackup: {backup}")
    except (OSError, UnicodeError, ValueError, check.AuditError, configure.ConfigureError, yaml.YAMLError):
        parser.exit(1, "Could not safely update local settings. Check the path and YAML.\n")


if __name__ == "__main__":
    main()
