"""Complete a standalone installation from the verified temporary Allgm checkout."""
import argparse
import fcntl
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

import github_https
import install_controller as installer

BASE = Path(__file__).resolve().parents[1]
TARGET = Path("/root/ansible")
sys.path.insert(0, str(BASE / "update_check"))
import staging_manifest


def verify_checkout(repo, name):
    entries = staging_manifest.verify(repo, name)
    for rel, entry in entries.items():
        path = repo / rel
        if (path.is_symlink() or not path.is_file() or installer.sha(path) != entry["sha256"]
                or bool(path.stat().st_mode & stat.S_IXUSR) != (entry["mode"] == "0755")):
            raise ValueError(f"{name}: Arbeitskopie weicht vom SHA-256-Manifest ab: {rel}")
    # Includes tracked first-run examples which the updater never ships to existing sites.
    subprocess.run(["git", "-C", str(repo), "diff", "--quiet", "HEAD", "--"], check=True)
    print(f"{name}: SHA-256 geprüft.", flush=True)


def save_token(source, destination):
    # Walk from the trusted root home. A symlink must never redirect the private file.
    path = Path(destination)
    if not path.is_relative_to("/root/.config") or ".." in path.parts or path.is_relative_to(TARGET):
        raise ValueError("Ungültiger Ablageort für den Token")
    for folder in reversed(path.parents):
        if folder == Path("/"):
            continue
        folder.mkdir(mode=0o700, exist_ok=True)
        info = folder.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise ValueError("Token-Verzeichnis muss root gehören und gegen fremde Schreibzugriffe geschützt sein")
    if path.exists() or path.is_symlink():
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_nlink != 1:
            raise ValueError("Unsichere vorhandene Token-Datei")
    value = github_https.read_token(source, TARGET)
    if path == Path(source):
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
        tmp = Path(output.name)
        try:
            os.fchmod(output.fileno(), 0o600)
            output.write(value + b"\n")
            output.flush()
            os.fsync(output.fileno())
            os.replace(tmp, path)
        finally:
            tmp.unlink(missing_ok=True)


def install(profile, token_file, destination):
    if TARGET.is_symlink() or (TARGET.exists() and not TARGET.is_dir()):
        raise ValueError("Eigenes Controller-Verzeichnis ohne Symlink erforderlich")
    fresh = not TARGET.exists() or not any(TARGET.iterdir())
    if not fresh:
        receipt = TARGET / installer.RECEIPT
        if not receipt.is_file() or receipt.is_symlink():
            raise ValueError("Bestandscontroller zuerst mit dem passenden Checkout-Installer und --update migrieren")
        if installer.read_json(receipt).get("profile") not in {"allgm", profile.lower()}:
            raise ValueError("Dieses Profil passt nicht zum installierten Controller")
        state = installer.parse_versions(installer.version_lines(TARGET / installer.VERSIONS, optional=True))
        for module in {"Allgm", profile} & state.keys():
            url = state[module][1]
            if url and url.removesuffix(".git").lower() != installer.module_url(module).removesuffix(".git").lower():
                raise ValueError("GitHub-Konto und vorhandene versions.txt passen nicht zusammen")

    verify_checkout(BASE, "Allgm")
    base_command = [str(BASE / "bin/install-controller"), "--target", str(TARGET)]
    if profile == "Allgm":
        subprocess.run(base_command, check=True)
        return

    overlay = BASE.parent / f"Ansible-{profile}"
    github_https.clone_main(installer.module_url(profile), overlay, token_file, TARGET)
    verify_checkout(overlay, profile)
    # Verify both repositories before writing the first controller file.
    if fresh:
        subprocess.run(base_command, check=True)
    args = [str(overlay / "install-controller"), "--target", str(TARGET)]
    if token_file:
        if destination:
            save_token(token_file, destination)
        args += ["--token-file", destination or token_file]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=staging_manifest.profile_name)
    parser.add_argument("--token-file", default="")
    parser.add_argument("--save-token-to")
    args = parser.parse_args()
    try:
        # Serialize the base and profile stages across concurrent pipe installers.
        fd = os.open(TARGET.parent, os.O_DIRECTORY)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            install(args.profile, args.token_file, args.save_token_to)
        finally:
            os.close(fd)
    except BlockingIOError:
        sys.exit("Ein Pipe-Installer läuft bereits.")
    except subprocess.CalledProcessError:
        sys.exit("Controllerinstallation fehlgeschlagen.")
    except (ValueError, OSError) as error:
        sys.exit(str(error))
