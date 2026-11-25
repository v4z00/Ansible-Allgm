"""Summary presentation, autonomous execution and latest-state regressions."""
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import urllib.parse

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / 'artifacts/script-library'
sys.path.insert(0, str(LIB / 'lib/python'))
from job_store import Store
from job_report import format_report
import job_notify


class Summary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = Store(self.root / 'jobs.db', 'docker01.example.invalid')
        self.addCleanup(self.store.close)

    def finish(self, job='dockerbackup', status='success', category='general', summary='Completed'):
        run = self.store.begin(job, category)
        self.store.update(run, status, summary, exit_code=1 if status == 'failed' else 0)
        return run

    def test_short_success_without_ids_counters_or_details(self):
        run = self.finish()
        report = self.store.report(reserve=False)
        self.assertEqual(report['body'], 'Job-Zusammenfassung\n\nDocker01 Backup ✅')
        self.assertNotIn(report['id'], report['body'])
        self.assertNotIn(run, report['body'])
        self.assertNotRegex(report['body'], r'✅\s+\d|Bericht:|success')

    def test_one_line_per_job_keeps_an_unreported_failure_visible(self):
        run = self.store.begin('dockerbackup')
        self.store.update(run, 'failed', 'Shell operation failed at line 20 (exit 124)', item='shell')
        self.store.update(run, 'failed', exit_code=124)
        self.finish()
        body = self.store.report(reserve=False)['body']
        self.assertEqual(body.count('Docker01 Backup'), 1)
        self.assertIn('Docker01 Backup ❌\n  Zeitlimit erreicht (Exitcode 124).', body)
        self.assertNotIn('line 20', body)

    def test_failed_objects_below_status_success_objects_stay_in_database(self):
        run = self.store.begin('weekly', 'vzdump')
        self.store.update(run, 'success', 'complete', item='101')
        self.store.update(run, 'failed', 'Quelldatei fehlt', item='102')
        self.store.update(run, 'failed', exit_code=1)
        body = self.store.report('vzdump', reserve=False)['body']
        self.assertIn('Docker01 Vzdump ❌\n  ID 102: Quelldatei fehlt', body)
        self.assertNotIn('101', body)
        self.assertIsNone(self.store.report('general'))
        self.assertEqual(len(self.store.details(run)[0]['items']), 2)

    def test_health_is_not_a_fake_failed_backup_and_snapshot_survives_retry(self):
        self.store.health('docker02', 'unreachable')
        report = self.store.report()
        self.assertIn('Docker02 Abfrage ❌', report['body'])
        self.store.health('docker02', 'ok')
        retry = self.store.report()
        self.assertEqual(retry, report)
        self.assertIn('Host nicht erreichbar', retry['body'])

    def test_old_queued_report_is_reformatted_without_losing_acknowledgements(self):
        self.finish()
        report = self.store.report()
        self.assertTrue(self.store.claim(report['id'], 'mail'))
        self.store.delivered(report['id'], 'mail', True)
        self.assertTrue(self.store.claim(report['id'], 'telegram'))
        self.store.delivered(report['id'], 'telegram', False)
        legacy = '📋 Job-Zusammenfassung\nBericht: ' + report['id'] + '\n✅ 1 | ❌ 0 | ⚠️ 0 | ⏭️ 0\n✅ docker01.example.invalid / dockerbackup: success'
        self.store.db.execute('UPDATE reports SET body=? WHERE id=?', (legacy, report['id']))
        retry = self.store.report()
        self.assertEqual(retry['id'], report['id'])
        self.assertEqual(retry['body'], 'Job-Zusammenfassung\n\nDocker01 Backup ✅')
        self.assertFalse(self.store.claim(report['id'], 'mail'))
        self.assertTrue(self.store.claim(report['id'], 'telegram'))

    def test_labels_and_own_ansible_errors(self):
        run = self.store.begin('ansible:maintenance.yml', 'ansible')
        self.store.update(run, 'failed', 'Unreachable', item='example-node')
        self.store.update(run, 'failed', exit_code=1)
        body = self.store.report(reserve=False, labels={'hosts': {'docker01.example.invalid': 'Controller'}, 'jobs': {'ansible:maintenance.yml': 'Wartung'}})['body']
        self.assertIn('Controller Wartung ❌\n  example-node: Host nicht erreichbar.', body)

    def test_channels_keep_the_same_clean_body_mail_ascii_telegram_utf8(self):
        run = self.store.begin('backup')
        self.store.update(run, 'warning', 'Prüfung: Größe geändert', item='object')
        self.store.update(run, 'warning', exit_code=0)
        report = self.store.report(reserve=False)
        with patch.object(job_notify.shutil, 'which', return_value='/fixture/mail'), patch.object(job_notify.subprocess, 'run') as send:
            job_notify.deliver('mail', report, {'EMAIL': 'admin@example.invalid'}, LIB)
            arguments = send.call_args.args[0]
            self.assertNotIn(report['id'], ' '.join(arguments))
            self.assertTrue(send.call_args.kwargs['input'].isascii())
            self.assertIn(b'Pruefung: Groesse geaendert', send.call_args.kwargs['input'])
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b'{"ok":true}'
        with patch.object(job_notify.urllib.request, 'urlopen', return_value=response) as send:
            job_notify.deliver('telegram', report, {'BOT_TOKEN': '123:fixture', 'CHAT_ID': '-42'}, LIB)
            message = urllib.parse.parse_qs(send.call_args.args[0].data.decode())['text'][0]
            self.assertIn('⚠️', message)
            self.assertIn('Größe geändert', message)
            self.assertNotIn(report['id'], message)

    def test_missing_weekly_run_stays_in_its_separate_central_summary(self):
        self.store.health('pve.example.invalid/weekly', 'missing-expected-run', category='vzdump')
        self.assertIsNone(self.store.report('general', reserve=False))
        report = self.store.report('vzdump')
        self.assertIn('Pve Vzdump ❌\n  Der erwartete Lauf fehlt.', report['body'])
        self.store.claim(report['id'], 'telegram')
        self.store.delivered(report['id'], 'telegram', True)
        self.assertIsNone(self.store.report('vzdump'))
        self.store.health('pve.example.invalid/weekly', 'ok', category='vzdump')
        self.assertIsNone(self.store.report('vzdump'))
        self.store.health('pve.example.invalid/weekly', 'missing-expected-run', category='vzdump')
        self.assertIsNotNone(self.store.report('vzdump'))

    def test_jobs_run_with_no_controller_and_no_notification_channel(self):
        program = self.root / 'offline.sh'
        program.write_text('. "$FIXTURE_LIBRARY/lib/load.sh"\nhm_send_mail fixture fixture nobody\nhm_send_telegram fixture\nexit 0\n')
        fake = self.root / 'bin'
        fake.mkdir()
        marker = self.root / 'network-called'
        for name in ('mail', 'mailx', 'curl'):
            binary = fake / name
            binary.write_text('#!/bin/sh\ntouch "$FIXTURE_MARKER"\nexit 88\n')
            binary.chmod(0o700)
        cfg = self.root / 'config.json'
        cfg.write_text('{"BOT_TOKEN":"deliberately invalid","CHAT_ID":""}')
        cfg.chmod(0o600)
        env = dict(os.environ, PATH=str(fake) + os.pathsep + os.environ['PATH'], FIXTURE_LIBRARY=str(LIB), FIXTURE_MARKER=str(marker))
        for category in ('general', 'vzdump'):
            result = subprocess.run([sys.executable, str(LIB / 'bin/script-jobs'), '--db', str(self.store.path), 'run', '--job', 'offline-' + category,
                                     '--category', category, '--program', str(program), '--config', str(cfg)], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.store.runs(job='offline-' + category)[0]['status'], 'success')
        self.assertFalse(marker.exists())
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM reports').fetchone()[0], 0)

    def test_latest_shows_running_instead_of_old_success_and_executes_nothing(self):
        self.finish()
        current = self.store.begin('dockerbackup')
        other = self.finish('second-backup')
        rows = self.store.latest()
        self.assertEqual(len(rows), 2)
        self.assertEqual(next(row for row in rows if row['job'] == 'dockerbackup')['run_id'], current)
        self.assertEqual(self.store.latest('dockerbackup')[0]['status'], 'running')
        result = subprocess.run(['bash', str(LIB / 'bin/job-status'), '--db', str(self.store.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Docker01 Backup ⏳', result.stdout)
        self.assertNotIn(current, result.stdout)
        self.assertEqual(len(self.store.runs()), 3)
        missing = self.root / 'not-attached.db'
        result = subprocess.run(['bash', str(LIB / 'bin/job-status'), '--db', str(missing), '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 3)
        self.assertFalse(missing.exists())

    def test_host_filter_removes_only_notification_values(self):
        spec = importlib.util.spec_from_file_location('local_config', ROOT / 'roles/script_jobs/filter_plugins/local_config.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        data = {'BOT_TOKEN': 'fixture', 'CHAT_ID': '-1', 'MAIL_TO': 'admin@example.invalid', 'PBS_SECRET': 'backup-secret', 'PATHS_TO_BACKUP': ['/fixture']}
        filtered = module.local_job_config(data)
        self.assertEqual(filtered['BOT_TOKEN'], '')
        self.assertEqual(filtered['MAIL_TO'], '')
        self.assertFalse(filtered['ENABLE_EMAIL_NOTIFICATION'])
        self.assertEqual(filtered['PBS_SECRET'], 'backup-secret')
        self.assertEqual(data['BOT_TOKEN'], 'fixture')

    def test_outage_backlog_sends_only_one_summary_per_cycle(self):
        import runpy
        rows = [('docker01.example.invalid', self.store.epoch, 'queued-' + str(index), 'backup', 'general', 'success', index, index, index, 0, 'Completed') for index in range(2001)]
        self.store.db.executemany('INSERT INTO runs(source,epoch,run_id,job,category,status,started,activity,finished,exit_code,summary) VALUES(?,?,?,?,?,?,?,?,?,?,?)', rows)
        cfg = self.root / 'notify.json'
        cfg.write_text('{"EMAIL":"admin@example.invalid"}')
        cfg.chmod(0o600)
        notify = runpy.run_path(str(LIB / 'bin/script-jobs'))['notify']
        sent = []
        with patch.object(job_notify, 'deliver', side_effect=lambda channel, report, config, root: sent.append(report['body'])):
            self.assertEqual(notify(self.store, 'general', [str(cfg)]), 0)
            self.assertEqual(len(sent), 1)
            self.assertEqual(self.store.db.execute('SELECT count(*) FROM report_runs').fetchone()[0], 2000)
            self.assertIn('Ergebniszusammenfassung ⚠️', sent[0])
            self.assertEqual(sent[0].count('Docker01 Backup ✅'), 1)
            self.assertEqual(notify(self.store, 'general', [str(cfg)]), 0)
            self.assertEqual(len(sent), 2)
            self.assertEqual(self.store.db.execute('SELECT count(*) FROM report_runs').fetchone()[0], 2001)


if __name__ == '__main__':
    unittest.main(verbosity=2)
