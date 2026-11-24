"""Exercise the normal Docker update launcher without a Docker daemon."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class DockerUpdateTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        scripts = root / "scripts"
        scripts.mkdir()
        self.runner = scripts / "run_docker_update.sh"
        source = Path(__file__).resolve().parents[2] / "scripts" / self.runner.name
        shutil.copyfile(source, self.runner)
        self.trace = root / "calls"
        driver = root / "ansible-playbook"
        driver.write_text("""#!/bin/sh
printf '%s\\n' "$*" >> "$TRACE"
case " $* " in
  *" --list-hosts "*) echo "  hosts ($HOST_COUNT):" ;;
  *"playbooks/docker/update_containers.yml"*) exit "$UPDATE_RC" ;;
  *"playbooks/maintenance/notify.yml"*) exit 0 ;;
  *) exit 42 ;;
esac
""")
        driver.chmod(0o700)
        self.env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"],
                        HOST_COUNT="1", UPDATE_RC="0", TRACE=str(self.trace))

    def invoke(self, *args):
        return subprocess.run(["bash", str(self.runner), *args], env=self.env, capture_output=True)

    def test_failed_playbook_does_not_report_success(self):
        self.env["UPDATE_RC"] = "7"
        self.assertEqual(self.invoke("--limit", "example").returncode, 7)
        calls = self.trace.read_text().splitlines()
        self.assertIn("--limit example", calls[1])
        self.assertIn("notify.yml", calls[-1])

    def test_empty_selection_and_tag_bypass(self):
        self.env["HOST_COUNT"] = "0"
        self.assertNotEqual(self.invoke("--limit", "missing").returncode, 0)
        self.assertEqual(len(self.trace.read_text().splitlines()), 1)
        self.assertNotEqual(self.invoke("--skip-tags=always").returncode, 0)
        self.assertEqual(len(self.trace.read_text().splitlines()), 1)

    def test_diagnostic_list_does_not_start_an_update_or_notify(self):
        self.assertEqual(self.invoke("--list-hosts").returncode, 0)
        self.assertEqual(self.trace.read_text().splitlines(), ["playbooks/docker/update_containers.yml --list-hosts"])
