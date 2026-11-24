"""GitHub main over HTTPS for controller checkouts and the first private clone."""

import argparse
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess
import sys
import tempfile

REPO = re.compile(r"https://github\.com/[A-Za-z0-9-]+/(?!\.{1,2}$)[A-Za-z0-9_.-]+\Z")
DEFAULT_ROOT = Path("/root/ansible")


def https_url(url):
    if not REPO.fullmatch(url) or "github_pat_" in url:
        raise ValueError("GitHub-HTTPS-URL ohne Zugangsdaten erforderlich")
    return url


def legacy_https(url):
    for prefix in ("git@github.com:", "ssh://git@github.com/"):
        if url.startswith(prefix):
            return https_url("https://github.com/" + url[len(prefix):])
    return None


def read_token(filename, *excluded):
    path = Path(filename)
    if not path.is_absolute() or any(c in filename for c in "|\r\n\0"):
        raise ValueError("Absoluten Token-Dateipfad außerhalb von Controller und Checkout angeben")
    try:
        location = path.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ValueError("Token-Datei fehlt oder ist nicht als reguläre Datei lesbar") from None
    if any(location.is_relative_to(root.resolve()) for root in (DEFAULT_ROOT, *excluded)):
        raise ValueError("Absoluten Token-Dateipfad außerhalb von Controller und Checkout angeben")
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(fd)
            if (not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o600
                    or info.st_uid != os.geteuid() or info.st_nlink != 1):
                raise ValueError("Token-Datei muss dem ausführenden Benutzer gehören und Modus 0600 haben")
            raw = stream.read(4097)
    except OSError:
        raise ValueError("Token-Datei fehlt oder ist nicht als reguläre Datei lesbar") from None
    # Reject a legacy SSH key, multiline input and arbitrary files before Git sees them.
    if len(raw) > 4096 or not re.fullmatch(rb"github_pat_[A-Za-z0-9_]+(?:\r?\n)?", raw):
        raise ValueError("Eine einzelne Zeile mit einem GitHub Fine-Grained Token wird erwartet")
    return raw.rstrip(b"\r\n")


def credential(operation):
    if operation != "get":
        return
    fields = dict(line.rstrip(b"\n").split(b"=", 1) for line in sys.stdin.buffer if b"=" in line)
    url = https_url(os.environ["CONTROLLER_GIT_URL"])
    if (fields.get(b"protocol") == b"https" and fields.get(b"host") == b"github.com"
            and fields.get(b"path") == url.removeprefix("https://github.com/").encode()):
        token = read_token(os.environ["CONTROLLER_TOKEN_FILE"], Path(os.environ["CONTROLLER_ROOT"]))
        sys.stdout.buffer.write(b"username=x-access-token\npassword=" + token + b"\n\n")


def clone_main(url, target, token_file="", controller=DEFAULT_ROOT):
    https_url(url)
    target = target.absolute()
    if token_file:
        read_token(token_file, controller, target, Path(__file__).resolve().parents[1])
    with tempfile.TemporaryDirectory(prefix="controller-git-") as home:
        # Cron and interactive runs use the same credentials. In particular, neither
        # Git config rewrites, credential stores, .netrc nor trace settings are inherited.
        env = {k: v for k, v in os.environ.items() if k in
               {"PATH", "HTTPS_PROXY", "https_proxy", "ALL_PROXY", "all_proxy", "NO_PROXY",
                "no_proxy", "GIT_SSL_CAINFO", "SSL_CERT_FILE", "SSL_CERT_DIR"}}
        env.update(HOME=home, XDG_CONFIG_HOME=home, GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="/bin/false",
                   GIT_ALLOW_PROTOCOL="https", GIT_CEILING_DIRECTORIES=str(Path(home).parent),
                   LC_ALL="C")
        cmd = ["git", "-c", "core.hooksPath=/dev/null", "-c", "fetch.fsckObjects=true",
               "-c", "http.followRedirects=false", "-c", "credential.helper="]
        if token_file:
            helper = shlex.join([sys.executable, str(Path(__file__).resolve()), "credential"])
            cmd += ["-c", "credential.useHttpPath=true", "-c", "credential.helper=!exec " + helper]
            env.update(CONTROLLER_GIT_URL=url, CONTROLLER_TOKEN_FILE=token_file,
                       CONTROLLER_ROOT=str(controller.resolve()))
        cmd += ["clone", "--quiet", "--no-tags", "--single-branch", "--branch", "main",
                "--depth", "1", "--", url, str(target)]
        try:
            result = subprocess.run(cmd, cwd=home, env=env, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        except (OSError, subprocess.TimeoutExpired):
            raise ValueError("GitHub main konnte über HTTPS nicht geladen werden") from None
        if result.returncode:
            raise ValueError("GitHub main konnte über HTTPS nicht geladen werden. Repo-URL und Leseberechtigung prüfen.")


def main():
    if sys.argv[1:2] == ["credential"]:
        credential(sys.argv[2])
        return
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("target", type=Path)
    parser.add_argument("--token-file", default="", metavar="PFAD")
    args = parser.parse_args()
    clone_main(args.url, args.target, args.token_file)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError):
        if sys.argv[1:2] != ["credential"]:
            sys.exit("HTTPS-Checkout fehlgeschlagen. Repo-URL, Token-Datei (0600) und Lesezugriff prüfen.")
        sys.exit(1)
