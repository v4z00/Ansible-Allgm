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
    ext.require(not path.is_symlink(), "Symlink als Schreibziel")
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


def policy(path):
    with ext.regular(path).open(encoding="utf8") as stream:
        top = [stream.readline().strip() for _ in range(3)]
    offset = int(top[0] == "---" or top[0].startswith("#!"))
    ext.require(top[offset] == "# manuell-integriert: ja", "Kopfmarkierung fehlt")
    for value in (ext.KEEP, ext.ONCE):
        if top[offset+1] == "# bereinigung: " + value:
            return value
    raise ValueError("Unbekannte Bereinigungsregel")


def approve(bundle, name, expected):
    code = ext.path_in(bundle, "code")
    path = ext.path_in(code, name)
    ext.require(ext.sha(path) == expected, "Angegebene SHA-256 stimmt nicht")
    manifest = ext.path_in(bundle, "register.json")
    data = ext.read_json(manifest) if manifest.exists() else {"schema": 1, "id": uuid.uuid4().hex, "files": {}}
    data["files"][name] = {"sha256": expected, "cleanup": policy(path)}
    record(manifest, data)


def new_supplement(parent, target, name):
    ext.supplement_name(name)
    ext.require(ext.scan(parent, delivery=True)["status"] == "OK", "Standortpaket vor der Zuordnung prüfen")
    identifier = ext.read_json(parent / "register.json")["id"]
    target.mkdir(mode=0o700)
    (target / "code").mkdir(mode=0o700)
    record(target / "register.json", {"schema": 1, "id": identifier, "supplement": name, "files": {}})


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
        raise OSError(ctypes.get_errno(), "Verzeichniswechsel fehlgeschlagen")


def install(controller, bundle):
    source = ext.read_json(ext.path_in(bundle, "register.json"))
    ext.require(ext.scan(bundle, delivery=True)["status"] == "OK", "Lieferbestand unvollständig oder verändert")
    dest = ext.location(controller)
    pin = ext.marker(controller)
    identifier = source["id"]
    if "supplement" in source:
        ext.require(pin.is_file() and dest.is_dir(), "Zuerst das lokale Standortpaket registrieren")
    if pin.exists() or pin.is_symlink():
        ext.require(ext.regular(pin).read_text().strip() == identifier, "Falsche Umgebung")
    current = {}
    if dest.exists() or dest.is_symlink():
        ext.require(ext.inspect(controller)["status"] == "OK", "Bestehender lokaler Bestand benötigt Prüfung")
        current = ext.read_json(dest / "register.json")["files"]
    owner = source.get("supplement")
    merged = current.copy()
    for name, entry in source["files"].items():
        ext.require(not ext.overlaps_base(controller, name), f"Pfad oder Rolle bereits im Controller belegt: {name}")
        ext.require(set(entry) == {"sha256", "cleanup"} and policy(ext.path_in(bundle/"code", name)) == entry["cleanup"],
                    "Die Lieferung muss aktive, markierte Dateien enthalten")
        previous = current.get(name)
        if previous is not None:
            ext.require(previous.get("supplement") == owner, f"Pfad bereits durch anderes Paket belegt: {name}")
            if previous["sha256"] == entry["sha256"]:
                continue  # Keep this revision's archive and run receipt.
        merged[name] = {**entry, "supplement": owner} if owner else entry
    if dest.is_dir() and merged == current:
        print("Lokaler Bestand aktuell.")
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
        record(stage/"register.json", {"schema": 1, "id": identifier, "files": merged})
        ext.require(ext.scan(stage, identifier)["status"] == "OK", "Kopie besteht SHA-Prüfung nicht")
        if not pin.exists():
            write(pin, identifier + "\n")
        if dest.exists():
            exchange(stage, dest)
        else:
            stage.rename(dest)
    print("Lokale Erweiterungen installiert.")


def run(controller, root, files, name, limit):
    entry = files[name]
    file = ext.path_in(root/"code", name)
    expected = entry["sha256"]
    ext.require("archive" not in entry and ext.sha(file) == expected and policy(file) == entry["cleanup"],
                "Datei nicht zur Ausführung freigegeben")
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
            ext.require(name.startswith("playbooks/") and limit and not limit.startswith("-"), "Playbook und --limit erforderlich")
            env.update(ANSIBLE_CALLBACK_PLUGINS=str(Path(__file__).parent/"local_callbacks"),
                       ANSIBLE_CALLBACKS_ENABLED="extension_receipt", LOCAL_EXTENSION_RESULT=str(result))
            command = [str(venv/"ansible-playbook"), "--limit", limit, str(file)]
        else:
            ext.require(file.suffix in (".sh",".py") and not limit, "Nur Shell-/Python-Einstiege ohne --limit")
            command = ["/bin/bash" if file.suffix == ".sh" else sys.executable, str(file)]
        subprocess.run(command, cwd=controller, env=env, check=True)
        if file.suffix in (".yml",".yaml"):
            ext.require(result.is_file() and ext.read_json(result)["completed_plays"] > 0,
                        "Kein vollständiger Ansible-Lauf mit erfolgreichen Zielaktionen nachgewiesen")
    ext.require(ext.sha(file) == expected, "Quelldatei während des Laufs verändert")
    record(receipt, {"path": name, "sha256": expected, "exit_code": 0, "completed_at": timestamp()})


def archive(controller, root, data, name, confirmed):
    entry = data["files"][name]
    approved = entry["sha256"]
    file = ext.path_in(root/"code", name)
    ext.require(entry["cleanup"] == ext.ONCE, "Dauerhafte Datei bleibt erhalten")
    if "archive" in entry:
        ext.archive_proof(root, name, entry)
        if not file.exists():
            print("Bereits archiviert.")
            return
    ext.require(ext.sha(file) == approved and policy(file) == ext.ONCE, "Datei verändert")
    run_proof = ext.read_json(ext.path_in(root, "runs/"+name+".json"))
    ext.require(run_proof.get("exit_code") == 0 and run_proof.get("sha256") == approved
                and run_proof.get("path") == name, "Erfolgreicher Lauf dieser Revision fehlt")
    sources, errors = cleanup.scan_sources(controller)
    sources = [("Controller/" + path, text) for path, text in sources]
    for other, row in data["files"].items():
        if other != name and "archive" not in row:
            sources.append(("Lokal/" + other, ext.regular(ext.path_in(root/"code",other)).read_text()))
    refs = cleanup.dependencies(root/"code", name, sources)
    ext.require(not refs and not errors, "Referenz vorhanden oder Prüfung unvollständig: " + ", ".join(refs + errors))
    print("Archivkandidat:", name, "SHA-256:", approved)
    if confirmed is None:
        return
    ext.require(confirmed == approved, "Zur Ausführung angezeigte SHA bestätigen")
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
            ext.require(observed == approved, "Archivkopie verändert")
            write(dst/"SHA256SUMS", ext.checksum_line(observed))
            record(dst/"BELEG.json", {"path":name,"approved_sha256":approved,"archived_sha256":observed,
                                       "archived_at":timestamp(),"run":run_proof})
            dst.rename(base/ident)
            sync_dir(base)
        entry["archive"] = ident
        record(root/"register.json", data)
    ext.archive_proof(root,name,entry)
    ext.require(ext.sha(file) == approved, "Quelle seit der Vorschau verändert")
    file.unlink()
    sync_dir(file.parent)
    print("Archiv:", root/"archiv"/entry["archive"])


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--controller",type=Path,default=Path("/root/ansible"))
    sub=p.add_subparsers(dest="action",required=True)
    a=sub.add_parser("approve");a.add_argument("bundle",type=Path);a.add_argument("path");a.add_argument("sha256")
    a = sub.add_parser("new-supplement", help="Leeres Zusatzpaket für einen lokalen Standort anlegen")
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
        ext.require(not bundle.is_symlink() and bundle.is_dir(), "Lieferverzeichnis fehlt")
        ext.require(bundle != ext.location(args.controller.resolve()), "Freigaben in der Pflegequelle durchführen")
        with locked(bundle):
            approve(bundle,args.path,args.sha256)
        return
    controller=args.controller.absolute()
    ext.require(not controller.is_symlink() and (controller/"bin/control").is_file()
                and (controller/"ansible.cfg").is_file(),"Controller nicht erkannt")
    with locked(controller):
        if args.action=="install":
            install(controller,args.bundle.absolute())
            return
        root=ext.location(controller)
        report=ext.inspect(controller)
        allowed = args.action=="archive" and report["status"]=="PRUEFBEDARF" and all(
            row["status"] in ("OK","ARCHIVIERT") or (row["path"]==args.path and row["status"]=="ARCHIVIERUNG_OFFEN")
            for row in report["files"])
        ext.require(report["status"]=="OK" or allowed,"Lokale SHA-Prüfung fehlgeschlagen")
        data=ext.read_json(root/"register.json")
        if args.action=="run":
            run(controller,root,data["files"],args.path,args.limit)
        else:
            archive(controller,root,data,args.path,args.confirm_sha)


if __name__=="__main__":
    try:
        main()
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as e:
        sys.exit("Abbruch: "+str(e))
