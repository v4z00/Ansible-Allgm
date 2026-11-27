"""Windows access preparation and real Ansible variable resolution; no host contact."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


setup = module('setup_windows', 'scripts/setup_windows.py')
bootstrap = module('platform_bootstrap', 'scripts/run_platform_bootstrap.py')


class WindowsAccess(unittest.TestCase):
    def test_prepare_never_reads_settings_and_preserves_existing_resolver(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'templates/windows/access.yml.example'
            source.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / 'templates/windows/access.yml.example', source)
            original_reader = Path.read_text

            def read(path, *args, **kwargs):
                if path.name == 'settings.yml':
                    self.fail('Password settings were opened')
                return original_reader(path, *args, **kwargs)

            with patch.object(Path, 'read_text', read):
                self.assertTrue(setup.prepare(root))
                target = root / 'group_vars/all_windows_systems/access.yml'
                self.assertFalse(target.exists())
                self.assertTrue(setup.prepare(root, apply=True))
                self.assertEqual(target.stat().st_mode & 0o777, 0o600)
                target.write_text('existing private resolver\n')
                self.assertFalse(setup.prepare(root, apply=True))
                self.assertEqual(target.read_text(), 'existing private resolver\n')

    def test_missing_template_does_not_create_an_empty_access_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            with self.assertRaises(FileNotFoundError):setup.prepare(root,apply=True)
            self.assertFalse((root/'group_vars/all_windows_systems/access.yml').exists())

    def test_linux_bootstrap_arguments_remain_unchanged(self):
        args = ['--limit', 'example-host', '--list-hosts']
        self.assertEqual(bootstrap.command(args)[2:], args)
        self.assertTrue(bootstrap.command(args)[1].endswith('scripts/run_bootstrap.py'))

    def test_windows_bootstrap_requires_a_nonempty_explicit_limit(self):
        for args in ([], ['--limit'], ['--limit', ''], ['--limit='], ['--limit', '--check']):
            with self.subTest(args=args), self.assertRaises(SystemExit):
                bootstrap.command(['--platform', 'windows', *args])
        command = bootstrap.command(['--platform', 'windows', '--limit', 'win01', '--check'])
        self.assertEqual(command, ['ansible-playbook', 'playbooks/windows/bootstrap.yml', '--limit', 'win01', '--check'])

    def test_inventory_windows_tags_do_not_add_a_linux_host_to_windows(self):
        generator = module('windows_inventory_fixture', 'scripts/generate_inventory.py')
        inventory = generator.make_inventory({
            'win01': {'inventory_os_family': 'windows', 'proxmox_tags': 'dc'},
            'linux01': {'inventory_os_family': 'linux', 'proxmox_tags': ''},
        }, {}, [])
        groups = inventory['all']['children']
        self.assertEqual(set(groups['all_windows_systems']['hosts']), {'win01'})
        self.assertEqual(set(groups['windows_domain_controllers']['hosts']), {'win01'})
        self.assertEqual(set(groups['all_linux_systems']['hosts']), {'linux01'})

    def test_real_ansible_resolves_windows_settings_without_changing_ssh_access(self):
        executable = Path(sys.executable).parent / 'ansible-playbook'
        if not executable.is_file():
            self.skipTest('Ansible runtime required')
        with tempfile.TemporaryDirectory(prefix='windows-access-fixture-') as temporary:
            root = Path(temporary)
            for group, source in [('all', 'examples/first_run/access.yml.example'),
                                  ('all_windows_systems', 'templates/windows/access.yml.example')]:
                folder = root / 'group_vars' / group
                folder.mkdir(parents=True)
                shutil.copyfile(ROOT / source, folder / 'access.yml')
            settings = {'ansible_auth_mode': 'key_only', 'managed_access_default_user': 'root',
                        'windows_access': {'user': 'EXAMPLE\\automation', 'password': 'fixture-only-password'}}
            (root / 'group_vars/all/settings.yml').write_text(yaml.safe_dump(settings))
            inventory = {'all': {'hosts': {'linux01': {}, 'win01': {}},
                                'children': {'all_windows_systems': {'hosts': {'win01': {}}}}}}
            (root / 'inventory.yml').write_text(yaml.safe_dump(inventory))
            checks = [{'name': 'Windows group overrides the Linux SSH resolver',
                       'ansible.builtin.assert': {'that': [
                           "ansible_connection == 'winrm'", "ansible_user == 'EXAMPLE\\\\automation'",
                           "ansible_password == 'fixture-only-password'", 'ansible_port | int == 5986',
                           'not ansible_become', "ansible_winrm_scheme == 'https'",
                           "ansible_winrm_server_cert_validation == 'validate'",
                           'ansible_winrm_ca_trust_path is none']},
                       'no_log': True, 'when': "inventory_hostname == 'win01'"},
                      {'name': 'Linux keeps SSH settings', 'ansible.builtin.assert': {'that': [
                           "ansible_user == 'root'", "ansible_password == ''", 'ansible_port | int == 22']},
                       'no_log': True, 'when': "inventory_hostname == 'linux01'"}]
            (root / 'check.yml').write_text(yaml.safe_dump([{'hosts': 'all', 'gather_facts': False, 'tasks': checks}]))
            result = subprocess.run([str(executable), '-i', str(root / 'inventory.yml'), str(root / 'check.yml')],
                                    cwd=root, env={**os.environ, 'ANSIBLE_LOCAL_TEMP': str(root / 'tmp'),
                                                   'SCRIPT_JOBS_CALLBACK': '0'}, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn('fixture-only-password', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
