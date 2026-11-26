import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER_DIR = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded_module = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded_module
    spec.loader.exec_module(loaded_module)
    return loaded_module


check = module('checker_new_tests', CHECKER_DIR / 'check.py')
clean = module('cleaner_new_tests', CHECKER_DIR / 'cleanup.py')


class CleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / 'bin').mkdir()
        (self.root / 'bin/control').write_text('# controller\n')
        (self.root / 'ansible.cfg').write_text('[defaults]\n')
        (self.root / 'old.txt').write_text('old payload\n')
        self.plan = {
            'schema': 1,
            'profile': 'test',
            'active_files': ['bin/control'],
            'candidates': [{'path': 'old.txt', 'sha256': clean.digest(self.root / 'old.txt')}],
        }

    def tearDown(self):
        self.tmp.cleanup()

    def preview(self):
        return clean.preview(self.root, self.plan, external=False)

    def test_preview_does_not_change(self):
        self.assertEqual(self.preview()['candidates'], 1)
        self.assertTrue((self.root / 'old.txt').exists())
        self.assertFalse((self.root / 'x').exists())

    def test_changed_file_kept(self):
        (self.root / 'old.txt').write_text('changed')
        self.assertEqual(self.preview()['files'][0]['status'], 'GEAENDERT_ERHALTEN')

    def test_reference_kept(self):
        (self.root / 'bin/reference.sh').write_text('cat old.txt\n')
        self.assertEqual(self.preview()['files'][0]['status'], 'ABHAENGIGKEIT_ERHALTEN')

    def test_glob_reference_kept(self):
        (self.root / 'bin/reference.sh').write_text("list(Path('.').glob('*.txt'))\n")
        self.assertEqual(self.preview()['files'][0]['status'], 'ABHAENGIGKEIT_ERHALTEN')

    def test_symlink_kept(self):
        (self.root / 'old.txt').unlink()
        (self.root / 'old.txt').symlink_to('/etc/hosts')
        self.assertEqual(self.preview()['files'][0]['status'], 'UNGEPRUEFT_ERHALTEN')

    def test_protected_path_forbidden(self):
        self.plan['candidates'][0]['path'] = 'group_vars/all/settings.yml'
        with self.assertRaises(clean.CleanupError):
            self.preview()

    def test_active_path_forbidden(self):
        self.plan['active_files'].append('old.txt')
        with self.assertRaises(clean.CleanupError):
            self.preview()

    def test_parent_traversal(self):
        self.plan['candidates'][0]['path'] = '../old.txt'
        self.assertEqual(self.preview()['files'][0]['status'], 'UNGEPRUEFT_ERHALTEN')

    def test_cancel_no_change(self):
        with self.assertRaises(clean.CleanupError):
            clean.interactive(
                self.root,
                self.plan,
                input_fn=lambda _: 'NO',
                output=lambda _: None,
                external=False,
            )
        self.assertTrue((self.root / 'old.txt').exists())
        self.assertFalse((self.root / 'x').exists())

    def test_archive_and_receipt(self):
        proof = clean.apply(
            self.root, self.plan, self.preview(), external=False, root_required=False
        )
        self.assertFalse((self.root / 'old.txt').exists())
        self.assertEqual(clean.receipt_status(self.root, self.plan), 'BEREINIGUNG_NACHGEWIESEN')
        saved = self.root / proof['archive'] / 'files/old.txt'
        self.assertEqual(saved.read_text(), 'old payload\n')
        saved.write_text('corrupt')
        self.assertEqual(clean.receipt_status(self.root, self.plan), 'NACHWEIS_ABWEICHEND')

    def test_parallel_change_abort(self):
        report = self.preview()
        (self.root / 'old.txt').write_text('parallel')
        with self.assertRaises(clean.CleanupError):
            clean.apply(self.root, self.plan, report, external=False, root_required=False)
        self.assertTrue((self.root / 'old.txt').exists())

    def test_new_dependency_abort(self):
        report = self.preview()
        (self.root / 'bin/reference.sh').write_text('cat old.txt\n')
        with self.assertRaises(clean.CleanupError):
            clean.apply(self.root, self.plan, report, external=False, root_required=False)

    def test_hardlink_kept(self):
        os.link(self.root / 'old.txt', self.root / 'second.txt')
        self.assertEqual(self.preview()['files'][0]['status'], 'SONDERDATEI_ERHALTEN')

    def test_bad_plan_hash(self):
        self.plan['candidates'][0]['sha256'] = 'bad'
        with self.assertRaises(clean.CleanupError):
            self.preview()

    def test_receipt_wrong_plan(self):
        clean.apply(self.root, self.plan, self.preview(), external=False, root_required=False)
        self.plan['version'] = 'next'
        self.assertEqual(clean.receipt_status(self.root, self.plan), 'ANDERER_PLANSTAND')


class FeatureTests(unittest.TestCase):
    def test_feature_disabled_missing_is_not_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            manifest = {
                'schema': 1,
                'id': 'test',
                'version': '1',
                'files': {'roles/optional/tasks/main.yml': '0' * 64},
                'file_features': {'roles/optional/tasks/main.yml': ['optional']},
            }
            result = check.check_component(root, manifest, {'optional': False})
            self.assertEqual(result['status'], 'AKTIVER_UMFANG_OK')
            self.assertIsNone(result['verified_version'])
            self.assertEqual(result['active_tracked'], 0)
            self.assertEqual(
                check.check_component(root, manifest, {'optional': True})['status'],
                'ABWEICHEND',
            )
            self.assertEqual(check.check_component(root, manifest, {})['status'], 'ABWEICHEND')

    def test_multiple_consumers(self):
        manifest = {'file_features': {'shared.py': ['a', 'b']}}
        self.assertTrue(check.file_enabled(manifest, 'shared.py', {'a': False, 'b': True}))
        self.assertFalse(check.file_enabled(manifest, 'shared.py', {'a': False, 'b': False}))
        self.assertTrue(check.file_enabled(manifest, 'shared.py', {'a': False}))

    def test_inventory_variables_found(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            settings_dir = root / 'inventory/group_vars/all'
            settings_dir.mkdir(parents=True)
            (settings_dir / 'settings.yml').write_text('features: {docker: false}\n')
            values, errors = check.global_settings(root)
            self.assertFalse(errors)
            self.assertIs(values['features']['docker'], False)

    def test_duplicate_variable_trees_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            (root / 'group_vars/all').mkdir(parents=True)
            (root / 'inventory/group_vars/all').mkdir(parents=True)
            with self.assertRaises(check.AuditError):
                check.global_settings(root)

    def test_shared_symlink_not_duplicate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            (root / 'group_vars/all').mkdir(parents=True)
            (root / 'inventory').mkdir()
            (root / 'inventory/group_vars').symlink_to('../group_vars')
            (root / 'group_vars/all/settings.yml').write_text('features: {}\n')
            self.assertFalse(check.global_settings(root)[1])


if __name__ == '__main__':
    unittest.main()
