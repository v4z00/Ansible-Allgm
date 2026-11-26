"""Portable controller paths, safe plan output and example provenance."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import plan_checkmk_migration as planner


class ControllerPaths(unittest.TestCase):
    def test_settings_environment_and_existing_checkmk_plans(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp).resolve()
            reports = project / "exports"
            file = "checkmk_migration_plan.yml"
            with patch.dict(os.environ, {"ANSIBLE_REPORTS_DIR": str(reports)}):
                self.assertEqual(planner.plan_destination(project, {}), reports / file)
                self.assertEqual(planner.plan_destination(project, {"controller_reports_dir": "local"}), project / "local" / file)
                self.assertEqual(planner.plan_destination(project, {"checkmk_migration_plan": "custom.yml"}), project / "custom.yml")
                self.assertEqual(planner.plan_destination(project, {"checkmk_migration_plan": "{{ inventory_dir }}/../x/reports/" + file}), project / "x/reports" / file)
                self.assertEqual(planner.plan_destination(project, {}, str(project / "explicit")), project / "explicit")
                with self.assertRaises(planner.MigrationError):
                    planner.plan_destination(project, {"checkmk_migration_plan": "{{ unknown_path }}"})
            planner.publish(reports / file, {"mappings": []})
            self.assertEqual((reports / file).stat().st_mode & 0o777, 0o600)
            alias = project / "linked"
            alias.symlink_to(reports)
            with self.assertRaises(planner.MigrationError):
                planner.publish(alias / file, {"mappings": ["replace"]})
            self.assertEqual(json.loads((reports / file).read_text()), {"mappings": []})

    def test_shell_profile_and_command_use_the_selected_controller(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp).resolve() / "spaced controller"
            (path / "config").mkdir(parents=True)
            (path / "config/shell_aliases.sh").write_text('export SELECTED_CONTROLLER="$ANSIBLE_PROJECT_ROOT"\n')
            script = 'source "$1"; test "$SELECTED_CONTROLLER" = "$2"; ROOT_DIR="$3"; source "$4"; test "$ANSIBLE_PROJECT_ROOT" = "$3"'
            subprocess.run(["bash", "-ec", script, "probe", ROOT / "config/bashrc", path, ROOT,
                            ROOT / "lib/controller_environment.sh"], check=True,
                           env=dict(os.environ, ANSIBLE_PROJECT_ROOT=str(path)))

    def test_settings_catalog_records_the_current_public_examples(self):
        catalog = json.loads((ROOT / "update_check/settings_catalog.json").read_text())
        for name, expected in catalog["example_sources"].items():
            self.assertTrue(name.startswith("examples/"))
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), expected, name)

    @unittest.skipUnless(shutil.which("ansible-playbook"), "requires ansible-playbook")
    def test_ansible_resolves_fstab_reports_and_job_root_without_touching_hosts(self):
        import yaml
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp).resolve()
            data = yaml.safe_load((ROOT / "playbooks/maintenance/audit_fstab.yml").read_text())[0]["vars"]
            data.update(yaml.safe_load((ROOT / "roles/script_jobs_controller/defaults/main.yml").read_text()))
            data["controller_reports_dir"] = "reports/custom"
            play = [{"hosts": "localhost", "gather_facts": False, "vars": data, "tasks": [
                {"ansible.builtin.assert": {"that": [
                    "script_jobs_controller_root == lookup('env', 'ANSIBLE_PROJECT_ROOT')",
                    "audit_fstab_directory == script_jobs_controller_root ~ '/reports/custom/fstab_audit'",
                ]}}]}]
            path = project / "check.yml"
            path.write_text(yaml.safe_dump(play))
            config = project / "ansible.cfg"
            config.write_text("[defaults]\n")
            env = dict(os.environ, HOME=str(project), ANSIBLE_HOME=str(project / ".ansible"),
                       ANSIBLE_PROJECT_ROOT=str(project), ANSIBLE_CONFIG=str(config))
            command = ["ansible-playbook", "-c", "local", "-i", "localhost,", str(path)]
            result = subprocess.run(command, env=env, cwd=project, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
