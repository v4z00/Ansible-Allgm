"""Regression tests for the handoff from the piped script to the local installer."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import pipe_install


class PipeInstallTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.target = root / "controller"
        self.base = root / "source/Allgm"
        self.base.mkdir(parents=True)
        for attr, val in (("TARGET", self.target), ("BASE", self.base)):
            replacement = patch.object(pipe_install, attr, val)
            replacement.start()
            self.addCleanup(replacement.stop)

    def test_overlay_checked_before_base_install(self):
        calls = []
        def verify(repo, profile):
            calls.append(("verify", profile))
        def clone(url, repo, token_file, controller):
            calls.append(("clone", repo.name))
        def run(argv, check):
            calls.append(("install", Path(argv[0]).parent.name))
        with patch.object(pipe_install, "verify_checkout", verify), \
                patch.object(pipe_install.github_https, "clone_main", clone), \
                patch.object(subprocess, "run", run):
            pipe_install.install("Homelab", "", None)
        self.assertEqual(calls, [("verify", "Allgm"), ("clone", "Ansible-Homelab"), ("verify", "Homelab"),
                                 ("install", "bin"), ("install", "Ansible-Homelab")])

    def test_invalid_overlay_never_starts_installer_or_persists_token(self):
        with patch.object(pipe_install, "verify_checkout", side_effect=[None, ValueError("SHA-256")]), \
                patch.object(pipe_install.github_https, "clone_main"), \
                patch.object(pipe_install, "save_token") as save, patch.object(subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                pipe_install.install("ExampleOverlay", "/fixture/input", "/fixture/output")
            save.assert_not_called()
            run.assert_not_called()
            self.assertFalse(self.target.exists())

    def test_existing_unmanaged_controller_is_preserved(self):
        self.target.mkdir()
        existing = self.target / "operator-file"
        existing.write_text("lokal\n")
        with patch.object(subprocess, "run") as run, self.assertRaisesRegex(ValueError, "--update"):
            pipe_install.install("Allgm", "", None)
        run.assert_not_called()
        self.assertEqual(existing.read_text(), "lokal\n")
