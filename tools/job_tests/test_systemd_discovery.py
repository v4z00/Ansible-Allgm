"""Systemd discovery exports allowed metadata only; no host/config side effects."""
import importlib.util
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('get_systemd_scripts', ROOT / 'scripts/get_systemd_scripts.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class Discovery(unittest.TestCase):
    def setUp(self):
        self.namespace = {'__name__': 'fixture'}
        exec(compile(reader.REMOTE, 'systemd-reader-fixture', 'exec'), self.namespace)

    def test_exec_arguments_and_inline_credentials_never_leave_host_filter(self):
        token = '123456789:synthetic_PRIVATE_TOKEN'
        raw = ('ExecStart={ path=/usr/bin/bash ; argv[]=/usr/bin/bash /opt/jobs/backup.sh '
               '--bot-token=' + token + ' ; ignore_errors=no ; start_time=n/a ; }\n')
        with patch.dict(self.namespace, command=lambda args: (0, raw)):
            result = self.namespace['references']('fixture.service')
        self.assertNotIn(token, json.dumps(result))
        self.assertNotIn('--bot-token', json.dumps(result))
        self.assertEqual(result['scripts'], [{'directive': 'ExecStart', 'path': '/opt/jobs/backup.sh'}])
        self.assertEqual(result['start_kind'], 'review')

    def test_no_environment_or_secret_properties_are_requested(self):
        calls = []

        def query(args):
            calls.append(args)
            return 0, 'Id=fixture.service\nType=oneshot\nEnvironment=BOT_TOKEN=never-export\nDescription=never-export\n'

        with patch.dict(self.namespace, command=query):
            result = self.namespace['properties']('fixture.service')
        self.assertNotIn('never-export', json.dumps(result))
        requested = ' '.join(calls[0])
        for forbidden in ('Environment', 'Credential', 'Description', 'ExecStart'):
            self.assertNotIn(forbidden, requested)

    def test_path_looking_secret_arguments_are_not_treated_as_script_references(self):
        raw = ('ExecStart={ path=/bin/bash ; argv[]=/bin/bash /opt/jobs/backup.sh '
               '--password=/private/confidential-value.sh ; ignore_errors=no ; pid=0 ; }\n'
               'ExecReload={ path=/bin/echo ; argv[]=/bin/echo /private/another-value.sh ; ignore_errors=no ; pid=0 ; }')
        with patch.dict(self.namespace, command=lambda args: (0, raw)):
            result = self.namespace['references']('fixture.service')
        self.assertNotIn('confidential-value', json.dumps(result))
        self.assertNotIn('another-value', json.dumps(result))
        self.assertEqual(result['scripts'], [{'directive': 'ExecStart', 'path': '/opt/jobs/backup.sh'}])

    def test_simple_script_starts_are_distinguished_from_shell_commands(self):
        cases = [('/opt/jobs/backup.sh', '/opt/jobs/backup.sh', 'direct-script'),
                 ('/bin/bash', '/bin/bash /opt/jobs/backup.sh', 'shell-script'),
                 ('/bin/bash', '/bin/bash -c "source /opt/jobs/backup.sh"', 'review')]
        for executable, arguments, expected in cases:
            with self.subTest(expected=expected):
                raw = 'ExecStart={ path=' + executable + ' ; argv[]=' + arguments + ' ; ignore_errors=no ; pid=0 ; }'
                with patch.dict(self.namespace, command=lambda args: (0, raw)):
                    self.assertEqual(self.namespace['references']('fixture.service')['start_kind'], expected)

    def test_secret_named_script_references_are_omitted(self):
        raw = 'ExecStart={ path=/root/secrets/token.sh ; argv[]=/root/secrets/token.sh ; ignore_errors=no ; pid=0 ; }'
        with patch.dict(self.namespace, command=lambda args: (0, raw)):
            result = self.namespace['references']('fixture.service')
        self.assertEqual(result['scripts'], [])
        self.assertIsNone(result['start_script'])

    def test_systemctl_errors_do_not_echo_raw_stderr_or_output(self):
        failure = subprocess.CompletedProcess([], 1, 'secret stdout', 'secret stderr')
        with patch.object(self.namespace['subprocess'], 'run', return_value=failure) as run:
            result = self.namespace['command'](['show', 'fixture.service'])
        self.assertEqual(result, (1, ''))
        self.assertNotIn('BOT_TOKEN', run.call_args.kwargs['env'])
        self.assertTrue(run.call_args.kwargs['capture_output'])


@unittest.skipUnless(os.environ.get('ANSIBLE_JOBS_INTEGRATION') == '1', 'explicit local Ansible integration')
class CollectorIntegration(unittest.TestCase):
    def test_standalone_collects_per_host_without_raw_arguments_or_changes(self):
        with tempfile.TemporaryDirectory(prefix='systemd-discovery-') as temporary:
            root = Path(temporary).resolve()
            fake = root / 'systemctl-fixture'
            marker = root / 'mutation-called'
            fake.write_text('#!' + sys.executable + '\n' + '''import sys
args=sys.argv[1:]
if 'list-unit-files' in args or 'list-units' in args:
 print('fixture.timer enabled' if '--type=timer' in args else 'fixture.service enabled')
elif 'show' in args:
 if '--property=ExecStart,ExecStartPre,ExecStartPost,ExecStop,ExecStopPost,ExecReload' in args:
  print('ExecStart={ path=/bin/bash ; argv[]=/bin/bash /opt/jobs/backup.sh --token=synthetic_NEVER_EXPORT ; ignore_errors=no ; pid=0 ; }')
 elif 'fixture.timer' in args:
  print('Id=fixture.timer\\nFragmentPath=/etc/systemd/system/fixture.timer\\nTriggers=fixture.service\\nUnitFileState=enabled')
 else:
  print('Id=fixture.service\\nFragmentPath=/etc/systemd/system/fixture.service\\nType=oneshot\\nUser=root\\nActiveState=inactive\\nUnitFileState=enabled')
else:
 from pathlib import Path
 Path(''' + repr(str(marker)) + ''').touch()
 sys.exit(99)
''')
            fake.chmod(0o700)
            project = root / 'controller'
            project.mkdir()
            inventory = {'all': {'children': {'all_linux_systems': {'hosts': {
                name: {'ansible_connection': 'local', 'ansible_become': False,
                       'ansible_python_interpreter': sys.executable, 'script_jobs_python': sys.executable}
                for name in ('alpha', 'beta')}}}}}
            (project / 'inventory.json').write_text(json.dumps(inventory))
            (project / 'ansible.cfg').write_text('[defaults]\ninventory=' + str(project / 'inventory.json') +
                                               '\nlocal_tmp=' + str(root / 'local-tmp') +
                                               '\nremote_tmp=' + str(root / 'remote-tmp') + '\n')
            remote = reader.REMOTE.replace("['systemctl','--no-pager',*arguments]",
                                           '[' + repr(str(fake)) + ",'--no-pager',*arguments]").replace('pwd.getpwall()', '[]')
            output = root / 'collected'
            stdout = io.StringIO()
            with patch.object(reader, 'REMOTE', remote), \
                    patch.object(sys, 'argv', ['get_systemd_scripts.py', '--project', str(project),
                                              '--limit', 'all_linux_systems', '--output', str(output)]), \
                    patch.dict(os.environ, PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ['PATH']), \
                    contextlib.redirect_stdout(stdout):
                self.assertEqual(reader.main(), 0, stdout.getvalue())
            self.assertFalse(marker.exists())
            for name in ('alpha', 'beta'):
                path = output / name / 'systemd.json'
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
                self.assertNotIn('synthetic_NEVER_EXPORT', path.read_text())
                data = json.loads(path.read_text())
                self.assertTrue(data['complete'])
                self.assertEqual(data['services'][0]['unit'], 'fixture.service')
                self.assertEqual(data['services'][0]['start_kind'], 'review')
                self.assertEqual(data['timers'][0]['unit'], 'fixture.timer')
            self.assertNotIn('synthetic_NEVER_EXPORT', stdout.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)
