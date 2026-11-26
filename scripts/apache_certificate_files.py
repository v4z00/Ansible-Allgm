"""Prepare a local PEM set or replace Apache's two files as one checked operation."""
from contextlib import ExitStack
import fcntl
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile


DEFAULTS = {
    "apache_certificate_filename": "certificate.crt",
    "apache_intermediate_filename": "intermediate1.crt",
    "apache_encrypted_key_filename": "wildcard_example_org.key",
    "apache_private_key_filename": "wildcard_example_org_unencrypted.key",
}
TARGET_OPTIONS = ("apache_certificate_directory", "apache_certificate_target", "apache_private_key_target",
                  "apache_certificate_target_filename", "apache_private_key_target_filename")
MAX_PEM = 2 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checked_path(value):
    path = Path(value)
    require(path.is_absolute() and path.name and str(path) == value and path.resolve() == path
            and all(ord(char) >= 32 and ord(char) != 127 for char in value),
            "Expected an absolute path without symlinks, traversal or control characters.")
    return path


def leaf(value):
    require(value not in ("", ".", "..") and Path(value).name == value
            and all(ord(char) >= 32 and ord(char) != 127 for char in value), "Invalid certificate file name.")
    return value


def trusted_directory(path):
    """Only a trusted account may redirect or replace a staged key or its destination."""
    for parent in (path, *path.parents):
        if not parent.exists():
            continue
        info = parent.lstat()
        sticky_ancestor = parent != path and info.st_uid == 0 and info.st_mode & stat.S_ISVTX
        require(stat.S_ISDIR(info.st_mode) and info.st_uid in (0, os.geteuid())
                and (sticky_ancestor or not info.st_mode & 0o022),
                "Use a private or administrator-owned path for the certificate pair.")


def read_file(path):
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), "rb") as stream:
        info = os.fstat(stream.fileno())
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and 0 < info.st_size <= MAX_PEM,
                "Expected a nonempty, regular, unlinked PEM file (maximum 2 MiB).")
        data = stream.read(MAX_PEM + 1)
        require(len(data) == info.st_size, "PEM file changed while being read.")
        return data, info


def openssl(args, data):
    result = subprocess.run(["openssl", *args], input=data, capture_output=True)
    require(result.returncode == 0, "OpenSSL rejected the certificate, chain or private key.")
    return result.stdout


def validate(sources):
    require(len(set(sources)) == 3, "Certificate, chain and key must have different paths.")
    certificate, chain, key = (read_file(path)[0] for path in sources)
    blocks = re.compile(rb"-----BEGIN CERTIFICATE-----\r?\n[A-Za-z0-9+/=\r\n]+-----END CERTIFICATE-----")
    require(blocks.fullmatch(certificate.strip()) and blocks.search(chain) and not blocks.sub(b"", chain).strip(),
            "Expected a PEM leaf certificate and a PEM certificate chain.")
    for part in blocks.findall(chain):
        openssl(["x509", "-noout"], part)
    public_cert = openssl(["x509", "-pubkey", "-noout"], certificate)
    public_key = openssl(["pkey", "-passin", "pass:", "-pubout"], key)
    require(public_cert == public_key, "Certificate and private key do not match.")
    bundle = certificate.strip() + b"\n" + chain.strip() + b"\n"
    require(len(bundle) <= MAX_PEM, "The combined PEM chain exceeds 2 MiB.")
    return bundle, key


def write_copy(path, data, mode, owner=None, *, prefix=None):
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=prefix or "." + path.name + "-", delete=False) as stream:
        name = Path(stream.name)
        try:
            if owner is not None and os.geteuid() == 0:
                os.fchown(stream.fileno(), *owner)
            stream.write(data)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            os.fsync(stream.fileno())
        except BaseException:
            name.unlink()
            raise
    return name


def install(sources, targets, check):
    chain, key = validate(sources)
    require(len(set(targets)) == 2 and not any(path in sibling.parents for path in targets for sibling in targets),
            "Certificate and private key targets must be distinct files.")
    require(not set(sources).intersection(targets), "Source and target paths must be distinct.")
    originals = {}
    desired = {}
    backups = {}
    replaced = []
    pending = {}
    restart_attempted = False
    with ExitStack() as stack:
        for folder in sorted({path.parent for path in targets}):
            trusted_directory(folder)
            if not check:
                folder.mkdir(parents=True, exist_ok=True, mode=0o755)
            if folder.exists():
                fd = os.open(folder, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                stack.callback(os.close, fd)
                fcntl.flock(fd, fcntl.LOCK_SH if check else fcntl.LOCK_EX)
        for path, content, mode in zip(targets, (chain, key), (0o644, 0o600)):
            try:
                old, info = read_file(path)
            except FileNotFoundError:
                old, info = None, None
            if (info and old == content and stat.S_IMODE(info.st_mode) == mode
                    and (info.st_uid, info.st_gid) == (os.geteuid(), os.getegid())):
                continue
            originals[path] = (old, info)
            desired[path] = (content, mode)
        if check or not desired:
            return bool(desired)
        for path, (content, mode) in desired.items():
            pending[path] = write_copy(path, content, mode, (os.geteuid(), os.getegid()))
            stack.callback(pending[path].unlink, missing_ok=True)
        for path, (old, info) in originals.items():
            if info:
                # Keep backups private even if the old key had permissive modes.
                backups[path] = write_copy(path, old, 0o600, prefix="." + path.name + ".previous-")
        try:
            for path, prepared in pending.items():
                os.replace(prepared, path)
                replaced.append(path)
            system(["apache2ctl", "configtest"])
            restart_attempted = True
            system(["service", "apache2", "restart"])
        except BaseException:
            for path in reversed(replaced):
                old, info = originals[path]
                if info is None:
                    path.unlink()
                else:
                    # The original bytes are already on the same filesystem. Recovery
                    # must not need space for a third copy after a failed exchange.
                    os.replace(backups[path], path)
                    if os.geteuid() == 0:
                        os.chown(path, info.st_uid, info.st_gid)
                    path.chmod(stat.S_IMODE(info.st_mode))
            if restart_attempted and all(path.exists() for path in targets):
                system(["apache2ctl", "configtest"])
                system(["service", "apache2", "restart"])
            raise
    return True


def system(argv):
    result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    require(result.returncode == 0, "Apache command failed: " + " ".join(argv))


def select(playbook, args):
    config = {key: leaf(os.environ.get(key.upper(), value)) for key, value in DEFAULTS.items()}
    require(len(set(config.values())) == len(config), "Certificate source names must be distinct.")
    names = list(config.values())
    source_options = ("APACHE_CERTIFICATE_SOURCE", "APACHE_INTERMEDIATE_SOURCE",
                      "APACHE_ENCRYPTED_KEY_SOURCE", "APACHE_PRIVATE_KEY_SOURCE")

    def sources(folder):
        paths = [checked_path(os.environ.get(option, str(folder / name))) for option, name in zip(source_options, names)]
        require(len(set(paths)) == 4, "Certificate source paths must be distinct.")
        return paths

    if os.environ.get("APACHE_CERTIFICATE_SOURCE_DIRECTORY"):
        selected = checked_path(os.environ["APACHE_CERTIFICATE_SOURCE_DIRECTORY"])
    else:
        root = checked_path(os.environ.get("APACHE_CERTIFICATE_ROOT", ""))
        sets = []
        for folder in root.iterdir():
            if folder.is_symlink() or not folder.is_dir():
                continue
            cert, chain, encrypted, _ = sources(folder)
            if all(path.is_file() for path in (cert, chain, encrypted)):
                sets.append((cert.stat().st_mtime_ns, folder))
        sets.sort(reverse=True)
        require(sets, "No complete certificate sets found.")
        for index, (_, folder) in enumerate(sets, 1):
            print(f"[{index}] {folder}")
        choice = input("Zertifikatssatz / certificate set: ").strip()
        require(choice.isascii() and choice.isdigit() and 1 <= int(choice) <= len(sets), "Invalid selection.")
        selected = sets[int(choice) - 1][1]
    cert, intermediate, encrypted, decrypted = sources(selected)
    trusted_directory(decrypted.parent)
    read_file(encrypted)
    if not decrypted.exists() or encrypted.stat().st_mtime_ns > decrypted.stat().st_mtime_ns:
        with tempfile.NamedTemporaryFile(dir=decrypted.parent, prefix=".apache-key-", delete=False) as stream:
            temporary = Path(stream.name)
        try:
            # OpenSSL reads an encrypted key's passphrase from its own terminal.
            result = subprocess.run(["openssl", "pkey", "-in", str(encrypted), "-out", str(temporary)],
                                    stdout=subprocess.DEVNULL)
            require(result.returncode == 0, "Private key decryption failed.")
            validate([cert, intermediate, temporary])
            os.replace(temporary, decrypted)
        finally:
            temporary.unlink(missing_ok=True)
    else:
        validate([cert, intermediate, decrypted])
        decrypted.chmod(0o600)
        if os.geteuid() == 0:
            os.chown(decrypted, 0, 0)
    config.update(apache_certificate_root=str(selected.parent), apache_certificate_year=selected.name,
                  apache_certificate_source_directory=str(selected))
    for name in source_options:
        if name != "APACHE_ENCRYPTED_KEY_SOURCE" and name in os.environ:
            config[name.lower()] = os.environ[name]
    for option in TARGET_OPTIONS:
        if option.upper() in os.environ:
            config[option] = os.environ[option.upper()]
    os.execvp("ansible-playbook", ["ansible-playbook", playbook, "--extra-vars", json.dumps(config), *args])


def main(args):
    if args[0] == "select":
        select(args[1], args[2:])
    elif args[0] == "validate" and len(args) == 4:
        validate([checked_path(path) for path in args[1:]])
    elif args[0] == "install" and len(args) == 7 and args[1] in ("check", "apply"):
        sources = [checked_path(path) for path in args[2:5]]
        targets = [checked_path(path) for path in args[5:]]
        changed = install(sources, targets, args[1] == "check")
        print("changed" if changed else "ok")
    else:
        raise ValueError("Invalid Apache certificate operation.")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ValueError, OSError, EOFError, RuntimeError) as exc:
        sys.exit(str(exc))
