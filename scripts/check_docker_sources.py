#!/usr/bin/env python3
"""Read-only controller-side checks. Never print rendered Compose/env data."""
import fnmatch
import ipaddress
import json
from pathlib import Path
import subprocess
import sys

try:
    import yaml
except ImportError:
    print('FEHLER: PyYAML fehlt im Python des Ansible-Controllers.')
    sys.exit(1)


class DuplicateKey(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        seen = set()
        # Check explicit keys before expanding YAML merges. Explicit overrides
        # of inherited anchor keys remain legal; repeated explicit keys do not.
        for key, _ in node.value:
            if key.tag == 'tag:yaml.org,2002:merge':
                continue
            value = self.construct_object(key, deep=deep)
            if value in seen:
                raise DuplicateKey(f'Doppelter YAML-Schluessel in Zeile {key.start_mark.line + 1}.')
            seen.add(value)
        self.flatten_mapping(node)
        return super().construct_mapping(node, deep=deep)


def check(config):
    errors = 0
    warnings = 0

    def error(message):
        nonlocal errors
        errors += 1
        print('FEHLER: ' + message)

    def warn(message):
        nonlocal warnings
        warnings += 1
        print('WARNUNG: ' + message)

    host = config['host']
    base = Path(config['base']) / host
    if not base.is_dir():
        error('Compose-Quellverzeichnis fuer diesen Host fehlt.')
        return 1
    desired = {}
    ranges = []
    for item in config['networks']:
        if item.get('state', 'present') == 'absent':
            continue
        families = [(4, '')]
        if str(item.get('enable_ipv6', False)).lower() in ('true', 'yes', '1', 'on'):
            families.append((6, 'ipv6_'))
        desired[item['name']] = {}
        for version, prefix in families:
            network = ipaddress.ip_network(item[prefix + 'subnet'])
            gateway = ipaddress.ip_address(item[prefix + 'gateway'])
            desired[item['name']][version] = (network, gateway)
            for other_name, other in ranges:
                if other.version == version and network.overlaps(other):
                    error(f'Hostlokal ueberlappende IPAM-Netze: {other_name} / {item["name"]}.')
            ranges.append((item['name'], network))

    files = sorted(p for p in base.rglob('*') if p.is_file() and any(
        fnmatch.fnmatchcase(p.name, pattern) for pattern in config['patterns']))
    if not files:
        error('Keine Compose-Dateien fuer diesen Host gefunden.')
        return 1
    allocated = {}
    directories = set()
    for path in files:
        label = str(path.relative_to(base))
        if path.parent in directories:
            error(f'{label}: mehrere eigenstaendige Compose-Dateien im selben Projektordner.')
        directories.add(path.parent)
        try:
            yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader)
        except DuplicateKey as exc:
            error(f'{label}: {exc}')
            continue
        except yaml.YAMLError as exc:
            mark = getattr(exc, 'problem_mark', None)
            location = f' (Zeile {mark.line + 1})' if mark else ''
            error(f'{label}: YAML ungueltig{location}; Inhalte bleiben verborgen.')
            continue
        except (OSError, ValueError, TypeError):
            error(f'{label}: Quelldatei konnte nicht sicher gelesen werden.')
            continue
        try:
            # config validates and renders, but does not start/pull containers
            # or inspect/create Docker networks. Resolved secrets stay in RAM.
            proc = subprocess.run(
                ['docker', 'compose', '-f', str(path.resolve()), 'config', '--format', 'json'],
                cwd=path.parent, capture_output=True, text=True, timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired):
            error(f'{label}: Docker Compose CLI fehlt oder Zeitlimit erreicht.')
            continue
        if proc.returncode:
            error(f'{label}: docker compose config fehlgeschlagen (Code {proc.returncode}); Rohfehler wegen moeglicher Secrets nicht ausgegeben.')
            continue
        if proc.stderr.strip():
            warn(f'{label}: Compose meldet Warnungen; Rohtext wegen moeglicher Secrets verborgen. Lokal mit config -q pruefen.')
            # Missing interpolation variables produce only a Compose warning.
            # Treat this as a failed preflight rather than accepting empty values.
            error(f'{label}: Compose-Warnungen muessen vor einem sauberen Prueflauf geklaert werden.')
        try:
            rendered = json.loads(proc.stdout)
            networks = rendered.get('networks', {})
            for service, definition in rendered.get('services', {}).items():
                for key, assignment in (definition.get('networks') or {}).items():
                    assignment = assignment or {}
                    net = networks[key]
                    external = net.get('external', False)
                    name = net.get('name', key)
                    if external:
                        if name not in desired:
                            warn(f'{label}: externes Netz {name} nicht in docker_networks; IPAM hier nicht gegenpruefbar.')
                        ipam = desired.get(name, {})
                        allocation_scope = ('external', name)
                    else:
                        ipam = {}
                        for pool in net.get('ipam', {}).get('config', []):
                            network = ipaddress.ip_network(pool['subnet'])
                            gateway = ipaddress.ip_address(pool['gateway']) if pool.get('gateway') else None
                            ipam[network.version] = (network, gateway)
                        allocation_scope = (str(path.parent), key)
                    for version in (4, 6):
                        raw = assignment.get(f'ipv{version}_address')
                        if not raw:
                            continue
                        address = ipaddress.ip_address(raw)
                        if address.version != version:
                            error(f'{label}/{service}: IPv{version}-Adresse hat falsche Adressfamilie.')
                            continue
                        if version not in ipam:
                            error(f'{label}/{service}: kein explizites IPv{version}-Subnetz fuer feste Adresse in {name}.')
                            continue
                        network, gateway = ipam[version]
                        if address not in network or address == gateway or address == network.network_address or (version == 4 and address == network.broadcast_address):
                            error(f'{label}/{service}: feste IPv{version}-Adresse ausserhalb {name} oder reserviert.')
                        allocation_key = (allocation_scope, address)
                        if allocation_key in allocated:
                            error(f'{label}/{service}: feste IPv{version}-Adresse in {name} bereits durch {allocated[allocation_key]} belegt.')
                        allocated[allocation_key] = f'{label}/{service}'
        except (ValueError, TypeError, KeyError, AttributeError):
            error(f'{label}: gerenderte Netzwerkdaten ungueltig; Inhalte bleiben verborgen.')
            continue
        print(f'GEPRUEFT: {label}')
    print(f'{host}: {len(files)} Compose-Dateien; {errors} Fehler; {warnings} Warnungen.')
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(check(json.load(sys.stdin)))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception:
        # Config/parser exceptions can contain secrets. Do not print tracebacks.
        print('FEHLER: Pruefeingabe oder interne Auswertung ungueltig; keine Konfigurationsinhalte ausgegeben.')
        sys.exit(1)
