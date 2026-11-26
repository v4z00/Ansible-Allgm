"""Language contract for CLI consumers, stable JSON and shipped message catalogs."""
import ast
from collections import Counter
import json
import os
from pathlib import Path
import re
import shutil
from string import Formatter
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import controller_i18n as i18n

PERCENT = re.compile(r"%(?:\((?P<name>[^)]+)\))?[-+# 0]*(?:\*|\d+)?(?:\.(?:\*|\d+))?[hlL]?[diouxXeEfFgGcrsa%]")


def placeholders(text):
    """Field order can differ for named placeholders. Positional slots cannot."""
    named = Counter()
    positional = []
    for _, field, spec, conversion in Formatter().parse(text):
        if field is not None:
            token = (field, spec, conversion)
            if not field:
                positional.append(token)
            else:
                named[token] += 1
    for match in PERCENT.finditer(text):
        token = match[0]
        if token == "%%":
            continue
        if match["name"]:
            named[token] += 1
        else:
            positional.append(token)
    return named, positional


class CatalogTests(unittest.TestCase):
    def test_equal_keys_fragments_and_placeholders(self):
        root = ROOT / "lib/i18n"
        fragments = {p.name for p in (root / "de").glob("*.json")}
        self.assertEqual(fragments, {p.name for p in (root / "en").glob("*.json")})
        pairs = [(root / "de.json", root / "en.json")]
        pairs += [(root / "de" / name, root / "en" / name) for name in sorted(fragments)]
        for left, right in pairs:
            de, en = i18n.read_catalog(left), i18n.read_catalog(right)
            self.assertEqual(de.keys(), en.keys(), str(right))
            for key in de:
                with self.subTest(key=key):
                    self.assertEqual(placeholders(de[key]), placeholders(en[key]))
        self.assertEqual(i18n.catalog("de").keys(), i18n.catalog("en").keys())

    def test_status_codes_and_display_labels_match(self):
        for legacy, code in i18n.status_codes().items():
            self.assertRegex(code, r"^[a-z][a-z0-9_]*$")
            for lang in i18n.LANGUAGES:
                self.assertIn("status." + legacy, i18n.catalog(lang))

    def test_every_literal_message_reference_exists(self):
        known = i18n.catalog("en")
        directories = (ROOT / "scripts", ROOT / "tools", ROOT / "update_check", ROOT / "lib", ROOT / "bin")
        candidates = [p for directory in directories for p in directory.rglob("*") if p.is_file()]
        candidates.append(ROOT / "configure_server_BASE.sh")
        for path in candidates:
            if path.is_symlink() or "tests" in path.parts or "job_tests" in path.parts or path.name.startswith("test_"):
                continue
            if path.suffix == ".py":
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call) or not node.args:
                        continue
                    name = node.func
                    if not (isinstance(name, ast.Name) and name.id == "tr"
                            or isinstance(name, ast.Attribute) and name.attr == "tr"):
                        continue
                    key = node.args[0]
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        self.assertIn(key.value, known, f"{path.name}:{node.lineno}")
                    else:
                        # Only the translation service accepts external keys and enumerated error templates.
                        self.assertEqual(path, ROOT / "scripts/controller_i18n.py",
                                         f"Use a literal catalog key at {path.name}:{node.lineno}")
            elif path.suffix == ".sh" or (path.is_relative_to(ROOT / "bin") and not path.suffix):
                for key in re.findall(r"""\bcontroller_tr\s+["']?([A-Za-z][A-Za-z0-9_.-]*[.][A-Za-z0-9_.-]+)""",
                                      path.read_text(encoding="utf-8")):
                    self.assertIn(key, known, str(path))

    def test_validator_catches_missing_fields_and_wrong_percent_types(self):
        self.assertNotEqual(placeholders("Run {host}"), placeholders("Lauf {path}"))
        self.assertNotEqual(placeholders("%(host)s %d"), placeholders("%(host)s %s"))
        self.assertEqual(placeholders("{id} {path} %%"), placeholders("%% {path} {id}"))

    def test_language_selection_and_safe_local_setting(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            root = Path(tmp).resolve()
            path = root / "group_vars/all/settings.yml"
            path.parent.mkdir(parents=True)
            path.write_text("controller_lang: 'en' # operator preference\n")
            self.assertEqual(i18n.configure(root), "en")
            os.environ["CONTROLLER_LANG"] = "de"
            self.assertEqual(i18n.configure(root), "de")
            self.assertEqual(i18n.cli_args(["--lang=en", "--root", str(root), "--remote"]), ["--root", str(root), "--remote"])
            self.assertEqual(i18n.language(), "en")
            del os.environ["CONTROLLER_LANG"]
            path.write_text("controller_lang: en\ncontroller_lang: de\n")
            self.assertEqual(i18n.configure(root), "de")
            path.unlink()
            other = root / "other.yml"
            other.write_text("controller_lang: en\n")
            path.symlink_to(other)
            self.assertEqual(i18n.configure(root), "de")
            path.unlink()
            os.mkfifo(path)
            self.assertEqual(i18n.configure(root), "de")
        i18n.configure(lang="de")

    def test_stable_status_code_at_every_depth_and_legacy_preservation(self):
        rows = {"status": "PRUEFBEDARF", "items": [{"status": "DEAKTIVIERT_FEHLT"}]}
        expected = {"status": "PRUEFBEDARF", "status_code": "review_required",
                    "items": [{"status": "DEAKTIVIERT_FEHLT", "status_code": "disabled_missing"}]}
        for lang in i18n.LANGUAGES:
            i18n.configure(lang=lang)
            self.assertEqual(i18n.machine_report(rows), expected)
        self.assertNotIn("status_code", rows)
        i18n.configure(lang="de")

    def test_shared_verifier_errors_preserve_details_in_both_languages(self):
        try:
            i18n.configure(lang="en")
            self.assertEqual(i18n.error_text("SHA-256-Manifest für Demo stimmt nicht mit HEAD überein"),
                             "SHA-256 manifest for Demo does not match HEAD")
            i18n.configure(lang="de")
            self.assertEqual(i18n.error_text("Module path collision: roles/new/tasks/main.yml"),
                             "Dateikonflikt zwischen Modulen: roles/new/tasks/main.yml")
        finally:
            i18n.configure(lang="de")

    def test_local_preference_can_be_repaired_after_invalid_choice(self):
        sys.path.insert(0, str(ROOT / "update_check"))
        import check
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            root = Path(tmp).resolve()
            settings = root / "group_vars/all/settings.yml"
            settings.parent.mkdir(parents=True)
            settings.write_text("controller_lang: xx\n")
            self.assertEqual(i18n.configure(root), "de")
            report = check.check_settings(root, {"fields": [{"key": "controller_lang", "type": "string",
                                         "choices": ["en", "de"]}]}, report_unknown=False, check_links=False)
            row = i18n.machine_report(report)["fields"][0]
            self.assertEqual((row["status_code"], row["severity"]), ("invalid_choice", "error"))

    def test_exported_cleanup_helper_runs_away_from_the_source_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            source, controller = fixture / "release", fixture / "controller"
            here = source / "update_check"
            here.mkdir(parents=True)
            (source / "scripts").mkdir()
            shutil.copy2(ROOT / "scripts/controller_i18n.py", source / "scripts")
            shutil.copytree(ROOT / "lib/i18n", source / "lib/i18n")
            shutil.copy2(ROOT / "update_check/cleanup.py", here)
            for file, content in {"release.json": {"manifests": []}, "integrity.json": {"files": {}},
                                  "cleanup_plan.json": {"schema": 1, "profile": "fixture", "candidates": []}}.items():
                (here / file).write_text(json.dumps(content))
            helper = fixture / "cleanup.py"
            subprocess.run([sys.executable, str(ROOT / "tools/update_check/build_release.py"),
                            "--release-root", source, "--check-dir", here, "--cleanup-script", helper],
                           check=True, capture_output=True)
            (controller / "bin").mkdir(parents=True)
            (controller / "ansible.cfg").touch()
            (controller / "bin/control").touch()
            shutil.rmtree(source)
            # Help resolves only from the generated archive, under Python isolated mode.
            result = subprocess.run([sys.executable, "-I", str(helper), "--lang=en", "--help"],
                                    cwd=fixture, check=True, capture_output=True, text=True)
            self.assertIn("one-time helper", result.stdout)
            self.assertTrue(helper.is_file())

    def test_shell_api_uses_arguments_as_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "output"
            value = 'a/b = %s; $(touch ' + str(path) + ')'
            script = '. "$ROOT_DIR/lib/control/i18n.sh"; controller_tr update.private_mode "file=$1"'
            env = dict(os.environ, ROOT_DIR=str(ROOT), CONTROLLER_LANG="en", CONTROLLER_PYTHON=sys.executable)
            result = subprocess.run(["bash", "-c", script, "test", value], env=env, check=True,
                                    text=True, capture_output=True)
            self.assertIn(value, result.stdout)
            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
