"""Exercise the normal Docker update launcher without a Docker daemon."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
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
        helper = root / "lib/control/helpers.sh"
        helper.parent.mkdir(parents=True)
        shutil.copyfile(source.parents[1]/"lib/control/helpers.sh",helper)
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


@unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook erforderlich")
class DockerStopTest(unittest.TestCase):
    def test_first_compose_file_and_working_directory(self):
        play = Path(__file__).resolve().parents[2] / "playbooks/docker/stop_all_docker.yaml"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            compose = root / "Team's $HOME" / "compose file.yaml"
            compose.parent.mkdir()
            compose.touch()
            projects = [{"Name": "example", "ConfigFiles": f"{compose},{root}/override.yaml"}]
            (root / "projects.json").write_text(json.dumps(projects))
            docker = root / "docker"
            docker.write_text(
                "#!/bin/sh\n"
                'if [ "$*" = "compose ls --format json" ]; then cat "$FIXTURE/projects.json"; exit; fi\n'
                'printf "%s\\n" "$PWD" "$@" >> "$FIXTURE/calls"\n'
            )
            docker.chmod(0o755)
            inventory = root / "hosts"
            inventory.write_text("[docker_deployment_hosts]\nfixture ansible_connection=local "
                                 f"ansible_become=false ansible_python_interpreter='{sys.executable}'\n")
            config = root / "ansible.cfg"
            config.write_text("[defaults]\n")
            env = dict(os.environ, PATH=str(root) + os.pathsep + os.environ["PATH"], FIXTURE=str(root),
                       ANSIBLE_CONFIG=str(config), ANSIBLE_LOCAL_TEMP=str(root / "local"),
                       ANSIBLE_REMOTE_TEMP=str(root / "remote"))
            result = subprocess.run(["ansible-playbook", "-i", str(inventory), str(play)], cwd=root,
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((root / "calls").read_text().splitlines(),
                             [str(compose.parent), "compose", "-f", str(compose), "stop"])
