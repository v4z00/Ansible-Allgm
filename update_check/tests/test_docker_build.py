"""Run the real Compose task graphs against an isolated recording CLI."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

BASE = Path(__file__).resolve().parents[2]
ANSIBLE = shutil.which('ansible-playbook')


@unittest.skipUnless(ANSIBLE, 'ansible-playbook required')
class ComposeBuildTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.trace = self.root / 'trace.jsonl'
        fakebin = self.root / 'bin'
        fakebin.mkdir()
        docker = fakebin / 'docker'
        docker.write_text('#!' + sys.executable + '''
import json,os,sys
from pathlib import Path
root=Path(os.environ['COMPOSE_TEST_ROOT'])
args=sys.argv[1:]
with (root/'trace.jsonl').open('a') as out:
 out.write(json.dumps({'args':args,'cwd':os.getcwd(),'parallel':os.environ.get('COMPOSE_PARALLEL_LIMIT')})+'\\n')
if 'pull' in args:
 counter=root/'attempts';n=int(counter.read_text())+1 if counter.exists() else 1;counter.write_text(str(n))
 if os.environ.get('PULL_TEST_MODE')=='permanent' or (os.environ.get('PULL_TEST_MODE')=='retry' and n<3):
  print('TLS handshake timeout',file=sys.stderr);sys.exit(1)
if 'up' in args:print('Recreated',file=sys.stderr)
''')
        docker.chmod(0o700)
        self.inventory = self.root / 'inventory.ini'
        self.inventory.write_text('[docker_deployment_hosts]\nfixture ansible_connection=local\n')
        (self.root / 'ansible.cfg').write_text('[defaults]\n')
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(('ANSIBLE_', 'CONTROLLER_'))}
        self.env.update(PATH=str(fakebin) + os.pathsep + os.environ['PATH'],
                        COMPOSE_TEST_ROOT=str(self.root), SCRIPT_JOBS_CALLBACK='0',
                        ANSIBLE_CONFIG=str(self.root / 'ansible.cfg'),
                        ANSIBLE_LOCAL_TEMP=str(self.root / 'local'),
                        ANSIBLE_REMOTE_TEMP=str(self.root / 'remote'), ANSIBLE_NOCOLOR='1')
        self.compose = self.root / "team's files" / 'compose $HOME special.yaml'
        self.compose.parent.mkdir()
        self.compose.write_text('services: {}\n')

    def run_tasks(self, tasks, variables=None, env=None):
        play = self.root / 'play.json'
        values = {'ansible_become': False, 'ansible_python_interpreter': sys.executable,
                  'compose_files': {'files': [{'path': str(self.compose)}]},
                  **(variables or {})}
        if 'all_compose_projects' in values:
            tasks = [{'ansible.builtin.set_fact': {'all_compose_projects': values['all_compose_projects']}}] + tasks
        play.write_text(json.dumps([{'hosts': 'docker_deployment_hosts', 'gather_facts': False,
                                    'vars': values, 'tasks': tasks}]))
        result = subprocess.run([ANSIBLE, '-i', str(self.inventory), str(play)], cwd=self.root,
                                env={**self.env, **(env or {})}, capture_output=True, text=True, timeout=45)
        calls = [json.loads(line) for line in self.trace.read_text().splitlines()] if self.trace.exists() else []
        return result, calls

    def update_tasks(self):
        tasks = yaml.safe_load((BASE / 'playbooks/docker/update_containers.yml').read_text())[0]['tasks']
        selected = [task for task in tasks if task['name'].startswith(
            ('Pull registry images', 'Build locally defined', 'Update containers and wait'))]
        self.assertEqual(len(selected), 3)
        selected[0]['delay'] = 0
        return selected

    def test_update_retries_pull_then_builds_before_starting_with_health_checks(self):
        result, calls = self.run_tasks(self.update_tasks(), env={'PULL_TEST_MODE': 'retry'})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(sum('pull' in c['args'] for c in calls), 3)
        self.assertIn('build', calls[-2]['args'])
        self.assertIn('--pull', calls[-2]['args'])
        up = calls[-1]['args']
        for flag in ('up', '--no-build', '--wait', '--wait-timeout'):
            self.assertIn(flag, up)
        self.assertEqual(up[up.index('--pull') + 1], 'never')
        for call in calls[:3]:
            self.assertIn('--ignore-buildable', call['args'])
            self.assertEqual(call['parallel'], '1')
        self.assertTrue(all(c['cwd'] == str(self.compose.parent) for c in calls))
        self.assertTrue(all(c['args'][c['args'].index('--file') + 1] == str(self.compose) for c in calls))

    def test_permanent_pull_failure_never_builds_or_changes_containers(self):
        tasks = self.update_tasks()
        tasks[0]['retries'] = 2
        result, calls = self.run_tasks(tasks, env={'PULL_TEST_MODE': 'permanent'})
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(calls)
        self.assertTrue(all('pull' in c['args'] for c in calls))
        self.assertLessEqual(len(calls), 4)

    def test_update_can_keep_locally_managed_images_without_implicit_build(self):
        result, calls = self.run_tasks(self.update_tasks(), {'docker_compose_build': False})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(any('build' in c['args'] for c in calls))
        self.assertIn('--no-build', calls[-1]['args'])

    def test_push_builds_critical_then_standard_stacks_and_honors_opt_out(self):
        deployment = yaml.safe_load((BASE / 'playbooks/docker/deploy_docker_stacks.yml').read_text())
        stage = next(p for p in deployment if p['name'].startswith('PLAY 6:'))
        tasks = [task for task in stage['tasks'] if not task['name'].startswith('TASK 6.4:')]
        critical = self.root / 'critical' / 'compose.yml'
        critical.parent.mkdir()
        critical.write_text('services: {}\n')
        for enabled in (True, False):
            with self.subTest(build=enabled):
                self.trace.unlink(missing_ok=True)
                result, calls = self.run_tasks(tasks, {
                    'all_compose_projects': {'files': [{'path': str(self.compose)}, {'path': str(critical)}]},
                    'critical_stacks': ['critical'], 'docker_compose_build': enabled,
                    'deployment_results': [],
                })
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual([c['args'][c['args'].index('--file') + 1] for c in calls],
                                 [str(critical), str(self.compose)])
                self.assertTrue(all(('--build' if enabled else '--no-build') in c['args'] for c in calls))


if __name__ == '__main__':
    unittest.main()
