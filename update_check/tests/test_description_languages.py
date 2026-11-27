"""Check localized controller contracts against the composed source tree."""
import hashlib
import json
import os
from pathlib import Path
import re
import unittest


BASE = Path(__file__).resolve().parents[2]
FENCE = re.compile(r"^```json\s*\n(.*?)\n```", re.M | re.S)


class DescriptionTests(unittest.TestCase):
    def check_contract(self, path, roots):
        text = path.read_text()
        match = FENCE.search(text)
        if not match:
            return
        data = json.loads(match[1])
        self.assertEqual(data["schema_version"], 1, path.name)
        field_ids = {field["id"] for field in data.get("fields", [])}
        for lang in ("de", "en"):
            translated = data["i18n"][lang]
            self.assertTrue(translated["title"].strip(), path.name)
            self.assertTrue(translated["description"].strip(), path.name)
            self.assertEqual(set(translated.get("fields", {})), field_ids, path.name)
            self.assertNotIn("source_hashes", translated)
        # The schema also accepts custom Markdown layouts from existing add-ons.
        public_text = text[:match.start()]
        english, marker, german = public_text.partition("<summary>Deutsch</summary>")
        if marker:
            self.assertIn(data["i18n"]["en"]["description"].strip(), english, path.name)
            self.assertIn(data["i18n"]["de"]["description"].strip(), german, path.name)
        for rel, expected in data["source_hashes"].items():
            parts = Path(rel).parts
            self.assertTrue(parts and not Path(rel).is_absolute() and ".." not in parts)
            self.assertNotIn(parts[0], ("inventory", "host_vars", "group_vars", ".git"))
            source = next((p for root in roots if (p := root / rel).is_file()), None)
            self.assertIsNotNone(source, rel)
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), expected, rel)

    def check_tree(self, roots):
        documents = {}
        for root in reversed(roots):
            for path in (root / "descriptions").rglob("*.md"):
                documents[path.relative_to(root)] = path
        for path in documents.values():
            with self.subTest(document=path):
                self.check_contract(path, roots)

    def test_base(self):
        self.check_tree([BASE])

    @unittest.skipUnless(os.environ.get("CONTROLLER_TEST_REPO_DIR"), "requires a sibling profile snapshot")
    def test_composed_homelab(self):
        self.check_tree([Path(os.environ["CONTROLLER_TEST_REPO_DIR"]) / "Ansible-Homelab", BASE])
