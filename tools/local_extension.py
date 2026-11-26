#!/usr/bin/env python3
"""Manage explicitly approved, local-only extensions on a controller."""
import argparse
from contextlib import contextmanager
import ctypes
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "update_check"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from controller_i18n import cli_args, tr

import cleanup
import local_extensions as ext


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write(path, data):
    path.parent.mkdir(mode=0o700, exist_ok=True, parents=True)
    ext.require(not path.is_symlink(), tr("package.link_target"))
    fd, tmp = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
        sync_dir(path.parent)
    finally:
        Path(tmp).unlink(missing_ok=True)


def record(path, data):
    write(path, json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def timestamp():
    return datetime.now(timezone.utc).isoformat()


# Keep the original importable API while sharing the exact header parser with the checker.
policy = ext.policy


def approve(bundle, name, expected):
    code = ext.path_in(bundle, "code")
    path = ext.path_in(code, name)
    ext.require(ext.sha(path) == expected, tr("package.digest_mismatch"))
    manifest = ext.path_in(bundle, "register.json")
    data = ext.read_json(manifest) if manifest.exists() else {"schema": 2, "id": uuid.uuid4().hex, "files": {}}
    value = policy(path)
    ext.require(type(data.get("schema")) is int and data["schema"] in (1, 2), tr("extension.invalid_register"))
    if data["schema"] == 1:
        value = next(old for old, canonical in ext.LEGACY_CLEANUP.items() if canonical == value)
    data["files"][name] = {"sha256": expected, "cleanup": value}
    record(manifest, data)


def new_supplement(parent, target, name):
    ext.supplement_name(name)
    ext.require(ext.scan(parent, delivery=True)["status"] == "OK", tr("package.inspect_parent"))
    identifier = ext.read_json(parent / "register.json")["id"]
    target.mkdir(mode=0o700)
    (target / "code").mkdir(mode=0o700)
    record(target / "register.json", {"schema": 2, "id": identifier, "supplement": name, "files": {}})


@contextmanager
def locked(controller):
    path = controller.parent / ("." + controller.name + ".controller-lock")
    with os.fdopen(os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600), "r+") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def exchange(old, new):
    # Debian supports atomic directory exchange; macOS provides the equivalent for staging tests.
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        rc = libc.renamex_np(os.fsencode(old), os.fsencode(new), 2)
    else:
        rc = libc.renameat2(-100, os.fsencode(old), -100, os.fsencode(new), 2)
    if rc:
        raise OSError(ctypes.get_errno(), tr("package.directory_swap"))


def install(controller, bundle):
    source = ext.read_json(ext.path_in(bundle, "register.json"))
    ext.require(ext.scan(bundle, delivery=True)["status"] == "OK", tr("package.invalid_bundle"))
    dest = ext.location(controller)
    pin = ext.marker(controller)
    identifier = source["id"]
    if "supplement" in source:
        ext.require(pin.is_file() and dest.is_dir(), tr("package.register_first"))
    if pin.exists() or pin.is_symlink():
        ext.require(ext.regular(pin).read_text().strip() == identifier, tr("package.wrong_site"))
    current = {}
    if dest.exists() or dest.is_symlink():
        report = ext.inspect(controller)
        ext.require(report["status"] == "OK", report.get("migration_command") or tr("package.existing_review"))
        current = ext.read_json(dest / "register.json")["files"]
    owner = source.get("supplement")
    merged = current.copy()
    for name, entry in source["files"].items():
        ext.require(not ext.overlaps_base(controller, name), tr("package.path_owned", path=name))
        entry = {**entry, "cleanup": ext.normalize_cleanup(entry["cleanup"], source["schema"])}
        ext.require(set(entry) == {"sha256", "cleanup"} and policy(ext.path_in(bundle/"code", name)) == entry["cleanup"],
                    tr("package.marked_files"))
        previous = current.get(name)
        if previous is not None:
            ext.require(previous.get("supplement") == owner, tr("package.other_owner", path=name))
            if previous["sha256"] == entry["sha256"]:
                continue  # Keep this revision's archive and run receipt.
        merged[name] = {**entry, "supplement": owner} if owner else entry
    # The installed checker must be able to read the register produced by this tool.
    descriptor = ext.path_in(controller, "controller-base.json")
    ext.require_compatible({"status": "OK", "schema": 2}, ext.read_json(descriptor) if descriptor.exists() else {})
    if dest.is_dir() and merged == current:
        print(tr("package.current"))
        return
    with tempfile.TemporaryDirectory(dir=controller.parent, prefix=".local-install-") as work:
        stage = Path(work) / "bundle"
        if dest.exists():
            shutil.copytree(dest, stage, symlinks=True)
        else:
            stage.mkdir(mode=0o700)
            (stage/"code").mkdir(mode=0o700)
        for name in source["files"]:
            entry = merged[name]
            if entry != current.get(name):
                target = ext.path_in(stage/"code", name)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ext.path_in(bundle/"code", name), target)
                target.chmod(0o600)
                proof = ext.path_in(stage, "runs/" + name + ".json")
                proof.unlink(missing_ok=True)
        record(stage/"register.json", {"schema": 2, "id": identifier, "files": merged})
        ext.require(ext.scan(stage, identifier)["status"] == "OK", tr("package.copy_digest"))
        if not pin.exists():
            write(pin, identifier + "\n")
        if dest.exists():
            exchange(stage, dest)
        else:
            stage.rename(dest)
    print(tr("package.installed"))


def run(controller, root, files, name, limit):
    entry = files[name]
    file = ext.path_in(root/"code", name)
    expected = entry["sha256"]
    ext.require("archive" not in entry and ext.sha(file) == expected and policy(file) == entry["cleanup"],
                tr("package.not_approved"))
    env = os.environ.copy()
    venv = controller / ".venv/bin"
    env.update(PYTHONDONTWRITEBYTECODE="1", PATH=str(venv)+os.pathsep+env.get("PATH",""), ANSIBLE_CONFIG=str(controller/"ansible.cfg"),
               ANSIBLE_ROLES_PATH=os.pathsep.join(map(str,[controller/"roles",root/"code/roles"])),
               LOCAL_CONTROLLER_ROOT=str(controller), LOCAL_EXTENSION_ROOT=str(root))
    receipt = ext.path_in(root, "runs/"+name+".json")
    receipt.unlink(missing_ok=True)  # A failed or interrupted retry invalidates previous success.
    with tempfile.TemporaryDirectory() as work:
        result = Path(work)/"result.json"
        if file.suffix in (".yml",".yaml"):
            ext.require(name.startswith("playbooks/") and limit and not limit.startswith("-"), tr("package.play_limit"))
            env.update(ANSIBLE_CALLBACK_PLUGINS=str(Path(__file__).parent/"local_callbacks"),
                       ANSIBLE_CALLBACKS_ENABLED="extension_receipt", LOCAL_EXTENSION_RESULT=str(result))
            job_configuration = controller/"config/script_jobs_controller.json"
            if job_configuration.is_file():
                job_data = json.loads(job_configuration.read_text())
                subprocess.run([str(venv/"python"),str(controller/"artifacts/script-library/bin/script-jobs"),"--db",job_data["database"],"init"],check=True,stdout=subprocess.DEVNULL)
                env["SCRIPT_JOBS_CALLBACK"] = "1"
                env["SCRIPT_JOBS_CONTROLLER_DB"] = job_data["database"]
                env["ANSIBLE_CALLBACK_PLUGINS"] += os.pathsep+str(controller/"tools/callbacks")
                env["ANSIBLE_CALLBACKS_ENABLED"] += ",script_job_results"
            command = [str(venv/"ansible-playbook"), "--limit", limit, str(file)]
        else:
            ext.require(file.suffix in (".sh",".py") and not limit, tr("package.script_limit"))
            command = ["/bin/bash" if file.suffix == ".sh" else sys.executable, str(file)]
        subprocess.run(command, cwd=controller, env=env, check=True)
        if file.suffix in (".yml",".yaml"):
            ext.require(result.is_file() and ext.read_json(result)["completed_plays"] > 0,
                        tr("package.no_play_receipt"))
    ext.require(ext.sha(file) == expected, tr("package.run_changed"))
    record(receipt, {"path": name, "sha256": expected, "exit_code": 0, "completed_at": timestamp()})


def archive(controller, root, data, name, confirmed):
    entry = data["files"][name]
    approved = entry["sha256"]
    file = ext.path_in(root/"code", name)
    ext.require(entry["cleanup"] == ext.ONCE, tr("package.persistent"))
    if "archive" in entry:
        ext.archive_proof(root, name, entry)
        if not file.exists():
            print(tr("package.already_archived"))
            return
    ext.require(ext.sha(file) == approved and policy(file) == ext.ONCE, tr("package.changed"))
    run_proof = ext.read_json(ext.path_in(root, "runs/"+name+".json"))
    ext.require(run_proof.get("exit_code") == 0 and run_proof.get("sha256") == approved
                and run_proof.get("path") == name, tr("package.missing_run"))
    sources, errors = cleanup.scan_sources(controller)
    sources = [("Controller/" + path, text) for path, text in sources]
    for other, row in data["files"].items():
        if other != name and "archive" not in row:
            sources.append(("Lokal/" + other, ext.regular(ext.path_in(root/"code",other)).read_text()))
    refs = cleanup.dependencies(root/"code", name, sources)
    ext.require(not refs and not errors, tr("package.references", references=", ".join(refs + errors)))
    print(tr("package.candidate"), name, "SHA-256:", approved)
    if confirmed is None:
        return
    ext.require(confirmed == approved, tr("package.confirm_hash"))
    if "archive" not in entry:
        ident = uuid.uuid4().hex
        base = ext.path_in(root,"archiv")
        base.mkdir(mode=0o700,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=base) as tmp:
            dst = Path(tmp)/"entry"
            dst.mkdir(mode=0o700)
            shutil.copyfile(file,dst/"datei")
            with (dst/"datei").open("rb") as stream:
                os.fsync(stream.fileno())
            observed = ext.sha(dst/"datei")
            ext.require(observed == approved, tr("package.archive_changed"))
            write(dst/"SHA256SUMS", ext.checksum_line(observed))
            record(dst/"BELEG.json", {"path":name,"approved_sha256":approved,"archived_sha256":observed,
                                       "archived_at":timestamp(),"run":run_proof})
            dst.rename(base/ident)
            sync_dir(base)
        entry["archive"] = ident
        record(root/"register.json", data)
    ext.archive_proof(root,name,entry)
    ext.require(ext.sha(file) == approved, tr("package.preview_changed"))
    file.unlink()
    sync_dir(file.parent)
    print(tr("package.archive"), root/"archiv"/entry["archive"])


def main(argv=None):
    argv = cli_args(argv, Path("/root/ansible"))
    p=argparse.ArgumentParser(description=tr("package.description"))
    p.add_argument("--lang", choices=("de", "en"), help=tr("cli.lang"))
    p.add_argument("--controller",type=Path,default=Path("/root/ansible"))
    sub=p.add_subparsers(dest="action",required=True)
    a=sub.add_parser("approve");a.add_argument("bundle",type=Path);a.add_argument("path");a.add_argument("sha256")
    a = sub.add_parser("new-supplement", help=tr("package.supplement_help"))
    a.add_argument("parent", type=Path)
    a.add_argument("target", type=Path)
    a.add_argument("name")
    a=sub.add_parser("install");a.add_argument("bundle",type=Path)
    a=sub.add_parser("run");a.add_argument("path");a.add_argument("--limit")
    a=sub.add_parser("archive");a.add_argument("path");a.add_argument("--confirm-sha")
    args=p.parse_args(argv)
    os.umask(0o077)
    if args.action == "new-supplement":
        new_supplement(args.parent.absolute(), args.target.absolute(), args.name)
        return
    if args.action=="approve":
        bundle=args.bundle.absolute()
        ext.require(not bundle.is_symlink() and bundle.is_dir(), tr("package.missing_bundle"))
        ext.require(bundle.resolve() != ext.location(args.controller.resolve()).resolve(), tr("package.approve_source"))
        with locked(bundle):
            approve(bundle,args.path,args.sha256)
        return
    controller=args.controller.absolute()
    ext.require(not controller.is_symlink() and (controller/"bin/control").is_file()
                and (controller/"ansible.cfg").is_file(),tr("package.invalid_controller"))
    with locked(controller):
        if args.action=="install":
            install(controller,args.bundle.absolute())
            return
        root=ext.location(controller)
        report=ext.inspect(controller)
        allowed = args.action=="archive" and report["status"]=="PRUEFBEDARF" and all(
            row["status"] in ("OK","ARCHIVIERT") or (row["path"]==args.path and row["status"]=="ARCHIVIERUNG_OFFEN")
            for row in report["files"])
        ext.require(report["status"]=="OK" or allowed, report.get("migration_command") or tr("package.local_digest"))
        data=ext.read_json(root/"register.json")
        if args.action=="run":
            run(controller,root,data["files"],args.path,args.limit)
        else:
            archive(controller,root,data,args.path,args.confirm_sha)


if __name__=="__main__":
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as e:
        sys.exit(tr("package.aborted")+str(e))
