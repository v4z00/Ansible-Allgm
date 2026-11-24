#!/usr/bin/env python3
"""Offline recovery for SSS1 envelopes; Python stdlib + ssss, no network."""
import getpass
import argparse
import base64
import binascii
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import re
import resource
import secrets
import shutil
import subprocess
import sys
import threading
import warnings
import webbrowser


def harden():
    os.umask(0o077)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    warnings.simplefilter('error', getpass.GetPassWarning)


MAX_BUNDLE_BYTES = 1024
MAX_BLOCKS = 9


def validate_password(value):
    if (not isinstance(value, str) or not 1 <= len(value.encode('utf-8')) <= 127
            or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise ValueError('Passwort: 1–127 UTF-8-Bytes, keine Steuerzeichen.')


def validate_bundle(bundle):
    if not isinstance(bundle, dict) or set(bundle) != {'password', 'second_factor_type', 'second_factor'}:
        raise ValueError('Ungültiges Format der Vaultwarden-Zugangsdaten.')
    validate_password(bundle['password'])
    kind, value = bundle['second_factor_type'], bundle['second_factor']
    if kind not in ('totp', 'recovery_code') or not isinstance(value, str):
        raise ValueError('Zweiter Zugangsschlüssel muss TOTP-Secret oder 2FA-Wiederherstellungscode sein.')
    if not value.strip() or len(value.encode('utf-8')) > 128 or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError('Zweiter Zugangsschlüssel: 1–128 UTF-8-Bytes, keine Steuerzeichen.')
    if kind == 'totp':
        if not re.fullmatch(r'[A-Z2-7]+', value):
            raise ValueError('TOTP: Base32-Einrichtungsschlüssel verwenden, keinen QR-Link oder aktuellen sechsstelligen Code.')
        try:
            decoded = base64.b32decode(value + '=' * (-len(value) % 8))
        except (binascii.Error, ValueError):
            raise ValueError('TOTP-Einrichtungsschlüssel hat kein gültiges Base32-Format.') from None
        if len(decoded) < 10:
            raise ValueError('TOTP-Einrichtungsschlüssel ist zu kurz.')


def encode(run, kind, threshold, count, raw, version='SSS1'):
    body = f'{version}|{run}|{kind}|{threshold}|{count}|{raw}'
    return body + '|' + hashlib.sha256(body.encode('ascii')).hexdigest()[:16]


def parse(value):
    value = ''.join(value.split())
    parts = value.split('|')
    if len(parts) != 7 or parts[0] not in ('SSS1', 'SSS2'):
        raise ValueError('Vollständigen SSS1- oder SSS2-Schlüsselteil eingeben.')
    version, run, kind, threshold, count, raw, checksum = parts
    if not re.fullmatch(r'[0-9a-f]{32}', run) or kind not in ('master', 'infra'):
        raise ValueError('Satz-ID oder Bereich ungültig.')
    if not threshold.isdecimal() or not count.isdecimal():
        raise ValueError('Schwellenwert ungültig.')
    t, n = int(threshold), int(count)
    blocks = raw.split('~')
    if not 2 <= t <= n <= 20 or not 1 <= len(blocks) <= MAX_BLOCKS:
        raise ValueError('Schlüsselteil hat ein ungültiges Format.')
    if (version == 'SSS1' and len(blocks) != 1) or (version == 'SSS2' and kind != 'master'):
        raise ValueError('Format passt nicht zum gewählten Bereich.')
    indices = []
    for block in blocks:
        match = re.fullmatch(r'([0-9]{1,3})-([0-9a-fA-F]{16,256})', block)
        if not match or len(match[2]) % 2 or not 1 <= int(match[1]) <= n:
            raise ValueError('Blockformat oder Teilnummer ungültig.')
        indices.append(int(match[1]))
    if len(set(indices)) != 1:
        raise ValueError('Alle Blöcke eines persönlichen Teils müssen dieselbe Teilnummer haben.')
    expected = hashlib.sha256('|'.join(parts[:-1]).encode('ascii')).hexdigest()[:16]
    if not hmac.compare_digest(checksum, expected):
        raise ValueError('Prüfsumme falsch: Schlüsselteil nochmals vom Original übernehmen.')
    return (run, kind, t, n, version, len(blocks)), indices[0], raw


def run_ssss(program, args, value):
    executable = shutil.which(program)
    if not executable:
        raise ValueError(f'{program} fehlt. Paket ssss auf diesem Offline-Rechner vorbereiten.')
    result = subprocess.run([executable, *args], input=value, text=True,
                            encoding='ascii', capture_output=True, timeout=60, check=False)
    if result.returncode:
        # stderr may contain secrets; never propagate it into errors or logs.
        raise ValueError(f'{program} fehlgeschlagen; Eingaben und Installation prüfen.')
    return result


def combine(values, kind=None):
    parsed = [parse(value) for value in values]
    if not parsed:
        raise ValueError('Keine Schlüsselteile vorhanden.')
    metadata = parsed[0][0]
    if kind is not None:
        expected = {'infra': 2, 'master': 3}
        if kind not in expected or metadata[1] != kind or metadata[2] != expected[kind]:
            raise ValueError('Teile passen nicht zur Auswahl: Infrastruktur benötigt 2 Personen, Master 3 Personen.')
    if any(p[0] != metadata for p in parsed):
        raise ValueError('Unterschiedliche Sätze oder Bereiche dürfen nicht gemischt werden.')
    if len(parsed) != metadata[2]:
        raise ValueError(f'Genau {metadata[2]} unterschiedliche Teile erforderlich.')
    if len({p[1] for p in parsed}) != len(parsed):
        raise ValueError('Ein Schlüsselteil wurde doppelt eingegeben.')
    blocks = [p[2].split('~') for p in parsed]
    payload = b''.join(combine_block([row[i] for row in blocks], metadata[2]) for i in range(metadata[5]))
    if metadata[4] == 'SSS2':
        if len(payload) > MAX_BUNDLE_BYTES:
            raise ValueError('Zugangsdaten-Paket zu groß.')
        try:
            bundle = json.loads(payload.decode('utf-8'))
        except (UnicodeError, ValueError):
            raise ValueError('Zugangsdaten-Paket konnte nicht gelesen werden.') from None
        validate_bundle(bundle)
        return bundle
    try:
        secret = payload.decode('utf-8')
    except UnicodeError:
        raise ValueError('Rekonstruktion ist kein gültiges UTF-8-Passwort.') from None
    validate_password(secret)
    return secret


def combine_block(raw_parts, threshold):
    if len({len(part.split('-')[1]) for part in raw_parts}) != 1:
        raise ValueError('Schlüsselteile haben unterschiedliche Längen.')
    result = run_ssss('ssss-combine', ['-t', str(threshold), '-x', '-Q'], '\n'.join(raw_parts) + '\n')
    # ssss writes the recovered value to stderr, even in quiet mode.
    lines = [line for line in result.stderr.splitlines()
             if re.fullmatch(r'[0-9a-fA-F]{16,256}', line)]
    if len(lines) != 1:
        raise ValueError('Unerwartete Ausgabe von ssss-combine.')
    payload = bytes.fromhex(lines[0]).lstrip(b'\x00')
    if not payload.startswith(b'\x01'):
        raise ValueError('Rekonstruktion ungültig; Originalteile prüfen.')
    return payload[1:]


def main():
    harden()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--web', action='store_true', help='Lokale Offline-HTML-Oberfläche starten')
    parser.add_argument('--open-browser', action='store_true', help='Mit --web: lokalen Browser nach Möglichkeit öffnen')
    parser.add_argument('--stop-on-stdin-close', action='store_true', help='Mit --web: Dienst beim Schließen des Starters beenden')
    args = parser.parse_args()
    if args.open_browser and not args.web:
        parser.error('--open-browser benötigt --web')
    if args.stop_on_stdin_close and not args.web:
        parser.error('--stop-on-stdin-close benötigt --web')
    if not shutil.which('ssss-combine'):
        installer = Path(__file__).with_name('install-voraussetzungen.sh')
        if not installer.is_file():
            raise ValueError('ssss fehlt. Bitte start-html.sh mit Installationshilfe verwenden.')
        subprocess.run(['bash', str(installer)], check=True)
        if not shutil.which('ssss-combine'):
            raise ValueError('ssss-combine ist nach der Installation nicht verfügbar.')
    if args.web:
        serve_web(open_browser=args.open_browser, stop_on_stdin_close=args.stop_on_stdin_close)
        return
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise ValueError('In einem lokalen Terminal ohne Umleitung starten.')
    print('Offline-Wiederherstellung. Kein Internet nötig. Keine Terminalaufzeichnung verwenden.')
    first = getpass.getpass('Erster vollständiger SSS1/SSS2-Schlüsselteil: ')
    metadata, _, _ = parse(first)
    print(f'Bereich: {metadata[1]} | Satz: {metadata[0]} | benötigt: {metadata[2]} Teile')
    values = [first]
    for i in range(1, metadata[2]):
        values.append(getpass.getpass(f'Schlüsselteil {i + 1}/{metadata[2]}: '))
    recovered = combine(values)
    bundle = recovered if isinstance(recovered, dict) else None
    secret = bundle['password'] if bundle else recovered
    if input('Zugangsdaten jetzt sichtbar anzeigen? Tippe ANZEIGEN: ') != 'ANZEIGEN':
        print('Beendet, ohne das Passwort anzuzeigen.')
        return
    print('\nPasswort (einschließlich eventueller Leerzeichen zwischen den Markierungen):')
    print('>>> ' + secret + ' <<<')
    if bundle:
        label = 'TOTP-Einrichtungsschlüssel' if bundle['second_factor_type'] == 'totp' else '2FA-Wiederherstellungscode'
        print('\n' + label + ':')
        print('>>> ' + bundle['second_factor'] + ' <<<')
        print('TOTP-Secret lokal in einen vertrauenswürdigen Authenticator übernehmen; Wiederherstellungscode nur im vorgesehenen Notfallverfahren verwenden.')
    if metadata[1] == 'master':
        print('\nMASTER: Dies ist das Vaultwarden-Master-Passwort. Konto, Serveradresse und ggf. 2FA laut Dokumentation verwenden.')
    else:
        print('\nINFRA: Dieses Passwort für den dokumentierten Infrastruktur-Zugang verwenden.')
    print('Die KDBX ist die Offline-Notfallvariante; deren Passwortzuordnung und Zusatzfaktoren separat prüfen.')
    print('Anschließend Terminal schließen. Den tatsächlichen Zugang mit dem Ergebnis prüfen.')


def create_server():
    page = Path(__file__).with_name('notfall_entschluesselung.html').read_bytes()
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def setup(self):
            super().setup()
            self.connection.settimeout(10)

        def respond(self, code, body, content_type='application/json; charset=utf-8'):
            self.send_response(code)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.headers.get('Host') != self.server.expected_host or self.path != '/' + token + '/':
                self.respond(404, b'{}')
                return
            self.respond(200, page, 'text/html; charset=utf-8')

        def do_POST(self):
            if (self.headers.get('Host') != self.server.expected_host
                    or self.headers.get('Origin') != 'http://' + self.server.expected_host
                    or self.path != '/' + token + '/combine'):
                self.respond(403, b'{}')
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 120000 or self.headers.get('Content-Type') != 'application/json':
                    raise ValueError('Ungültige Anfrage.')
                data = json.loads(self.rfile.read(length))
                values = data.get('shares')
                if not isinstance(values, list) or not 2 <= len(values) <= 20 or any(not isinstance(v, str) for v in values):
                    raise ValueError('Schlüsselteile fehlen oder sind ungültig.')
                kind = data.get('kind')
                if not isinstance(kind, str) or kind not in ('infra', 'master'):
                    raise ValueError('Bitte Infrastruktur (2 Personen) oder Master (3 Personen) auswählen.')
                recovered = combine(values, kind=kind)
                data = ({'secret': recovered['password'], 'second_factor_type': recovered['second_factor_type'],
                         'second_factor': recovered['second_factor']} if isinstance(recovered, dict)
                        else {'secret': recovered, 'second_factor_type': None, 'second_factor': None})
                self.respond(200, json.dumps(data).encode('utf-8'))
            except ValueError as exc:
                self.respond(400, json.dumps({'error': str(exc)}).encode('utf-8'))
            except (OSError, subprocess.SubprocessError, TypeError, AttributeError):
                self.respond(400, b'{"error":"Lokale Wiederherstellung fehlgeschlagen."}')

    server = HTTPServer(('127.0.0.1', 0), Handler)
    server.expected_host = f'127.0.0.1:{server.server_port}'
    return server, f'http://{server.expected_host}/{token}/'


def open_local_browser(url):
    if sys.platform.startswith('linux') and not (os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY')):
        print('Keine grafische Sitzung erkannt. Die Adresse im Browser dieses Rechners öffnen.', flush=True)
        return
    try:
        opened = webbrowser.open(url, new=2)
    except Exception:
        opened = False
    if not opened:
        print('Browser konnte nicht automatisch geöffnet werden. Die angezeigte Adresse manuell öffnen.', flush=True)


def stop_when_input_closes(server, stream):
    try:
        while stream.read(1):
            pass
    finally:
        server.shutdown()


def serve_web(open_browser=False, stop_on_stdin_close=False):
    server, url = create_server()
    print('Offline-Oberfläche läuft nur auf diesem Rechner. Im lokalen Browser öffnen:')
    print(url, flush=True)
    print('Beenden mit Strg+C. Keine Netzwerkfreigabe oder Portweiterleitung einrichten.', flush=True)
    try:
        if stop_on_stdin_close:
            threading.Thread(target=stop_when_input_closes, args=(server, sys.stdin.buffer), daemon=True).start()
        if open_browser:
            # A browser launcher can block; the recovery server must remain responsive.
            threading.Thread(target=open_local_browser, args=(url,), daemon=True).start()
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError, getpass.GetPassWarning):
        print('Wiederherstellung fehlgeschlagen. Originalteile, gleichen Satz, unterschiedliche IDs und ssss-Installation prüfen.', file=sys.stderr)
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print('\nAbgebrochen.', file=sys.stderr)
        sys.exit(130)
