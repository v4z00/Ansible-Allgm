"""End-to-end controller composition using isolated, SHA-sealed Git fixtures."""
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE / "update_check"))
import staging_manifest
sys.path.insert(0, str(BASE / "tools"))
import pipe_install

URLS = {"Allgm": "https://github.com/example/base.git",
        "Homelab": "https://github.com/example/profile.git",
        "SSS": "https://github.com/example/Quorum.git",
        "Reports": "https://github.com/v4z00/Reports.git"}
SSS_PATH = "playbooks/security/sss/setup.yml"
PASSIVE = "Other|7.0.0|https://github.com/example/never-fetched.git|/not-a-token"


def write(root, rel, content):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if isinstance(content, str) else json.dumps(content, indent=2) + "\n")
    return path


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, "-c", "core.hooksPath=/dev/null",
                           "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                           "-c", "commit.gpgsign=false", *args], check=True, capture_output=True,
                          text=True, env=dict(os.environ, GIT_CONFIG_NOSYSTEM="1",
                                              GIT_CONFIG_GLOBAL=os.devnull)).stdout


def commit(repo, name, *, sealed=True):
    git(repo, "add", "-A")
    if sealed:
        if (repo / "controller-addon.json").is_file():
            # Independently seal every tracked file, including unmounted documentation.
            entries = {}
            for record in git(repo, "ls-files", "--stage", "-z").rstrip("\0").split("\0"):
                attrs, rel = record.split("\t")
                if rel != "SHA256SUMS.json":
                    entries[rel] = {"mode": "0755" if attrs.startswith("100755 ") else "0644",
                                    "sha256": hashlib.sha256((repo / rel).read_bytes()).hexdigest()}
            data = {"schema": 1, "profile": name, "files": entries}
        else:
            data = staging_manifest.create(repo, name, ":index")
        write(repo, "SHA256SUMS.json", data)
        git(repo, "add", "SHA256SUMS.json")
    git(repo, "commit", "-qm", "Synthetic release")


def branches(repo, name, payload):
    commit(repo, name)
    git(repo, "switch", "-qc", "staging")
    with (repo / payload).open("a") as stream:
        stream.write("# staging\n")
    commit(repo, name)
    git(repo, "switch", "-q", "main")


def snapshot(root):
    """Compare contents, links and modes, including state and any backups."""
    result = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            value = os.readlink(path)
        elif path.is_file():
            value = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            continue
        result[path.relative_to(root).as_posix()] = (stat.S_IMODE(path.lstat().st_mode), value)
    return result


class AddonTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name).resolve()
        self.target = self.work / "controller"
        self.marker = self.target / "versions.txt"
        self.receipt = self.target / ".controller-install.json"
        self.repos = {name: self.work / name for name in URLS}
        shim = self.work / "bin"
        shim.mkdir()
        cases = "\n".join(f"    {shlex.quote(url)}) arg={shlex.quote(str(self.repos[name]))} ;;"
                          for name, url in URLS.items())
        write(shim, "git", "#!/bin/bash\na=()\nfor arg in \"$@\"; do\n  case \"$arg\" in\n"
              + cases + "\n    https://*) exit 90 ;;\n  esac\n  a+=(\"$arg\")\ndone\n"
              + "GIT_ALLOW_PROTOCOL=file exec " + shlex.quote(shutil.which("git")) + ' "${a[@]}"\n').chmod(0o755)
        write(shim, "python3", "#!/bin/sh\nexec " + shlex.quote(sys.executable) + ' "$@"\n').chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.work), PATH=str(shim) + os.pathsep + os.defpath,
                        CONTROLLER_PYTHON=sys.executable, PYTHONDONTWRITEBYTECODE="1",
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        for name, repo in self.repos.items():
            repo.mkdir()
            git(repo, "init", "-qb", "main")
            git(repo, "remote", "add", "origin", URLS[name])
        self.make_base()

    def make_base(self):
        repo = self.repos["Allgm"]
        control = "bin/control.d/update-check.json"
        required = json.loads((BASE / control).read_text())["commands"][0]["requires"]
        files = {control, "bin/control", "bin/install-controller", "bin/control.d/update-check.sh",
                 "controller-base.json", "lib/controller_environment.sh", "scripts/control_runtime.py",
                 "scripts/controller_i18n.py", "lib/control/i18n.sh",
                 *(p.relative_to(BASE).as_posix() for p in (BASE / "lib/i18n").rglob("*.json")), *required}
        for folder in ("tools", "update_check"):
            files.update(p.relative_to(BASE).as_posix() for p in (BASE / folder).glob("*.py"))
        for rel in files:
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(BASE / rel, repo / rel)
        write(repo, "VERSION.txt", "1.0.0\n")
        write(repo, "update_check/settings_contract.json", {"fields": []})
        write(repo, "update_check/release.json", {"feature_defaults": {}, "manifests": []})
        write(repo, "update_check/legacy_sss.json", {"schema": 1, "module": "SSS", "feature": "sss", "files": [SSS_PATH]})
        for name in ("ansible.cfg.example", "inventory.yml.example", "inventory_config.yml.example",
                     "settings.yml.example", "access.yml.example"):
            write(repo, "examples/first_run/" + name, "features: {}\n" if name.startswith("settings.") else "{}\n")
        write(repo, "scripts/base.sh", "# base\n")
        branches(repo, "Allgm", "scripts/base.sh")

    def make_profile(self):
        repo = self.repos["Homelab"]
        write(repo, "VERSION.txt", "2.0.0\n")
        write(repo, "controller-overlay.json", {"schema": 1, "profile": "Homelab", "replaces": ["scripts/base.sh"]})
        write(repo, "scripts/base.sh", "# profile\n")
        branches(repo, "Homelab", "scripts/base.sh")

    def make_addon(self, name, *, prefix=None, command=None):
        repo = self.repos[name]
        short = name.lower()
        descriptor = {"schema": 1, "kind": "addon", "name": name,
                      "mount_prefix": prefix or ("playbooks/security/sss" if name == "SSS" else "roles/monthly_summary"),
                      "payload": ["setup.yml"], "exports": {"integration/command.json": f"bin/control.d/{short}.json",
                                                            "integration/run.sh": f"bin/control.d/{short}.sh"},
                      "replaces": []}
        write(repo, "controller-addon.json", descriptor)
        write(repo, "VERSION.txt", "3.0.0\n")
        write(repo, "setup.yml", "---\n[]\n")
        write(repo, "integration/run.sh", "#!/bin/sh\nexit 0\n").chmod(0o755)
        write(repo, "integration/command.json", {"schema": 1, "commands": [
            {"name": command or short, "description": name, "handler": f"bin/control.d/{short}.sh", "aliases": []}]})
        write(repo, "README.md", "# Standalone usage\n")
        branches(repo, name, "setup.yml")
        return descriptor

    def invoke(self, args, *, env=None, success=True):
        result = subprocess.run(args, env=env or self.env, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode == 0, success, f"{args}\n{result.stderr}\n{result.stdout}")
        return result.stdout

    def install(self, *names, profile=False, success=True):
        args = [self.repos["Allgm"] / "bin/install-controller", "--target", self.target, "--skip-runtime"]
        for name in names:
            args.extend(["--addon", self.repos[name], "--addon-url", name + "=" + URLS[name]])
        env = self.env.copy()
        if profile:
            env.update(ANSIBLE_STAGING_SOURCE=str(self.repos["Homelab"]), ANSIBLE_STAGING_OVERLAY="Homelab")
        return self.invoke(args, env=env, success=success)

    def register(self, name):
        with self.marker.open("a") as stream:
            stream.write(f"# addon={name}\n{name}|3.0.0|{URLS[name]}|\n")

    def versions(self):
        return self.invoke([self.target / "bin/control", "module-versions"]).splitlines()

    def check(self, *args, success=True):
        return self.invoke([self.target / "bin/control", "update-check", *args], success=success)

    def assert_blocked(self):
        before = snapshot(self.target)
        result = self.check("--auto", success=False)
        self.assertEqual(snapshot(self.target), before)
        return result

    def test_base_only_and_unknown_rows(self):
        self.install()
        with self.marker.open("a") as stream:
            stream.write("# local note\n" + PASSIVE + "\n")
        preview = json.loads(self.check("--remote", "--json"))
        self.assertEqual(preview["versions"], {"Allgm": "1.0.0"})
        self.check("--auto")
        self.assertEqual(self.versions(), ["Allgm 1.0.0", "Other 7.0.0"])
        self.assertIn("# local note\n" + PASSIVE + "\n", self.marker.read_text())
        self.assertFalse((self.target / SSS_PATH).exists())

    def test_pipe_installer_forwards_two_addons_to_verified_checkout(self):
        args = ["--addon", "SSS=" + URLS["SSS"], "--addon", "Reports=" + URLS["Reports"]]
        # Exercise stdin and the public Bash option parser without requiring root.
        shell = subprocess.run(["bash", "-s", "--", *args, "--help"], input=(BASE / "install.sh").read_text(),
                               env=self.env, capture_output=True, text=True, check=True)
        self.assertIn("--addon", shell.stdout)
        self.make_addon("SSS")
        self.make_addon("Reports")
        launch = subprocess.run

        def code_only(argv, *positional, **kwargs):
            # Skip the OS/venv preparation on the machine running this test.
            if argv[0] == str(self.repos["Allgm"] / "bin/install-controller"):
                argv = [*argv, "--skip-runtime"]
            return launch(argv, *positional, **kwargs)

        with patch.object(pipe_install, "BASE", self.repos["Allgm"]), patch.object(pipe_install, "TARGET", self.target), \
                patch.dict(os.environ, self.env, clear=True), patch.object(subprocess, "run", code_only):
            pipe_install.install("Allgm", "", None, [args[1], args[3]])
        self.assertCountEqual(self.versions(), ["Allgm 1.0.0", "SSS 3.0.0", "Reports 3.0.0"])
        self.assertTrue((self.target / SSS_PATH).is_file())

    def test_install_single_addon_then_round_trip(self):
        self.make_addon("SSS")
        self.install("SSS")
        self.round_trip(["SSS"], "allgm")

    def test_install_profile_with_two_addons_then_round_trip(self):
        self.make_addon("SSS")
        self.make_addon("Reports")
        self.make_profile()
        self.install("SSS", "Reports", profile=True)
        self.round_trip(["SSS", "Reports"], "homelab")
        self.assertEqual((self.target / "scripts/base.sh").read_text(), "# profile\n")

    def round_trip(self, names, profile):
        with self.marker.open("a") as stream:
            stream.write("# local note\n" + PASSIVE + "\n")
        expectations = {name: "3.0.0" for name in names}
        expectations["Allgm"] = "1.0.0"
        if profile == "homelab":
            expectations["Homelab"] = "2.0.0"
        receipt = json.loads(self.receipt.read_text())
        self.assertEqual((receipt["schema"], receipt["profile"]), (2, profile))
        self.assertEqual(receipt["owners"][SSS_PATH], "SSS")
        self.assertEqual(set(receipt["modules"]), set(expectations))
        if profile == "homelab":
            self.assertEqual(receipt["owners"]["scripts/base.sh"], "Homelab")
        for name, version in expectations.items():
            module = receipt["modules"][name]
            self.assertEqual(module["version"], version)
            self.assertEqual(module["commit"], git(self.repos[name], "rev-parse", "HEAD").strip())
        self.assertFalse((self.target / "playbooks/security/sss/README.md").exists())
        marker = self.marker.read_bytes()
        receipt_bytes = self.receipt.read_bytes()
        preview = json.loads(self.check("--staging", "--json"))
        self.assertFalse(preview["applied"])
        self.assertEqual(preview["versions"], {n: "s" + v for n, v in expectations.items()})
        self.assertEqual(self.marker.read_bytes(), marker)
        self.check("--staging", "--apply")
        self.assertIn("# staging", (self.target / SSS_PATH).read_text())
        self.assertCountEqual(self.versions(), [f"{n} s{v}" for n, v in expectations.items()] + ["Other 7.0.0"])
        self.assertIn("# local note\n" + PASSIVE + "\n", self.marker.read_text())
        for name in names:
            self.assertIn(URLS[name], self.marker.read_text())
        backup = max((self.target / ".local/controller-updates").iterdir()).name
        self.check("--rollback", backup)
        self.assertEqual(self.receipt.read_bytes(), receipt_bytes)
        self.assertEqual(self.marker.read_bytes(), marker)
        self.assertNotIn("# staging", (self.target / SSS_PATH).read_text())
        self.check("--staging", "--apply")
        self.check("--auto")
        self.assertEqual(json.loads(self.check("--remote", "--json"))["changes"], [])
        self.assertEqual((self.target / SSS_PATH).read_text(), "---\n[]\n")

    def test_malformed_registration_and_failed_hash_leave_everything_intact(self):
        self.install()
        self.make_addon("SSS")
        self.register("SSS")
        repo = self.repos["SSS"]
        marker = self.marker.read_text()
        self.marker.write_text(marker + "# addon=sss\n")
        self.assert_blocked()
        self.marker.write_text(marker)
        write(repo, "README.md", "undeclared change to standalone documentation\n")
        commit(repo, "SSS", sealed=False)
        self.assert_blocked()

    def test_collision_with_even_identical_addon_payload_is_blocked(self):
        self.make_addon("SSS")
        self.install("SSS")
        self.make_addon("Reports", prefix="playbooks/security/sss")
        self.register("Reports")
        self.assert_blocked()

    def test_duplicate_registry_command_is_blocked(self):
        self.install()
        self.make_addon("SSS", command="update-check")
        self.register("SSS")
        self.assert_blocked()

    def test_registered_local_copy_blocks_new_addon_without_changing_its_approval(self):
        self.install()
        self.make_addon("SSS")
        self.register("SSS")
        local = self.target.with_name(self.target.name + "-local")
        pin = "a" * 32
        write(self.target, ".local/local-extension-id", pin + "\n")
        code = write(local, "code/" + SSS_PATH, "---\n# manuell-integriert: ja\n# bereinigung: behalten\n[]\n")
        digest = hashlib.sha256(code.read_bytes()).hexdigest()
        write(local, "register.json", {"schema": 2, "id": pin,
              "files": {SSS_PATH: {"sha256": digest, "cleanup": "keep"}}})
        local_before = snapshot(local)
        result = json.loads(self.check("--remote", "--json", success=False))
        self.assertEqual(result["local_extensions"]["status"], "OK")
        self.assertEqual(result["local_conflicts"], [SSS_PATH])
        self.assert_blocked()
        self.assertEqual(snapshot(local), local_before)

    def test_checkout_installer_preserves_legacy_register_until_explicit_migration(self):
        self.install()
        local = self.target.with_name(self.target.name + "-local")
        pin = "b" * 32
        write(self.target, ".local/local-extension-id", pin + "\n")
        name = "roles/site_task/tasks/main.yml"
        file = write(local, "code/" + name, "---\n# manuell-integriert: ja\n# bereinigung: behalten\n[]\n")
        write(local, "register.json", {"schema": 1, "id": pin,
              "files": {name: {"sha256": hashlib.sha256(file.read_bytes()).hexdigest(), "cleanup": "behalten"}}})
        before = snapshot(self.target), snapshot(local)
        repo = self.repos["Allgm"]
        cmd = [repo / "bin/install-controller", "--target", self.target]
        for option in ("--skip-runtime", "--update"):
            self.invoke([*cmd, option], success=False)
            self.assertEqual((snapshot(self.target), snapshot(local)), before)
        migrator = [sys.executable, repo / "tools/migrate_local_extensions.py", "--controller", self.target]
        self.invoke([*migrator, "--apply"])
        self.invoke([*cmd, "--update"])
        after = snapshot(self.target), snapshot(local)
        for rel in (name, "roles/site_task/defaults/main.yml"):
            candidate = write(repo, rel, "---\n{}\n")
            self.invoke([*cmd, "--update"], success=False)
            self.assertEqual((snapshot(self.target), snapshot(local)), after)
            candidate.unlink()
        meta = json.loads((repo / "controller-base.json").read_text())
        meta.pop("local_extension_schema")
        write(repo, "controller-base.json", meta)
        self.invoke([*cmd, "--update"], success=False)
        self.assertEqual((snapshot(self.target), snapshot(local)), after)

    def test_fresh_install_rejects_alias_collision_before_writing_controller(self):
        self.make_addon("SSS")
        repo = self.repos["SSS"]
        source = "integration/command.json"
        entry = json.loads((repo / source).read_text())
        entry["commands"][0]["aliases"] = [{"name": "update-check", "args": []}]
        write(repo, source, entry)
        commit(repo, "SSS")
        self.install("SSS", success=False)
        self.assertFalse(self.target.exists())

    def test_installed_addon_blocks_incompatible_target_branch(self):
        self.make_addon("SSS")
        self.install("SSS")
        repo = self.repos["Allgm"]
        git(repo, "switch", "-q", "staging")
        meta = json.loads((repo / "controller-base.json").read_text())
        del meta["addon_contract"]
        write(repo, "controller-base.json", meta)
        commit(repo, "Allgm")
        before = snapshot(self.target)
        self.check("--staging", "--apply", success=False)
        self.assertEqual(snapshot(self.target), before)

    def test_missing_remote_branch_aborts_entire_multi_module_preview_and_apply(self):
        self.make_addon("SSS")
        self.make_addon("Reports")
        self.install("SSS", "Reports")
        git(self.repos["Reports"], "branch", "-D", "staging")
        before = snapshot(self.target)
        for mode in (["--staging"], ["--staging", "--apply"]):
            with self.subTest(mode=mode):
                self.check(*mode, success=False)
                self.assertEqual(snapshot(self.target), before)

    def test_unsafe_descriptor_is_rejected_before_writing(self):
        self.install()
        descriptor = self.make_addon("SSS")
        self.register("SSS")
        repo = self.repos["SSS"]
        for overrides in ({"mount_prefix": "../controller"}, {"replaces": ["bin/control"]},
                          {"exports": {"integration/run.sh": "group_vars/all/settings.yml"}},
                          {"exports": {"integration/run.sh": "bin/control.d/update-check.sh"}},
                          {"mount_prefix": "playbooks/security/../override"}, {"name": "sss"}):
            with self.subTest(overrides=overrides):
                write(repo, "controller-addon.json", {**descriptor, **overrides})
                commit(repo, "SSS")
                self.assert_blocked()

    def test_receipted_addon_must_not_be_silently_unregistered(self):
        self.make_addon("SSS")
        self.install("SSS")
        self.marker.write_text("\n".join(line for line in self.marker.read_text().splitlines()
                                         if line.strip() != "# addon=SSS") + "\n")
        self.assert_blocked()

    def test_legacy_migration_requires_consent_and_preserves_local_files(self):
        self.install()
        self.make_addon("SSS")
        old = write(self.target, SSS_PATH, "# old managed version\n")
        extra = write(self.target, "playbooks/security/sss/operator.txt", "keep\n")
        settings = write(self.target, "group_vars/all/settings.yml", "features:\n  sss: true\n")
        fresh = json.loads(self.receipt.read_text())
        legacy = {k: fresh[k] for k in ("profile", "files")}
        legacy.update(schema=1, source="main")
        legacy["files"][SSS_PATH] = hashlib.sha256(old.read_bytes()).hexdigest()
        write(self.target, ".controller-install.json", legacy)
        self.assert_blocked()
        self.register("SSS")
        old.write_text("# edited locally\n")
        self.assert_blocked()
        old.write_text("# old managed version\n")
        before = (self.receipt.read_bytes(), self.marker.read_bytes())
        self.check("--apply")
        self.assertEqual(old.read_text(), "---\n[]\n")
        self.assertEqual(json.loads(self.receipt.read_text())["owners"][SSS_PATH], "SSS")
        self.assertEqual(extra.read_text(), "keep\n")
        self.assertEqual(settings.read_text(), "features:\n  sss: true\n")
        backup = max((self.target / ".local/controller-updates").iterdir()).name
        self.check("--rollback", backup)
        self.assertEqual(old.read_text(), "# old managed version\n")
        self.assertEqual((self.receipt.read_bytes(), self.marker.read_bytes()), before)
        self.assertEqual(extra.read_text(), "keep\n")

    def test_unmanaged_file_at_addon_destination_is_a_conflict(self):
        self.install()
        self.make_addon("SSS")
        self.register("SSS")
        write(self.target, SSS_PATH, "# site-specific\n")
        self.assert_blocked()

    @unittest.skipUnless(os.environ.get("CONTROLLER_TEST_ADDON_REPO"), "set CONTROLLER_TEST_ADDON_REPO to test the SSS staging checkout")
    def test_actual_sss_staging_in_synthetic_controller(self):
        repo = self.repos["SSS"]
        source = Path(os.environ["CONTROLLER_TEST_ADDON_REPO"]).resolve()
        git(repo, "fetch", "--no-tags", str(source), "refs/heads/staging:refs/heads/staging")
        git(repo, "switch", "staging")
        self.make_profile()
        self.install("SSS", profile=True)
        self.assertEqual((self.target / SSS_PATH).read_bytes(), (repo / "setup.yml").read_bytes())
        self.assertEqual(json.loads(self.receipt.read_text())["modules"]["SSS"]["commit"],
                         git(source, "rev-parse", "staging").strip())
        self.assertEqual(json.loads(self.check("--staging", "--json"))["versions"]["SSS"],
                         "s" + (repo / "VERSION.txt").read_text().strip())

    @unittest.skipUnless(os.environ.get("CONTROLLER_TEST_REPO_DIR"),
                         "set CONTROLLER_TEST_REPO_DIR for the stable migration chain")
    def test_documented_verifiers_start_at_last_stable_controller(self):
        import re
        source = Path(os.environ["CONTROLLER_TEST_REPO_DIR"]) / "Ansible-Allgm"
        self.load_full_snapshot("Allgm", "f5be1ec9331357dd60bd8f385ec6a0d874ea60d4")
        verifier = self.work / "prior-verifier.py"
        relative = "update_check/staging_manifest.py"
        verifier.write_bytes((self.repos["Allgm"] / relative).read_bytes())
        guide = (source / "descriptions/commands/update-check.md").read_text()
        english, german = guide.split("<summary>Deutsch</summary>", 1)
        pattern = r"^  git checkout --quiet --detach ([0-9a-f]{40})$"
        refs = re.findall(pattern, english, re.MULTILINE)
        self.assertEqual(refs, re.findall(pattern, german, re.MULTILINE))
        self.assertGreaterEqual(len(refs), 1)
        # Each verifier is taken from the tree authenticated by its predecessor.
        for ref in [*refs, git(source, "rev-parse", "HEAD").strip()]:
            subprocess.run([sys.executable, verifier, "verify", "Allgm", ref],
                           cwd=source, check=True, capture_output=True)
            verifier.write_bytes(subprocess.check_output(["git", "-C", source, "show", f"{ref}:{relative}"]))

    def load_full_snapshot(self, name, ref="staging", destination="main"):
        # Pull only committed trees from explicitly provided local repositories.
        source = Path(os.environ["CONTROLLER_TEST_REPO_DIR"]).resolve() / ("Ansible-" + name)
        repo = self.repos[name]
        git(repo, "fetch", "--no-tags", str(source), ref)
        git(repo, "switch", "-qC", destination, "FETCH_HEAD")
        return git(repo, "rev-parse", "HEAD").strip()

    @unittest.skipUnless(os.environ.get("CONTROLLER_TEST_REPO_DIR"),
                         "set CONTROLLER_TEST_REPO_DIR to test the complete sealed sibling repositories")
    def test_full_profile_and_addon_snapshot(self):
        revisions = {}
        for name in ("Allgm", "Homelab", "SSS"):
            revisions[name] = self.load_full_snapshot(name)
            git(self.repos[name], "branch", "-f", "staging", "main")
        home = self.repos["Homelab"]
        sss = self.repos["SSS"]
        self.invoke([home / "install-controller", "--allgm", self.repos["Allgm"], "--target", self.target,
                     "--skip-runtime", "--addon", sss, "--addon-url", "SSS=" + URLS["SSS"]])
        for path in (SSS_PATH, "bin/control.d/sss.json", "descriptions/commands/sss.md"):
            self.assertTrue((self.target / path).is_file())
        self.assertEqual((self.target / SSS_PATH).read_bytes(), (sss / "setup.yml").read_bytes())
        self.assertEqual(json.loads(self.receipt.read_text())["owners"][SSS_PATH], "SSS")
        audit = json.loads(self.check("--only", "addon-sss", "--json"))
        self.assertEqual([(c["id"], c["status"]) for c in audit["extensions"]], [("addon-sss", "OK")])
        preview = json.loads(self.check("--staging", "--json"))
        self.assertEqual(set(preview["versions"]), set(revisions))
        self.assertFalse(preview["applied"])
        receipt, versions = self.receipt.read_bytes(), self.marker.read_bytes()
        self.check("--staging", "--apply")
        modules = json.loads(self.receipt.read_text())["modules"]
        self.assertEqual({n: m["commit"] for n, m in modules.items()}, revisions)
        post_update = json.loads(self.check("--only", "addon-sss", "--json"))["extensions"]
        self.assertEqual(post_update[0]["verified_version"], preview["versions"]["SSS"])
        self.assertCountEqual(self.versions(), [f"{n} {v}" for n, v in preview["versions"].items()])
        backup = max((self.target / ".local/controller-updates").iterdir()).name
        self.check("--rollback", backup)
        self.assertEqual((self.receipt.read_bytes(), self.marker.read_bytes()), (receipt, versions))

    @unittest.skipUnless(os.environ.get("CONTROLLER_TEST_REPO_DIR") and os.environ.get("CONTROLLER_TEST_PRE_ADDON_REF"),
                         "set CONTROLLER_TEST_REPO_DIR and CONTROLLER_TEST_PRE_ADDON_REF for downgrade coverage")
    def test_full_base_downgrade_then_run_previous_checker(self):
        self.load_full_snapshot("Allgm", destination="staging")
        self.install()
        stage_only = {"tools/controller_addons.py", "tools/controller_transaction.py", "update_check/legacy_sss.json"}
        self.assertTrue(stage_only <= json.loads(self.receipt.read_text())["files"].keys())
        repo = self.repos["Allgm"]
        self.load_full_snapshot("Allgm", ref=os.environ["CONTROLLER_TEST_PRE_ADDON_REF"])
        self.assertNotIn("addon_contract", json.loads((repo / "controller-base.json").read_text()))
        self.check("--auto")
        self.assertEqual((self.target / "update_check/rollout.py").read_bytes(), (repo / "update_check/rollout.py").read_bytes())
        old_preview = json.loads(self.check("--remote", "--json"))
        self.assertEqual(old_preview["versions"], {"Allgm": (repo / "VERSION.txt").read_text().strip()})
        for path in stage_only:
            self.assertFalse((self.target / path).exists(), path)

        # The verified new checkout can migrate the old controller without making its legacy
        # checker load the new contract. Roll back with the now-installed new checker.
        git(repo, "switch", "-q", "staging")
        self.invoke([sys.executable, repo / "update_check/rollout.py", "--staging", "--apply", "--root", self.target])
        self.assertTrue((self.target / "lib/i18n/status_codes.json").is_file())
        backup = max((self.target / ".local/controller-updates").iterdir()).name
        result = self.check("--lang=en", "--rollback", backup)
        self.assertIn("Controller code restored", result)
        self.assertFalse((self.target / "lib/i18n/status_codes.json").exists())
        self.assertEqual(json.loads(self.check("--remote", "--json"))["versions"], old_preview["versions"])

    @unittest.skipUnless(os.environ.get("CONTROLLER_TEST_REPO_DIR"),
                         "set CONTROLLER_TEST_REPO_DIR to exercise the previous register format")
    def test_registered_site_can_migrate_and_return_to_previous_controller(self):
        # Last published schema-1 checker. Its own tooling creates the historical register.
        previous = "ddae5ac0b5326d9780c6924aae25674060930566"
        self.load_full_snapshot("Allgm", previous)
        self.install()
        receipt_before = self.receipt.read_bytes()
        package = self.work / "approved-package"
        name = "scripts/site-only.sh"
        source = write(package, "code/" + name, "#!/bin/sh\n# manuell-integriert: ja\n# bereinigung: behalten\nexit 0\n")
        old = [sys.executable, self.target / "tools/local_extension.py", "--controller", self.target]
        self.invoke([*old, "approve", package, name, hashlib.sha256(source.read_bytes()).hexdigest()])
        self.invoke([*old, "install", package])
        site = self.target.with_name(self.target.name + "-local")
        before = (site / "register.json").read_bytes()
        code_before = snapshot(site / "code")
        self.assertEqual(json.loads(before)["schema"], 1)

        self.load_full_snapshot("Allgm", destination="staging")
        repo = self.repos["Allgm"]
        checker = [sys.executable, repo / "update_check/check.py", "--root", self.target]
        migrate = [sys.executable, repo / "tools/migrate_local_extensions.py", "--controller", self.target]
        report = json.loads(self.invoke([*checker, "--staging", "--apply", "--json"], success=False))
        self.assertEqual(report["local_extensions"]["status"], "MIGRATION_REQUIRED")
        self.assertEqual(self.receipt.read_bytes(), receipt_before)
        self.invoke([*migrate, "--check"])
        self.invoke([*migrate, "--apply"])
        backup, = site.glob("register.json.schema1.*.bak")
        self.assertEqual(backup.read_bytes(), before)
        self.invoke([*checker, "--staging", "--apply"])
        self.assertEqual(json.loads(self.check("--only", "local", "--json"))["local_extensions"]["status"], "OK")
        controller_backup = max((self.target / ".local/controller-updates").iterdir()).name
        installed = self.receipt.read_bytes()
        self.check("--rollback", controller_backup, success=False)
        self.assertEqual(self.receipt.read_bytes(), installed)
        self.invoke([*migrate, "--rollback", backup])
        self.check("--rollback", controller_backup)
        self.assertEqual(self.receipt.read_bytes(), receipt_before)
        self.assertEqual((site / "register.json").read_bytes(), before)
        self.assertEqual(snapshot(site / "code"), code_before)
        self.assertEqual(json.loads(self.check("--only", "local", "--json"))["local_extensions"]["status"], "OK")
