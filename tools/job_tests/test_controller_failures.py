"""Controller selection failures are queued without an immediate notification."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'artifacts/script-library/lib/python'))
from job_store import Store


class ControllerFailures(unittest.TestCase):
    def exercise(self, name, arguments, expected_job):
        with tempfile.TemporaryDirectory(prefix='controller-failure-') as temporary:
            root = Path(temporary)
            (root / 'scripts').mkdir()
            shutil.copyfile(ROOT / 'scripts' / name, root / 'scripts' / name)
            (root / 'lib/control').mkdir(parents=True)
            shutil.copyfile(ROOT / 'lib/control/helpers.sh', root / 'lib/control/helpers.sh')
            shutil.copytree(ROOT / 'artifacts/script-library', root / 'artifacts/script-library')
            (root / 'config').mkdir()
            database = root / 'controller.db'
            (root / 'config/script_jobs_controller.json').write_text(json.dumps({'database': str(database)}))
            for rel in ('playbooks/maintenance/update_hosts.yaml', 'playbooks/maintenance/notify.yml', 'ansible.cfg'):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            fake = root / 'bin'
            fake.mkdir()
            (fake / 'ansible-playbook').write_text('#!/bin/sh\necho "$*" >> "$TRACE"\nprintf "  hosts (0):\\n"\n')
            (fake / 'flock').write_text('#!/bin/sh\nexit 0\n')
            for file in fake.iterdir():
                file.chmod(0o700)
            trace = root / 'trace'
            env = dict(os.environ, PATH=str(fake) + os.pathsep + str(Path(sys.executable).parent) + os.pathsep + os.environ['PATH'], TRACE=str(trace))
            result = subprocess.run(['bash', str(root / 'scripts' / name), *arguments], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertNotIn('notify.yml', trace.read_text())
            state = Store(database)
            rows = state.runs()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['job'], expected_job)
            self.assertEqual(rows[0]['status'], 'failed')
            self.assertIn('❌', state.report(reserve=False)['body'])
            state.close()

    def test_host_update_precheck_failure_is_queued(self):
        self.exercise('run_host_updates.sh', ['--limit', 'fixture'], 'ansible:host-updates')

    def test_docker_update_precheck_failure_is_queued(self):
        self.exercise('run_docker_update.sh', ['--limit', 'fixture'], 'ansible:docker-update')


if __name__ == '__main__':
    unittest.main(verbosity=2)
