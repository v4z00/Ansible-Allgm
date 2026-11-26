"""Exercise language selection at the public command entry points."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class EntryPointTests(unittest.TestCase):
    def run_command(self, *args, lang="de", ok=True):
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home, CONTROLLER_LANG=lang, PYTHONDONTWRITEBYTECODE="1")
            env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env["PATH"]
            result = subprocess.run(args, cwd=ROOT, env=env, text=True, capture_output=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def test_dispatch_help_and_unknown_command(self):
        self.assertIn("Usage:", self.run_command("bin/control", "--lang", "en", "help").stdout)
        self.assertIn("Aufruf:", self.run_command("bin/control", "--lang=de", "help", lang="en").stdout)
        error = self.run_command("bin/control", "--lang=en", "missing-command", ok=False)
        self.assertIn("Unknown command: missing-command", error.stderr)

    def test_inventory_listing_keeps_machine_ids(self):
        de = self.run_command("bin/control", "--lang", "de", "list")
        en = self.run_command("bin/control", "--lang", "en", "list")
        self.assertEqual(de.stdout.splitlines(), en.stdout.splitlines())

    def test_bootstrap_and_job_console(self):
        help_text = self.run_command(sys.executable, "scripts/run_bootstrap.py", "--lang=en", "--help")
        self.assertIn("Usage: control bootstrap", help_text.stdout)
        with tempfile.TemporaryDirectory() as temp:
            args = [sys.executable, "scripts/job_console.py", "--project", temp,
                    "--db", str(Path(temp) / "local.db"), "runs"]
            self.assertIn("No matching results", self.run_command(*args, "--lang=en").stdout)
            self.assertEqual(json.loads(self.run_command(*args, "--lang=de", "--json").stdout), [])
