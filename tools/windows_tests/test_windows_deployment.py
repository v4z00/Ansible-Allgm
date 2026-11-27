"""Controller-only deployment checks; no remote Windows actions are executed."""
import ast
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT=Path(__file__).resolve().parents[2]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


class WindowsDeployment(unittest.TestCase):
    def test_security_channel_filter_never_copies_unselected_credentials(self):
        module=load('security_configuration','roles/script_security_alerts/filter_plugins/security_config.py')
        source={'MAIL_TO':'receiver@example.invalid','BOT_TOKEN':'12345:synthetic-token','CHAT_ID':'-12345',
                'SMTP_HOST':'relay.example.invalid','SMTP_FROM':'sender@example.invalid','SMTP_TLS':'none','SMTP_AUTH':'none',
                'SMTP_USERNAME':'unused','SMTP_PASSWORD':'must-not-copy'}
        mail=module.configuration(source,['mail'],True)
        self.assertNotIn('BOT_TOKEN',mail);self.assertNotIn('SMTP_PASSWORD',mail);self.assertEqual(mail['SMTP_PORT'],25)
        telegram=module.configuration(source,['telegram'],True)
        self.assertEqual(set(telegram),{'SECURITY_CHANNELS','BOT_TOKEN','CHAT_ID'})
        with self.assertRaises(ValueError):module.configuration({**source,'SMTP_TLS':'tls'},['mail'],True)
    def test_public_library_allowlist_excludes_runtime_binaries_and_configs(self):
        module=load('staging_public_windows','update_check/staging_manifest.py')
        for path in ('artifacts/script-library/windows/lib/ScriptLibrary.psm1',
                     'artifacts/script-library/windows/lib/functions/Start-ScriptJob.ps1',
                     'artifacts/script-library/lib/data/job-schema.sql'):
            self.assertTrue(module.allowed(path),path)
        for path in ('artifacts/sqlite/windows/sqlite3.exe','artifacts/script-library/windows/config/security.json',
                     'artifacts/script-library/windows/lib/functions/../secrets.ps1'):
            self.assertFalse(module.allowed(path),path)
    def test_windows_and_linux_path_assertions_in_real_ansible(self):
        binary=Path(sys.executable).with_name('ansible-playbook')
        if not binary.exists():self.skipTest('Ansible required')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            tasks=yaml.safe_load((ROOT/'roles/windows_bootstrap/tasks/main.yml').read_text())
            checks=next(task['ansible.builtin.assert']['that'] for task in tasks if 'ansible.builtin.assert' in task)
            defaults=yaml.safe_load((ROOT/'roles/windows_bootstrap/defaults/main.yml').read_text())
            play=[{'hosts':'localhost','connection':'local','gather_facts':False,
                   'vars':{**defaults,'ansible_facts':{'os_family':'Windows'}},
                   'tasks':[{'ansible.builtin.assert':{'that':checks}}]}]
            path=root/'assert.yml';path.write_text(yaml.safe_dump(play))
            result=subprocess.run([str(binary),'-i','localhost,',str(path)],env={**os.environ,'ANSIBLE_LOCAL_TEMP':str(root/'tmp')},capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
    def test_new_playbooks_and_generated_collector_parse_in_ansible(self):
        binary=Path(sys.executable).with_name('ansible-playbook')
        if not binary.exists():self.skipTest('Ansible required')
        tree=ast.parse((ROOT/'scripts/job_console.py').read_text())
        collector=next(ast.literal_eval(node.value) for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PLAY' for t in node.targets))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);query=root/'query.yml';query.write_text(collector)
            paths=list((ROOT/'playbooks/windows').glob('*.yml'))+[ROOT/'playbooks/scripts/security_alerts.yml',ROOT/'playbooks/scripts/checkmk_jobs.yml',ROOT/'playbooks/scripts/show_status.yml',query]
            env={**os.environ,'ANSIBLE_LOCAL_TEMP':str(root/'tmp'),'ANSIBLE_ROLES_PATH':str(ROOT/'roles')}
            for path in paths:
                with self.subTest(playbook=path.name):
                    result=subprocess.run([str(binary),'-i','localhost,','--syntax-check','-e','job_targets=localhost',str(path)],env=env,capture_output=True,text=True)
                    self.assertEqual(result.returncode,0,result.stdout+result.stderr)


if __name__=='__main__':unittest.main()
