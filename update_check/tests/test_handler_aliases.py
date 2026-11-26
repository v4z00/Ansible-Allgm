"""Run legacy and current notifications against a harmless SSH handler fixture."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml


@unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook required")
class HandlerAliasTest(unittest.TestCase):
    def test_both_spellings_notify_the_same_handler(self):
        source = Path(__file__).resolve().parents[2] / "roles/security_ssh/handlers/main.yml"
        original, = yaml.safe_load(source.read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            handlers = root / "roles/security_ssh/handlers"
            handlers.mkdir(parents=True)
            # Use the real dispatch metadata. The fixture action just increments a fact.
            replacement = {"name": original["name"], "listen": original["listen"],
                           "ansible.builtin.set_fact": {"runs": "{{ runs | int + 1 }}"}}
            (handlers / "main.yml").write_text(yaml.safe_dump([replacement]))
            tasks = []
            for count, name in enumerate(("SSH neu starten", "Restart SSH", "security_ssh : SSH neu starten"), 1):
                tasks += [
                    {"name": "Notify " + name, "ansible.builtin.debug": {"msg": "test"},
                     "changed_when": True, "notify": name},
                    {"ansible.builtin.meta": "flush_handlers"},
                    {"ansible.builtin.assert": {"that": f"runs | int == {count}"}},
                ]
            play = {"hosts": "localhost", "connection": "local", "gather_facts": False,
                    "roles": ["security_ssh"], "vars": {"runs": 0}, "tasks": tasks}
            (root / "play.yml").write_text(yaml.safe_dump([play]))
            (root / "ansible.cfg").write_text("[defaults]\n")
            env = dict(os.environ, ANSIBLE_CONFIG=str(root / "ansible.cfg"),
                       ANSIBLE_LOCAL_TEMP=str(root / "local-tmp"), ANSIBLE_ROLES_PATH=str(root / "roles"))
            result = subprocess.run(["ansible-playbook", "-i", "localhost,", "play.yml"], env=env,
                                    cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
