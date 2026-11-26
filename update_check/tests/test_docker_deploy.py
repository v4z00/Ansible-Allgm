"""Docker deployment controls against isolated local hosts and a recording Docker CLI."""
import json
import os
from pathlib import Path
import pty
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

import yaml

BASE = Path(__file__).resolve().parents[2]
ANSIBLE = shutil.which("ansible-playbook")


@unittest.skipUnless(ANSIBLE, "ansible-playbook required")
class DockerDeploymentTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name).resolve()
        self.root = self.work / "site controller"
        self.plays = self.root / "playbooks/docker"
        (self.plays / "vars").mkdir(parents=True)
        shutil.copy2(BASE / "playbooks/docker/vars/paths.yml", self.plays / "vars/paths.yml")
        (self.root / "templates").mkdir()
        shutil.copy2(BASE / "templates/summary_templates.j2", self.root / "templates")
        (self.root / "ansible.cfg").write_text("[defaults]\n")
        self.inventory = self.work / "hosts.ini"
        self.inventory.write_text("[docker_deployment_hosts]\nsample ansible_connection=local\n"
                                  "[controllers]\nlocalhost ansible_connection=local\n")
        compose = self.work / "orphan compose.yml"
        compose.write_text("services: {}\n")
        self.trace = self.work / "docker-calls"
        shim = self.work / "bin"
        shim.mkdir()
        docker = shim / "docker"
        docker.write_text('#!/bin/sh\nprintf "%s\\n" "$@" >> "$DOCKER_TEST_TRACE"\n')
        docker.chmod(0o700)
        self.env = {k:v for k,v in os.environ.items()
                    if not k.startswith(("ANSIBLE_", "CONTROLLER_", "MJH_", "DOCKER_"))}
        self.env.update(HOME=str(self.work), PATH=str(shim) + os.pathsep + os.environ["PATH"],
                        ANSIBLE_CONFIG=str(self.root / "ansible.cfg"), ANSIBLE_NOCOLOR="1",
                        ANSIBLE_LOCAL_TEMP=str(self.work / "local-tmp"), ANSIBLE_REMOTE_TEMP=str(self.work / "remote-tmp"),
                        DOCKER_TEST_TRACE=str(self.trace))
        data = yaml.safe_load((BASE / "playbooks/docker/deploy_docker_stacks.yml").read_text())
        select_plays = [p for p in data if p["name"].startswith(("PLAY 2.5:", "PLAY 2.6:", "PLAY 9:"))]
        self.assertEqual(len(select_plays), 3)
        select_plays[-1]["gather_facts"] = False
        seed = {"hosts": "docker_deployment_hosts", "gather_facts": False, "tasks": [
            {"ansible.builtin.set_fact": {"prune_candidates": [{"Name": "retired", "ConfigFiles": str(compose)}]}}]}
        self.play = self.plays / "integration.yml"
        self.play.write_text(yaml.safe_dump([seed, *select_plays]))
        self.extra = {"ansible_become": False, "ansible_python_interpreter": sys.executable,
                      "ansible_date_time": {"iso8601_basic_short": "test"}, "ansible_host": "localhost",
                      "global_pruned_stacks": [], "global_deployment_results": [], "global_problem_containers": []}

    def command(self, extra=None):
        return [ANSIBLE, "-i", str(self.inventory), str(self.play), "-e", json.dumps({**self.extra, **(extra or {})})]

    def test_unattended_summary_keeps_report_and_never_removes_orphans(self):
        report_root = self.work / "chosen reports"
        args = {"docker_deploy_pause_summary": False, "controller_reports_dir": str(report_root),
                "global_prune_confirmed": True}
        env = {**self.env, "ANSIBLE_REPORTS_DIR": str(self.work / "other reports")}
        result = subprocess.run(self.command(args), input="yes\n", cwd=self.plays, env=env, text=True,
                                capture_output=True, timeout=35)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Deployment complete.", result.stdout)
        self.assertNotIn("Press Enter to continue.", result.stdout)
        self.assertFalse(self.trace.exists())
        self.assertTrue((report_root / "docker/deployment-test.log").is_file())
        self.assertFalse((self.work / "other reports").exists())

    def test_preset_answer_cannot_authorize_removal(self):
        args = {"docker_deploy_pause_summary": False, "global_prune_confirmed": True,
                "global_prune_confirmation": {"user_input": "yes"}}
        result = subprocess.run(self.command(args), input="", capture_output=True, text=True,
                                cwd=self.plays, env=self.env, timeout=25)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("A preset orphan confirmation is invalid", result.stdout + result.stderr)
        self.assertFalse(self.trace.exists())

    def test_interactive_default_requires_two_distinct_answers(self):
        pid, fd = pty.fork()
        if pid == 0:
            os.chdir(self.plays)
            os.execve(ANSIBLE, self.command(), self.env)
        output = bytearray()
        answers = [(b'Type exactly "yes"', b"yes\n"), (b"Press Enter to continue.", b"\n")]
        deadline = time.monotonic() + 35
        try:
            while time.monotonic() < deadline:
                if select.select([fd], [], [], .1)[0]:
                    try:
                        block = os.read(fd, 65536)
                    except OSError:
                        break
                    if not block:
                        break
                    output.extend(block)
                if answers and answers[0][0] in output:
                    time.sleep(.15)
                    os.write(fd, answers.pop(0)[1])
            self.assertFalse(answers, output.decode(errors="replace"))
            while True:
                finished, status = os.waitpid(pid, os.WNOHANG)
                if finished:
                    break
                self.assertLess(time.monotonic(), deadline, output.decode(errors="replace"))
                time.sleep(.05)
            self.assertEqual(os.waitstatus_to_exitcode(status), 0, output.decode(errors="replace"))
        finally:
            os.close(fd)
            try:
                os.kill(pid, signal.SIGTERM)
                os.waitpid(pid, 0)
            except (ChildProcessError, ProcessLookupError):
                pass
        self.assertIn("down", self.trace.read_text().splitlines())
        self.assertTrue((self.root / "x/reports/docker/deployment-test.log").is_file())

    def test_project_environment_and_inventory_path_precedence(self):
        env_root = self.work / "alternate" / "controller override"
        custom = self.work / "explicit Docker source"
        checks = [
            {"ansible.builtin.assert": {"that": ["_docker_local_config_dir == expected_local",
                                                 "_docker_remote_config_dir == '/srv/docker-configs'",
                                                 "_docker_reports_dir == expected_reports"]}},
            {"ansible.builtin.assert": {"that": ["_docker_local_config_dir == 'legacy-local'",
                                                 "_docker_remote_config_dir == 'legacy-remote'"]},
             "vars": {"local_base_dir": "legacy-local", "remote_base_dir": "legacy-remote",
                      "docker_local_base_dir": "canonical-local", "docker_remote_base_dir": "canonical-remote"}},
            {"ansible.builtin.assert": {"that": ["_docker_local_config_dir == 'canonical-local'"]},
             "vars": {"docker_local_base_dir": "canonical-local"}},
        ]
        self.play.write_text(yaml.safe_dump([{"hosts": "localhost", "gather_facts": False,
                                             "vars_files": ["vars/paths.yml"], "tasks": checks}]))
        cases = [
            (env_root, {}, {}, env_root.parent / "docker-configs", env_root / "x/reports"),
            (Path("/root/ansible"), {}, {}, "/root/docker-configs", "/root/ansible/x/reports"),
            (env_root, {"ANSIBLE_DOCKER_CONFIG_ROOT": str(custom), "ANSIBLE_REPORTS_DIR": "env reports"},
             {}, custom, env_root / "env reports"),
            (env_root, {"ANSIBLE_REPORTS_DIR": "env reports"}, {"controller_reports_dir": "site/reports"},
             env_root.parent / "docker-configs", env_root / "site/reports"),
        ]
        for root, env, variables, source, reports in cases:
            with self.subTest(root=root, variables=variables):
                result = subprocess.run(self.command({**variables, "expected_local": str(source),
                                                       "expected_reports": str(reports)}),
                                        env={**self.env, "ANSIBLE_PROJECT_ROOT": str(root), **env},
                                        cwd=self.plays, capture_output=True, text=True, timeout=25)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class DockerExportPathTests(unittest.TestCase):
    def test_direct_export_uses_cli_then_environment_then_project_sibling(self):
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary).resolve()
            cli_root = site / "cli" / "ansible"
            env_root = site / "env" / "ansible"
            cli_source = site / "CLI source"
            env_source = site / "env source"
            for path in (cli_source, env_source, cli_root.parent / "docker-configs", env_root.parent / "docker-configs"):
                path.mkdir(parents=True)
            clean = {name: value for name, value in os.environ.items()
                     if name not in {"ANSIBLE_PROJECT_ROOT", "ANSIBLE_DOCKER_CONFIG_ROOT"}}
            cases = [
                ([], {}, env_root.parent / "docker-configs"),
                (["--root", str(cli_root)], {}, cli_root.parent / "docker-configs"),
                (["--root", str(cli_root)], {"ANSIBLE_DOCKER_CONFIG_ROOT": str(env_source)}, env_source),
                (["--source", str(cli_source)], {"ANSIBLE_DOCKER_CONFIG_ROOT": str(env_source)}, cli_source),
            ]
            for flags, env, expected in cases:
                with self.subTest(flags=flags, env=env):
                    result = subprocess.run([sys.executable, str(BASE / "scripts/export_docker_users.py"),
                                             "--check", *flags], cwd=site,
                                            env={**clean, "ANSIBLE_PROJECT_ROOT": str(env_root), **env},
                                            text=True, capture_output=True, timeout=10)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(yaml.safe_load(result.stdout)["source"], str(expected))
