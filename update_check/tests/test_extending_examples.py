"""Validate the runnable guide in a source checkout.

Set CONTROLLER_TEST_EXTENDING_EXAMPLES=1 to exercise both guides using local Git
and disposable controllers. The guides themselves are repository-only.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


BASE = Path(__file__).resolve().parents[2]
GUIDES = ("EXTENDING.md", "EXTENDING.de.md")
SECTIONS = ("setup", "A", "B", "C", "D")
BLOCK = re.compile(r"^<!-- example: (\w+) -->\n\s*```bash\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


def examples(name):
    return [(m[1], m[2]) for m in BLOCK.finditer((BASE / name).read_text(encoding="utf-8"))]


@unittest.skipUnless((BASE / ".git").exists(), "developer guides are repository-only")
class ExtendingGuideTests(unittest.TestCase):
    def test_sections_have_matching_executable_examples(self):
        guides = [examples(name) for name in GUIDES]
        self.assertEqual(guides[0], guides[1], "English and German commands differ")
        self.assertEqual(tuple(label for label, _ in guides[0]), SECTIONS)
        for label, block in guides[0]:
            with self.subTest(section=label):
                result = subprocess.run(["bash", "-n"], input=block, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.environ.get("CONTROLLER_TEST_EXTENDING_EXAMPLES") == "1",
                         "set CONTROLLER_TEST_EXTENDING_EXAMPLES=1 for local end-to-end exercises")
    def test_examples_on_disposable_controllers(self):
        for guide in GUIDES:
            with self.subTest(guide=guide), tempfile.TemporaryDirectory() as tmp:
                self.run_guide(guide, Path(tmp).resolve())

    def run_guide(self, guide, work):
        home = work / "home"
        temporary = work / "temp"
        home.mkdir()
        temporary.mkdir()
        source = work / "source"
        # Start from the committed base. Only copy tracked source through Git.
        # Nested test discovery in recipe D must not re-enter this end-to-end test.
        env = {"HOME": str(home), "TMPDIR": str(temporary),
               "PATH": os.pathsep.join([str(Path(sys.executable).parent), os.environ["PATH"]]),
               "LANG": "C", "LC_ALL": "C", "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
               "CONTROLLER_PYTHON": sys.executable,
               "GIT_AUTHOR_NAME": "Guide Test", "GIT_AUTHOR_EMAIL": "guide@example.invalid",
               "GIT_COMMITTER_NAME": "Guide Test", "GIT_COMMITTER_EMAIL": "guide@example.invalid",
               "GIT_ALLOW_PROTOCOL": "file", "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_GLOBAL": str(home / ".gitconfig"),
               "ANSIBLE_LOCAL_TEMP": str(temporary / "ansible-local"),
               "ANSIBLE_REMOTE_TEMP": str(temporary / "ansible-remote")}
        if os.environ.get("ANSIBLE_COLLECTIONS_PATH"):
            env["ANSIBLE_COLLECTIONS_PATH"] = os.environ["ANSIBLE_COLLECTIONS_PATH"]
        shims = work / "bin"
        shims.mkdir()
        git = shims / "git"
        # The HTTPS helper resets its own Git environment. Enforce file-only transport
        # also in subprocesses that deliberately clear inherited Git settings.
        git.write_text('#!/bin/sh\nGIT_ALLOW_PROTOCOL=file exec ' + shlex.quote(shutil.which("git")) + ' "$@"\n')
        git.chmod(0o700)
        env["PATH"] = str(shims) + os.pathsep + env["PATH"]
        fixture = Path(os.environ.get("CONTROLLER_TEST_GUIDE_BASE", BASE)).resolve()
        subprocess.run(["git", "clone", "--no-local", "--quiet", str(fixture), str(source)], env=env, check=True)
        subprocess.run(["git", "remote", "set-url", "origin", "https://github.com/example/Ansible-Allgm.git"],
                       cwd=source, env=env, check=True)
        blocks = examples(guide)
        self.assertEqual(tuple(label for label, _ in blocks), SECTIONS)
        script = "set -euo pipefail\n" + "\n".join(block for _, block in blocks)
        result = subprocess.run(["bash"], input=script, cwd=source, env=env,
                                text=True, capture_output=True, timeout=600)
        self.assertEqual(result.returncode, 0, result.stdout[-4000:] + result.stderr[-4000:])
        labs = list(temporary.glob("*/heartbeat-audit.json"))
        self.assertEqual(len(labs), 1)
        lab = labs[0].parent
        target = lab / "controller"
        extension, = json.loads(labs[0].read_text())["extensions"]
        self.assertEqual((extension["id"], extension["status"]), ("addon-heartbeat", "OK"))
        self.check_feature(target, env)
        self.check_local_archive(target)
        self.check_addon_rollback(lab, target, env)
        self.check_local_archive(target)

    def launch(self, cwd, env, args, *, ok=True, stdin=None):
        result = subprocess.run(args, cwd=cwd, env=env, input=stdin, capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode == 0, ok, f"{args}\n{result.stdout}\n{result.stderr}")
        return result.stdout

    def check_feature(self, target, env):
        settings = target / "group_vars/all/settings.yml"
        data = yaml.safe_load(settings.read_text())
        control = target / "bin/control"
        data["features"]["demo_hello"] = False
        settings.write_text(yaml.safe_dump(data))
        self.assertNotIn("Hello!", self.launch(target, env, [control, "--lang", "en", "demo-hello"], ok=False))
        data["features"]["demo_hello"] = True
        settings.write_text(yaml.safe_dump(data))
        for language, message in [("en", "Hello!"), ("de", "Hallo!")]:
            self.assertEqual(self.launch(target, env, [control, "--lang", language, "demo-hello"]).strip(), message)

    def check_local_archive(self, target):
        local = target.with_name(target.name + "-local")
        register = json.loads((local / "register.json").read_text())
        self.assertEqual(register["schema"], 2)
        records = register["files"]
        keep, = (path for path, row in records.items() if "supplement" not in row)
        self.assertTrue((local / "code" / keep).is_file())
        once, = (path for path, row in records.items() if row.get("supplement") == "once")
        entry = records[once]
        archive = local / "archiv" / entry["archive"]
        self.assertFalse((local / "code" / once).exists())
        observed = hashlib.sha256((archive / "datei").read_bytes()).hexdigest()
        proof = json.loads((archive / "BELEG.json").read_text())
        run = json.loads((local / "runs" / (once + ".json")).read_text())
        self.assertEqual(entry["sha256"], observed)
        self.assertEqual((proof["approved_sha256"], proof["archived_sha256"], proof["run"]), (observed, observed, run))
        self.assertEqual((run["path"], run["sha256"], run["exit_code"]), (once, observed, 0))
        self.assertEqual((archive / "SHA256SUMS").read_text().split(), [observed, "datei"])

    def check_addon_rollback(self, lab, target, env):
        addon = lab / "heartbeat"
        base = lab / "base"
        cli = [sys.executable, ".githooks/staging_manifest.py", "addon-verify", "Heartbeat"]
        receipt = target / ".controller-install.json"
        versions = target / "versions.txt"
        before = (receipt.read_bytes(), versions.read_bytes())
        meta = json.loads(before[0])
        self.assertEqual(meta["owners"]["playbooks/heartbeat/check.yml"], "Heartbeat")
        self.assertEqual(set(meta["modules"]), {"Allgm", "Heartbeat"})
        # Revision two adds a file. Its stale seal must be rejected before the hook rebuilds it.
        desc = addon / "controller-addon.json"
        doc = json.loads(desc.read_text())
        doc["payload"].append("extra.yml")
        desc.write_text(json.dumps(doc) + "\n")
        (addon / "extra.yml").write_text("---\n[]\n")
        (addon / "VERSION.txt").write_text("0.2.0\n")
        self.launch(addon, env, ["git", "add", "--", "VERSION.txt", desc.name, "extra.yml"])
        self.launch(addon, env, [*cli, ":index"], ok=False)
        self.launch(addon, env, [*cli, "HEAD"])
        tree = self.launch(addon, env, ["git", "write-tree"]).strip()
        unsealed = self.launch(addon, env, ["git", "commit-tree", tree, "-p", "HEAD", "-m", "Unsealed fixture"]).strip()
        self.launch(addon, env, [".githooks/pre-push"], ok=False,
                    stdin=f"refs/heads/staging {unsealed} refs/heads/staging {'0' * 40}\n")
        self.launch(addon, env, ["git", "commit", "-qm", "Add rollback example"])
        self.launch(addon, env, [*cli, "HEAD"])
        installer = [base / "bin/install-controller", "--target", target, "--skip-runtime", "--addon", addon,
                     "--addon-url", "Heartbeat=https://github.com/example/Ansible-Heartbeat.git", "--update"]
        preview = self.launch(base, env, installer)
        plan = re.search(r"--apply ([0-9a-f]{64})", preview)
        self.assertIsNotNone(plan, preview)
        self.launch(base, env, [*installer, "--apply", plan[1]])
        mounted = target / "playbooks/heartbeat/extra.yml"
        self.assertEqual(mounted.read_bytes(), (addon / "extra.yml").read_bytes())
        backup, = (target / ".local/controller-updates").iterdir()
        self.launch(target, env, [target / "bin/control", "update-check", "--rollback", backup.name])
        self.assertFalse(mounted.exists())
        self.assertEqual((receipt.read_bytes(), versions.read_bytes()), before)


class InstallerSourceTests(unittest.TestCase):
    def test_checkout_traversal_preserves_public_files_and_skips_private_directories(self):
        from unittest.mock import patch
        sys.path.insert(0, str(BASE / "tools"))
        try:
            import install_controller as install
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public = {"README.md", "configure_server_BASE.sh", "scripts/entry.sh",
                      "bin/control.d/.versions/feature.json", "examples/inventory/test.example.yml",
                      "artifacts/script-library/lib/common/example.sh",
                      "artifacts/script-library/lib/data/mail-translations.json"}
            private = {".git/objects", "host_vars/group", "config/host_vars", "roles/local/.git",
                       "artifacts/private", "artifacts/script-library/lib/private"}
            for rel in public:
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text("fixture")
            for rel in private:
                (root / rel).mkdir(parents=True)
            visited = []
            contents = Path.iterdir

            def visit(path):
                visited.append(path.relative_to(root).as_posix())
                return contents(path)

            with patch.object(Path, "iterdir", visit):
                self.assertEqual(set(install.code_files(root)), public)
            for path in visited:
                self.assertFalse(any(path == rel or path.startswith(rel + "/") for rel in private), path)
            self.assertEqual(set(install.code_files(root, overlay=True)),
                             {p for p in public if not p.startswith("artifacts/") and p != "README.md"})
            (root / "scripts/link").symlink_to(root / "host_vars")
            with self.assertRaisesRegex(ValueError, "Link"):
                install.code_files(root)
            (root / "scripts/link").unlink()
            os.mkfifo(root / "scripts/pipe")
            with self.assertRaisesRegex(ValueError, "Sonderdatei"):
                install.code_files(root)

    def test_real_consumer_glob_rejects_local_archiving(self):
        sys.path.insert(0, str(BASE / "update_check"))
        try:
            import cleanup
        finally:
            sys.path.pop(0)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            caller = root / "scripts" / "consumer.py"
            caller.parent.mkdir()
            caller.write_text("jobs = (root / 'scripts').glob('site-*.sh')\n")
            sources, errors = cleanup.scan_sources(root, external=False)
            self.assertEqual(errors, [])
            self.assertEqual(cleanup.dependencies(root, "scripts/site-example.sh", sources), ["scripts/consumer.py"])
