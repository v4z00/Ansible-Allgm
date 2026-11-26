"""Konservative Controllerbereinigung: nur freigegebene Dateihashes, Vorschau/YES/Archiv."""
import argparse
import datetime
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

if not getattr(globals().get("__loader__"), "archive", None):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from controller_i18n import cli_args, status_text, tr

class CleanupError(Exception): pass
PROTECTED={'group_vars','host_vars','inventory','artifacts','collections','x','_local','logs','reports','.git','.ssh','state'}
CODE_DIRS=('bin','lib','scripts','roles','playbooks','templates','config','tools','filter_plugins','plugins','inventory','group_vars','host_vars')
TEXT_SUFFIX={'.py','.sh','.yml','.yaml','.j2','.cfg','.ini','.json','.service','.timer','.conf','.toml','.ps1','.command','.bat'}

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
    return h.hexdigest()

def plan_digest(plan):return hashlib.sha256(json.dumps(plan,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def safe_path(root,rel):
    p=Path(rel)
    if not isinstance(rel,str) or not rel or p.is_absolute() or '..' in p.parts or '\\' in rel:raise CleanupError(tr("cleanup.invalid_path"))
    current=root
    for part in p.parts:
        current=current/part
        if current.is_symlink():raise CleanupError(tr("cleanup.symlink"))
    if not current.resolve().is_relative_to(root):raise CleanupError(tr("cleanup.outside"))
    return current

def validate_plan(plan):
    if plan.get('schema')!=1 or not isinstance(plan.get('candidates'),list):raise CleanupError(tr("cleanup.invalid_plan"))
    seen=set();active=set(plan.get('active_files',[]))
    for row in plan['candidates']:
        rel=row.get('path','');p=Path(rel)
        if rel in seen or rel in active or any(x in PROTECTED for x in p.parts) or re.search(r'(?i)(secret|password|private[_-]?key|\.env$|\.pem$)',rel):raise CleanupError(tr("cleanup.protected_path"))
        if not re.fullmatch('[a-f0-9]{64}',row.get('sha256','')):raise CleanupError(tr("cleanup.missing_digest"))
        seen.add(rel)

def scan_sources(root,exclude=None,external=True):
    """Nur Text lesen, keine Shell/Lookups/Inventories ausfuehren. Keine Inhalte ausgeben."""
    result=[];errors=[];seen=set();exclude=Path(exclude).resolve() if exclude else None
    files=[]
    for name in CODE_DIRS:
        base=root/name
        if base.is_dir():files.extend(p for p in base.rglob('*') if p.is_file())
    files.extend(p for p in root.iterdir() if p.is_file() and p.suffix in TEXT_SUFFIX)
    for p in sorted(set(files)):
        if any(x in {'__pycache__','.git','tests','backups','.venv'} for x in p.relative_to(root).parts):continue
        rel=p.relative_to(root)
        if rel.parts[0]=='update_check' and p.suffix=='.json':continue
        if p.suffix not in TEXT_SUFFIX and p.name not in {'control','bashrc'} and not (p.stat().st_mode & 0o111):continue
        if p.resolve()==exclude:continue
        if p.is_symlink() and not p.resolve().is_relative_to(root):errors.append('QUELLVERWEIS_AUSSERHALB');continue
        if p.resolve() in seen:continue
        seen.add(p.resolve())
        try:
            if p.stat().st_size>8*1024*1024:errors.append('QUELLE_ZU_GROSS');continue
            result.append((str(p.relative_to(root)),p.read_text()))
        except (OSError,UnicodeError):errors.append('QUELLE_NICHT_PRUEFBAR')
    if external:
        external_paths=[Path('/etc/crontab')]
        for base in ['/etc/cron.d','/etc/cron.hourly','/etc/cron.daily','/etc/cron.weekly','/etc/cron.monthly','/var/spool/cron/crontabs','/etc/systemd/system','/usr/local/lib/systemd/system','/usr/lib/systemd/system','/lib/systemd/system','/etc/init.d']:
            directory=Path(base)
            if directory.exists():
                try:external_paths.extend(p for p in directory.rglob('*') if p.is_file() and (not p.is_symlink() or p.resolve().is_file()))
                except OSError:errors.append('SYSTEMVERWEISE_NICHT_PRUEFBAR')
        for p in external_paths:
            if not p.exists():continue
            try:
                if p.stat().st_size>1024*1024:errors.append('SYSTEMVERWEIS_ZU_GROSS');continue
                result.append(('Systemverweis:'+p.name,p.read_text()))
            except (OSError,UnicodeError):errors.append('SYSTEMVERWEIS_NICHT_PRUEFBAR')
    return result,sorted(set(errors))

def dependencies(root,rel,sources):
    # Auch reine Dateinamen und literale Globs pruefen; Unklarheit behaelt die Datei.
    name=Path(rel).name;hits=[]
    token=re.compile(r'(?<![A-Za-z0-9_.-])'+re.escape(name)+r'(?![A-Za-z0-9_.-])')
    for source,text in sources:
        if source==rel:continue
        direct=rel in text or str(root/rel) in text or bool(token.search(text))
        glob=False
        # Nur erkennbare Dateisystem-Globaufrufe; Shell-Sentinels wie --limit '*' sind keine Abhaengigkeit.
        for call in re.finditer(r"(?:glob|rglob)\(\s*([\"'])([^\"'\n]+)\1",text):
            literal=call.group(2)
            if '*' not in literal and '?' not in literal:continue
            before=text[text.rfind('\n',0,call.start())+1:call.start()]
            prefixes=[v for v in re.findall(r"[\"']([^\"']+)[\"']",before) if v.split('/')[0] in CODE_DIRS]
            # Dynamische Globs fremder Datenverzeichnisse sind kein belegter Projektdateiverweis.
            if not prefixes and not literal.startswith('/') and not re.search(r'\b(?:root|project_root|ansible_root)\b|Path\([\"\']\.[\"\']',before):continue
            if prefixes and not (rel==prefixes[-1] or rel.startswith(prefixes[-1].rstrip('/')+'/')):continue
            if literal.startswith('/'):glob=fnmatch.fnmatch(str(root/rel),literal)
            elif '/' in literal:glob=fnmatch.fnmatch(rel,literal.removeprefix('./'))
            else:glob=fnmatch.fnmatch(name,literal)
            if glob:break
        if direct or glob:hits.append(source)
    return sorted(set(hits))

def preview(root,plan,exclude=None,external=True):
    root=root.resolve();validate_plan(plan)
    if not (root/'ansible.cfg').is_file() or not (root/'bin/control').is_file():raise CleanupError(tr("cleanup.invalid_project"))
    sources,errors=scan_sources(root,exclude,external)
    rows=[]
    for item in plan['candidates']:
        row={'path':item['path'],'reason':item.get('reason','Freigegebener Altbestand')}
        try:
            p=safe_path(root,item['path'])
            if not p.exists():row['status']='BEREITS_ENTFERNT'
            elif not p.is_file() or p.stat().st_nlink!=1:row['status']='SONDERDATEI_ERHALTEN'
            elif digest(p)!=item['sha256']:row['status']='GEAENDERT_ERHALTEN'
            else:
                hits=dependencies(root,item['path'],sources)
                if hits:row.update(status='ABHAENGIGKEIT_ERHALTEN',references=hits)
                elif errors:row['status']='UNGEPRUEFT_ERHALTEN'
                else:row['status']='ARCHIVIEREN'
        except (OSError,CleanupError):row['status']='UNGEPRUEFT_ERHALTEN'
        rows.append(row)
    candidates=sum(x['status']=='ARCHIVIEREN' for x in rows)
    retained=sum(x['status'].endswith('_ERHALTEN') for x in rows)
    return {'schema':1,'profile':plan['profile'],'plan_sha256':plan_digest(plan),'status':'BEREINIGUNG_MOEGLICH' if candidates else 'BESTAND_ERHALTEN' if retained else 'SAUBER','candidates':candidates,'retained':retained,'files':rows,'scan_errors':errors,'scope':'Nur explizite Planpfade; Konfiguration, Runtime und unbekannte Dateien bleiben erhalten.'}

def show(report,output=print):
    output(tr("cleanup.summary", profile=report["profile"], status=status_text(report["status"])))
    absent=sum(r['status']=='BEREITS_ENTFERNT' for r in report['files'])
    if absent:output(tr("cleanup.absent")+str(absent))
    for row in report['files']:
        if row['status']=='BEREITS_ENTFERNT':continue
        output('  '+status_text(row['status'])+'  '+row['path'])
        for ref in row.get('references',[]):output(tr("cleanup.reference")+ref)
    for error in report['scan_errors']:output('  '+status_text(error))
    output(tr("cleanup.confirmation_scope"))

def apply(root,plan,report,exclude=None,external=True,root_required=True):
    root=root.resolve()
    if root_required and os.geteuid()!=0:raise CleanupError(tr("cleanup.root"))
    fresh=preview(root,plan,exclude,external)
    if fresh!=report:raise CleanupError(tr("cleanup.preview_changed"))
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    base=safe_path(root,'x/backups/controller_cleanup');base.mkdir(parents=True,exist_ok=True,mode=0o700)
    archive=base/stamp;archive.mkdir(mode=0o700)
    moved=[];items={x['path']:x for x in plan['candidates']}
    state_dir=safe_path(root,'update_check/state');state_dir.mkdir(mode=0o700,parents=True,exist_ok=True)
    receipt=state_dir/'cleanup.json'
    if receipt.is_symlink():raise CleanupError(tr("cleanup.receipt_link"))
    try:
        for row in fresh['files']:
            if row['status']!='ARCHIVIEREN':continue
            src=safe_path(root,row['path']);st=src.stat()
            if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1 or digest(src)!=items[row['path']]['sha256']:raise CleanupError(tr("cleanup.changed"))
            dst=archive/'files'/row['path'];dst.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
            src.rename(dst);moved.append((src,dst,items[row['path']]['sha256']))
            if digest(dst)!=items[row['path']]['sha256']:raise CleanupError(tr("cleanup.archive_hash"))
        proof={'schema':1,'profile':plan['profile'],'plan_sha256':plan_digest(plan),'completed_at':stamp,'archive':str(archive.relative_to(root)),'archived':[{'path':str(src.relative_to(root)),'sha256':h} for src,dst,h in moved],'retained':[r for r in fresh['files'] if r['status'].endswith('_ERHALTEN')],'scope':fresh['scope']}
        (archive/'BELEG.json').write_text(json.dumps(proof,indent=2)+'\n');os.chmod(archive/'BELEG.json',0o600)
        fd,tmp=tempfile.mkstemp(dir=state_dir,prefix='.cleanup-',text=True)
        try:
            with os.fdopen(fd,'w') as f:json.dump(proof,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
            os.replace(tmp,receipt)
        finally:
            if Path(tmp).exists():Path(tmp).unlink()
        return proof
    except Exception:
        for src,dst,h in reversed(moved):
            if not src.exists() and dst.is_file() and digest(dst)==h:dst.rename(src)
        raise CleanupError(tr("cleanup.aborted")) from None

def interactive(root,plan,exclude=None,input_fn=input,output=print,external=True):
    report=preview(root,plan,exclude,external);show(report,output)
    if input_fn(tr("cleanup.confirm")).strip()!='YES':raise CleanupError(tr("cleanup.cancelled"))
    proof=apply(root,plan,report,exclude,external)
    output(tr("cleanup.completed")+proof['archive']+tr("cleanup.receipt_location"))
    return proof

def receipt_status(root,plan):
    try:
        path=safe_path(root.resolve(),'update_check/state/cleanup.json')
        if not path.is_file():return 'NOCH_KEIN_LAUFNACHWEIS'
        record=json.loads(path.read_text())
        if record.get('plan_sha256')!=plan_digest(plan):return 'ANDERER_PLANSTAND'
        archive=safe_path(root.resolve(),record['archive'])
        if not str(archive.relative_to(root.resolve())).startswith('x/backups/controller_cleanup/'):return 'NACHWEIS_UNGUELTIG'
        for item in record['archived']:
            original=safe_path(root.resolve(),item['path']);saved=safe_path(archive,'files/'+item['path'])
            if original.exists() or not saved.is_file() or digest(saved)!=item['sha256']:return 'NACHWEIS_ABWEICHEND'
        return 'BEREINIGUNG_NACHGEWIESEN'
    except (OSError,ValueError,KeyError,CleanupError):return 'NACHWEIS_UNGUELTIG'

def standalone(plan):
    argv = cli_args(sys.argv[1:], Path("/root/ansible"))
    parser=argparse.ArgumentParser(description=tr("cleanup.description"))
    parser.add_argument("--lang", choices=("de", "en"), help=tr("cli.lang"))
    parser.add_argument('--root',type=Path,default=Path('/root/ansible'))
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args(argv)
    own=Path(sys.argv[0]).absolute()
    if own.is_symlink():raise CleanupError(tr("cleanup.helper_link"))
    own_hash=digest(own);own_stat=own.stat()
    if args.preview:show(preview(args.root,plan,own));return
    interactive(args.root,plan,own)
    if own.is_symlink() or own.stat().st_ino!=own_stat.st_ino or digest(own)!=own_hash:raise CleanupError(tr("cleanup.helper_changed"))
    own.unlink();print(tr("cleanup.removed"))
