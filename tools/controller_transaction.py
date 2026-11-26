"""Durable, single-writer code updates. Callers hold the controller lock."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile


def sync_directory(path):
    fd = os.open(path, os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def sync_files(directory):
    for base, _, files in os.walk(directory, topdown=False):
        for name in files:
            fd = os.open(Path(base) / name, os.O_RDONLY | os.O_NOFOLLOW)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        sync_directory(base)


def state(path):
    if path is None:
        return None
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("Unexpected file type in controller transaction")
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return [digest.hexdigest(), stat.S_IMODE(info.st_mode)]


def replace(target, src):
    if src is None:
        target.unlink(missing_ok=True)
    else:
        missing = [p for p in target.parents if not p.exists()]
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        for directory in reversed(missing):
            sync_directory(directory.parent)
        fd, name = tempfile.mkstemp(prefix=".controller-write-", dir=target.parent)
        try:
            with os.fdopen(fd, "wb") as stream, src.open("rb") as inp:
                shutil.copyfileobj(inp, stream)
                os.fchmod(stream.fileno(), stat.S_IMODE(src.stat().st_mode))
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, target)
        finally:
            Path(name).unlink(missing_ok=True)
    sync_directory(target.parent)


def finish(folder):
    # Rename is the commit point. Interrupted cleanup is outside the live journal.
    with tempfile.TemporaryDirectory(dir=folder.parent, prefix=".complete-") as tmp:
        os.rename(folder, Path(tmp) / "transaction")
        sync_directory(folder.parent)


def recover(dest, backups, safe_target):
    folder = backups / ".transaction"
    if not folder.exists() and not folder.is_symlink():
        return
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("Invalid transaction directory")
    manifest = folder / "journal.json"
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError("Invalid controller transaction journal")
    data = json.loads(manifest.read_text())
    if data.get("schema") != 1 or data.get("target") != str(dest.resolve()):
        raise ValueError("Transaction belongs to another controller")
    restore = []
    for rel, row in data["files"].items():
        target = safe_target(dest, rel)
        saved = safe_target(folder / "original", rel) if row["before"] is not None else None
        before = state(saved)
        current = state(target)
        if before != row["before"] or current not in (before, row["after"]):
            raise ValueError(f"Interrupted transaction requires manual inspection: {rel}")
        if current != before:
            restore.append((target, saved))
    for target, saved in reversed(restore):
        replace(target, saved)
    finish(folder)


def apply(dest, backups, pending, originals, safe_target, validate=None):
    folder = backups / ".transaction"
    if folder.exists() or folder.is_symlink():
        raise ValueError("An interrupted controller transaction requires recovery")
    with tempfile.TemporaryDirectory(dir=backups, prefix=".journal-") as work:
        preparing = Path(work) / "transaction"
        saved = preparing / "original"
        saved.mkdir(parents=True, mode=0o700)
        entries = {}
        for rel, source in pending.items():
            target = safe_target(dest, rel)
            original = originals.get(rel)
            before = state(original)
            if state(target) != before:
                raise ValueError(f"File changed during preparation: {rel}")
            if original is not None:
                copy = saved / rel
                copy.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, copy)
            entries[rel] = {"before": before, "after": state(source)}
        (preparing / "journal.json").write_text(json.dumps(
            {"schema": 1, "target": str(dest.resolve()), "files": entries}))
        sync_files(preparing)
        os.rename(preparing, folder)
        sync_directory(backups)
    try:
        for rel, source in pending.items():
            target = safe_target(dest, rel)
            if state(target) != entries[rel]["before"]:
                raise ValueError(f"File changed during transaction: {rel}")
            replace(target, source)
        if validate:
            validate()
    except BaseException:
        recover(dest, backups, safe_target)
        raise
    finish(folder)
