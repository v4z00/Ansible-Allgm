"""Explicit profile source mapping, generated units and privacy-safe lifecycle."""
import grp
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pwd
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


planner = module('profile_planner', 'roles/script_jobs/filter_plugins/profile_deployment.py')
guard = module('profile_guard', 'scripts/job_profile_guard.py')
manager = module('profile_manager', 'scripts/job_profile_apply.py')


class Profiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory();self.root = Path(self.tmp.name).resolve()
        self.source = self.root / 'private/alpha/services/watcher';self.source.mkdir(parents=True)
        (self.source / 'bin').mkdir();self.program = self.source / 'bin/watcher.sh'
        self.program.write_text('#!/bin/sh\nexit 0\n')
        self.manifest = {'files': [{'path': 'bin/watcher.sh', 'kind': 'script', 'sha256': hashlib.sha256(self.program.read_bytes()).hexdigest()}]}
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        self.profile = {'source': 'services/watcher', 'target': str(self.root / 'destination'),
                        'services': [{'unit': 'example-watcher.service', 'mode': 'active', 'exec_start': ['{target}/bin/watcher.sh']}]}

    def tearDown(self):self.tmp.cleanup()

    def plan(self):
        return planner.deployment({'watcher': self.profile}, ['watcher'], str(self.root / 'private/alpha'), str(self.root / 'library'))

    def test_relative_files_follow_changed_profile_destination_and_service_path(self):
        first = self.plan();self.assertEqual(first['files'][0]['dest'], str(self.root / 'destination/bin/watcher.sh'))
        self.profile['target'] = str(self.root / 'another destination')
        second = self.plan()
        self.assertIn(str(self.root / 'another destination/bin/watcher.sh'), str(second['services'][0]['sections']))
        self.assertEqual(second['files'][0]['mode'], '0700')
        self.assertEqual(second['services'][0]['action'], {'unit': 'example-watcher.service'})
        self.assertEqual(second['files'][0]['source'], first['files'][0]['source'])

    def test_review_hash_links_traversal_and_library_overwrite_are_refused(self):
        self.program.write_text('changed')
        with self.assertRaises(ValueError):self.plan()
        self.program.write_text('#!/bin/sh\nexit 0\n')
        for key in ('review_required', 'sanitized_import'):
            (self.source / 'deployment.json').write_text(json.dumps({**self.manifest, key: True}))
            with self.assertRaises(ValueError):self.plan()
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        self.program.unlink();self.program.symlink_to(self.source / 'deployment.json')
        with self.assertRaises(ValueError):self.plan()
        for value in ('../escape', '/absolute', '.', 'bin/../file', 'bin//file'):
            with self.assertRaises(ValueError):planner.relative(value)
        self.profile['target'] = '/root/ansible/private-programs'
        with self.assertRaises(ValueError):self.plan()

    def test_arguments_are_literal_and_profile_flags_do_not_inject_unit_lines(self):
        row = planner.service({'unit': 'fixture.service', 'mode': 'active', 'exec_start': ['/bin/echo', '$TOKEN', '100%', 'a"b', 'a\\b']}, '/opt/example', '/scripte', 'root', 'root')
        command = dict(row['sections']['Service'])['ExecStart']
        self.assertIn('"$$TOKEN"', command);self.assertIn('"100%%"', command);self.assertIn('a\\"b', command)
        for spec in ({'description': 'x\nExecStart=/bad'}, {'enabled': 'yes'}, {'state': 'start'}, {'restart': 'bad'}):
            with self.assertRaises((ValueError, KeyError)):
                planner.service({'unit': 'fixture.service', 'mode': 'active', 'exec_start': ['/bin/true'], **spec}, '/opt/example', '/scripte', 'root', 'root')

    def test_tagged_ansible_numbers_are_accepted_without_accepting_flags_or_nonfinite_values(self):
        class TaggedInt(int):pass
        values={'unit':'fixture.service','mode':'active','exec_start':['/bin/true']}
        row=planner.service({**values,'timeout_start_sec':TaggedInt(30)},'/opt/example','/scripte','root','root')
        self.assertIn(('TimeoutStartSec','30'),row['sections']['Service'])
        for value in (True,False,float('nan'),float('inf'),-1,'30'):
            with self.assertRaises(ValueError):planner.service({**values,'timeout_start_sec':value},'/opt/example','/scripte','root','root')

    def test_private_mapping_cannot_replace_units_or_runtime_history(self):
        self.manifest['files'][0]['dest'] = 'unreviewed.service'
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):self.plan()
        self.manifest['files'][0]['dest'] = 'jobs.sqlite3'
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):
            planner.deployment({'watcher': self.profile}, ['watcher'], str(self.root / 'private/alpha'),
                               str(self.root / 'library'), database=str(self.root / 'destination/jobs.sqlite3'))

    def test_destination_ancestors_and_existing_types_are_guarded_without_reads(self):
        directory = self.root / 'target';directory.mkdir();(directory / 'link').symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError):guard.check([['file', str(directory / 'link/file')]])
        with self.assertRaises(ValueError):guard.check([['file', str(directory)]])
        guard.check([['file', str(directory / 'new/file')]])

    def test_service_user_gets_an_isolated_library_and_json_configuration(self):
        self.profile.update(library=True, owner='serviceuser', group='serviceuser')
        self.manifest['files'][0]['dest'] = 'programs/watcher.sh'
        config = self.source / 'settings.json';config.write_text('{"API_TOKEN":""}')
        self.manifest['files'].append({'path': 'settings.json', 'kind': 'config', 'config_key': 'watcher',
                                      'sha256': hashlib.sha256(config.read_bytes()).hexdigest()})
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        plan = self.plan()
        self.assertEqual(plan['libraries'], [{'path': self.profile['target'], 'owner': 'serviceuser', 'group': 'serviceuser'}])
        self.assertEqual(plan['files'][1]['config_key'], 'watcher')
        self.assertEqual(plan['files'][1]['mode'], '0600')
        self.assertIn('SCRIPT_LIBRARY_ROOT=' + self.profile['target'], str(plan['services']))
        self.assertIn(['directory', self.profile['target'] + '/lib/common'], plan['checks'])
        self.manifest['files'][0]['dest'] = 'lib/common/injected.sh'
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):self.plan()

    def test_profile_rendering_rejects_non_json_and_overlapping_libraries(self):
        self.manifest['files'][0]['config_key'] = 'watcher'
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        with self.assertRaises(ValueError):self.plan()
        self.manifest['files'][0].pop('config_key')
        (self.source / 'deployment.json').write_text(json.dumps(self.manifest))
        self.profile.update(library=True, target=str(self.root / 'library/nested'))
        with self.assertRaises(ValueError):self.plan()
        self.profile['target'] = str(self.root / 'library')
        with self.assertRaises(ValueError):self.plan()

    def test_lifecycle_is_explicit_idempotent_and_does_not_request_environment(self):
        calls = []
        def command(args):
            calls.append(args)
            return 'LoadState=loaded\nActiveState=active\nUnitFileState=enabled\nEnvironment=synthetic_NEVER_EXPORT\n'
        with patch.object(manager, 'command', side_effect=command):
            self.assertFalse(manager.apply([{'unit': 'fixture.service'}])['changed'])
            self.assertEqual(calls, [])
            self.assertFalse(manager.apply([{'unit': 'fixture.service', 'enabled': True, 'state': 'started'}])['changed'])
            self.assertTrue(manager.apply([{'unit': 'fixture.service', 'state': 'restarted'}])['changed'])
        self.assertIn(['restart', 'fixture.service'], calls)
        requested = [call[-1] for call in calls if call[0] == 'show']
        self.assertTrue(all(value == '--property=LoadState,ActiveState,UnitFileState' for value in requested))


@unittest.skipUnless(os.environ.get('ANSIBLE_JOBS_INTEGRATION') == '1', 'explicit local Ansible integration')
class ProfileIntegration(unittest.TestCase):
    def test_actual_play_deploys_folder_generates_unit_and_keeps_start_opt_in(self):
        with tempfile.TemporaryDirectory(prefix='profile-deploy-') as temporary:
            root = Path(temporary).resolve();source = root / 'private/alpha/watcher';source.mkdir(parents=True)
            (source / 'programs').mkdir();program = source / 'programs/watcher.sh'
            marker = root / 'program-ran';program.write_text('#!/bin/sh\ntouch ' + str(marker) + '\n')
            manifest = {'files': [{'path': 'programs/watcher.sh', 'kind': 'script', 'sha256': hashlib.sha256(program.read_bytes()).hexdigest()}]}
            settings = source / 'settings.json';settings.write_text('{"API_TOKEN":"", "BOT_TOKEN":"source-must-not-deploy"}')
            manifest['files'].append({'path': 'settings.json', 'kind': 'config', 'config_key': 'fixture',
                                      'sha256': hashlib.sha256(settings.read_bytes()).hexdigest()})
            (source / 'deployment.json').write_text(json.dumps(manifest))
            log = root / 'systemctl-actions';fakebin = root / 'fakebin';fakebin.mkdir()
            fake = fakebin / 'systemctl'
            fake.write_text('#!' + sys.executable + '\nimport sys\nfrom pathlib import Path\nwith Path(' + repr(str(log)) + ').open("a") as f:f.write(" ".join(sys.argv[1:])+"\\n")\nif "show" in sys.argv:print("LoadState=loaded\\nActiveState=active\\nUnitFileState=enabled")\n')
            fake.chmod(0o700)
            who = pwd.getpwuid(os.getuid()).pw_name;team = grp.getgrgid(os.getgid()).gr_name
            host = {'ansible_connection': 'local', 'ansible_become': False, 'ansible_python_interpreter': sys.executable,
                    'script_jobs_python': sys.executable, 'script_jobs_source_root': str(root / 'private'),
                    'script_jobs_target_root': str(root / 'library'), 'script_jobs_database_path': str(root / 'data/jobs.db'),
                    'script_jobs_owner': who, 'script_jobs_group': team,
                    'script_jobs_systemd_unit_dir': str(root / 'units'), 'script_jobs_systemd_unit_owner': who, 'script_jobs_systemd_unit_group': team,
                    'script_jobs_job_config': {'fixture': {'API_TOKEN': 'synthetic-api', 'BOT_TOKEN': 'synthetic-do-not-copy'}},
                    'script_jobs_profile_config': {'fixture': {'API_TOKEN': 'synthetic-profile-api'}},
                    'script_jobs_systemd_profiles': {'watcher': {'source': 'watcher', 'target': str(root / 'installed'), 'library': True,
                        'services': [{'unit': 'fixture.service', 'mode': 'active', 'timeout_start_sec':30, 'restart_sec':5, 'exec_start': ['{target}/programs/watcher.sh'], 'wanted_by': ['multi-user.target']}]}},
                    'script_jobs_systemd_selected_profiles': ['watcher']}
            inventory = {'all': {'children': {'all_linux_systems': {'hosts': {'alpha': host}}}}}
            (root / 'inventory.json').write_text(json.dumps(inventory))
            (root / 'ansible.cfg').write_text('[defaults]\ninventory=' + str(root / 'inventory.json') + '\nroles_path=' + str(ROOT / 'roles') + '\nlocal_tmp=' + str(root / 'local-tmp') + '\nremote_tmp=' + str(root / 'remote-tmp') + '\n')
            env = dict(os.environ, ANSIBLE_CONFIG=str(root / 'ansible.cfg'), SCRIPT_JOBS_CALLBACK='0', PATH=str(fakebin) + os.pathsep + os.environ['PATH'])
            command = [str(Path(sys.executable).parent / 'ansible-playbook'), str(ROOT / 'playbooks/scripts/deploy_systemd.yml'), '--limit', 'alpha']
            # Role defaults must remain available to the following library role.
            # This plan-only check deliberately has no user/group host overrides.
            defaults_host=dict(host);defaults_host.pop('script_jobs_owner');defaults_host.pop('script_jobs_group')
            defaults_inventory={'all': {'hosts': {'alpha': defaults_host}}}
            defaults_file=root/'default-inventory.json';defaults_file.write_text(json.dumps(defaults_inventory))
            defaults_play=root/'default-scope.json'
            defaults_play.write_text(json.dumps([{'hosts':'alpha','gather_facts':False,'tasks':[
                {'ansible.builtin.include_role':{'name':'script_jobs','tasks_from':'systemd_plan','public':True}},
                {'ansible.builtin.assert':{'that':["script_jobs_owner == 'root'", "script_jobs_group == 'root'"]}}]}]))
            defaults_run=subprocess.run([command[0],str(defaults_play),'-i',str(defaults_file),'--limit','alpha'],env=env,cwd=root,capture_output=True,text=True)
            self.assertEqual(defaults_run.returncode,0,defaults_run.stdout+defaults_run.stderr)
            preview = subprocess.run(command + ['--check'], env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertFalse((root / 'installed').exists())
            self.assertFalse((root / 'units').exists())
            self.assertFalse(log.exists());self.assertFalse(marker.exists())
            first = subprocess.run(command, env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            unit = (root / 'units/fixture.service').read_text()
            self.assertIn('ExecStart="' + str(root / 'installed/programs/watcher.sh') + '"', unit)
            self.assertEqual((root / 'installed/programs/watcher.sh').read_bytes(), program.read_bytes())
            rendered = json.loads((root / 'installed/settings.json').read_text())
            self.assertEqual(rendered['API_TOKEN'], 'synthetic-profile-api');self.assertEqual(rendered['BOT_TOKEN'], '')
            self.assertEqual((root / 'installed/settings.json').stat().st_mode & 0o777, 0o600)
            self.assertTrue((root / 'installed/lib/common/hm_load_config.sh').is_file())
            self.assertFalse(marker.exists());self.assertIn('daemon-reload', log.read_text());self.assertNotIn(' start ', log.read_text())
            second = subprocess.run(command, env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertRegex(second.stdout, r'changed=0\s')
            self.assertEqual(log.read_text().count('daemon-reload'), 1)
            # Selecting an explicit action changes only the requested service.
            host['script_jobs_systemd_profiles']['watcher']['services'][0].update(enabled=True, state='restarted')
            (root / 'inventory.json').write_text(json.dumps(inventory))
            third = subprocess.run(command, env=env, cwd=root, capture_output=True, text=True)
            self.assertEqual(third.returncode, 0, third.stdout + third.stderr)
            self.assertIn('restart fixture.service', log.read_text());self.assertFalse(marker.exists())


if __name__ == '__main__':unittest.main(verbosity=2)
