import copy
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "tools"))
import local_extensions as ext
import local_extension as cli
import rollout


class LocalExtensionsTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.controller = Path(temporary.name) / "ansible"
        (self.controller / "bin").mkdir(parents=True)
        (self.controller / "bin/control").touch()
        (self.controller / "ansible.cfg").touch()
        self.bundle = self.controller.parent / "example"
        self.name = "scripts/task.sh"
        self.source = self.bundle / "code" / self.name
        self.source.parent.mkdir(parents=True)
        self.source.write_text("#!/bin/bash\n# manuell-integriert: ja\n# bereinigung: nach-erfolg-archivieren\nexit 0\n")
        self.root = ext.location(self.controller)
        self.approve()
        self.addCleanup(patch.stopall)
        patch.object(cli.cleanup, "scan_sources", return_value=([], [])).start()

    def approve(self):
        cli.approve(self.bundle, self.name, ext.sha(self.source))

    def register(self):
        return ext.read_json(self.root / "register.json")

    def install(self):
        cli.install(self.controller, self.bundle)

    def test_legacy_cron_drift_and_missing_directory(self):
        self.assertEqual(ext.inspect(self.controller)["status"], "NICHT_EINGERICHTET")
        self.install()
        target = self.root / "code" / self.name
        target.write_text("changed")
        self.assertEqual(ext.inspect(self.controller)["files"][0]["status"], "SHA_ABWEICHUNG")
        with patch.object(rollout, "rollout", side_effect=AssertionError("unexpected network or rollout")):
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(rollout.main(["--auto", "--json", "--root", str(self.controller)]), 1)
            self.assertFalse(json.loads(out.getvalue())["applied"])
        with self.assertRaises(ValueError):
            self.install()
        self.root.rename(self.root.with_suffix(".missing"))
        self.assertFalse(ext.passed(ext.inspect(self.controller)))

    def test_archive_requires_run_and_no_caller_and_preserves_both_hashes(self):
        self.install()
        sha = ext.sha(self.source)
        with self.assertRaises(FileNotFoundError):
            cli.archive(self.controller, self.root, self.register(), self.name, sha)
        cli.run(self.controller, self.root, self.register()["files"], self.name, None)
        with patch.object(cli.cleanup, "scan_sources", return_value=([("timer", "task.sh")], [])):
            with self.assertRaises(ValueError):
                cli.archive(self.controller, self.root, self.register(), self.name, sha)
        cli.archive(self.controller, self.root, self.register(), self.name, None)
        self.assertTrue((self.root / "code" / self.name).is_file())
        with self.assertRaises(ValueError):
            cli.archive(self.controller, self.root, self.register(), self.name, "0" * 64)
        cli.archive(self.controller, self.root, self.register(), self.name, sha)
        self.install()
        entry = self.register()["files"][self.name]
        saved = self.root / "archiv" / entry["archive"]
        proof = ext.archive_proof(self.root, self.name, entry)
        self.assertEqual((saved / "datei").read_bytes(), self.source.read_bytes())
        self.assertEqual((saved / "SHA256SUMS").read_text(), sha + "  datei\n")
        self.assertEqual([proof["archived_sha256"], proof["approved_sha256"]], [sha, sha])
        # Recover interruption after the archive and register committed, before removal of the live copy.
        (self.root / "code" / self.name).write_bytes(self.source.read_bytes())
        self.assertFalse(ext.passed(ext.inspect(self.controller)))
        cli.archive(self.controller, self.root, self.register(), self.name, sha)
        self.assertTrue(ext.passed(ext.inspect(self.controller)))
        (saved / "datei").write_text("changed")
        self.assertFalse(ext.passed(ext.inspect(self.controller)))

    def test_unknown_link_failed_run_and_new_revision(self):
        self.install()
        extra = self.root / "code/unapproved"
        extra.touch()
        self.assertFalse(ext.passed(ext.inspect(self.controller)))
        extra.unlink()
        extra.symlink_to(self.source)
        self.assertFalse(ext.passed(ext.inspect(self.controller)))
        extra.unlink()
        self.source.write_text(self.source.read_text().replace("exit 0", "exit 7"))
        self.approve()
        self.install()
        with self.assertRaises(subprocess.CalledProcessError):
            cli.run(self.controller, self.root, self.register()["files"], self.name, None)
        self.assertFalse((self.root / "runs" / (self.name + ".json")).exists())

    def test_wrong_bundle_traversal_and_keep(self):
        self.install()
        with self.assertRaises(ValueError):
            ext.path_in(self.root, "../register.json")
        data = ext.read_json(self.bundle/"register.json")
        wrong = copy.deepcopy(data)
        wrong["id"] = "0"*32
        cli.record(self.bundle/"register.json",wrong)
        with self.assertRaises(ValueError):
            self.install()
        cli.record(self.bundle/"register.json",data)
        self.source.write_text(self.source.read_text().replace(ext.ONCE, ext.KEEP))
        self.approve()
        self.install()
        with self.assertRaises(ValueError):
            cli.archive(self.controller,self.root,self.register(),self.name,ext.sha(self.source))
