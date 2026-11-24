"""Exercise manual channel changes on disposable Git repositories."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "update_check"))
import rollout


class BranchTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name).resolve()
        self.controller = self.work / "controller"
        self.controller.mkdir()
        settings = self.controller / "group_vars/all/settings.yml"
        settings.parent.mkdir(parents=True)
        settings.write_text("features: {}\n")
        self.remote = self.work / "remote"
        self.remote.mkdir()
        self.git("init", "-q", "-b", "main")
        cmd = json.loads((BASE / "bin/control.d/update-check.json").read_text())["commands"][0]
        for rel in (*cmd["requires"], "bin/control", "bin/control.d/update-check.json", "bin/control.d/update-check.sh",
                    "lib/controller_environment.sh", "scripts/control_runtime.py",
                    "tools/github_https.py", "tools/install_controller.py",
                    "update_check/check.sh", "update_check/check.py", "update_check/rollout.py",
                    "update_check/local_extensions.py", "update_check/staging_manifest.py"):
            dest = self.remote / rel
            dest.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy2(BASE / rel, dest)
        self.file("VERSION.txt", "1.2.3\n")
        self.file("update_check/settings_contract.json", '{"fields": []}')
        self.file("update_check/release.json", '{"feature_defaults": {}}')
        self.file("scripts/main-only.sh", "main\n")
        self.commit()
        self.git("switch", "-qc", "staging")
        (self.remote / "scripts/main-only.sh").unlink()
        self.file("scripts/staging-only.sh", "staging\n")
        self.commit()
        # Route the expected test URL to the fixture while running real Git clones.
        real_git = shlex.quote(shutil.which("git"))
        shim = self.work / "test-bin"
        shim.mkdir()
        script = shim / "git"
        script.write_text(
            "#!/bin/bash\nargs=()\n"
            "for arg in \"$@\"; do\n"
            "  case \"$arg\" in\n"
            "    https://github.com/example/fixture.git) arg=" + shlex.quote(str(self.remote)) + ";;\n"
            "    https://github.com/example/overlay.git) arg=" + shlex.quote(str(self.work / "overlay")) + ";;\n"
            "    https://*) exit 90;;\n"
            "  esac\n  args+=(\"$arg\")\ndone\n"
            "GIT_ALLOW_PROTOCOL=file exec " + real_git + " \"${args[@]}\"\n")
        script.chmod(0o755)
        interpreter = shim / "python3"
        interpreter.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + ' "$@"\n')
        interpreter.chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.work), PATH=str(shim) + os.pathsep + os.defpath,
                        PYTHONDONTWRITEBYTECODE="1")
        self.git("switch", "-q", "main")
        for rel in rollout.manifest.verify(self.remote, "Allgm"):
            dest = self.controller / rel
            dest.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy2(self.remote / rel, dest)
        self.marker = self.controller / "versions.txt"
        self.marker.write_text("Allgm|1.2.3|https://github.com/example/fixture.git|\n"
                               "# lokal\nZusatz|4.5.6|https://github.com/example/other.git|/local/token\n")
        self.marker.chmod(0o600)
        baseline = {k: v["sha256"] for k, v in rollout.manifest.verify(self.remote, "Allgm").items()}
        rollout.install.write_receipt(self.controller, "allgm", baseline, "main")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.remote), "-c", "user.name=Tests",
                               "-c", "user.email=tests@example.invalid", *args],
                              check=True, capture_output=True)

    def file(self, name, text):
        (self.remote / name).write_text(text)

    def commit(self, profile="Allgm"):
        self.git("add", "-A")
        data = rollout.manifest.create(self.remote, profile, ":index")
        self.file("SHA256SUMS.json", json.dumps(data))
        self.git("add", "SHA256SUMS.json")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "test fixture")

    def control(self, *args, code=0):
        result = subprocess.run([str(self.controller / "bin/control"), *args],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stderr + result.stdout)
        return result.stdout

    def test_round_trip_with_same_version_and_rollback(self):
        local = self.controller / "scripts/own.sh"
        local.write_text("private\n")
        stable = self.controller / "scripts/main-only.sh"
        staged = self.controller / "scripts/staging-only.sh"
        preview = json.loads(self.control("update-check", "--staging", "--json"))
        self.assertEqual((preview["branch"], preview["versions"]["Allgm"]), ("staging", "s1.2.3"))
        self.assertTrue(stable.exists() and not staged.exists())
        self.assertFalse(preview["applied"])
        stable.write_text("changed locally")
        blocked = json.loads(self.control("update-check", "--staging", "--apply", "--json", code=1))
        self.assertIn("scripts/main-only.sh", blocked["conflicts"])
        stable.write_text("main\n")
        self.control("update-check", "--staging", "--apply")
        self.assertTrue(staged.exists() and not stable.exists())
        self.assertEqual(self.control("module-versions"), "Allgm s1.2.3\nZusatz 4.5.6\n")
        shell_init = self.control("shell-init")
        self.assertIn("module-versions=control update-check --versions", shell_init)
        for previous in ("ansible-Version", "ansible-version"):
            self.assertNotIn(previous + "=", shell_init)
            self.control(previous, code=2)
        self.assertEqual(json.loads(self.control("update-check", "--remote", "--json"))["branch"], "main")
        self.control("update-check", "--apply")
        self.assertTrue(stable.exists() and not staged.exists())
        self.assertEqual(self.control("update-check", "--versions"), "Allgm 1.2.3\nZusatz 4.5.6\n")
        self.assertIn("# lokal\nZusatz|4.5.6|", self.marker.read_text())
        backups = sorted(rollout.install.backup_home(self.controller).iterdir())
        self.control("update-check", "--rollback", backups[-1].name)
        self.assertTrue(staged.exists() and not stable.exists())
        self.assertIn("s1.2.3", self.control("module-versions"))
        self.control("update-check", "--auto")
        self.assertTrue(stable.exists() and not staged.exists())
        self.assertEqual(local.read_text(), "private\n")

    def test_cron_rejects_staging_and_missing_branch_never_uses_main_or_tag(self):
        self.control("update-check", "--auto", "--staging", code=2)
        self.git("branch", "-D", "staging")
        self.control("update-check", "--apply", "--staging", code=2)
        self.git("tag", "staging")
        self.control("update-check", "--apply", "--staging", code=2)
        self.assertIn("Allgm 1.2.3", self.control("module-versions"))
        self.assertFalse(rollout.install.backup_home(self.controller).exists())

    def test_homelab_follows_base(self):
        self.exercise_overlay("Homelab", "roles/openwrt_operations/tasks/main.yml")

    def test_external_overlay_follows_its_receipt_and_token(self):
        token = self.work / "test.token"
        token.write_text("github_" + "pat_test_fixture")
        token.chmod(0o600)
        self.exercise_overlay("ExampleOverlay", "roles/sample_service/tasks/main.yml", str(token))

    def test_legacy_overlay_marker_blocks_base_only_update(self):
        marker = self.controller / "update_check/extensions/example/manifest.json"
        marker.parent.mkdir(parents=True)
        marker.write_text("{}")
        (self.controller / "roles/example").mkdir(parents=True)
        (self.controller / rollout.install.RECEIPT).unlink()
        self.assertEqual(rollout.install.installed_profile(self.controller), "example")
        with self.assertRaisesRegex(ValueError, "Overlay-Installer"):
            rollout.install.update_controller(self.controller, {}, "allgm", None)
        self.control("update-check", "--remote", code=2)

    def exercise_overlay(self, profile, feature, token_file=""):
        self.remote = self.work / "overlay"
        self.remote.mkdir()
        self.git("init", "-q", "-b", "main")
        self.file("VERSION.txt", "4.5.6\n")
        self.file("controller-overlay.json", json.dumps({"schema": 1, "profile": profile, "replaces": []}))
        (self.remote / feature).parent.mkdir(parents=True)
        self.file(feature, "---\n[]\n")
        self.commit(profile)
        self.git("switch", "-qc", "staging")
        self.file(feature, "---\n# staging\n[]\n")
        self.commit(profile)
        self.git("switch", "-q", "main")
        dest = self.controller / feature
        dest.parent.mkdir(parents=True)
        shutil.copy2(self.remote / feature, dest)
        receipt = json.loads((self.controller / rollout.install.RECEIPT).read_text())
        receipt["files"][feature] = rollout.install.sha(dest)
        rollout.install.write_receipt(self.controller, profile.lower(), receipt["files"], "main")
        with self.marker.open("a") as f:
            f.write(f"{profile}|4.5.6|https://github.com/example/overlay.git|{token_file}\n")
        self.control("update-check", "--apply", "--staging")
        self.assertIn("# staging", dest.read_text())
        versions = self.control("module-versions").splitlines()
        self.assertEqual(versions, ["Allgm s1.2.3", "Zusatz 4.5.6", profile + " s4.5.6"])
        self.control("update-check", "--apply")
        self.assertNotIn("# staging", dest.read_text())
        self.assertIn(profile + " 4.5.6", self.control("module-versions"))

    def test_optional_tui_version_without_network_or_service(self):
        binary = self.work / ".local/bin/ansible-tui"
        binary.parent.mkdir(parents=True)
        binary.write_text('#!/bin/sh\n[ "$1" = "--version" ] && echo "ansible-tui 0.2.2"\n')
        binary.chmod(0o755)
        self.assertIn("Ansible-TUI 0.2.2", self.control("module-versions").splitlines())
