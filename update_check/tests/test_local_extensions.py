import copy
import hashlib
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "tools"))
import local_extensions as ext
import local_extension as cli
import rollout
import controller_i18n


class LocalExtensionsTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.controller = Path(temporary.name) / "ansible"
        (self.controller / "bin").mkdir(parents=True)
        (self.controller / "bin/control").touch()
        (self.controller / "ansible.cfg").touch()
        (self.controller / "controller-base.json").write_text(
            '{"local_extension_schema":2,"local_extension_layouts":["sibling","internal"]}\n')
        self.bundle = self.controller.parent / "example"
        self.name = "scripts/task.sh"
        self.source = self.bundle / "code" / self.name
        self.source.parent.mkdir(parents=True)
        self.source.write_text("#!/bin/bash\n# manuell-integriert: ja\n# bereinigung: nach-erfolg-archivieren\nexit 0\n")
        self.root = ext.location(self.controller)
        self.approve()
        self.addCleanup(patch.stopall)
        patch.object(cli.cleanup, "scan_sources", return_value=([], [])).start()

    def approve(self):
        cli.approve(self.bundle, self.name, ext.sha(self.source))

    def register(self):
        return ext.read_json(self.root / "register.json")

    def install(self):
        cli.install(self.controller, self.bundle)

    def test_legacy_cron_drift_and_missing_directory(self):
        self.assertEqual(ext.inspect(self.controller)["status"], "NICHT_EINGERICHTET")
        self.install()
        target = self.root / "code" / self.name
        target.write_text("changed")
        self.assertEqual(ext.inspect(self.controller)["files"][0]["status"], "SHA_ABWEICHUNG")
        with patch.object(rollout, "rollout", side_effect=AssertionError("unexpected network or rollout")):
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(rollout.main(["--auto", "--json", "--root", str(self.controller)]), 1)
            self.assertFalse(json.loads(out.getvalue())["applied"])
        with self.assertRaises(ValueError):
            self.install()
        self.root.rename(self.root.with_suffix(".missing"))
        self.assertFalse(ext.passed(ext.inspect(self.controller)))

    def test_installed_internal_register_is_checked_and_can_receive_updates(self):
        self.install()
        internal = self.controller / ".local/extensions"
        self.root.rename(internal)
        self.root = internal
        self.assertEqual(ext.inspect(self.controller)["status"], "OK")
        self.source.write_text(self.source.read_text() + "# reviewed update\n")
        self.approve()
        self.install()
        self.assertEqual((internal / 'code' / self.name).read_bytes(), self.source.read_bytes())
        self.assertEqual(ext.inspect(self.controller)["status"], "OK")

    def test_internal_layout_blocks_unsupported_target_and_rollback(self):
        self.install()
        self.root.rename(self.controller / ".local/extensions")
        report = ext.inspect(self.controller)
        self.assertEqual(report["layout"], "internal")
        for rollback in (False, True):
            with self.assertRaises(ValueError):
                ext.require_compatible(report, {"local_extension_schema": 2}, rollback=rollback)
        ext.require_compatible(report, {"local_extension_schema": 2,
                                       "local_extension_layouts": ["sibling", "internal"]})

    def test_archive_requires_run_and_no_caller_and_preserves_both_hashes(self):
        self.install()
        sha = ext.sha(self.source)
        with self.assertRaises(FileNotFoundError):
            cli.archive(self.controller, self.root, self.register(), self.name, sha)
        cli.run(self.controller, self.root, self.register()["files"], self.name, None)
        with patch.object(cli.cleanup, "scan_sources", return_value=([("timer", "task.sh")], [])):
            with self.assertRaises(ValueError):
                cli.archive(self.controller, self.root, self.register(), self.name, sha)
        cli.archive(self.controller, self.root, self.register(), self.name, None)
        self.assertTrue((self.root / "code" / self.name).is_file())
        with self.assertRaises(ValueError):
            cli.archive(self.controller, self.root, self.register(), self.name, "0" * 64)
        cli.archive(self.controller, self.root, self.register(), self.name, sha)
        self.install()
        entry = self.register()["files"][self.name]
        saved = self.root / "archiv" / entry["archive"]
        proof = ext.archive_proof(self.root, self.name, entry)
        self.assertEqual((saved / "datei").read_bytes(), self.source.read_bytes())
        self.assertEqual((saved / "SHA256SUMS").read_text(), sha + "  datei\n")
        self.assertEqual([proof["archived_sha256"], proof["approved_sha256"]], [sha, sha])
        # Recover interruption after the archive and register committed, before removal of the live copy.
        (self.root / "code" / self.name).write_bytes(self.source.read_bytes())
        self.assertFalse(ext.passed(ext.inspect(self.controller)))
        cli.archive(self.controller, self.root, self.register(), self.name, sha)
        self.assertTrue(ext.passed(ext.inspect(self.controller)))
        (saved / "datei").write_text("changed")
        self.assertFalse(ext.passed(ext.inspect(self.controller)))

    def test_unknown_link_failed_run_and_new_revision(self):
        self.install()
        extra = self.root / "code/unapproved"
        extra.touch()
        self.assertFalse(ext.passed(ext.inspect(self.controller)))
        extra.unlink()
        extra.symlink_to(self.source)
        self.assertFalse(ext.passed(ext.inspect(self.controller)))
        extra.unlink()
        self.source.write_text(self.source.read_text().replace("exit 0", "exit 7"))
        self.approve()
        self.install()
        with self.assertRaises(subprocess.CalledProcessError):
            cli.run(self.controller, self.root, self.register()["files"], self.name, None)
        self.assertFalse((self.root / "runs" / (self.name + ".json")).exists())

    def test_wrong_bundle_traversal_and_keep(self):
        self.install()
        with self.assertRaises(ValueError):
            ext.path_in(self.root, "../register.json")
        data = ext.read_json(self.bundle/"register.json")
        wrong = copy.deepcopy(data)
        wrong["id"] = "0"*32
        cli.record(self.bundle/"register.json",wrong)
        with self.assertRaises(ValueError):
            self.install()
        cli.record(self.bundle/"register.json",data)
        self.source.write_text(self.source.read_text().replace("nach-erfolg-archivieren", "behalten"))
        self.approve()
        self.install()
        cli.run(self.controller, self.root, self.register()["files"], self.name, None)
        with self.assertRaises(ValueError):
            cli.archive(self.controller,self.root,self.register(),self.name,ext.sha(self.source))

    def supplement(self, slug, name):
        bundle = self.bundle.parent / slug
        cli.new_supplement(self.bundle, bundle, slug)
        path = bundle / "code" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.source.read_bytes())
        cli.approve(bundle, name, ext.sha(path))
        return bundle

    def test_additions_survive_site_updates_and_archive(self):
        self.install()
        name = "scripts/extra.sh"
        first = self.supplement("extra", name)
        second = self.supplement("other", "scripts/other.sh")
        cli.install(self.controller, first)
        cli.install(self.controller, second)
        cli.run(self.controller, self.root, self.register()["files"], name, None)
        cli.archive(self.controller, self.root, self.register(), name, ext.sha(self.source))
        archived = self.register()["files"][name]
        self.source.write_text(self.source.read_text() + "# revision 2\n")
        self.approve()
        self.install()
        cli.install(self.controller, first)
        self.assertEqual(archived, self.register()["files"][name])
        self.assertEqual(self.register()["files"]["scripts/other.sh"]["supplement"], "other")
        self.assertEqual((self.root / "code" / self.name).read_bytes(), self.source.read_bytes())
        self.assertTrue(ext.passed(ext.inspect(self.controller)))
        path = first / "code" / name
        path.write_bytes(self.source.read_bytes())
        cli.approve(first, name, ext.sha(path))
        cli.install(self.controller, first)
        self.assertNotIn("archive", self.register()["files"][name])
        self.assertFalse((self.root / "runs" / (name + ".json")).exists())

    def test_package_collisions_fail_without_modifying_any_owner(self):
        self.install()
        name = "scripts/extra.sh"
        extra = self.supplement("extra", name)
        cli.install(self.controller, extra)
        before = self.register()
        for bundle in (self.supplement("collision", self.name), self.supplement("other", name)):
            with self.assertRaisesRegex(ValueError, "anderes Paket"):
                cli.install(self.controller, bundle)
        (self.bundle / "code" / name).write_bytes(self.source.read_bytes())
        cli.approve(self.bundle, name, ext.sha(self.source))
        with self.assertRaisesRegex(ValueError, "anderes Paket"):
            self.install()
        self.assertEqual(before, self.register())

    def test_git_role_and_playbook_names_are_reserved(self):
        self.install()
        for name in ("roles/shared/tasks/extra.yml", "playbooks/example.yml"):
            reserved = self.controller / ("roles/shared" if name.startswith("roles/") else name)
            reserved.parent.mkdir(parents=True, exist_ok=True)
            if name.startswith("roles/"):
                reserved.mkdir()
            else:
                reserved.touch()
            slug = "role" if name.startswith("roles/") else "play"
            bundle = self.supplement(slug, name)
            with self.assertRaisesRegex(ValueError, "Controller belegt"):
                cli.install(self.controller, bundle)

    def test_modified_supplement_blocks_auto_before_checkout(self):
        self.install()
        name = "scripts/extra.sh"
        cli.install(self.controller, self.supplement("extra", name))
        target = self.root / "code" / name
        target.write_text("local edit")
        with patch.object(rollout, "checkout", side_effect=AssertionError("unexpected checkout")):
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(rollout.main(["--auto", "--json", "--root", str(self.controller)]), 1)
        report = json.loads(out.getvalue())
        self.assertFalse(report["applied"])
        row = next(r for r in report["local_extensions"]["files"] if r["path"] == name)
        self.assertEqual((row["supplement"], row["status"]), ("extra", "SHA_ABWEICHUNG"))
        self.assertEqual(target.read_text(), "local edit")

    def test_supplement_requires_registered_matching_site(self):
        extra = self.supplement("extra", "scripts/extra.sh")
        with self.assertRaisesRegex(ValueError, "Standortpaket"):
            cli.install(self.controller, extra)
        self.install()
        data = ext.read_json(extra / "register.json")
        data["id"] = "0" * 32
        cli.record(extra / "register.json", data)
        with self.assertRaisesRegex(ValueError, "Falsche Umgebung"):
            cli.install(self.controller, extra)

    def test_later_delivery_never_deletes_registered_files(self):
        self.install()
        data = ext.read_json(self.bundle / "register.json")
        self.source.unlink()
        data["files"].clear()
        cli.record(self.bundle / "register.json", data)
        self.install()
        self.assertIn(self.name, self.register()["files"])
        self.assertTrue((self.root / "code" / self.name).is_file())


class RegisterMigrationTests(unittest.TestCase):
    """Independent v1 fixtures, including archive receipts in their original format."""

    live = "scripts/keep.sh"
    archived = "scripts/completed.sh"
    archive_id = "b" * 32
    site_id = "a" * 32

    def setUp(self):
        previous_language = controller_i18n.language()
        self.addCleanup(controller_i18n.configure, lang=previous_language)
        language_env = patch.dict(os.environ, {"CONTROLLER_LANG": "de"})
        language_env.start()
        self.addCleanup(language_env.stop)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name).resolve()
        self.controller = self.work / "controller"
        self.root = ext.location(self.controller)
        self.register = self.root / "register.json"
        self.history = self.root / "archiv" / self.archive_id
        self.put(self.controller / "bin/control", b"#!/bin/sh\nexit 0\n")
        self.put(self.controller / "ansible.cfg", b"[defaults]\n")
        self.put_json(self.controller / "controller-base.json", {"local_extension_schema": 2})
        self.put(ext.marker(self.controller), (self.site_id + "\n").encode())
        first = b"#!/bin/sh\n# manuell-integriert: ja\n# bereinigung: behalten\nexit 0\n"
        retired = first.replace(b"behalten", b"nach-erfolg-archivieren")
        self.put(self.root / "code" / self.live, first)
        self.put(self.history / "datei", retired)
        sha = hashlib.sha256(retired).hexdigest()
        old_run = {"path": self.archived, "sha256": sha, "completed_at": "2020-01-01T12:00:00+00:00", "exit_code": 0}
        self.put(self.history / "SHA256SUMS", f"{sha}  datei\n".encode())
        self.put_json(self.history / "BELEG.json", {"path": self.archived, "approved_sha256": sha,
                      "archived_sha256": sha, "archived_at": "2020-01-02T12:00:00+00:00", "run": old_run})
        self.put_json(self.root / "runs" / (self.archived + ".json"), old_run)
        self.put_json(self.root / "runs" / (self.live + ".json"), {
            **old_run, "path": self.live, "sha256": hashlib.sha256(first).hexdigest()})
        self.put_json(self.register, {"schema": 1, "id": self.site_id, "files": {
            self.live: {"sha256": hashlib.sha256(first).hexdigest(), "cleanup": "behalten"},
            self.archived: {"sha256": sha, "cleanup": "nach-erfolg-archivieren",
                            "archive": self.archive_id, "supplement": "historical"}}})
        self.original = self.register.read_bytes()

    @staticmethod
    def put(path, data):
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o600)

    def put_json(self, path, data):
        # Deliberately different from the new writer. Rollback must preserve the original bytes.
        self.put(path, (json.dumps(data, indent=4) + "\n").encode())

    def tree(self, root):
        """Compare content, mode, inode and modification time, including any added files."""
        return {path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mode,
                path.stat().st_ino, path.stat().st_mtime_ns) for path in root.rglob("*") if path.is_file()}

    def migrate(self, *args, success=True):
        result = subprocess.run([sys.executable, str(HERE.parent / "tools/migrate_local_extensions.py"),
                                 "--controller", str(self.controller), *map(str, args)],
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "CONTROLLER_LANG": "en"},
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout + result.stderr)
        return result

    def backups(self):
        return sorted(self.root.glob("register.json.schema1.*.bak"))

    def test_preview_migration_and_rollback_preserve_historical_evidence(self):
        baseline = self.tree(self.work)
        original_proof = ext.archive_proof(self.root, self.archived, json.loads(self.original)["files"][self.archived])
        self.migrate("--check")
        self.assertEqual(self.tree(self.work), baseline)
        self.migrate("--apply")
        self.assertEqual(len(self.backups()), 1)
        backup, = self.backups()
        self.assertEqual(backup.read_bytes(), self.original)
        self.assertEqual((backup.stat().st_uid, backup.stat().st_mode & 0o777), (os.geteuid(), 0o600))
        self.assertEqual((self.register.stat().st_mode & 0o777, self.register.stat().st_uid), (0o600, os.geteuid()))
        self.assertNotEqual(self.register.stat().st_ino, baseline[self.register.relative_to(self.work).as_posix()][2])
        expected = json.loads(self.original)
        expected["schema"] = 2
        expected["files"][self.live]["cleanup"] = "keep"
        expected["files"][self.archived]["cleanup"] = "archive-after-success"
        self.assertEqual(ext.read_json(self.register), expected)
        self.assertTrue(ext.passed(ext.inspect(self.controller)))
        self.assertEqual(ext.archive_proof(self.root, self.archived, expected["files"][self.archived]), original_proof)
        after_apply = self.tree(self.work)
        self.migrate("--check")
        self.migrate("--apply")
        self.assertEqual(self.tree(self.work), after_apply)
        self.migrate("--rollback", backup.name)
        self.assertEqual(self.register.read_bytes(), self.original)
        self.migrate("--rollback", backup)
        self.assertEqual(self.register.read_bytes(), self.original)
        after_rollback = self.tree(self.work)
        for name, file_state in baseline.items():
            if name != self.register.relative_to(self.work).as_posix():
                self.assertEqual(after_apply[name], file_state, name)
                self.assertEqual(after_rollback[name], file_state, name)
        self.assertEqual(ext.inspect(self.controller)["status"], "MIGRATION_REQUIRED")

    def test_cron_reports_schema1_before_network_or_controller_changes(self):
        # A normal controller has already taken this lock during installation.
        self.put(self.work / ".controller.controller-lock", b"")
        initial = self.tree(self.work)
        report = ext.inspect(self.controller)
        self.assertEqual(report["status"], "MIGRATION_REQUIRED")
        self.assertEqual(report["schema"], 1)
        self.assertIn("migrate_local_extensions.py", str(report["migration_command"]))
        self.assertFalse(ext.passed(report))
        with patch.object(rollout, "rollout", side_effect=AssertionError("rollout must not start")), \
                patch.object(rollout, "checkout", side_effect=AssertionError("no fetch")), \
                patch.object(rollout.install, "recover_transaction", side_effect=AssertionError("no writes")), \
                redirect_stdout(io.StringIO()) as out:
            self.assertEqual(rollout.main(["--root", str(self.controller), "--auto", "--json"]), 1)
        response = json.loads(out.getvalue())
        self.assertFalse(response["applied"])
        self.assertEqual(response["local_extensions"]["status"], "MIGRATION_REQUIRED")
        self.assertIn("migrate_local_extensions.py", str(response["local_extensions"]["migration_command"]))
        self.assertEqual(self.tree(self.work), initial)

    def test_legacy_code_requires_register_rollback_for_both_update_and_restore(self):
        # Create the same private backup/receipt pair as a past v1 -> v2 code update.
        active = self.controller / "controller-base.json"
        new = self.work / "new-code" / active.name
        self.put(new, active.read_bytes())
        self.put_json(active, {})
        old = active.read_bytes()
        legacy_source = self.work / "old-code" / active.name
        self.put(legacy_source, old)
        versions = self.controller / "versions.txt"
        self.put(versions, b"Allgm|s1.0.0|https://github.com/example/fixture.git|\n")
        files = {active.name: new}
        _, token = rollout.install.update_plan(self.controller, files, "allgm")
        with redirect_stdout(io.StringIO()):
            rollout.install.update_controller(self.controller, files, "allgm", token, receipt_source="staging")
        code_backup, = (d.name for d in rollout.install.backup_home(self.controller).iterdir()
                        if rollout.install.BACKUP_ID.fullmatch(d.name))
        self.migrate("--apply")
        register_backup, = self.backups()
        before = self.tree(self.controller)
        local_before = self.tree(self.root)
        arguments = ["--root", str(self.controller), "--json", "--lang", "en"]
        with patch.object(rollout, "checkout", return_value=(legacy_source.parent, {active.name: legacy_source})) as checkout, \
                patch.object(rollout.install, "update_controller", side_effect=AssertionError("code writes blocked")), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(rollout.main([*arguments, "--apply"]), 2)
            checkout.assert_called_once()
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(rollout.main([*arguments, "--rollback", code_backup]), 2)
        self.assertEqual(self.tree(self.controller), before)
        self.assertEqual(self.tree(self.root), local_before)
        self.migrate("--rollback", register_backup)
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(rollout.main([*arguments, "--rollback", code_backup]), 0)
        self.assertEqual(active.read_bytes(), old)
        self.assertEqual(self.register.read_bytes(), self.original)
        self.assertTrue(ext.archive_proof(self.root, self.archived, json.loads(self.original)["files"][self.archived]))

    def test_damaged_historical_archive_blocks_migration_without_side_effects(self):
        self.put(self.history / "SHA256SUMS", b"damaged synthetic checksum\n")
        baseline = self.tree(self.root)
        self.migrate("--check", success=False)
        self.migrate("--apply", success=False)
        self.assertEqual(self.tree(self.root), baseline)

    def test_shared_controller_lock_and_rollback_after_local_revision_change(self):
        with cli.locked(self.controller):
            self.migrate("--apply", success=False)
        self.assertEqual(self.register.read_bytes(), self.original)
        self.assertEqual(self.backups(), [])
        self.migrate("--apply")
        backup, = self.backups()
        source = self.root / "code" / self.live
        source.write_bytes(source.read_bytes() + b"# approved revision\n")
        current = ext.read_json(self.register)
        current["files"][self.live]["sha256"] = ext.sha(source)
        self.put_json(self.register, current)
        baseline = self.tree(self.root)
        self.migrate("--rollback", backup, success=False)
        self.assertEqual(self.tree(self.root), baseline)

    def test_schema1_packages_and_supplements_install_as_schema2_with_both_header_languages(self):
        self.migrate("--apply")
        for suffix, name, header in [
                ("", "scripts/legacy.sh", "#!/bin/sh\n# manuell-integriert: ja\n# bereinigung: behalten\nexit 0\n"),
                ("addon", "playbooks/local-example.yml", "---\n# manually-integrated: yes\n# cleanup: keep\n[]\n")]:
            package = self.work / ("bundle-" + (suffix or "site"))
            script = package / "code" / name
            self.put(script, header.encode())
            legacy = {"schema": 1, "id": self.site_id, "files": {name: {"sha256": ext.sha(script), "cleanup": "behalten"}}}
            if suffix:
                legacy["supplement"] = suffix
            self.put_json(package / "register.json", legacy)
            baseline = self.tree(package)
            cli.install(self.controller, package)
            self.assertEqual(self.tree(package), baseline)
            stored = ext.read_json(self.register)
            self.assertEqual(stored["schema"], 2)
            entry = stored["files"][name]
            self.assertEqual(entry["cleanup"], "keep")
            self.assertEqual(entry.get("supplement"), suffix or None)
            self.assertEqual(ext.sha(self.root / "code" / name), ext.sha(script))
        self.assertTrue(ext.passed(ext.inspect(self.controller)))

    def test_policy_recognizes_canonical_cleanup_for_both_languages_and_file_types(self):
        for filename, start in [("entry.sh", "#!/bin/bash\n"), ("play.yml", "---\n")]:
            for header, cleanup, expected in [
                    ("# manuell-integriert: ja", "# bereinigung: behalten", "keep"),
                    ("# manuell-integriert: ja", "# bereinigung: nach-erfolg-archivieren", "archive-after-success"),
                    ("# manually-integrated: yes", "# cleanup: keep", "keep"),
                    ("# manually-integrated: yes", "# cleanup: archive-after-success", "archive-after-success")]:
                with self.subTest(filename=filename, cleanup=cleanup):
                    source = self.work / filename
                    self.put(source, f"{start}{header}\n{cleanup}\n".encode())
                    before = source.read_bytes()
                    self.assertEqual(cli.policy(source), expected)
                    self.assertEqual(source.read_bytes(), before)
