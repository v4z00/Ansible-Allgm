"""Guard the destination of a restore against registered local files and whole roles."""
from unittest import mock
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import install_controller as install
import local_extensions as ext


BACKUP_ID = "20260101T000000000000Z-aaaaaaaaaaaa"


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    path.chmod(0o600)
    return path


def encode(value):
    return json.dumps(value, sort_keys=True).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


class LocalRestorePathsTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve() / "controller"
        self.identifier = "e" * 32
        put(self.root / ".local/local-extension-id", self.identifier.encode())
        self.descriptor = put(self.root / "controller-base.json", encode({"schema": 1, "local_extension_schema": 2}))
        self.receipt = {"schema": 1, "profile": "allgm", "files": {"controller-base.json": install.sha(self.descriptor)}}
        put(self.root / install.RECEIPT, encode(self.receipt))
        self.local = ext.location(self.root)
        self.backups = install.backup_home(self.root, create=True)
        self.journal = self.backups / ".transaction"

    def approve(self, rel, schema=2):
        code = put(self.local / "code" / rel, b"#!/bin/sh\n# manually-integrated: yes\n# cleanup: keep\nexit 0\n")
        entry = {"sha256": install.sha(code), "cleanup": "keep" if schema == 2 else "behalten"}
        put(self.local / "register.json", encode({"schema": schema, "id": self.identifier, "files": {rel: entry}}))
        return code

    def write_journal(self, changes):
        entries = {}
        for name, (before, after) in changes.items():
            target = self.root / name
            if after is not None:
                put(target, after)
            else:
                target.unlink(missing_ok=True)
            if before is not None:
                put(self.journal / "original" / name, before)
            entries[name] = {"before": [digest(before), 0o600] if before is not None else None,
                             "after": [digest(after), 0o600] if after is not None else None}
        put(self.journal / "journal.json", encode({"schema": 1, "target": str(self.root), "files": entries}))

    def make_backup(self, restored):
        backup = self.backups / BACKUP_ID
        old = b"# old managed task\n"
        put(backup / restored, old)
        old_receipt = {**self.receipt, "files": {**self.receipt["files"], restored: digest(old)}}
        put(backup / install.RECEIPT, encode(old_receipt))
        plan = {"schema": 1, "target": str(self.root), "installed_receipt": install.receipt_hash(self.root),
                "previous_receipt": digest(encode(old_receipt)), "files": {restored: {
                    "before": digest(old), "before_mode": 0o600, "after": None, "after_mode": None}}}
        put(backup / "plan.json", encode(plan))
        return old

    def test_rollback_blocks_reintroduced_managed_role(self):
        local = self.approve("playbooks/roles/site_only/tasks/local.yml")
        restored = "roles/SITE_ONLY/handlers/main.yml"
        self.make_backup(restored)
        before = (local.read_bytes(), (self.root / install.RECEIPT).read_bytes())
        with self.assertRaises(ValueError):
            install.rollback_controller(self.root, BACKUP_ID)
        self.assertFalse((self.root / restored).exists())
        self.assertEqual((local.read_bytes(), (self.root / install.RECEIPT).read_bytes()), before)

    def test_rollback_of_unrelated_file_still_works(self):
        self.approve("playbooks/site/local.yml")
        restored = "playbooks/base/main.yml"
        old = self.make_backup(restored)
        install.rollback_controller(self.root, BACKUP_ID)
        self.assertEqual((self.root / restored).read_bytes(), old)

    def test_recovery_will_not_reintroduce_approved_local_file(self):
        name = "playbooks/site/one.yml"
        local = self.approve(name)
        self.write_journal({name: (b"old managed file", None),
                            "scripts/other.sh": (b"before", b"after")})
        self.assertEqual(ext.inspect(self.root)["status"], "OK")
        with self.assertRaises(ValueError):
            install.recover_transaction(self.root)
        self.assertTrue((self.journal / "journal.json").exists())
        self.assertFalse((self.root / name).exists())
        self.assertEqual((self.root / "scripts/other.sh").read_bytes(), b"after")
        self.assertTrue(local.exists())

    def test_recovery_can_remove_only_the_transient_collision(self):
        name = "playbooks/site/one.yml"
        self.approve(name)
        prior_receipt = encode(self.receipt)
        new_receipt = encode({**self.receipt, "files": {}})
        self.write_journal({name: (None, b"half-installed code"),
                            install.RECEIPT: (prior_receipt, new_receipt)})
        self.assertEqual(ext.inspect(self.root)["files"][0]["status"], "BASIS_KONFLIKT")
        report = install.inspect_before_change(self.root, write=True)
        self.assertEqual(report["status"], "OK")
        self.assertFalse(self.journal.exists())
        self.assertFalse((self.root / name).exists())
        self.assertEqual((self.root / install.RECEIPT).read_bytes(), prior_receipt)

    def test_damaged_prior_receipt_blocks_recovery_before_any_file_exchange(self):
        self.approve("playbooks/site/one.yml")
        self.write_journal({install.RECEIPT: (encode(self.receipt), encode({**self.receipt, "files": {}})),
                            "scripts/other.sh": (b"before", b"after")})
        put(self.journal / "original" / install.RECEIPT, b"damaged receipt")
        with self.assertRaises(ValueError):
            install.recover_transaction(self.root)
        self.assertEqual((self.root / "scripts/other.sh").read_bytes(), b"after")
        self.assertTrue(self.journal.is_dir())

    def test_unrelated_conflict_and_local_sha_mismatch_remain_blocking(self):
        name = "playbooks/site/one.yml"
        local = self.approve(name)
        put(self.root / name, b"unrelated existing overlap")
        self.write_journal({"scripts/other.sh": (None, b"half-installed")})
        with self.assertRaises(ValueError):
            install.inspect_before_change(self.root, write=True)
        self.write_journal({name: (None, b"half-installed code")})
        local.write_bytes(b"unapproved change")
        with self.assertRaises(ValueError):
            install.inspect_before_change(self.root, write=True)
        self.assertTrue(self.journal.is_dir())
        self.assertEqual(local.read_bytes(), b"unapproved change")
        self.assertEqual((self.root / name).read_bytes(), b"half-installed code")

    def test_legacy_register_does_not_exempt_path_conflicts_on_explicit_restore(self):
        name = "playbooks/site/one.yml"
        self.approve(name, schema=1)
        put(self.descriptor, encode({"schema": 1}))
        self.receipt["files"]["controller-base.json"] = install.sha(self.descriptor)
        put(self.root / install.RECEIPT, encode(self.receipt))
        self.write_journal({name: (b"old managed file", None)})
        self.assertEqual(ext.inspect(self.root)["status"], "MIGRATION_REQUIRED")
        with self.assertRaises(ValueError):
            install.inspect_before_change(self.root, write=True, rollback=True)
        self.assertFalse((self.root / name).exists())
        self.assertTrue(self.journal.is_dir())

    def test_recovery_restores_catalog_already_removed_by_an_interrupted_exchange(self):
        import controller_i18n as messages
        import shutil

        self.approve("playbooks/site/one.yml")
        catalogs = self.root / "lib/i18n"
        shutil.copytree(ROOT / "lib/i18n", catalogs)
        rel = "lib/i18n/status_codes.json"
        original = (self.root / rel).read_bytes()
        self.write_journal({rel: (original, None)})
        with mock.patch.object(messages, "CATALOGS", catalogs):
            messages.status_codes.cache_clear()
            try:
                install.recover_transaction(self.root)
                self.assertEqual((self.root / rel).read_bytes(), original)
                self.assertTrue(messages.status_codes())
                self.assertFalse(self.journal.exists())
            finally:
                messages.status_codes.cache_clear()
