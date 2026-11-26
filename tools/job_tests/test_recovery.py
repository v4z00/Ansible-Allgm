"""Crash, concurrent collection and old SQLite compatibility regressions."""
import concurrent.futures
import copy
import json
import os
from pathlib import Path
import runpy
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / 'artifacts/script-library'
sys.path.insert(0, str(LIB / 'lib/python'))
sys.path.insert(0, str(ROOT / 'scripts'))
from job_store import Store
import job_store
import job_notify
import job_console

notify = runpy.run_path(str(LIB / 'bin/script-jobs'))['notify']


class Recovery(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='job-recovery-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.store = Store(self.root / 'jobs.sqlite3', 'controller.example.invalid')
        self.addCleanup(self.store.close)
        self.config = self.root / 'notify.json'
        self.config.write_text(json.dumps({'EMAIL': 'admin@example.invalid',
                                          'BOT_TOKEN': '123:synthetic', 'CHAT_ID': '-42'}))
        self.config.chmod(0o600)

    def finish(self):
        run = self.store.begin('backup')
        self.store.update(run, 'success', exit_code=0)
        return run

    def test_crash_after_first_ack_keeps_other_channel_pending(self):
        self.finish()
        sent = []
        acknowledge = self.store.delivered

        def crash_after_mail(report, channel, ok):
            acknowledge(report, channel, ok)
            if channel == 'mail':
                raise KeyboardInterrupt('simulated process termination after mail ACK')

        with patch.object(job_notify, 'deliver', side_effect=lambda channel, *args: sent.append(channel)):
            with patch.object(self.store, 'delivered', side_effect=crash_after_mail):
                with self.assertRaises(KeyboardInterrupt):
                    notify(self.store, 'general', [str(self.config)])
            pending = self.store.report()
            self.assertIsNotNone(pending, 'Telegram must remain pending after the mail ACK')
            self.assertEqual(notify(self.store, 'general', [str(self.config)]), 0)
        self.assertEqual(sent, ['mail', 'telegram'])
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM reports').fetchone()[0], 1)
        self.assertIsNone(self.store.report())

    def test_parallel_senders_deliver_each_channel_once(self):
        self.finish()
        first_transport = threading.Event()
        release_transport = threading.Event()
        sent = []
        guard = threading.Lock()

        def deliver(channel, report, *args):
            with guard:
                sent.append((channel, report['id']))
            if channel == 'mail':
                first_transport.set()
                if not release_transport.wait(10):
                    raise RuntimeError('fixture did not release transport')

        def sender():
            state = Store(self.store.path)
            try:
                return notify(state, 'general', [str(self.config)])
            finally:
                state.close()

        with patch.object(job_notify, 'deliver', side_effect=deliver):
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                first = pool.submit(sender)
                self.assertTrue(first_transport.wait(10))
                try:
                    self.assertEqual({row[0] for row in self.store.db.execute('SELECT channel FROM deliveries')},
                                     {'mail', 'telegram'})
                    second = pool.submit(sender)
                    self.assertIn(second.result(timeout=10), (0, 75))
                finally:
                    release_transport.set()
                self.assertEqual(first.result(timeout=10), 0)
        self.assertCountEqual([channel for channel, _ in sent], ['mail', 'telegram'])
        self.assertEqual(len({report for _, report in sent}), 1)
        self.assertIsNone(self.store.report())

    def test_failed_transport_with_partial_spool_cannot_claim_complete_collection(self):
        project = self.root / 'project'
        project.mkdir()
        (project / 'ansible.cfg').touch()

        def incomplete_ansible(command, **kwargs):
            parameters = json.loads(Path(command[command.index('-e') + 1][1:]).read_text())
            spool = Path(parameters['job_spool'])
            (spool / 'alpha.json').write_text(json.dumps({'host': 'alpha', 'ok': True, 'data': {}}))
            return subprocess.CompletedProcess(command, 2, b'', b'synthetic second-host task failure')

        with patch.object(job_console.shutil, 'which', return_value='/fixture/ansible-playbook'), \
                patch.object(job_console.subprocess, 'run', side_effect=incomplete_ansible):
            with self.assertRaises(ValueError):
                job_console.transport(project, 'alpha,beta', {})
            result = job_console.collect(self.store, project, 'alpha,beta')
        self.assertEqual(result, [{'host': 'controller:collection', 'status': 'query-failed'}])
        self.assertEqual(self.store.runs(), [])
        self.assertEqual(self.store.cursor('alpha')['last_id'], 0)
        self.assertIn('Ergebnisabfrage ❌', self.store.report(reserve=False)['body'])

    def test_crashed_sender_is_reclaimed_after_lease_without_repeating_mail(self):
        self.finish()
        report = self.store.report(channels=['mail', 'telegram'])
        self.assertTrue(self.store.claim(report['id'], 'mail'))
        self.store.delivered(report['id'], 'mail', True)
        self.assertTrue(self.store.claim(report['id'], 'telegram'))
        self.assertFalse(self.store.claim(report['id'], 'telegram'))
        sent = []
        future = job_store.utc() + 301
        with patch.object(job_store, 'utc', return_value=future), \
                patch.object(job_notify, 'deliver', side_effect=lambda channel, *args: sent.append(channel)):
            self.assertEqual(notify(self.store, 'general', [str(self.config)]), 0)
        self.assertEqual(sent, ['telegram'])
        self.assertIsNone(self.store.report())

    def test_interrupted_batch_rolls_back_rows_and_cursor_together(self):
        run = self.finish()
        batch = self.store.export()
        malformed = copy.deepcopy(batch)
        malformed['events'][-1]['payload']['items'] = [
            {'item_id': 'object', 'status': 'invalid-state', 'message': '', 'updated': 1}]
        other = Store(self.root / 'collector.sqlite3')
        self.addCleanup(other.close)
        with self.assertRaises(ValueError):
            other.ingest('alpha', malformed)
        self.assertEqual(other.runs(), [])
        self.assertEqual(other.cursor('alpha'), {'epoch': None, 'last_id': 0})
        other.ingest('alpha', batch)
        self.assertEqual(other.runs()[0]['run_id'], run)
        self.assertEqual(other.cursor('alpha')['last_id'], batch['next'])

    def test_out_of_order_collectors_never_regress_success_or_cursor(self):
        run = self.finish()
        complete = self.store.export()
        older = copy.deepcopy(complete)
        older['events'] = older['events'][:1]
        older['next'] = older['events'][-1]['id']
        destination = self.root / 'collector.sqlite3'
        initial = Store(destination)
        initial.close()
        start = threading.Barrier(2)

        def collect(batch):
            state = Store(destination)
            try:
                start.wait(timeout=10)
                state.ingest('alpha', batch)
            finally:
                state.close()

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(collect, [complete, older]))
        state = Store(destination)
        self.addCleanup(state.close)
        self.assertEqual(state.cursor('alpha')['last_id'], complete['next'])
        self.assertEqual(len(state.runs()), 1)
        self.assertEqual(state.details(run)[0]['status'], 'success')

    def test_existing_database_without_new_table_or_duration_keeps_data_and_ack(self):
        path = self.root / 'old.sqlite3'
        db = sqlite3.connect(path)
        db.executescript('''
            CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
            INSERT INTO meta VALUES('schema','1'),('epoch','fixture-generation'),
                ('host','legacy.example.invalid'),('floor','0');
            CREATE TABLE runs(source TEXT NOT NULL,epoch TEXT NOT NULL,run_id TEXT NOT NULL,
                job TEXT NOT NULL,category TEXT NOT NULL,status TEXT NOT NULL,started REAL NOT NULL,
                activity REAL NOT NULL,finished REAL,exit_code INTEGER,summary TEXT NOT NULL DEFAULT '',
                PRIMARY KEY(source,epoch,run_id));
            INSERT INTO runs VALUES('legacy.example.invalid','fixture-generation','fixture-run',
                'backup','general','success',1,2,2,0,'Completed');
        ''')
        db.close()
        path.chmod(0o600)
        old = Store(path)
        report = old.report()
        old.claim(report['id'], 'mail')
        old.delivered(report['id'], 'mail', True)
        old.claim(report['id'], 'telegram')
        old.delivered(report['id'], 'telegram', False)
        old.close()
        reopened = Store(path)
        self.addCleanup(reopened.close)
        self.assertEqual(reopened.epoch, 'fixture-generation')
        self.assertEqual(reopened.latest()[0]['run_id'], 'fixture-run')
        self.assertIsNone(reopened.latest()[0]['duration_seconds'])
        self.assertEqual(reopened.report()['id'], report['id'])
        self.assertFalse(reopened.claim(report['id'], 'mail'))
        self.assertTrue(reopened.claim(report['id'], 'telegram'))
        self.assertEqual(reopened.db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_nonprivate_database_refused_before_program_execution(self):
        program = self.root / 'never-run.sh'
        marker = self.root / 'executed'
        program.write_text('touch "' + str(marker) + '"\n')
        self.store.path.chmod(0o644)
        result = subprocess.run([sys.executable, str(LIB / 'bin/script-jobs'), '--db',
                                 str(self.store.path), 'run', '--job', 'backup', '--program',
                                 str(program)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists())
        self.assertEqual(self.store.runs(), [])


@unittest.skipUnless(os.environ.get('ANSIBLE_JOBS_INTEGRATION') == '1', 'explicit local Ansible integration')
class TransportIntegration(unittest.TestCase):
    def test_real_partial_ansible_failure_cannot_report_green(self):
        with tempfile.TemporaryDirectory(prefix='partial-query-') as temporary:
            root = Path(temporary).resolve()
            project = root / 'controller'
            project.mkdir()
            hosts = {}
            for host in ('alpha', 'beta'):
                runtime = root / host
                shutil.copytree(LIB, runtime)
                database = root / (host + '-state/jobs.sqlite3')
                state = Store(database, host + '.example.invalid')
                run = state.begin('backup')
                state.update(run, 'success', exit_code=0)
                state.close()
                if host == 'beta':
                    (runtime / 'bin/script-jobs').write_text('print("not JSON: synthetic incompatible helper")\n')
                hosts[host] = {'ansible_connection': 'local', 'ansible_become': False,
                               'ansible_python_interpreter': sys.executable, 'script_jobs_python': sys.executable,
                               'script_jobs_target_root': str(runtime), 'script_jobs_database_path': str(database)}
            inventory = project / 'inventory.json'
            inventory.write_text(json.dumps({'all': {'children': {'all_linux_systems': {'hosts': hosts}}}}))
            (project / 'ansible.cfg').write_text('[defaults]\ninventory=' + str(inventory) +
                                               '\nlocal_tmp=' + str(root / 'local-tmp') +
                                               '\nremote_tmp=' + str(root / 'remote-tmp') + '\n')
            controller = Store(root / 'controller.sqlite3')
            try:
                result = job_console.collect(controller, project, 'alpha,beta')
                self.assertEqual(result, [{'host': 'controller:collection', 'status': 'query-failed'}])
                self.assertEqual(controller.runs(), [])
                self.assertIn('Ergebnisabfrage ❌', controller.report(reserve=False)['body'])
                shutil.copyfile(LIB / 'bin/script-jobs', root / 'beta/bin/script-jobs')
                recovered = job_console.collect(controller, project, 'alpha,beta')
                self.assertTrue(all(record['status'] == 'ok' for record in recovered))
                self.assertEqual({row['source'] for row in controller.runs()}, {'alpha', 'beta'})
                self.assertEqual(len(controller.runs()), 2)
                self.assertTrue(all(row['status'] == 'success' for row in controller.runs()))
                self.assertNotIn('Ergebnisabfrage ❌', controller.report(reserve=False)['body'])
            finally:
                controller.close()
            for host in hosts:
                state = Store(hosts[host]['script_jobs_database_path'])
                try:
                    self.assertEqual(len(state.runs()), 1)
                    self.assertEqual(state.runs()[0]['status'], 'success')
                finally:
                    state.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
