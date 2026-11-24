#!/usr/bin/env python3
"""Entwicklungswerkzeug: pro Datei SHA aus ausdruecklich geprueftem OFFLINE-Release pflegen."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "update_check"))
from staging_manifest import public_library

FORBIDDEN={'group_vars','host_vars','inventory','artifacts','collections','x','_local','logs','reports','.git','.ssh','state'}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
    return h.hexdigest()
def safe(root,rel):
    p=Path(rel)
    if p.is_absolute() or '..' in p.parts or '\\' in rel or (any(part in FORBIDDEN for part in p.parts) and not public_library(rel)):raise ValueError('Kein Codepfad: '+rel)
    result=(root/p).resolve()
    if not result.is_relative_to(root) or (public_library(rel) and result != root/p) or not result.is_file():raise ValueError('Release-Datei fehlt oder verlaesst Releasewurzel: '+rel)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--release-root',type=Path,required=True,help='Vollstaendiger gepruefter Offline-Releasebaum, niemals produktiver Controller')
    p.add_argument('--check-dir',type=Path,required=True,help='Pruefdaten im Staging oder Offline-Release')
    p.add_argument('--write',action='store_true',help='Manifest-SHA und Integritaet aktualisieren; sonst nur verifizieren')
    p.add_argument('--release-source-reviewed',action='store_true',help='Explizite Bestaetigung: Offlinequellen fachlich geprueft; Drift nicht pauschal uebernehmen')
    p.add_argument('--cleanup-script',type=Path,help='Geprueften Plan als selbstloeschenden Einmalhelfer exportieren')
    a=p.parse_args();root=a.release_root.resolve();here=a.check_dir.resolve()
    if a.write and not a.release_source_reviewed:p.error('--write verlangt --release-source-reviewed; nie Live-Drift automatisch freigeben.')
    if root==Path('/root/ansible') or root.is_relative_to(Path('/root/ansible')):p.error('Produktiver Standardpfad ist keine Offline-Releasequelle.')
    release=json.loads((here/'release.json').read_text());changes=[];outputs={}
    for rel in release['manifests']:
        m=json.loads((here/rel).read_text())
        for code,wanted in m['files'].items():
            actual=sha(safe(root,code))
            if actual!=wanted:changes.append(code)
            m['files'][code]=actual
        outputs[here/rel]=json.dumps(m,indent=2,ensure_ascii=False)+'\n'
    for ext in sorted((here/'extensions').glob('*/manifest.json')):
        m=json.loads(ext.read_text())
        for rel,wanted in m['files'].items():
            actual=sha(safe(root,rel))
            if actual!=wanted:changes.append(rel)
            m['files'][rel]=actual
        outputs[ext]=json.dumps(m,indent=2,ensure_ascii=False)+'\n'
        seal=json.loads((ext.parent/'integrity.json').read_text());seal['manifest_sha256']=hashlib.sha256(outputs[ext].encode()).hexdigest()
        outputs[ext.parent/'integrity.json']=json.dumps(seal,indent=2,ensure_ascii=False)+'\n'
    if a.write:
        # Erst alle Quelldateien pruefen; bis hier kein Schreibzugriff.
        for path,text in outputs.items():path.write_text(text)
        seal=json.loads((here/'integrity.json').read_text())
        seal['files']={rel:sha(safe(here,rel)) for rel in seal['files']}
        (here/'integrity.json').write_text(json.dumps(seal,indent=2,ensure_ascii=False)+'\n')
    else:
        seal=json.loads((here/'integrity.json').read_text())
        for rel,wanted in seal['files'].items():
            if sha(safe(here,rel))!=wanted:changes.append('update_check/'+rel)
    if a.cleanup_script:
        if changes and not a.write:raise ValueError('Geaenderte Pruefdaten nicht als Helfer exportieren.')
        if a.cleanup_script.exists():raise ValueError('Ausgabedatei existiert bereits.')
        plan=json.loads((here/'cleanup_plan.json').read_text());text=(here/'cleanup.py').read_text()
        text+='\nPLAN = '+repr(plan)+'''\nif __name__=='__main__':
    try:standalone(PLAN)
    except (CleanupError,OSError,EOFError,KeyboardInterrupt):
        print('Abbruch; Helfer bleibt erhalten. Vorschau/Archiv pruefen.',file=sys.stderr)
        sys.exit(1)
'''
        a.cleanup_script.write_text(text)
    print(('Aktualisiert' if a.write else 'Geprueft')+': '+str(len(set(changes)))+' unterschiedliche Code-/Pruefdateien. Keine Settings oder Secrets gehasht.')
    return 0 if a.write or not changes else 1
if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError,KeyError):raise SystemExit('Release-/Pruefdaten ungueltig; keine automatische Freigabe. Eingaben pruefen.')
