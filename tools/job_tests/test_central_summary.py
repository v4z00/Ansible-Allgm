"""Full local collection/summary play; no jobs or real notification transports."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / 'artifacts/script-library'
sys.path.insert(0, str(LIB / 'lib/python'))
from job_store import Store


@unittest.skipUnless(os.environ.get('ANSIBLE_JOBS_INTEGRATION') == '1', 'explicit local Ansible integration')
class CentralSummary(unittest.TestCase):
    def test_collect_own_ansible_send_retry_and_query_failure_without_running_jobs(self):
        with tempfile.TemporaryDirectory(prefix='central-summary-') as temporary:
            root = Path(temporary).resolve()
            project = root / 'controller'
            project.mkdir()
            (project / 'scripts').symlink_to(ROOT / 'scripts')
            artifact = project / 'artifacts/script-library'
            shutil.copytree(LIB, artifact)
            messages = root / 'messages.jsonl'
            # Only this isolated artifact copy has a fake notification transport.
            (artifact / 'lib/python/job_notify.py').write_text('''import json,os
def deliver(channel,report,cfg,root):
 with open(os.environ['SUMMARY_MESSAGES'],'a') as stream:
  stream.write(json.dumps({'channel':channel,'body':report['body'],'id':report['id']})+'\\n')
 if channel=='mail' and os.environ.get('FAIL_MAIL')=='1':raise RuntimeError('fixture SMTP unavailable')
''')
            database = root / 'controller-state/jobs.sqlite3'
            state = Store(database, 'controller')
            state.close()
            sources = {}
            for host in ('alpha', 'beta'):
                runtime = root / host
                shutil.copytree(LIB, runtime)
                for binary in (runtime / 'bin').iterdir():
                    binary.chmod(0o700)
                db = root / (host + '-state/jobs.sqlite3')
                local = Store(db, host + '.example.invalid')
                run = local.begin('backup')
                if host == 'beta':local.update(run, 'failed', 'Backupziel nicht verfuegbar.', item='storage')
                local.update(run, 'success' if host == 'alpha' else 'failed', exit_code=0 if host == 'alpha' else 1)
                if host == 'alpha':
                    run = local.begin('weekly', 'vzdump')
                    local.update(run, 'failed', 'Abgeschlossenes Archiv fehlt.', item='102')
                    local.update(run, 'failed', exit_code=1)
                local.close()
                sources[host] = {'root': str(runtime), 'database': str(db)}
            # Inventory paths deliberately point elsewhere. Explicit test source
            # overrides must be honored without altering production-like vars.
            inventory = {'all': {'children': {'all_linux_systems': {'hosts': {
                host: {'ansible_connection': 'local', 'ansible_become': False, 'ansible_python_interpreter': sys.executable,
                       'script_jobs_target_root': str(root / 'wrong-root'), 'script_jobs_database_path': str(root / 'wrong.db')}
                for host in sources}}}}}
            (project / 'inventory.json').write_text(json.dumps(inventory))
            (project / 'ansible.cfg').write_text('[defaults]\ninventory=' + str(project / 'inventory.json') + '\nlocal_tmp=' + str(root / 'local-tmp') + '\nremote_tmp=' + str(root / 'remote-tmp') + '\n')
            (project / 'group_vars/all').mkdir(parents=True)
            (project / 'group_vars/all/channels.yml').write_text('telegram_bot_token: "123:synthetic-never-print"\ntelegram_chat_id: "-42"\nscript_jobs_mail_to: "admin@example.invalid"\n')
            config = root / 'summary-test.json'
            settings = {'database': str(database), 'targets': 'alpha,beta', 'source_overrides': sources,
                        'labels': {'hosts': {'alpha': 'Server A', 'beta': 'Server B', 'controller': 'Controller'},
                                   'jobs': {'ansible:synthetic.yml': 'Ansible-Test'}}}
            config.write_text(json.dumps(settings))
            (root / 'vars.json').write_text(json.dumps({'job_root': str(project), 'script_jobs_controller_config_file': str(config), 'ansible_become': False}))
            env = dict(os.environ, ANSIBLE_CONFIG=str(project / 'ansible.cfg'), SCRIPT_JOBS_CALLBACK='0', SUMMARY_MESSAGES=str(messages), FAIL_MAIL='1')
            binary = str(Path(sys.executable).parent / 'ansible-playbook')
            own_play = root / 'synthetic.yml'
            own_play.write_text('- hosts: all_linux_systems\n  gather_facts: false\n  tasks:\n    - debug:\n        msg: synthetic-private-task-argument\n')
            own_env = dict(env, ANSIBLE_CALLBACK_PLUGINS=str(ROOT / 'tools/callbacks'), ANSIBLE_CALLBACKS_ENABLED='script_job_results', SCRIPT_JOBS_CALLBACK='1', SCRIPT_JOBS_CONTROLLER_DB=str(database))
            own = subprocess.run([binary, str(own_play), '--limit', 'alpha,beta'], env=own_env, cwd=project, capture_output=True, text=True)
            self.assertEqual(own.returncode, 0, own.stdout + own.stderr)
            command = [binary, str(ROOT / 'playbooks/scripts/summary_jobs.yml'), '-e', '@' + str(root / 'vars.json')]
            first = subprocess.run(command, env=env, cwd=project, capture_output=True, text=True)
            self.assertNotEqual(first.returncode, 0)
            sent = [json.loads(line) for line in messages.read_text().splitlines()]
            self.assertEqual(len(sent), 4, first.stdout + first.stderr)  # two categories, each mail + Telegram
            general = next(message['body'] for message in sent if message['body'].startswith('Job-'))
            self.assertIn('Server A Backup ✅', general)
            self.assertIn('Server B Backup ❌\n  storage: Backupziel nicht verfuegbar.', general)
            self.assertIn('Controller Ansible-Test ✅', general)
            self.assertNotIn('Vzdump', general)
            self.assertTrue(any('Server A Vzdump ❌' in message['body'] for message in sent))
            for message in sent:
                self.assertNotIn(message['id'], message['body'])
                self.assertNotRegex(message['body'], r'✅\s+\d|Bericht:')
                self.assertNotIn('synthetic-private-task-argument', message['body'])
            self.assertNotIn('synthetic-never-print', first.stdout)
            env['FAIL_MAIL'] = '0'
            second = subprocess.run(command, env=env, cwd=project, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            sent = [json.loads(line) for line in messages.read_text().splitlines()]
            self.assertEqual(sum(message['channel'] == 'telegram' for message in sent), 2)
            self.assertEqual(sum(message['channel'] == 'mail' for message in sent), 4)
            state = Store(database)
            self.assertEqual(len(state.runs()), 4)  # three host jobs + own Ansible run
            self.assertEqual(state.db.execute("SELECT count(*) FROM deliveries WHERE status='sent'").fetchone()[0], 4)
            state.close()

            settings['failure_targets'] = 'beta'
            settings['separate_failure_jobs'] = ['backup']
            config.write_text(json.dumps(settings))
            beta = Store(sources['beta']['database'], 'beta.example.invalid')
            failure = beta.begin('backup')
            beta.update(failure, 'failed', exit_code=1)
            beta.close()
            failure_command = command + ['-e', 'script_jobs_failures_only=true']
            failures = subprocess.run(failure_command, env=env, cwd=project, capture_output=True, text=True)
            self.assertEqual(failures.returncode, 0, failures.stdout + failures.stderr)
            individual = [json.loads(line) for line in messages.read_text().splitlines()][len(sent):]
            self.assertEqual({message['channel'] for message in individual}, {'telegram', 'mail'})
            self.assertTrue(all(message['body'].startswith('Job fehlgeschlagen') for message in individual))
            self.assertEqual(len(individual), 2)
            repeated = subprocess.run(failure_command, env=env, cwd=project, capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
            self.assertEqual(len(messages.read_text().splitlines()), len(sent) + 2)

            # A failed subsequent query must be reported as an unavailable
            # collection, never as a new successful backup or a rerun.
            settings['source_overrides']['beta']['root'] = str(root / 'missing-helper')
            config.write_text(json.dumps(settings))
            third = subprocess.run(command, env=env, cwd=project, capture_output=True, text=True)
            self.assertNotEqual(third.returncode, 0)
            sent = [json.loads(line) for line in messages.read_text().splitlines()]
            self.assertIn('Server B Abfrage ❌', sent[-1]['body'])
            for value in sources.values():
                local = Store(value['database'])
                self.assertEqual(local.db.execute('SELECT count(*) FROM reports').fetchone()[0], 0)
                self.assertIn(len(local.runs()), (1, 2))
                local.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
