"""Exercise real OpenSSL and local Ansible against temporary, unrelated Apache paths."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/apache_certificate_files.py"
PLAY = ROOT / "playbooks/pki/deploy_apache_certificate.yml"
SHELL = ROOT / "scripts/deploy_apache_certificate.sh"


@unittest.skipUnless(shutil.which("openssl"), "OpenSSL required")
class ApacheCertificatePathsTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name).resolve()
        self.source = self.tmp / "PEM source" / "release 1"
        self.source.mkdir(parents=True)
        self.target = self.tmp / "target files"
        self.cert = self.source / "my leaf.pem"
        self.chain = self.source / "issuing chain.pem"
        self.key = self.source / "plain key.pem"
        self.source_pair(self.cert, self.key)
        self.chain.write_bytes(self.cert.read_bytes())
        self.traces = self.tmp / "calls"
        self.traces.touch()
        binaries = self.tmp / "bin"
        binaries.mkdir()
        for exe in ("apache2ctl", "service"):
            fake = binaries / exe
            fake.write_text('#!/bin/sh\nprintf "%s %s\\n" "${0##*/}" "$*" >> "$APACHE_TEST_CALLS"\n'
                            'if test -f "$APACHE_TEST_FAIL/${0##*/}"; then rm "$APACHE_TEST_FAIL/${0##*/}"; exit 1; fi\n')
            fake.chmod(0o755)
        self.fail = self.tmp / "fail"
        self.fail.mkdir()
        self.config = self.tmp / "ansible.cfg"
        self.config.write_text("[defaults]\nretry_files_enabled=False\n")
        self.env = dict(os.environ, TMPDIR=str(self.tmp), PATH=str(binaries) + os.pathsep + os.environ["PATH"],
                        ANSIBLE_CONFIG=str(self.config), ANSIBLE_LOCAL_TEMP=str(self.tmp / "ansible-temp"),
                        ANSIBLE_REMOTE_TEMP=str(self.tmp / "ansible-remote-tmp"), ANSIBLE_NOCOLOR="1", APACHE_TEST_CALLS=str(self.traces), APACHE_TEST_FAIL=str(self.fail))

    def source_pair(self, cert, key):
        subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                        "-keyout", str(key), "-out", str(cert), "-days", "1",
                        "-subj", "/CN=apache-cert-test.invalid"], check=True, capture_output=True, timeout=30)

    def invoke(self, argv, *, ok=True, env=None, stdin=None):
        result = subprocess.run([str(word) for word in argv], env=env or self.env, cwd=self.tmp,
                                input=stdin, capture_output=True, text=True, timeout=90)
        report = result.stdout + result.stderr
        for line in self.key.read_text().splitlines():
            self.assertNotIn(line, report)
        self.assertEqual(result.returncode == 0, ok, report)
        return report

    def run_pair(self, cert_dest, key_dest, *, check=False, ok=True):
        return self.invoke([sys.executable, HELPER, "install", "check" if check else "apply", self.cert,
                            self.chain, self.key, cert_dest, key_dest], ok=ok)

    def test_failed_restart_restores_old_pair_and_file_modes_then_restarts_previous_pair(self):
        dst = self.tmp / "custom" / "leaf.pem"
        key_dst = self.tmp / "private" / "key.pem"
        self.run_pair(dst, key_dst)
        old = dst.read_bytes(), key_dst.read_bytes()
        self.source_pair(self.cert, self.key)
        (self.fail / "service").touch()
        self.run_pair(dst, key_dst, ok=False)
        self.assertEqual((dst.read_bytes(), key_dst.read_bytes()), old)
        self.assertEqual(key_dst.stat().st_mode & 0o777, 0o600)
        prior_key, = key_dst.parent.glob(".key.pem.previous-*")
        self.assertEqual(prior_key.read_bytes(), old[1])
        self.assertEqual(prior_key.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.traces.read_text().splitlines(), ["apache2ctl configtest", "service apache2 restart"] * 3)

    def test_first_install_config_failure_removes_pair_and_check_does_not_write(self):
        dst, key_dst = self.target / "leaf.pem", self.target / "key.pem"
        self.assertEqual(self.run_pair(dst, key_dst, check=True).strip(), "changed")
        self.assertFalse(self.target.exists())
        (self.fail / "apache2ctl").touch()
        self.run_pair(dst, key_dst, ok=False)
        self.assertEqual(list(self.target.iterdir()), [])
        self.assertEqual(self.traces.read_text().splitlines(), ["apache2ctl configtest"])

    def test_invalid_source_or_alias_target_cannot_change_any_target(self):
        self.target.mkdir()
        dst, key_dst = self.target / "cert", self.target / "key"
        key_dst.write_bytes(b"original")
        key_dst.chmod(0o600)
        link = self.target / "link"
        link.symlink_to(key_dst)
        hard = self.target / "hard"
        os.link(key_dst, hard)
        for candidate in (dst, link, hard, self.tmp / "safe" / ".." / "escape", self.target / "cert" / "child"):
            with self.subTest(candidate=candidate):
                self.run_pair(dst, candidate, ok=False)
                self.assertFalse(dst.exists())
                self.assertEqual(key_dst.read_bytes(), b"original")
        self.chain.write_bytes(b"not a certificate")
        self.run_pair(dst, key_dst, ok=False)
        self.assertEqual(self.traces.read_text(), "")
        self.assertFalse(dst.exists())

    def test_selector_passes_safe_json_and_uses_the_selected_source_names(self):
        encrypted = self.source / "sealed key.pem"
        shutil.copy2(self.key, encrypted)
        self.key.unlink()
        fake = self.tmp / "bin/ansible-playbook"
        fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$APACHE_TEST_ARGS"\n')
        fake.chmod(0o755)
        args = self.tmp / "args"
        env = dict(self.env, ANSIBLE_PROJECT_ROOT=str(ROOT), APACHE_CERTIFICATE_ROOT=str(self.source.parent),
                   APACHE_CERTIFICATE_FILENAME=self.cert.name, APACHE_INTERMEDIATE_FILENAME=self.chain.name,
                   APACHE_ENCRYPTED_KEY_FILENAME=encrypted.name, APACHE_PRIVATE_KEY_FILENAME=self.key.name,
                   APACHE_CERTIFICATE_TARGET=str(self.tmp / "custom.pem"), APACHE_TEST_ARGS=str(args))
        # On Debian as root this also runs the actual public shell entry point.
        entry = ["/bin/bash", SHELL] if os.geteuid() == 0 else [sys.executable, HELPER, "select", PLAY]
        self.invoke([*entry, "--limit", "web"], env=env, stdin="1\n")
        forwarded = args.read_text().splitlines()
        config = json.loads(forwarded[forwarded.index("--extra-vars") + 1])
        self.assertEqual(config["apache_certificate_source_directory"], str(self.source))
        self.assertEqual(config["apache_certificate_target"], str(self.tmp / "custom.pem"))
        self.assertEqual(config["apache_private_key_filename"], self.key.name)
        self.assertEqual(forwarded[-2:], ["--limit", "web"])
        self.assertEqual(self.key.stat().st_mode & 0o777, 0o600)

    @unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook required")
    def test_real_local_play_inventory_paths_check_apply_repeat_and_mismatch(self):
        local = self.tmp / "remote-tmp"
        local.mkdir()
        inventory = self.tmp / "inventory.json"
        variables = {"ansible_connection": "local", "ansible_become": False,
                     "ansible_python_interpreter": sys.executable, "ansible_remote_tmp": str(local),
                     "apache_certificate_source_directory": str(self.source),
                     "apache_certificate_filename": self.cert.name, "apache_intermediate_filename": self.chain.name,
                     "apache_private_key_filename": self.key.name, "apache_certificate_directory": str(self.target),
                     "apache_certificate_target_filename": "bundle.pem", "apache_private_key_target_filename": "priv.pem"}
        inventory.write_text(json.dumps({"all": {"children": {"checkmk_webserver_hosts": {
            "hosts": {"localweb": variables}}}}}))
        play = ["ansible-playbook", "-i", inventory, PLAY]
        self.invoke([*play, "--check", "--diff"])
        self.assertFalse(self.target.exists())
        self.assertEqual(self.traces.read_text(), "")
        self.invoke([*play, "--diff"])
        cert, key = self.target / "bundle.pem", self.target / "priv.pem"
        self.assertEqual(cert.read_bytes(), self.cert.read_bytes() + self.chain.read_bytes())
        self.assertEqual(key.read_bytes(), self.key.read_bytes())
        self.assertEqual(key.stat().st_mode & 0o777, 0o600)
        self.assertIn("changed=0", self.invoke(play))
        old = cert.read_bytes(), key.read_bytes()
        self.source_pair(self.source / "another.crt", self.key)
        self.invoke([*play, "--diff"], ok=False)
        self.assertEqual((cert.read_bytes(), key.read_bytes()), old)
        self.assertEqual(self.traces.read_text().splitlines(), ["apache2ctl configtest", "service apache2 restart"])
        self.assertFalse(any(local.rglob("key.pem")))

    @unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook required")
    def test_legacy_source_layout_and_absolute_target_overrides(self):
        shutil.copy2(self.cert, self.source / "certificate.crt")
        shutil.copy2(self.chain, self.source / "intermediate1.crt")
        shutil.copy2(self.key, self.source / "wildcard_example_org_unencrypted.key")
        target_cert = self.target / "public" / "certificate"
        target_key = self.target / "private" / "key"
        self.invoke(["ansible-playbook", "-i", "checkmk_webserver_hosts,", PLAY, "-e", json.dumps({
            "ansible_connection": "local", "ansible_become": False, "ansible_python_interpreter": sys.executable,
            "apache_certificate_root": str(self.source.parent), "apache_certificate_year": self.source.name,
            "apache_certificate_target": str(target_cert), "apache_private_key_target": str(target_key)})])
        self.assertEqual(target_cert.read_bytes(), self.cert.read_bytes() + self.chain.read_bytes())
        self.assertEqual(target_key.read_bytes(), self.key.read_bytes())
