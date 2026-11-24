#!/usr/bin/env python3
"""Interaktiv Checkmk-Altbestand dem generierten Ansible-Inventar zuordnen."""
import argparse
import json
import os
from pathlib import Path
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

class MigrationError(Exception):
    pass


def inventory(root):
    executable = shutil.which('ansible-inventory')
    if not executable:
        raise MigrationError('ansible-inventory fehlt im PATH')
    proc = subprocess.run(
        [executable, '-i', str(root / 'inventory'), '--playbook-dir', str(root), '--list'],
        cwd=root, capture_output=True, text=True,
        env=dict(os.environ, ANSIBLE_NOCOLOR='1'),
    )
    if proc.returncode:
        raise MigrationError('Ansible-Inventar ist ungueltig: ' + proc.stderr.strip())
    try:
        data = json.loads(proc.stdout)
        names = data['checkmk_inventory_hosts']['hosts']
        hostvars = data['_meta']['hostvars']
    except (ValueError, KeyError, TypeError) as exc:
        raise MigrationError('Gruppe checkmk_inventory_hosts fehlt im Inventory') from exc
    desired = []
    for name in sorted(names):
        values = hostvars.get(name, {})
        target = str(values.get('checkmk_hostname', name)).strip()
        address = str(values.get('ansible_host', '')).strip()
        folder = str(values.get('checkmk_target_folder', '')).strip()
        if not target or not address or not folder:
            raise MigrationError('%s: Checkmk-Name, IP oder Zielordner fehlt' % name)
        desired.append({
            'inventory_host': name,
            'checkmk_hostname': target,
            'ipaddress': address,
            'folder': folder,
            'alias': str(values.get('checkmk_alias', name)),
        })
    target_names = [item['checkmk_hostname'] for item in desired]
    if len(target_names) != len(set(target_names)):
        raise MigrationError('Doppelte Checkmk-Zielnamen im Inventory')
    common = hostvars.get(names[0], {}) if names else {}
    return desired, common


class CheckmkAPI:
    def __init__(self, server_url, site, user, secret, validate_certs=True):
        if not isinstance(validate_certs, bool):
            raise MigrationError("TLS-Schalter fuer Migrationsplan muss true oder false sein")
        self.ssl_context = ssl.create_default_context()
        if not validate_certs:
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
        self.base = server_url.rstrip('/') + '/' + site + '/check_mk/api/v1'
        self.headers = {
            'Authorization': 'Bearer %s %s' % (user, secret),
            'Accept': 'application/json',
        }

    def get(self, path):
        request = urllib.request.Request(self.base + path, headers=self.headers)
        try:
            with urllib.request.urlopen(request, timeout=30, context=self.ssl_context) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            code = exc.code
            exc.close()
            raise MigrationError('Checkmk API GET %s: HTTP %s' % (path, code)) from None
        except (OSError, ValueError) as exc:
            raise MigrationError('Checkmk API nicht erreichbar oder Antwort ungueltig') from exc

    def hosts(self):
        payload = self.get('/domain-types/host_config/collections/all?effective_attributes=true')
        result = []
        for item in payload.get('value', []):
            name = str(item.get('id', '')).strip()
            extensions = item.get('extensions', {}) or {}
            attributes = extensions.get('attributes') or extensions.get('effective_attributes') or {}
            if name:
                result.append({
                    'name': name,
                    'ipaddress': str(attributes.get('ipaddress', '')).strip(),
                    'folder': str(extensions.get('folder', attributes.get('folder', ''))).strip(),
                })
        return sorted(result, key=lambda item: item['name'].lower())


def short_name(value):
    return value.lower().split('.')[0]


def automatic_target(current, remaining):
    if current['ipaddress']:
        hits = [item for item in remaining if item['ipaddress'] == current['ipaddress']]
        if len(hits) == 1:
            return hits[0], 'ipaddress'
    hits = [item for item in remaining if short_name(item['inventory_host']) == short_name(current['name'])]
    if len(hits) == 1:
        return hits[0], 'short_name'
    return None, None


def choose_target(current, remaining):
    print('\nCheckmk-Altbestand passt nicht zum Zielschema:')
    print('  Host:   %s' % current['name'])
    print('  IP:     %s' % (current['ipaddress'] or '-'))
    print('  Ordner: %s' % (current['folder'] or '-'))
    print('\nNoch nicht zugeordnete Inventory-Ziele:')
    for number, item in enumerate(remaining, 1):
        print('  %2d) %-24s -> %-36s %s' % (
            number, item['inventory_host'], item['checkmk_hostname'], item['ipaddress']))
    while True:
        answer = input('Zuordnung [1-%d], s=ueberspringen, q=abbrechen: ' % len(remaining)).strip().lower()
        if answer == 's':
            return None
        if answer == 'q':
            raise MigrationError('Migration durch Benutzer abgebrochen')
        if answer.isdigit() and 1 <= int(answer) <= len(remaining):
            return remaining[int(answer) - 1]
        print('Ungueltige Auswahl.')


def confirm_automatic(current, target, matched_by):
    print('\nCheckmk-Altbestand passt nicht zum Zielschema:')
    print('  %s (%s) -> %s (%s)' % (
        current['name'], current['ipaddress'] or '-',
        target['checkmk_hostname'], target['ipaddress']))
    while True:
        answer = input(
            'Vorschlag ueber %s: ENTER=uebernehmen, a=andere Auswahl, '
            's=ueberspringen, q=abbrechen: ' % matched_by
        ).strip().lower()
        if not answer:
            return target
        if answer == 'a':
            return False
        if answer == 's':
            return None
        if answer == 'q':
            raise MigrationError('Migration durch Benutzer abgebrochen')
        print('Ungueltige Auswahl.')


def publish(path, document):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as handle:
        json.dump(document, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
        temporary = Path(handle.name)
    temporary.chmod(0o600)
    os.replace(temporary, path)


def run(args):
    if not sys.stdin.isatty():
        raise MigrationError('Interaktive Migration benoetigt ein Terminal')
    root = Path(args.root).resolve()
    desired, common = inventory(root)
    user = common.get('checkmk_api_user') or common.get('checkmk_registration_user')
    secret = common.get('checkmk_api_password') or common.get('checkmk_registration_password')
    if not all((common.get('checkmk_server_url'), common.get('checkmk_site'), user, secret)):
        raise MigrationError('Checkmk-Endpunkt oder API-Credentials fehlen')
    tls = common.get('tls_validate_certs', {})
    if not isinstance(tls, dict):
        raise MigrationError('tls_validate_certs muss eine YAML-Zuordnung sein')
    current = CheckmkAPI(
        common['checkmk_server_url'], common['checkmk_site'], user, secret,
        validate_certs=tls.get('checkmk_migration_plan_read', common.get('tls_validate_certs_default', True))
    ).hosts()
    desired_names = {item['checkmk_hostname'] for item in desired}
    existing_names = {item['name'] for item in current}
    remaining = [item for item in desired if item['checkmk_hostname'] not in existing_names]
    legacy = [item for item in current if item['name'] not in desired_names]
    mappings, skipped = [], []
    for old in legacy:
        target, matched_by = automatic_target(old, remaining)
        if target:
            confirmed = confirm_automatic(old, target, matched_by)
            if confirmed is False:
                target = choose_target(old, remaining)
                matched_by = 'interactive' if target else None
            else:
                target = confirmed
        elif remaining:
            target = choose_target(old, remaining)
            matched_by = 'interactive' if target else None
        else:
            target = None
        if not target:
            skipped.append(old['name'])
            continue
        mappings.append({
            'source': old['name'],
            'target_inventory_host': target['inventory_host'],
            'target_checkmk_hostname': target['checkmk_hostname'],
            'target_ipaddress': target['ipaddress'],
            'target_folder': target['folder'],
            'target_alias': target['alias'],
            'matched_by': matched_by,
        })
        remaining.remove(target)
    output = Path(args.output) if args.output else root / 'x/reports/checkmk_migration_plan.yml'
    plan = {
        'checkmk_site': common['checkmk_site'],
        'mappings': mappings,
        'targets': desired,
        'already_correct': sorted(desired_names.intersection(existing_names)),
        'skipped_checkmk_hosts': skipped,
        'unmatched_inventory_hosts': [item['inventory_host'] for item in remaining],
    }
    publish(output, plan)
    print('\nPlan gespeichert: %s' % output)
    print('Umbenennungen: %d | bereits korrekt: %d | uebersprungen: %d | ohne Quelle: %d' % (
        len(mappings), len(plan['already_correct']), len(skipped), len(remaining)))
    print('Es wurden keine Checkmk-Aenderungen ausgefuehrt.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument('--output')
    args = parser.parse_args()
    try:
        run(args)
    except MigrationError as exc:
        print('Checkmk-Migrationsfehler: %s' % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
