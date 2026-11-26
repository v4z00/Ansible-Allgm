#!/usr/bin/env python3
"""Migrate the active local-extension register under the controller's existing writer lock."""
import argparse
from contextlib import contextmanager, ExitStack
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import stat
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "update_check"))
from controller_i18n import cli_args, tr
import local_extensions as ext


REGISTER = "register.json"
BACKUP = re.compile(r"register\.json\.schema1\.\d{8}T\d{12}Z\.([0-9a-f]{64})\.bak\Z")
DIR = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
READ = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
NEW = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW


def secure(info):
    if info.st_uid != os.geteuid() or info.st_mode & 0o022:
        raise ValueError(tr("migration.permissions"))


@contextmanager
def parent_directory(path):
    """Descend without following directory links, retaining an open anchor."""
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError(tr("migration.path"))
    fd = os.open("/", DIR)
    try:
        for part in path.parts[1:]:
            child = os.open(part, DIR, dir_fd=fd)
            os.close(fd)
            fd = child
        secure(os.fstat(fd))
        yield fd
    finally:
        os.close(fd)


@contextmanager
def directory(parent, name):
    fd = os.open(name, DIR, dir_fd=parent)
    try:
        secure(os.fstat(fd))
        yield fd
    finally:
        os.close(fd)


@contextmanager
def locked(parent, name, check):
    """The preview never creates a lock file; an existing writer excludes it."""
    try:
        flags = READ if check else os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK
        fd = os.open(name, flags, 0o600, dir_fd=parent)
    except FileNotFoundError:
        if not check:
            raise
        yield
        return
    try:
        info = os.fstat(fd)
        secure(info)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError(tr("migration.lock_file"))
        fcntl.flock(fd, (fcntl.LOCK_SH if check else fcntl.LOCK_EX) | fcntl.LOCK_NB)
        yield
    finally:
        os.close(fd)


def read_file(folder, name, *, private=False):
    fd = os.open(name, READ, dir_fd=folder)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(fd)
        secure(info)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError(tr("migration.regular"))
        if private and stat.S_IMODE(info.st_mode) != 0o600:
            raise ValueError(tr("migration.backup_mode"))
        content = stream.read()
    return content, (info.st_dev, info.st_ino)


def unique(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError(tr("migration.invalid"))
    return result


def reject_constant(_value):
    raise ValueError(tr("migration.invalid"))


def register(raw, identifier):
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=reject_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise ValueError(tr("migration.invalid")) from None
    if (not isinstance(data, dict) or type(data.get("schema")) is not int or data["schema"] not in (1, 2)
            or data.get("id") != identifier or not isinstance(data.get("files"), dict)):
        raise ValueError(tr("migration.invalid"))
    if "supplement" in data:
        ext.supplement_name(data["supplement"])
    for path, entry in data["files"].items():
        if (not all(ext.PART.fullmatch(part) for part in path.split("/")) or not isinstance(entry, dict)
                or not isinstance(entry.get("sha256"), str) or not ext.HEX.fullmatch(entry["sha256"])):
            raise ValueError(tr("migration.invalid"))
        if "supplement" in entry:
            ext.supplement_name(entry["supplement"])
        if "archive" in entry and not (isinstance(entry["archive"], str) and ext.IDENT.fullmatch(entry["archive"])):
            raise ValueError(tr("migration.invalid"))
        entry["cleanup"] = ext.normalize_cleanup(entry.get("cleanup"), schema=data["schema"])
    return data


def schema_two(data):
    upgraded = {**data, "schema": 2}
    return (json.dumps(upgraded, sort_keys=True, indent=2, ensure_ascii=False, allow_nan=False) + "\n").encode()


def new_file(folder, name, data):
    fd = os.open(name, NEW, 0o600, dir_fd=folder)
    try:
        with os.fdopen(fd, "wb") as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        os.unlink(name, dir_fd=folder)
        raise


def replace_register(folder, expected, updated):
    name = ".register-migration-" + secrets.token_hex(16)
    new_file(folder, name, updated)
    try:
        if read_file(folder, REGISTER) != expected:
            raise ValueError(tr("migration.changed"))
        os.replace(name, REGISTER, src_dir_fd=folder, dst_dir_fd=folder)
        os.fsync(folder)
    finally:
        try:
            os.unlink(name, dir_fd=folder)
        except FileNotFoundError:
            pass


def run(controller, *, apply=False, rollback=None):
    controller = controller.absolute()
    if not controller.name or controller.name in (".", ".."):
        raise ValueError(tr("migration.path"))
    local = ext.location(controller)
    with ExitStack() as scope:
        parent = scope.enter_context(parent_directory(controller.parent))
        scope.enter_context(locked(parent, "." + controller.name + ".controller-lock", not (apply or rollback)))
        project = scope.enter_context(directory(parent, controller.name))
        state = scope.enter_context(directory(project, ".local"))
        folder = scope.enter_context(directory(parent, local.name))
        raw_id, _ = read_file(state, "local-extension-id")
        try:
            identifier = raw_id.decode("ascii").strip()
        except UnicodeError:
            raise ValueError(tr("migration.invalid")) from None
        if not ext.IDENT.fullmatch(identifier):
            raise ValueError(tr("migration.invalid"))
        current = read_file(folder, REGISTER)
        data = register(current[0], identifier)
        audit = ext.inspect(controller)
        if audit.get("integrity_status") != "OK" or audit.get("schema") != data["schema"]:
            raise ValueError(tr("migration.integrity"))
        # A read-only preview can run before any writer has created a lock file.
        if read_file(folder, REGISTER) != current:
            raise ValueError(tr("migration.changed"))

        if rollback is not None:
            backup = Path(rollback)
            match = BACKUP.fullmatch(backup.name)
            if not match or backup not in (Path(backup.name), local / backup.name):
                raise ValueError(tr("migration.backup_path"))
            original, _ = read_file(folder, backup.name, private=True)
            if hashlib.sha256(original).hexdigest() != match[1]:
                raise ValueError(tr("migration.backup_digest"))
            old = register(original, identifier)
            if old["schema"] != 1:
                raise ValueError(tr("migration.invalid"))
            if current[0] == original:
                return tr("migration.restored")
            if current[0] != schema_two(old):
                raise ValueError(tr("migration.stale"))
            replace_register(folder, current, original)
            return tr("migration.restored")

        if data["schema"] == 2:
            return tr("migration.current")
        if not apply:
            return tr("migration.preview", count=len(data["files"]))
        updated = schema_two(data)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = f"{REGISTER}.schema1.{stamp}.{hashlib.sha256(current[0]).hexdigest()}.bak"
        new_file(folder, backup, current[0])
        os.fsync(folder)  # The byte-identical backup must survive before the live file is replaced.
        replace_register(folder, current, updated)
        return tr("migration.applied", count=len(data["files"]), backup=local / backup)


def main(argv=None):
    os.umask(0o077)
    argv = cli_args(argv, Path("/root/ansible"))
    parser = argparse.ArgumentParser(description=tr("migration.description"))
    parser.add_argument("--controller", type=Path, default=Path("/root/ansible"))
    parser.add_argument("--lang", choices=("de", "en"), help=tr("cli.lang"))
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--check", action="store_true", help=tr("migration.check_help"))
    actions.add_argument("--apply", action="store_true", help=tr("migration.apply_help"))
    actions.add_argument("--rollback", metavar="BACKUP", help=tr("migration.rollback_help"))
    args = parser.parse_args(argv)
    try:
        print(run(args.controller, apply=args.apply, rollback=args.rollback))
    except BlockingIOError:
        print(tr("migration.busy"), file=sys.stderr)
        return 1
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    except OSError:
        # Register contents, paths and OS errors can expose site-specific information.
        print(tr("migration.io_error"), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
