#!/usr/bin/env python3
"""Entwicklungswerkzeug: pro Datei SHA aus ausdruecklich geprueftem OFFLINE-Release pflegen."""

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "update_check"))
from staging_manifest import public_library

FORBIDDEN = {
    'group_vars',
    'host_vars',
    'inventory',
    'artifacts',
    'collections',
    'x',
    '_local',
    'logs',
    'reports',
    '.git',
    '.ssh',
    'state',
}


def sha(p):
    hasher = hashlib.sha256()
    with p.open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(data)
    return hasher.hexdigest()


def safe(root, rel):
    relative_path = Path(rel)
    if (
        relative_path.is_absolute()
        or '..' in relative_path.parts
        or '\\' in rel
        or (any(part in FORBIDDEN for part in relative_path.parts) and not public_library(rel))
    ):
        raise ValueError('Kein Codepfad: ' + rel)
    result = (root / relative_path).resolve()
    if (
        not result.is_relative_to(root)
        or (public_library(rel) and result != root / relative_path)
        or not result.is_file()
    ):
        raise ValueError('Release-Datei fehlt oder verlaesst Releasewurzel: ' + rel)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--release-root',
        type=Path,
        required=True,
        help='Vollstaendiger gepruefter Offline-Releasebaum, niemals produktiver Controller',
    )
    parser.add_argument(
        '--check-dir',
        type=Path,
        required=True,
        help='Pruefdaten im Staging oder Offline-Release',
    )
    parser.add_argument(
        '--write',
        action='store_true',
        help='Manifest-SHA und Integritaet aktualisieren; sonst nur verifizieren',
    )
    parser.add_argument(
        '--release-source-reviewed',
        action='store_true',
        help='Explizite Bestaetigung: Offlinequellen fachlich geprueft; Drift nicht pauschal uebernehmen',
    )
    parser.add_argument(
        '--cleanup-script',
        type=Path,
        help='Geprueften Plan als selbstloeschenden Einmalhelfer exportieren',
    )
    args = parser.parse_args()
    root = args.release_root.resolve()
    here = args.check_dir.resolve()
    if args.write and not args.release_source_reviewed:
        parser.error(
            '--write verlangt --release-source-reviewed; nie Live-Drift automatisch freigeben.'
        )
    if root == Path('/root/ansible') or root.is_relative_to(Path('/root/ansible')):
        parser.error('Produktiver Standardpfad ist keine Offline-Releasequelle.')
    release = json.loads((here / 'release.json').read_text())
    changes = []
    outputs = {}
    for rel in release['manifests']:
        manifest = json.loads((here / rel).read_text())
        for code, wanted in manifest['files'].items():
            actual = sha(safe(root, code))
            if actual != wanted:
                changes.append(code)
            manifest['files'][code] = actual
        outputs[here / rel] = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
    for ext in sorted((here / 'extensions').glob('*/manifest.json')):
        manifest = json.loads(ext.read_text())
        for rel, wanted in manifest['files'].items():
            actual = sha(safe(root, rel))
            if actual != wanted:
                changes.append(rel)
            manifest['files'][rel] = actual
        outputs[ext] = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
        seal = json.loads((ext.parent / 'integrity.json').read_text())
        seal['manifest_sha256'] = hashlib.sha256(outputs[ext].encode()).hexdigest()
        outputs[ext.parent / 'integrity.json'] = (
            json.dumps(seal, indent=2, ensure_ascii=False) + '\n'
        )
    if args.write:
        # Verify every source before writing any seal.
        for path, text in outputs.items():
            path.write_text(text)
        seal = json.loads((here / 'integrity.json').read_text())
        seal['files'] = {rel: sha(safe(here, rel)) for rel in seal['files']}
        (here / 'integrity.json').write_text(
            json.dumps(seal, indent=2, ensure_ascii=False) + '\n'
        )
    else:
        seal = json.loads((here / 'integrity.json').read_text())
        for rel, wanted in seal['files'].items():
            if sha(safe(here, rel)) != wanted:
                changes.append('update_check/' + rel)
    if args.cleanup_script:
        if changes and not args.write:
            raise ValueError('Geaenderte Pruefdaten nicht als Helfer exportieren.')
        if args.cleanup_script.exists():
            raise ValueError('Ausgabedatei existiert bereits.')
        plan = json.loads((here / 'cleanup_plan.json').read_text())
        text = (here / 'cleanup.py').read_text()
        text += (
            '\nPLAN = '
            + repr(plan)
            + '''\nif __name__=='__main__':
    try:standalone(PLAN)
    except (CleanupError,OSError,EOFError,KeyboardInterrupt):
        print(tr('cleanup.abort'),file=sys.stderr)
        sys.exit(1)
'''
        )
        # A single Python zip application also works away from the controller checkout.
        languages = here.parent / "lib/i18n"
        with zipfile.ZipFile(
            args.cleanup_script, "x", compression=zipfile.ZIP_DEFLATED
        ) as bundle:
            bundle.writestr("__main__.py", text)
            bundle.write(here.parent / "scripts/controller_i18n.py", "controller_i18n.py")
            for catalog in sorted(languages.rglob("*.json")):
                bundle.write(catalog, catalog.relative_to(here.parent).as_posix())
    print(
        ('Aktualisiert' if args.write else 'Geprueft')
        + ': '
        + str(len(set(changes)))
        + ' unterschiedliche Code-/Pruefdateien. Keine Settings oder Secrets gehasht.'
    )
    return 0 if args.write or not changes else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError):
        raise SystemExit(
            'Release-/Pruefdaten ungueltig; keine automatische Freigabe. Eingaben pruefen.'
        )
