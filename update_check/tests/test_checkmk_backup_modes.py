"""Run the migration playbook with local inventory, a fake OMD and offline Checkmk actions."""
import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
PLAYBOOK = ROOT / "playbooks/checkmk/migrate_hosts.yml"
CANARY = "fixture-private-backup-content"

# The host interpreter stamps its identity on the environment before Ansible starts
# a module. The trace therefore records where the original backup commands ran.
COMMAND = """#!/usr/bin/env python3
import io, json, os, sys, tarfile
from pathlib import Path
tool = Path(sys.argv[0]).name
args = sys.argv[1:]
if tool in ("omd", "docker") or any(arg.startswith(os.environ["FIXTURE_ARCHIVE_DIR"]) for arg in args):
    with open(os.environ["FIXTURE_TRACE"], "a") as f:
        print(json.dumps([tool, os.getenv("FIXTURE_HOST"), args]), file=f)
if tool not in ("docker", "omd"):
    os.execv(os.environ["FIXTURE_REAL_" + tool], [tool, *args])
if tool == "docker":
    if args[:2] != ["exec", "fixture-container"]:
        sys.exit(61)
    os.execvp(args[2], args[2:])
if tool != "omd" or args[:2] != ["backup", "fixture"] or len(args) != 3:
    sys.exit(62)
destination = Path(args[2])
print("fixture-private-backup-content", file=sys.stderr)
if os.getenv("FIXTURE_FAILURE"):
    destination.write_bytes(b"invalid tarball")
    sys.exit(1 if os.environ["FIXTURE_FAILURE"] == "omd" else 0)
with tarfile.open(destination, "w:gz") as archive:
    entry = tarfile.TarInfo("fixture-private-backup-content")
    archive.addfile(entry, io.BytesIO())
"""

# No network, Python Checkmk client or installed Checkmk collection is needed.
ACTION = """import json, os
from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        with open(os.environ["FIXTURE_TRACE"], "a") as f:
            print(json.dumps(["api", task_vars["inventory_hostname"], self._task.action]), file=f)
        return {"changed": False}
"""


@unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook required")
class CheckmkBackupModes(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.trace = self.root / "trace.jsonl"
        self.archive_dir = self.root / "backups with spaces"
        self.system_commands = ("mkdir", "mktemp", "chmod", "tar", "mv", "rm", "rmdir")
        for tool in ("docker", "omd", *self.system_commands):
            script = self.bin / tool
            script.write_text(COMMAND)
            script.chmod(0o700)

        self.inventory = self.root / "inventory"
        self.inventory.mkdir()
        hosts = {}
        for alias in ("localhost", "backup", "bystander"):
            interpreter = self.bin / (alias + "-python")
            interpreter.write_text("#!/bin/sh\nexport FIXTURE_HOST=" + alias +
                                   "\nexec " + shlex.quote(sys.executable) + ' "$@"\n')
            interpreter.chmod(0o700)
            hosts[alias] = {"ansible_connection": "local", "ansible_become": False,
                            "ansible_python_interpreter": str(interpreter)}
        (self.inventory / "hosts.yml").write_text(json.dumps({"all": {"hosts": hosts}}))
        variables = self.inventory / "group_vars" / "all"
        variables.mkdir(parents=True)
        self.settings_file = variables / "settings.yml"
        self.settings = {
            "checkmk_backup_target_host": "backup",
            "checkmk_backup_dir": str(self.archive_dir),
            "checkmk_server_url": "http://127.0.0.1:1",
            "checkmk_site": "fixture", "checkmk_api_user": "fixture", "checkmk_api_password": CANARY,
            "checkmk_folders": [{"name": "fixture", "path": "/fixture"}],
        }
        self.plan = {"checkmk_site": "fixture", "mappings": [],
                     "targets": [{"folder": "/fixture", "checkmk_hostname": "target",
                                  "ipaddress": "192.0.2.1", "alias": "target"}]}
        self.set_plan("x/reports/checkmk_migration_plan.yml")
        actions = self.root / "collections/ansible_collections/checkmk/general/plugins/action"
        actions.mkdir(parents=True)
        for name in ("folder", "activation", "host"):
            (actions / (name + ".py")).write_text(ACTION)
        config = self.root / "ansible.cfg"
        config.write_text("[defaults]\nretry_files_enabled = False\n")
        self.env = dict(os.environ, ANSIBLE_CONFIG=str(config), ANSIBLE_PROJECT_ROOT=str(self.root),
                        ANSIBLE_COLLECTIONS_PATH=str(self.root / "collections"),
                        ANSIBLE_HOME=str(self.root / "home"), ANSIBLE_REMOTE_TEMP=str(self.root / "remote"),
                        FIXTURE_TRACE=str(self.trace), FIXTURE_ARCHIVE_DIR=str(self.archive_dir),
                        PATH=str(self.bin) + os.pathsep + os.environ["PATH"])
        for tool in self.system_commands:
            self.env["FIXTURE_REAL_" + tool] = shutil.which(tool, path=os.defpath)
        for key in ("FIXTURE_FAILURE", "ANSIBLE_REPORTS_DIR"):
            self.env.pop(key, None)

    def set_plan(self, name):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.plan))
        return path

    def run_play(self, *options, success=True):
        self.settings_file.write_text(json.dumps(self.settings))
        self.trace.write_text("")
        result = subprocess.run(["ansible-playbook", "-vv", "-i", str(self.inventory / "hosts.yml"),
                                 str(PLAYBOOK), *options], cwd=self.root, env=self.env,
                                capture_output=True, text=True, timeout=100)
        output = result.stdout + result.stderr
        self.assertNotIn(CANARY, output)
        if success:
            self.assertEqual(result.returncode, 0, output)
        else:
            self.assertNotEqual(result.returncode, 0, output)
        return [json.loads(line) for line in self.trace.read_text().splitlines()]

    def check_archive(self, trace):
        omd = [call for call in trace if call[0] == "omd"]
        self.assertEqual(len(omd), 1)
        _, host, argv = omd[0]
        self.assertEqual((host, argv[:2]), ("backup", ["backup", "fixture"]))
        temporary = Path(argv[2])
        self.assertEqual(temporary.parent.parent, self.archive_dir)
        self.assertFalse(temporary.parent.exists())
        archives = list(self.archive_dir.iterdir())
        self.assertEqual(len(archives), 1)
        archive = archives[0]
        self.assertRegex(archive.name, r"^fixture-pre-host-migration-.*\.tar\.gz$")
        self.assertEqual(stat.S_IMODE(archive.stat().st_mode), 0o600)
        with tarfile.open(archive, "r:gz") as verified:
            self.assertEqual(verified.getnames(), [CANARY])
        actions = [(host, name) for kind, host, name in trace if kind == "api"]
        self.assertEqual(actions, [("localhost", "checkmk.general." + name)
                                   for name in ("folder", "activation", "host", "activation")])
        return temporary, archive

    def test_default_docker_backup_and_api_on_separate_hosts(self):
        self.settings["checkmk_container_name"] = "fixture-container"
        trace = self.run_play("--limit", "backup,localhost")
        temp, final = self.check_archive(trace)
        docker = [argv for tool, host, argv in trace if tool == "docker" and host == "backup"]
        self.assertTrue(all(argv[:2] == ["exec", "fixture-container"] for argv in docker))
        self.assertEqual([argv[2] for argv in docker],
                         ["mkdir", "mktemp", "omd", "chmod", "tar", "mv", "rm", "rmdir"])
        self.assertIn(["exec", "fixture-container", "omd", "backup", "fixture", str(temp)], docker)
        self.assertIn(["exec", "fixture-container", "tar", "-tzf", str(temp)], docker)
        self.assertIn(["exec", "fixture-container", "mv", "--", str(temp), str(final)], docker)

    def test_native_backup_without_docker_or_container_and_relative_plan_override(self):
        self.settings.update(checkmk_backup_mode="native", checkmk_migration_plan="operator/plan.yml",
                             controller_reports_dir="ignored")
        self.env["ANSIBLE_REPORTS_DIR"] = "also-ignored"
        (self.root / "x/reports/checkmk_migration_plan.yml").unlink()
        self.set_plan("operator/plan.yml")
        limit = self.root / "limit"
        limit.write_text("backup\nlocalhost\n")
        trace = self.run_play("--limit", "@" + str(limit))
        temp, final = self.check_archive(trace)
        self.assertIn(["tar", "backup", ["-tzf", str(temp)]], trace)
        self.assertIn(["mv", "backup", ["--", str(temp), str(final)]], trace)
        self.assertNotIn("docker", [kind for kind, _, _ in trace])

    def test_check_mode_validates_settings_and_environment_report_directories(self):
        self.settings.update(checkmk_backup_mode="native", controller_reports_dir="configured")
        self.env["ANSIBLE_REPORTS_DIR"] = "from-env"
        (self.root / "x/reports/checkmk_migration_plan.yml").unlink()
        self.set_plan("configured/checkmk_migration_plan.yml")
        self.assertEqual(self.run_play("--check"), [])
        del self.settings["controller_reports_dir"]
        self.set_plan("from-env/checkmk_migration_plan.yml")
        self.assertEqual(self.run_play("--check"), [])
        self.assertFalse(self.archive_dir.exists())

    def test_failed_omd_or_invalid_archive_blocks_migration_and_removes_partial_files(self):
        self.settings["checkmk_backup_mode"] = "native"
        for stage in ("omd", "tar"):
            with self.subTest(stage=stage):
                self.env["FIXTURE_FAILURE"] = stage
                trace = self.run_play(success=False)
                tools = [kind for kind, _, _ in trace]
                self.assertIn("omd", tools)
                self.assertNotIn("mv", tools)
                self.assertNotIn("api", tools)
                self.assertEqual(list(self.archive_dir.iterdir()), [])

    def test_invalid_mode_host_and_limit_do_not_start_backup_or_api(self):
        self.settings["checkmk_backup_mode"] = "unknown"
        self.assertEqual(self.run_play(success=False), [])
        self.settings["checkmk_backup_mode"] = "native"
        self.assertEqual(self.run_play("--limit", "localhost,bystander", success=False), [])
        self.assertEqual(self.run_play("--limit", "backup", success=False), [])
        self.settings["checkmk_backup_target_host"] = "all"
        self.assertEqual(self.run_play(success=False), [])
        self.assertFalse(self.archive_dir.exists())
