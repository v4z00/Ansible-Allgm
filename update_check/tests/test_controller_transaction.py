"""Exercise interrupted multi-file writes using only temporary controllers."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "tools"))
import controller_transaction as transaction
import install_controller as install


class TransactionTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.controller = self.root / "controller"
        self.controller.mkdir()
        self.backups = install.backup_home(self.controller, create=True)
        self.assets = self.root / "assets"
        self.assets.mkdir()
        self.target = self.controller / "scripts" / "task.sh"
        self.target.parent.mkdir()
        self.target.write_text("old")
        self.target.chmod(0o700)
        self.proposed = self.assets / "replacement"
        self.proposed.write_text("new")
        self.proposed.chmod(0o600)
        self.marker = self.controller / "versions.txt"
        self.marker.write_text("original registration")
        self.marker.chmod(0o600)

    def apply(self, validate=None):
        transaction.apply(self.controller, self.backups,
                          {"scripts/task.sh": self.proposed, "versions.txt": self.proposed},
                          {"scripts/task.sh": self.target, "versions.txt": self.marker},
                          install.transaction_path, validate)

    def test_failed_validation_restores_original_files_and_modes(self):
        def reject():
            raise ValueError("validation failed")
        with self.assertRaisesRegex(ValueError, "validation failed"):
            self.apply(reject)
        self.assertEqual(self.target.read_text(), "old")
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o700)
        self.assertEqual(self.marker.read_text(), "original registration")
        self.assertFalse((self.backups / ".transaction").exists())

    def interrupt_writer(self):
        child = """
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import controller_transaction as tx
import install_controller as install
root, source = map(Path, sys.argv[2:])
original = tx.replace
def write_one(target, proposed):
    original(target, proposed)
    os._exit(77)
tx.replace = write_one
tx.apply(root, install.backup_home(root),
         {"scripts/task.sh": source, "versions.txt": source},
         {"scripts/task.sh": root / "scripts/task.sh", "versions.txt": root / "versions.txt"},
         install.transaction_path)
"""
        result = subprocess.run([sys.executable, "-B", "-c", child, str(BASE / "tools"),
                                 str(self.controller), str(self.proposed)], capture_output=True)
        self.assertEqual(result.returncode, 77, result.stderr)
        self.assertEqual(self.target.read_text(), "new")
        self.assertEqual(self.marker.read_text(), "original registration")

    def test_uncatchable_exit_is_recovered_by_next_writer(self):
        self.interrupt_writer()
        install.recover_transaction(self.controller)
        install.recover_transaction(self.controller)
        self.assertEqual(self.target.read_text(), "old")
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o700)
        self.assertFalse((self.backups / ".transaction").exists())

    def test_recovery_preserves_an_intervening_local_edit(self):
        self.interrupt_writer()
        self.target.write_text("operator edit")
        with self.assertRaisesRegex(ValueError, "manual inspection"):
            install.recover_transaction(self.controller)
        self.assertEqual(self.target.read_text(), "operator edit")
        self.assertTrue((self.backups / ".transaction/journal.json").is_file())
