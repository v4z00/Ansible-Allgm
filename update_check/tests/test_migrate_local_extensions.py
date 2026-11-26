"""Schema migration uses only synthetic, pinned local-extension directories."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "tools"))
import migrate_local_extensions as migration


def snapshot(root):
    result = {}
    for path in root.rglob("*"):
        info = path.lstat()
        data = os.readlink(path) if path.is_symlink() else path.read_bytes() if path.is_file() else None
        result[path.relative_to(root)] = (info.st_ino, info.st_mtime_ns, info.st_mode, data)
    return result


class MigrationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.site = Path(tmp.name).resolve()
        self.controller = self.site / "controller"
        self.local = self.site / "controller-local"
        self.pin = self.controller / ".local/local-extension-id"
        self.pin.parent.mkdir(mode=0o700, parents=True)
        self.identifier = "a" * 32
        self.pin.write_text(self.identifier + "\n")
        self.local.mkdir(mode=0o700)
        self.code = self.local / "code/scripts/job.sh"
        self.code.parent.mkdir(parents=True)
        self.code.write_text("#!/bin/sh\n# manuell-integriert: ja\n# bereinigung: behalten\nexit 0\n")
        digest = hashlib.sha256(self.code.read_bytes()).hexdigest()
        self.entry = {"sha256": digest, "cleanup": "behalten", "custom": "preserve this"}
        self.record = self.local / "register.json"
        self.document = {"id": self.identifier, "files": {"scripts/job.sh": self.entry},
                         "schema": 1, "vendor": {"site_count": 3}}
        self.original = (" \n" + json.dumps(self.document, indent=4) + "\n\n").encode()
        self.record.write_bytes(self.original)
        self.record.chmod(0o600)
        self.lock = self.site / ".controller.controller-lock"

    def cli(self, *args, success=True):
        env = dict(os.environ, CONTROLLER_LANG="en", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, "-B", BASE / "tools/migrate_local_extensions.py",
                                 "--controller", self.controller, *args], env=env,
                                capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=10)
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result.stdout if success else result.stderr

    def backups(self):
        return list(self.local.glob("register.json.schema1.*.bak"))

    def test_preview_creates_no_files_or_locks_and_does_not_expose_entry_data(self):
        before = snapshot(self.site)
        for flags in ([], ["--check"], ["--lang", "de", "--check"]):
            output = self.cli(*flags)
            self.assertIn("1", output)
            self.assertNotIn("job.sh", output)
            self.assertNotIn(self.identifier, output)
            self.assertNotIn(self.entry["sha256"], output)
        self.assertEqual(before, snapshot(self.site))

    def test_private_backup_idempotent_migration_and_byte_exact_restore(self):
        output = self.cli("--apply")
        backup, = self.backups()
        self.assertIn(str(backup), output)
        self.assertEqual(backup.read_bytes(), self.original)
        self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(self.record.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(self.lock.stat().st_mode), 0o600)
        self.assertEqual(json.loads(self.record.read_bytes()),
                         {**self.document, "schema": 2, "files": {"scripts/job.sh": {**self.entry, "cleanup": "keep"}}})
        after = snapshot(self.site)
        self.cli("--apply")
        self.cli("--check")
        self.assertEqual(snapshot(self.site), after)
        self.cli("--rollback", backup.name)
        self.assertEqual(self.record.read_bytes(), self.original)
        restored = snapshot(self.site)
        self.cli("--rollback", str(backup))
        self.assertEqual(snapshot(self.site), restored)
        self.assertEqual(after[Path("controller-local/code/scripts/job.sh")], restored[Path("controller-local/code/scripts/job.sh")])

    def test_rollback_refuses_changed_register_or_tampered_backup(self):
        self.cli("--apply")
        backup, = self.backups()
        migrated = self.record.read_bytes()
        self.record.write_bytes(migrated + b"\n")
        self.assertIn("changed after migration", self.cli("--rollback", backup.name, success=False))
        self.assertEqual(self.record.read_bytes(), migrated + b"\n")
        self.record.write_bytes(migrated)
        backup.write_bytes(self.original + b"\n")
        self.assertIn("SHA-256", self.cli("--rollback", backup.name, success=False))
        self.assertEqual(self.record.read_bytes(), migrated)

    def test_both_actions_honor_existing_controller_writer(self):
        self.lock.touch(mode=0o600)
        before = snapshot(self.site)
        with self.lock.open("r+") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            for flag in ("--check", "--apply"):
                self.assertIn("lock", self.cli(flag, success=False))
        self.assertEqual(snapshot(self.site), before)

    def test_rejects_linked_nonprivate_or_external_backup(self):
        self.cli("--apply")
        backup, = self.backups()
        other = self.site / backup.name
        for wrong in (str(other), "../controller-local/" + backup.name):
            self.cli("--rollback", wrong, success=False)
        backup.chmod(0o644)
        self.cli("--rollback", backup.name, success=False)
        backup.chmod(0o600)
        backup.rename(other)
        backup.symlink_to(other)
        self.cli("--rollback", backup.name, success=False)
        backup.unlink()
        os.link(other, backup)
        self.cli("--rollback", backup.name, success=False)
        self.assertEqual(json.loads(self.record.read_bytes())["schema"], 2)
        self.assertEqual(other.read_bytes(), self.original)

    def test_symlink_pin_lock_and_register_are_rejected_without_following_them(self):
        for path in (self.lock, self.pin, self.record):
            with self.subTest(path=path.name):
                previous = path.read_bytes() if path.exists() else None
                other = self.site / "private-sentinel"
                other.write_bytes(previous or b"must not be accessed")
                path.unlink(missing_ok=True)
                path.symlink_to(other)
                self.cli("--check", success=False)
                self.cli("--apply", success=False)
                self.assertTrue(path.is_symlink())
                self.assertEqual(other.read_bytes(), previous or b"must not be accessed")
                path.unlink()
                other.unlink()
                if previous is not None:
                    path.write_bytes(previous)
        self.assertFalse(self.backups())

    def test_preview_refuses_links_in_controller_and_local_ancestry(self):
        alias = self.site / "alias"
        alias.symlink_to(self.site, target_is_directory=True)
        self.cli("--controller", str(alias / self.controller.name), "--check", success=False)
        self.assertFalse(self.lock.exists())
        for original in (self.controller, self.local, self.pin.parent):
            moved = original.with_name(original.name + "-saved")
            original.rename(moved)
            original.symlink_to(moved, target_is_directory=True)
            try:
                self.cli("--check", success=False)
                self.assertFalse(self.lock.exists())
                self.assertFalse(list(moved.glob("*.bak")))
            finally:
                original.unlink()
                moved.rename(original)

    def test_wrong_site_duplicate_keys_invalid_hash_and_dirty_code_are_rejected(self):
        self.pin.write_text("b" * 32)
        self.cli("--apply", success=False)
        self.pin.write_text(self.identifier)
        for raw in (self.original.replace(b'"schema": 1', b'"schema": 1, "schema": 1'),
                    self.original.replace(self.entry["sha256"].encode(), b"invalid"),
                    self.original.replace(b'"behalten"', b'"keep"')):
            with self.subTest(raw_size=len(raw)):
                self.record.write_bytes(raw)
                self.cli("--apply", success=False)
                self.assertEqual(self.record.read_bytes(), raw)
        self.record.write_bytes(self.original)
        self.code.write_text("site-specific private contents")
        error = self.cli("--apply", success=False)
        self.assertNotIn("site-specific", error)
        self.assertNotIn("job.sh", error)
        self.assertEqual(self.record.read_bytes(), self.original)
        self.assertFalse(self.backups())

    def test_backup_is_durable_before_failed_replace_and_retry(self):
        with patch.object(migration.os, "replace", side_effect=OSError("injected write failure")):
            with self.assertRaises(OSError):
                migration.run(self.controller, apply=True)
        backup, = self.backups()
        self.assertEqual(self.record.read_bytes(), self.original)
        self.assertEqual(backup.read_bytes(), self.original)
        self.assertFalse(list(self.local.glob(".register-migration-*")))
        self.cli("--apply")
        self.assertEqual(json.loads(self.record.read_bytes())["schema"], 2)

    def test_uncooperative_edit_after_backup_is_not_overwritten(self):
        save = migration.new_file

        def change_live(folder, name, data):
            save(folder, name, data)
            if migration.BACKUP.fullmatch(name):
                self.record.write_bytes(self.original + b"\n")

        with patch.object(migration, "new_file", side_effect=change_live), self.assertRaises(ValueError):
            migration.run(self.controller, apply=True)
        self.assertEqual(self.record.read_bytes(), self.original + b"\n")
        self.assertFalse(list(self.local.glob(".register-migration-*")))
