"""Controller transport and local state tests. No network or live credentials."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import github_https as github
import install_controller as install


class ControllerHttpsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name).resolve()
        self.target = self.work / "controller"
        self.target.mkdir()
        self.token = self.work / "token file"
        self.value = b"github_" + b"pat_fixture_only"
        self.token.write_bytes(self.value + b"\n")
        self.token.chmod(0o600)
        self.url = "https://github.com/example/fixture.git"
        self.source = self.work / "source"
        self.source.mkdir()
        (self.source / "VERSION.txt").write_text("2.0\n")
        self.marker = self.target / install.VERSIONS

    def test_only_https_repo_urls(self):
        self.assertEqual(github.https_url(self.url), self.url)
        for url in ("http://github.com/a/b", "git@github.com:a/b", "ssh://git@github.com/a/b",
                    "https://user:secret@github.com/a/b", self.url + "?auth=x",
                    self.url + "#ref", "https://github.com/a/..", "https://github.com.evil/a/b"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                github.https_url(url)

    def test_private_file_checks(self):
        self.assertEqual(github.read_token(str(self.token), self.target), self.value)
        link = self.work / "link"
        link.symlink_to(self.token)
        for filename in (str(link), "relative", str(self.work / "missing")):
            with self.assertRaises(ValueError):
                github.read_token(filename, self.target)
        with self.assertRaises(ValueError):
            github.read_token(str(self.token), self.work)
        self.token.chmod(0o644)
        with self.assertRaises(ValueError):
            github.read_token(str(self.token))
        self.token.chmod(0o600)
        for invalid in (b"", b"first\nsecond", b"-----BEGIN OPENSSH PRIVATE KEY-----"):
            self.token.write_bytes(invalid)
            with self.assertRaises(ValueError):
                github.read_token(str(self.token))

    def test_credential_is_scoped_and_never_stored(self):
        env = dict(os.environ, CONTROLLER_GIT_URL=self.url, CONTROLLER_TOKEN_FILE=str(self.token),
                   CONTROLLER_ROOT=str(self.target))
        query = b"protocol=https\nhost=github.com\npath=example/fixture.git\n\n"
        for action, message, authorized in (
                ("get", query, True), ("get", query.replace(b"https", b"http"), False),
                ("get", query.replace(b"github.com", b"other.test"), False),
                ("get", query.replace(b"fixture.git", b"other.git"), False),
                ("store", query, False), ("erase", query, False)):
            with self.subTest(action=action, message=message):
                p = subprocess.run([sys.executable, github.__file__, "credential", action],
                                   env=env, input=message, capture_output=True, check=True)
                self.assertEqual(p.stdout, b"username=x-access-token\npassword=" + self.value + b"\n\n"
                                 if authorized else b"")
                self.assertFalse(p.stderr)

    def test_clone_is_isolated_from_credentials_traces_and_rewrites(self):
        with patch.dict(os.environ, GIT_TRACE_CURL="1", GIT_CONFIG_PARAMETERS="poison",
                        GIT_SSL_NO_VERIFY="1", GIT_ASKPASS="/example/askpass"), \
                patch.object(github.subprocess, "run") as run:
            run.return_value.returncode = 1
            for token in ("", str(self.token)):
                with self.assertRaisesRegex(ValueError, "HTTPS"):
                    github.clone_main(self.url, self.target / "clone", token, self.target)
                cmd = run.call_args.args[0]
                env = run.call_args.kwargs["env"]
                self.assertEqual(env["GIT_ALLOW_PROTOCOL"], "https")
                self.assertEqual(env["GIT_CONFIG_GLOBAL"], os.devnull)
                self.assertEqual(env["GIT_ASKPASS"], "/bin/false")
                self.assertFalse({"GIT_TRACE_CURL", "GIT_CONFIG_PARAMETERS", "GIT_SSL_NO_VERIFY"} & env.keys())
                self.assertEqual("CONTROLLER_TOKEN_FILE" in env, bool(token))
                self.assertNotIn(self.value.decode(), repr((cmd, env)))

    def test_preserves_local_rows_and_migrates_ssh(self):
        custom = "# Wartungsfenster\n\nFuture|3.0|https://github.com/example/future.git|\n"
        self.marker.write_text("Allgm|1.0|git@github.com:example/base.git|/old/key\n" + custom
                               + "NXTS3|1.0|git@github.com:example/private.git|/old/key\n")
        sources = {"Allgm": self.source, "NXTS3": self.source}
        with self.assertRaisesRegex(ValueError, "--token-file"):
            install.version_source(self.target, sources, self.work)
        result = install.version_source(self.target, sources, self.work, token_file=str(self.token))
        data = result.read_text()
        self.assertTrue(data.startswith(install.VERSION_HEADER + "\n"))
        self.assertIn(custom, data)
        self.assertIn("Allgm|2.0|https://github.com/example/base.git|\n", data)
        self.assertIn("|https://github.com/example/private.git|" + str(self.token) + "\n", data)
        self.assertNotIn(self.value.decode(), data)
        result.replace(self.marker)
        self.assertEqual(install.version_source(self.target, sources, self.work).read_text(), data)

    def test_public_token_entry_blocks(self):
        self.marker.write_text(f"Homelab|1.0|{self.url}|{self.token}\n")
        with self.assertRaisesRegex(ValueError, "anonym"):
            install.version_source(self.target, {"Homelab": self.source}, self.work)


if __name__ == "__main__":
    unittest.main()
