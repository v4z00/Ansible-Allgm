"""Systemd observations preserve service ownership and exclude credential data."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
LIB = ROOT / 'artifacts/script-library'
sys.path.insert(0, str(LIB / 'lib/python'))
sys.path.insert(0, str(ROOT / 'scripts'))
from job_store import Systemd as job_systemd
from job_store import Store


def properties(**overrides):
    return {'LoadState': 'loaded', 'ActiveState': 'active', 'SubState': 'running',
            'Type': 'simple', 'Result': 'success', 'ExecMainCode': '0', 'ExecMainStatus': '0',
            'ExecMainStartTimestampMonotonic': '1000',
            'ExecMainExitTimestampMonotonic': '0', **overrides}


class SystemdStatus(unittest.TestCase):
    def test_profile_selection_is_explicit_and_rejects_unknown_or_overlapping_units(self):
        profiles = {'base': [{'unit': 'fixture.service', 'mode': 'active'}],
                    'optional': [{'unit': 'optional.service', 'mode': 'observe'}]}
        self.assertEqual(job_systemd.resolve_profiles(profiles, []), [])
        self.assertEqual([r['unit'] for r in job_systemd.resolve_profiles(profiles, ['base'])], ['fixture.service'])
        for selected in (['missing'], ['base', 'base']):
            with self.assertRaises(ValueError):job_systemd.resolve_profiles(profiles, selected)
        with self.assertRaises(ValueError):job_systemd.resolve_profiles({'a': profiles['base'], 'b': profiles['base']}, ['a', 'b'])
    def test_modes_do_not_invent_a_completed_oneshot_or_treat_inactive_as_success(self):
        daemon = {'unit': 'fixture.service', 'mode': 'active'}
        one = {**daemon, 'mode': 'oneshot'}
        self.assertEqual(job_systemd.assess(daemon, properties())[0], 'success')
        self.assertEqual(job_systemd.assess(daemon, properties(ActiveState='inactive'))[0], 'failed')
        self.assertEqual(job_systemd.assess({**daemon, 'mode': 'observe'}, properties(ActiveState='inactive'))[0], 'skipped')
        self.assertEqual(job_systemd.assess(one, properties(Type='oneshot', ActiveState='inactive', ExecMainStartTimestampMonotonic='0'))[0], 'skipped')
        self.assertEqual(job_systemd.assess(one, properties(Type='oneshot', ActiveState='inactive', ExecMainCode='1', ExecMainStatus='0', ExecMainExitTimestampMonotonic='2000'))[0], 'success')
        for change in ({'Result': 'exit-code'}, {'LoadState': 'not-found'}, {'ActiveState': 'failed'}):
            self.assertEqual(job_systemd.assess(daemon, properties(**change))[0], 'failed')
        self.assertEqual(job_systemd.assess(daemon, properties(ActiveState='activating'))[0], 'warning')
        self.assertEqual(job_systemd.assess(one, properties(Type='oneshot', ExecMainCode='n/a'))[0], 'warning')

    def test_validation_rejects_templates_options_payloads_and_duplicate_names(self):
        for unit in ('--all', '../fixture.service', 'fixture@.service', 'fixture.service\nother.service'):
            with self.assertRaises(ValueError):job_systemd.normalize([{'unit': unit, 'mode': 'active'}])
        for entries in ([{'unit': 'fixture.service'}], [{'unit': 'fixture.service', 'mode': 'active', 'token': 'no'}],
                        [{'unit': 'a.service', 'mode': 'active', 'name': 'same'}, {'unit': 'b.service', 'mode': 'active', 'name': 'same'}]):
            with self.assertRaises(ValueError):job_systemd.normalize(entries)
        self.assertEqual(job_systemd.normalize([{'unit': 'fixture@one.service', 'mode': 'active'}])[0]['unit'], 'fixture@one.service')

    def test_only_status_properties_are_queried_and_unknown_output_is_discarded(self):
        secret = 'synthetic_NEVER_EXPORT'
        text = '\n'.join(key + '=' + value for key, value in properties().items())
        text += '\nEnvironment=BOT_TOKEN=' + secret + '\nExecStart=' + secret + '\nDescription=' + secret
        with patch.object(job_systemd.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, text, secret)) as run:
            rows = job_systemd.observe([{'unit': 'fixture.service', 'mode': 'active'}])
        self.assertEqual(rows[0]['status'], 'success')
        self.assertNotIn(secret, json.dumps(rows))
        args = run.call_args.args[0]
        self.assertEqual(args[1:4], ['--no-pager', 'show', 'fixture.service'])
        queried = args[-1].split('=', 1)[1].split(',')
        self.assertEqual(tuple(queried), job_systemd.PROPERTIES)
        for forbidden in ('Environment', 'ExecStart', 'Description', 'Credential'):
            self.assertFalse(any(value.startswith(forbidden) for value in queried))
        with patch.object(job_systemd.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, secret, secret)):
            failed = job_systemd.observe([{'unit': 'fixture.service', 'mode': 'active'}])
        self.assertEqual(failed[0]['status'], 'failed')
        self.assertNotIn(secret, json.dumps(failed))

    def test_snapshot_transaction_is_idempotent_per_collection_and_streams_normally(self):
        with tempfile.TemporaryDirectory() as td:
            state = Store(Path(td) / 'host/jobs.db', 'alpha')
            controller = Store(Path(td) / 'controller/jobs.db', 'controller')
            binding = [{'unit': 'fixture.service', 'mode': 'active'}]
            sample = str(uuid.uuid4())
            with patch.object(job_systemd, 'observe', return_value=[{**binding[0], 'name': 'systemd:fixture', 'status': 'success', 'summary': 'Systemd-Dienst zum Abfragezeitpunkt aktiv.'}]):
                job_systemd.record(state, binding, sample)
                job_systemd.record(state, binding, sample)
            self.assertEqual(len(state.runs()), 1)
            batch = state.export()
            self.assertEqual(len(batch['events']), 1)
            controller.ingest('alpha', batch)
            self.assertIsNone(controller.report(reserve=False))
            self.assertEqual(controller.latest()[0]['status'], 'success')
            state.close(); controller.close()

    def test_status_query_does_not_create_database_and_record_requires_existing_store(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)
            cfg = path / 'systemd.json';cfg.write_text('[]');cfg.chmod(0o600)
            db = path / 'missing/jobs.db'
            base = [sys.executable, str(LIB / 'bin/script-jobs'), '--db', str(db)]
            result = subprocess.run(base + ['systemd-status', '--config', str(cfg)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertFalse(db.exists())
            result = subprocess.run(base + ['systemd-record', '--config', str(cfg), '--sample', str(uuid.uuid4())], capture_output=True, text=True)
            self.assertEqual(result.returncode, 3)
            self.assertFalse(db.exists())


@unittest.skipUnless(os.environ.get('ANSIBLE_JOBS_INTEGRATION') == '1', 'explicit local Ansible integration')
class SystemdCollection(unittest.TestCase):
    def test_real_ansible_collects_unit_observation_into_existing_summary(self):
        import job_console
        with tempfile.TemporaryDirectory(prefix='systemd-collect-') as td:
            root = Path(td).resolve()
            runtime = root / 'runtime';shutil.copytree(LIB, runtime)
            fake = root / 'systemctl-fixture'
            fake.write_text('#!' + sys.executable + '\nimport sys\nassert sys.argv[1:4]==["--no-pager","show","fixture.service"]\nprint(' + repr('\n'.join(k + '=' + v for k, v in properties().items()) + '\nEnvironment=BOT_TOKEN=synthetic_NEVER_EXPORT') + ')\n')
            fake.chmod(0o700)
            module = runtime / 'lib/python/job_store.py'
            module.write_text(module.read_text().replace("'/usr/bin/systemctl'", repr(str(fake))))
            db = root / 'host-state/jobs.db';state = Store(db, 'alpha');state.close()
            config = db.parent / 'systemd.json'
            config.write_text(json.dumps([{'unit': 'fixture.service', 'mode': 'active'}]));config.chmod(0o600)
            inventory = {'all': {'hosts': {'alpha': {'ansible_connection': 'local', 'ansible_become': False,
                         'ansible_python_interpreter': sys.executable, 'script_jobs_python': sys.executable,
                         'script_jobs_target_root': str(runtime), 'script_jobs_database_path': str(db),
                         'script_jobs_systemd_profiles': {'watcher': [{'unit': 'fixture.service', 'mode': 'active'}]},
                         'script_jobs_systemd_selected_profiles': ['watcher']}}}}
            (root / 'inventory.json').write_text(json.dumps(inventory))
            (root / 'ansible.cfg').write_text('[defaults]\ninventory=' + str(root / 'inventory.json') + '\nlocal_tmp=' + str(root / 'tmp') + '\nremote_tmp=' + str(root / 'remote-tmp') + '\n')
            controller = Store(root / 'controller/jobs.db', 'controller')
            rows = job_console.collect(controller, root, 'alpha')
            self.assertTrue(all(row['status'] == 'ok' for row in rows), rows)
            self.assertIsNone(controller.report(reserve=False))
            self.assertEqual(controller.latest()[0]['status'], 'success')
            self.assertNotIn('synthetic_NEVER_EXPORT', json.dumps(controller.export()) + str(rows))
            # A stale deployed profile must block an old green import.
            config.write_text('[]')
            rows = job_console.collect(controller, root, 'alpha')
            self.assertTrue(any(row['status'] != 'ok' for row in rows))
            self.assertIn('Alpha Abfrage ❌', controller.report(reserve=False)['body'])
            controller.close()


if __name__ == '__main__':unittest.main(verbosity=2)
