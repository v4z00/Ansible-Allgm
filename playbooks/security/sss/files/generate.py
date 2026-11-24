#!/usr/bin/env python3
"""Generate personalized documents only below /root/rescue/SSS."""
import argparse
import datetime
import getpass
import html
import itertools
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import uuid

# Deployed scripts are in bin/ and offline/; source tests import from files/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'offline'))
from recover import combine, encode, harden, run_ssss, validate_password, validate_bundle, MAX_BUNDLE_BYTES

BASE = Path('/root/rescue/SSS')


def validate(config):
    settings, people = config['settings'], config['people']
    if settings.get('konfiguration_bestaetigt') is not True:
        raise ValueError('config.yml ausfüllen und konfiguration_bestaetigt auf true setzen.')
    for key in ('kontakt', 'datenorte', 'master_anlass', 'infra_anlass'):
        if not isinstance(settings.get(key), str) or not settings[key].strip() or 'BITTE EINTRAGEN' in settings[key]:
            raise ValueError(f'Angabe {key} fehlt.')
    if not isinstance(people, list) or not people:
        raise ValueError('Treuhänderliste fehlt.')
    names, ids = set(), set()
    for p in people:
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', p['id']) or p['id'] in ids:
            raise ValueError('Personen-ID ungültig oder doppelt.')
        ids.add(p['id'])
        if any(not isinstance(p[k], str) or not p[k].strip() for k in ('vorname', 'nachname')):
            raise ValueError('Vorname und Nachname erforderlich.')
        name = (p['vorname'].strip().casefold(), p['nachname'].strip().casefold())
        if name in names or 'beispiel' in name[0] or name[1] == 'ersetzen':
            raise ValueError('Beispielpersonen ersetzen; doppelte Namen eindeutig unterscheiden.')
        names.add(name)
        if p['master_id'] is False and p['infra_id'] is False:
            raise ValueError('Jede Person muss mindestens einen Teil erhalten.')
    for kind in ('master', 'infra'):
        t, n = settings[kind]['threshold'], settings[kind]['shares']
        if type(t) is not int or type(n) is not int or not 2 <= t <= n <= 20:
            raise ValueError('Erforderlich: 2 <= threshold <= shares <= 20.')
        if sum(1 for _ in itertools.combinations(range(n), t)) > 1000:
            raise ValueError('Maximal 1000 Prüfkombinationen pro Bereich erlaubt.')
        assigned = []
        for p in people:
            value = p[kind + '_id']
            if value is False:
                continue
            if type(value) is not int or not 1 <= value <= n:
                raise ValueError(f'{kind}: IDs müssen Ganzzahlen von 1 bis {n} oder false sein.')
            assigned.append(value)
        if sorted(assigned) != list(range(1, n + 1)):
            raise ValueError(f'{kind}: Jede ID von 1 bis {n} muss genau einmal vergeben sein.')


def split_bytes(raw, scheme):
    if not 1 <= len(raw) <= 127:
        raise ValueError('Ungültige Blocklänge.')
    payload = b'\x01' + raw
    bits = max(64, len(payload) * 8)
    t, n = scheme['threshold'], scheme['shares']
    result = run_ssss('ssss-split', ['-t', str(t), '-n', str(n), '-s', str(bits), '-x', '-Q'],
                      payload.hex().zfill(bits // 4) + '\n')
    shares = result.stdout.splitlines()
    if len(shares) != n:
        raise ValueError('Unerwartete Anzahl generierter Teile.')
    return shares


def split(secret, run, kind, scheme):
    validate_password(secret)
    t, n = scheme['threshold'], scheme['shares']
    shares = split_bytes(secret.encode('utf-8'), scheme)
    envelopes = [encode(run, kind, t, n, share) for share in shares]
    # Every quorum is verified before any private document is written.
    for quorum in itertools.combinations(envelopes, t):
        if combine(quorum) != secret:
            raise ValueError('Roundtrip-Prüfung fehlgeschlagen; keine Ausgabe erstellt.')
    return envelopes


def split_bundle(bundle, run, scheme):
    validate_bundle(bundle)
    raw = json.dumps(bundle, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if len(raw) > MAX_BUNDLE_BYTES:
        raise ValueError('Zugangsdaten-Paket überschreitet die maximale Größe.')
    t, n = scheme['threshold'], scheme['shares']
    blocks = [split_bytes(raw[i:i + 127], scheme) for i in range(0, len(raw), 127)]
    envelopes = [encode(run, 'master', t, n, '~'.join(block[j] for block in blocks), version='SSS2')
                 for j in range(n)]
    for quorum in itertools.combinations(envelopes, t):
        if combine(quorum) != bundle:
            raise ValueError('Roundtrip-Prüfung der Zugangsdaten fehlgeschlagen; keine Ausgabe erstellt.')
    return envelopes


def prompt_second_factor(password):
    print('Zusätzlich zum Vaultwarden-Master-Passwort sichern:')
    print('1 = TOTP-Einrichtungsschlüssel, 2 = 2FA-Wiederherstellungscode, 0 = nur Passwort')
    choice = input('Art auswählen (0/1/2): ').strip()
    if choice == '0':
        return None
    if choice not in ('1', '2'):
        raise ValueError('Bitte 0, 1 oder 2 wählen; es wurde kein Satz erzeugt.')
    kind = 'totp' if choice == '1' else 'recovery_code'
    label = 'TOTP-Einrichtungsschlüssel (kein aktueller sechsstelliger Code)' if choice == '1' else '2FA-Wiederherstellungscode'
    first = getpass.getpass(label + ': ')
    second = getpass.getpass('Zweiten Zugangsschlüssel wiederholen: ')
    if kind == 'totp':
        first, second = (''.join(value.split()).upper().rstrip('=') for value in (first, second))
    if first != second:
        raise ValueError('Die Eingaben des zweiten Zugangsschlüssels stimmen nicht überein.')
    bundle = {'password': password, 'second_factor_type': kind, 'second_factor': first}
    validate_bundle(bundle)
    return bundle


def document(person, settings, run, shares):
    lines = ['DIGITALER NACHLASS & IT-NOTFALL',
             f"FÜR: {person['vorname']} {person['nachname']}", f'Satz-ID: {run}', '',
             f"Hallo {person['vorname']},", '',
             'bewahre diesen Brief verschlossen und getrennt von anderen Schlüsselteilen auf.',
             'Prüfe bei Übergabe das vereinbarte Siegel. Bei Beschädigung den Administrator informieren.',
             'Ein Teil allein reicht nicht. Nur unterschiedliche Teile desselben Bereichs und Satzes kombinieren.', '',
             'TECHNISCHE HILFE', settings['kontakt'], '',
             'TRESORE UND OFFLINE-MEDIUM', settings['datenorte'], '']
    for kind, title in [('master', 'MASTER – VAULTWARDEN / DIGITALER NACHLASS'), ('infra', 'INFRASTRUKTUR – IT-NOTFALL')]:
        index = person[kind + '_id']
        if index is False:
            continue
        scheme = settings[kind]
        purpose = ('Diese Teile rekonstruieren das Master-Passwort und bei SSS2 zusätzlich den zweiten Zugangsschlüssel.'
                   if kind == 'master' else 'Diese Teile rekonstruieren das vereinbarte Infrastruktur-Passwort.')
        lines += [title, purpose, settings[kind + '_anlass'],
                  f"Dein Teil: {index} von {scheme['shares']}. Benötigt: {scheme['threshold']} unterschiedliche Teile.",
                  'Vollständiger Schlüsselteil (von SSS1/SSS2 bis zum Ende der Prüfsumme; alle Blöcke übernehmen):',
                  shares[kind][index - 1], '']
    lines += ['WIEDERHERSTELLUNG',
              '1. Technische Hilfe kontaktieren und die Notfalldokumentation bereitstellen.',
              '2. Vorbereiteten Notfallrechner starten; Plattform-Einrichtung siehe START-HIER.md.',
              '3. Windows: start-html.bat; macOS: start-html.command; Linux: bash start-html.sh.',
              '   Der Browser öffnet sich nach Möglichkeit automatisch; sonst die angezeigte Adresse öffnen.',
              '   Alternative ohne Startskript: python3 recover.py --web',
              '4. Vollständige SSS1/SSS2-Teile eingeben; auf Satz-ID und Bereich achten.',
              '5. Zugangsdaten anzeigen lassen. Passwort und zweiter Zugangsschlüssel erscheinen getrennt.',
              '   Ein TOTP-Secret ist der Einrichtungsschlüssel für den Authenticator, kein aktueller Login-Code.',
              '   Einen Wiederherstellungscode nur für das dokumentierte 2FA-Notfallverfahren verwenden.',
              '   MASTER: Vaultwarden-Master-Passwort; Serveradresse, Konto und ggf. 2FA laut Dokumentation.',
              '   INFRA: den in der Dokumentation festgelegten Infrastruktur-Zugang verwenden.',
              '   KDBX ist die Offline-Notfallvariante. Passwortzuordnung und Zusatzfaktoren separat prüfen.',
              '   Das Vaultwarden-Master-Passwort öffnet die KDBX nur, wenn diese entsprechend eingerichtet ist.', '',
              'KI-HILFE OHNE GEHEIMNISSE',
              'Frage bei Bedarf: „Wir haben Vaultwarden, eine KDBX-Offline-Notfallvariante und recover.py',
              'für Shamir-Schlüsselteile. Erkläre uns in einfacher Sprache die lokale Bedienung.“',
              'Keine Schlüsselteile, Passwörter oder Tresore in Chats oder Online-Tools eingeben.']
    return '\n'.join(lines) + '\n'


def render_html(text):
    return '''<!doctype html><html lang="de"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>Persönlicher Notfallbrief</title><style>
@page { size: A4; margin: 16mm; }
body { max-width: 180mm; margin: 20px auto; color: #162331; background: white; }
pre { font: 10pt/1.45 monospace; white-space: pre-wrap; overflow-wrap: anywhere; }
@media print { body { margin: 0; max-width: none; } }
</style><pre>''' + html.escape(text) + '</pre></html>\n'


def secure_directory(path):
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode) != 0o700:
        raise ValueError('Ausgabeverzeichnisse müssen echte root-eigene Verzeichnisse mit Modus 0700 sein.')


def write_private(path, content):
    with path.open('x', encoding='utf-8') as handle:
        handle.write(content)


def generate(config):
    validate(config)
    if os.geteuid() != 0:
        raise ValueError('Generator auf dem Ansible-Host als root starten.')
    for path in (Path('/root/rescue'), BASE, BASE / 'ausgaben'):
        secure_directory(path)
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise ValueError('Generator in einem interaktiven Terminal ohne Umleitung starten.')
    run = uuid.uuid4().hex
    print(f'Neuer Satz: {run}. Bestehende Ausgaben werden nicht verändert.')
    if input('Neue persönliche Umschläge erzeugen? Tippe GENERIEREN: ') != 'GENERIEREN':
        return
    secrets = {}
    for kind in ('master', 'infra'):
        prompt = ('MASTER – bestehendes Vaultwarden-Master-Passwort: ' if kind == 'master'
                  else 'INFRA – vereinbartes Infrastruktur-Passwort: ')
        value = getpass.getpass(prompt)
        if value != getpass.getpass('Passwort wiederholen: '):
            raise ValueError('Passworteingaben stimmen nicht überein.')
        secrets[kind] = value
    if secrets['master'] == secrets['infra']:
        raise ValueError('Master und Infra benötigen unterschiedliche Passwörter.')
    bundle = prompt_second_factor(secrets['master'])
    print('Erzeuge Teile und prüfe sämtliche erforderlichen Kombinationen …')
    shares = {
        'master': split_bundle(bundle, run, config['settings']['master']) if bundle
                  else split(secrets['master'], run, 'master', config['settings']['master']),
        'infra': split(secrets['infra'], run, 'infra', config['settings']['infra'])}
    del secrets
    del bundle
    destination = BASE / 'ausgaben' / run
    destination.mkdir(mode=0o700)
    # A failed write remains visibly incomplete; nothing is silently removed or overwritten.
    write_private(destination / 'UNVOLLSTAENDIG', 'Nicht verteilen: Ausgabe wurde nicht abgeschlossen.\n')
    for person in config['people']:
        text = document(person, config['settings'], run, shares)
        write_private(destination / (person['id'] + '.txt'), text)
        write_private(destination / (person['id'] + '.html'), render_html(text))
    manifest = {'satz_id': run, 'erstellt_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'format': 'SSS1 password or SSS2 master bundle / independent ssss hex blocks / diffusion enabled / 01 prefix',
                'settings': config['settings'], 'people': config['people'], 'alle_quoren_geprueft': True}
    write_private(destination / 'manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (destination / 'UNVOLLSTAENDIG').unlink()
    print(f'Fertig: {destination}')
    print('Pro Person die HTML-Datei lokal öffnen und drucken. TXT ist die alternative Darstellung desselben Briefs.')
    print('Vor Verteilung Vaultwarden-Zugang und Infra-Zugang testen; KDBX-Offline-Variante separat prüfen.')


def main():
    harden()
    parser = argparse.ArgumentParser()
    parser.add_argument('--validate', action='store_true', help='Nur bereitgestellte Konfiguration prüfen')
    args = parser.parse_args()
    config = json.loads((BASE / 'config.json').read_text(encoding='utf-8'))
    if args.validate:
        validate(config)
        print('Konfiguration gültig.')
    else:
        generate(config)


if __name__ == '__main__':
    try:
        main()
    except ValueError as exc:
        print(f'Abbruch: {exc}', file=sys.stderr)
        sys.exit(1)
    except (OSError, KeyError, TypeError, subprocess.SubprocessError, getpass.GetPassWarning):
        print('Abbruch: Konfiguration, Verzeichnisrechte und Installation prüfen. Unvollständige Ausgaben nicht verteilen.', file=sys.stderr)
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print('\nAbgebrochen. Eventuelle unvollständige Ausgabe nicht verteilen.', file=sys.stderr)
        sys.exit(130)
