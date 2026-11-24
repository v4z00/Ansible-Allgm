#!/usr/bin/env python3
"""Proxmox GET API -> validated static YAML inventories. No SSH connections."""
import argparse
import copy
import fcntl
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import yaml


class InventoryError(Exception):
    pass


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise InventoryError('Doppelter YAML-Schluessel (Zeile %s)' % (key_node.start_mark.line + 1))
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_yaml(path):
    try:
        with open(path, encoding='utf-8') as handle:
            result = yaml.load(handle, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        # Do not print source snippets: these may contain credentials.
        raise InventoryError('%s: ungueltiges YAML; genau ein Dokument erforderlich' % path) from exc
    if not isinstance(result, dict):
        raise InventoryError('%s: YAML-Mapping erwartet' % path)
    return result


def merge(base, override):
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        elif value is None and isinstance(result.get(key), dict):
            continue  # empty host/group membership does not erase its variables
        else:
            result[key] = copy.deepcopy(value)
    return result


def static_hosts(inventory):
    hosts = {}
    def walk(group):
        if group is None:
            return
        if not isinstance(group, dict) or set(group) - {'hosts', 'vars', 'children'}:
            raise InventoryError('Statisches Inventory: nur hosts/vars/children sind erlaubt')
        for section in ('hosts', 'vars', 'children'):
            if section in group and not isinstance(group[section], dict):
                raise InventoryError('Statisches Inventory: %s muss ein Mapping sein' % section)
        for name, values in group.get('hosts', {}).items():
            if not isinstance(name, str) or values is not None and not isinstance(values, dict):
                raise InventoryError('Ungueltiger statischer Host')
            hosts[name] = merge(hosts.get(name, {}), values or {})
        for child in group.get('children', {}).values():
            walk(child)
    if set(inventory) != {'all'}:
        raise InventoryError('Statisches Inventory muss unter all: beginnen')
    walk(inventory['all'])
    return hosts


def tags(value):
    if isinstance(value, str):
        value = value.split(';')
    return sorted({str(t).strip().lower() for t in (value or []) if str(t).strip()})


def group_slug(value):
    return re.sub('[^a-z0-9_]', '_', value.lower())


TAG_GROUPS = {
    'adguard_hosts': ['adguard'], 'certbot_host': ['certbot'],
    'opnsense_firewall': ['firewall', 'opnsense'],
    'dmz_hosts': ['dmz'], 'external_ntp_hosts': ['external-ntp'],
    'rsyslog_clients': ['rsyslog', 'syslog'],
    'fail2ban_hosts': ['fail2ban'], 'snmpd_hosts': ['snmp', 'snmpd'],
    'chrony_hosts': ['ntp', 'chrony'], 'ssh_tcp_forwarding': ['ssh-forward'],
    'checkmk_docker_hosts': ['docker'], 'docker_deployment_hosts': ['docker'],
    'docker_monitoring_hosts': ['docker-monitoring'],
    'docker_dmz_hosts': ['docker-dmz'],
    'checkmk_cups_hosts': ['cups', 'print'],
    'checkmk_webserver_hosts': ['web', 'ox', 'nginx', 'apache'],
    'checkmk_database_hosts': ['db', 'mysql', 'postgres', 'redis'],
    'checkmk_smart_hosts': ['smart'], 'checkmk_proxmox_hosts': ['proxmox'],
    'proxmox_gui_hosts': ['proxmox-gui'],
    'proxmox_backup_hosts': ['proxmox-backup'],
    'crl_distribution_hosts': ['crl-distribution'],
}


def folder_from_rules(values, guest_tags, cfg):
    """Return the first matching Checkmk folder rule from inventory_config."""
    overrides = cfg.get('checkmk_folder_tag_overrides', {})
    if not isinstance(overrides, dict):
        raise InventoryError('checkmk_folder_tag_overrides muss ein Mapping sein')
    matching_overrides = sorted(guest_tags.intersection(overrides))
    if len(matching_overrides) > 1:
        raise InventoryError(
            'Mehrere Checkmk-Ordner-Override-Tags gesetzt: ' + ', '.join(matching_overrides)
        )
    if matching_overrides:
        return str(overrides[matching_overrides[0]])

    rules = cfg.get('checkmk_folder_rules', [])
    if not isinstance(rules, list):
        raise InventoryError('checkmk_folder_rules muss eine Liste sein')
    for position, rule in enumerate(rules, 1):
        if not isinstance(rule, dict) or not str(rule.get('folder', '')).strip():
            raise InventoryError('checkmk_folder_rules Eintrag %s ist ungueltig' % position)
        accepted_tags = set(tags(rule.get('tags_any', [])))
        accepted_families = set(tags(rule.get('os_families', [])))
        tag_match = not accepted_tags or bool(guest_tags.intersection(accepted_tags))
        family_match = not accepted_families or values.get('inventory_os_family') in accepted_families
        if not tag_match or not family_match:
            continue
        folder = str(rule['folder']).rstrip('/')
        if rule.get('append_location', False):
            locations = sorted(guest_tags.intersection(cfg.get('location_tags', [])))
            if len(locations) == 1:
                folder += '/' + locations[0]
        return folder
    return None


def decorate(name, values, cfg, notes):
    t = set(tags(values.get('proxmox_tags')))
    values['proxmox_tags'] = ';'.join(sorted(t))
    values['proxmox_tag_list'] = sorted(t)
    explicit_checkmk_exclude = values.get('checkmk_exclude', False)
    if not isinstance(explicit_checkmk_exclude, bool):
        raise InventoryError('%s: checkmk_exclude muss true oder false sein' % name)
    values['checkmk_exclude'] = explicit_checkmk_exclude or bool(
        t.intersection(cfg.get('checkmk_exclude_tags', ['checkmk_exclude']))
    )
    companies = sorted(t.intersection(cfg.get('company_tags', [])))
    places = sorted(t.intersection(cfg.get('location_tags', [])))
    infrastructure = sorted(t.intersection(cfg.get('infrastructure_tags', [])))
    default_folder = str(cfg.get('checkmk_unassigned_folder', '/unassigned'))
    location_root = str(cfg.get('checkmk_location_root', 'managed')).strip('/')
    configured_folder = folder_from_rules(values, t, cfg)
    if configured_folder:
        folder = configured_folder
    elif t.intersection(set(cfg.get('root_folder_tags', []))):
        folder = str(cfg.get('checkmk_root_folder', default_folder))
    elif len(companies) == 1 and len(places) <= 1:
        folder = '/' + companies[0] + ('/' + places[0] if places else '')
    elif len(infrastructure) == 1 and len(places) <= 1:
        folder = '/' + location_root + '/' + infrastructure[0] + ('/' + places[0] if places else '')
    elif len(places) == 1:
        folder = '/' + location_root + '/' + places[0]
    else:
        folder = default_folder
    folder = str(values.get('checkmk_target_folder', folder)).strip()
    folder_parts = folder.strip('/').split('/')
    folder_roots = cfg.get('checkmk_folder_roots', {})
    if folder_parts and folder_parts[0] in folder_roots:
        folder_parts[0] = str(folder_roots[folder_parts[0]]).strip('/')
        folder = '/' + '/'.join(folder_parts)
    if not re.fullmatch(r'(?:/[a-z0-9_]+)+', folder):
        raise InventoryError('%s: ungueltiger Checkmk-Ordner %s' % (name, folder))
    values['checkmk_target_folder'] = folder
    folder_parts = folder.strip('/').split('/')
    folder_root = folder_parts[0]
    tenant_prefix = cfg.get('checkmk_tenant_prefixes', {}).get(folder_root)
    if tenant_prefix is None:
        tenant_prefix = str(cfg.get('checkmk_default_prefix', 'SITE'))
    explicit_device_type = str(values.get('checkmk_device_type', '')).strip().upper()
    if explicit_device_type:
        device_type = explicit_device_type
    elif t.intersection({'firewall', 'opnsense'}):
        device_type = 'FIREWALL'
    elif t.intersection({'ap', 'accesspoint'}):
        device_type = 'AP'
    elif 'router' in t:
        device_type = 'ROUTER'
    elif 'switch' in t or 'snmp' in t:
        device_type = 'SWITCH'
    elif values.get('proxmox_type') == 'qemu':
        device_type = 'VM'
    elif values.get('proxmox_type') == 'lxc':
        device_type = 'LXC'
    else:
        device_type = 'SERVER'
    if not re.fullmatch(r'[A-Z0-9-]+', device_type):
        raise InventoryError('%s: ungueltiger checkmk_device_type %s' % (name, device_type))
    values['checkmk_device_type'] = device_type
    folder_scopes = cfg.get('checkmk_folder_scopes', {})
    if not isinstance(folder_scopes, dict):
        raise InventoryError('checkmk_folder_scopes muss ein Mapping sein')
    scope = folder_scopes.get(folder_parts[1], '') if len(folder_parts) > 1 else ''
    if not isinstance(scope, str) or (scope and not re.fullmatch(r'[A-Z0-9-]+', scope)):
        raise InventoryError('Ungueltiger Namenszusatz in checkmk_folder_scopes')
    name_scope = scope + '_' if scope else ''
    desired_hostname = tenant_prefix + '_' + device_type + '_' + name_scope + name.lower()
    values.setdefault('checkmk_hostname', desired_hostname)
    if not re.fullmatch(r'[A-Z0-9-]+_[A-Z0-9-]+_(?:[A-Z0-9-]+_)*[a-z0-9][a-z0-9.-]*', str(values['checkmk_hostname'])):
        raise InventoryError('%s: ungueltiger checkmk_hostname %s' % (name, values['checkmk_hostname']))
    if folder == default_folder:
        notes.append({'host': name, 'reason': 'Firma/Ort nicht eindeutig; ' + default_folder})
    for flag, group in [('docker', 'checkmk_docker_hosts'), ('cups', 'checkmk_cups_hosts'),
                        ('webserver', 'checkmk_webserver_hosts'), ('database', 'checkmk_database_hosts'),
                        ('smart', 'checkmk_smart_hosts')]:
        values.setdefault('checkmk_enable_' + flag, bool(t.intersection(TAG_GROUPS[group])))
    return t


def make_inventory(hosts, cfg, notes):
    children = {
        'checkmk_inventory_hosts': {'hosts': {}},
        'checkmk_managed_hosts': {'hosts': {}},
    }
    def member(group, name):
        children.setdefault(group, {'hosts': {}})['hosts'][name] = {}
    for name, values in sorted(hosts.items()):
        t = decorate(name, values, cfg, notes)
        if not values['checkmk_exclude']:
            member('checkmk_inventory_hosts', name)
            if values.get('inventory_os_family') == 'linux':
                member('checkmk_managed_hosts', name)
        for tag in sorted(t):
            member('tag_' + group_slug(tag), name)
        if values.get('inventory_os_family') == 'linux':
            member('all_linux_systems', name)
            if values.get('script_path'):
                member('all_script_hosts', name)
            for group in cfg.get('default_linux_groups', []):
                member(group, name)
            if values.get('proxmox_type') == 'lxc':
                for group in cfg.get('default_lxc_groups', ['lxc_hosts', 'all_lxc_hosts']):
                    member(group, name)
            elif values.get('proxmox_type') == 'qemu':
                for group in cfg.get('default_qemu_groups', ['vm_hosts', 'linux_generic_servers']):
                    member(group, name)
            if 'dmz' in t:
                member('dmz_linux_servers', name)
        elif values.get('inventory_os_family') == 'windows':
            member('windows_servers', name)
        elif values.get('proxmox_vmid'):
            member('unknown_os', name)
        for group, accepted in TAG_GROUPS.items():
            deployment_excluded = group == 'docker_deployment_hosts' and 'deployment-exclude' in t
            if t.intersection(accepted) and not deployment_excluded and not (
                    values['checkmk_exclude'] and group.startswith('checkmk_')):
                member(group, name)
        if values.get('proxmox_type'):
            member('proxmox_' + values['proxmox_type'], name)
        folder = values['checkmk_target_folder'].strip('/').split('/')
        member('company_' + folder[0], name)
        if len(folder) > 1:
            member('location_' + '_'.join(folder), name)
    return {'all': {'hosts': dict(sorted(hosts.items())), 'children': dict(sorted(children.items()))}}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class API:
    def __init__(self, cfg):
        self.name = str(cfg.get('name', 'unbekannt'))
        self.url = cfg['url'].rstrip('/')
        if not self.url.startswith('https://'):
            raise InventoryError('Proxmox API URL muss https:// verwenden')
        # Bei mehreren Quellen muss immer das bereits pro Quelle aufgeloeste
        # Secret gewinnen. Die Umgebungsvariable bleibt nur als Legacy-Fallback
        # fuer alte Einzelquellen-Konfigurationen erhalten.
        secret = cfg.get('token_secret') or os.environ.get('PROXMOX_TOKEN_SECRET')
        if not secret:
            raise InventoryError('Proxmox token_secret fehlt')
        self.auth = 'PVEAPIToken=%s!%s=%s' % (cfg['user'], cfg['token_id'], secret)
        context = ssl.create_default_context()
        if not cfg.get('validate_certs', True):
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        self.opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=context))
        self.timeout = cfg.get('timeout', 20)

    def get(self, path, optional=False):
        req = urllib.request.Request(self.url + '/api2/json' + path,
                                     headers={'Authorization': self.auth, 'Accept': 'application/json'})
        try:
            with self.opener.open(req, timeout=self.timeout) as response:
                payload = json.load(response)
            return payload['data']
        except urllib.error.HTTPError as exc:
            exc.close()
            # Missing/stopped agent or unsupported runtime endpoint: explicit fallback.
            if optional and exc.code in (400, 404, 500, 501):
                return None
            raise InventoryError(
                'Proxmox-Quelle %s: API %s: HTTP %s; Inventory unveraendert'
                % (self.name, path, exc.code)
            ) from None
        except (OSError, ValueError, KeyError) as exc:
            raise InventoryError(
                'Proxmox-Quelle %s: API %s: Verbindung/Antwort ungueltig (%s)'
                % (self.name, path, type(exc).__name__)
            ) from None


def usable_ip(value):
    try:
        ip = ipaddress.ip_interface(str(value)).ip
    except ValueError:
        return None
    if ip.version != 4 or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_unspecified:
        return None
    return str(ip)


def candidates(interfaces, cfg):
    result = set()
    ignored = cfg.get('ignore_interfaces_regex', r'^(lo$|docker|veth|br-|virbr|tap|fwbr)')
    for interface in interfaces or []:
        if re.search(ignored, str(interface.get('name', ''))):
            continue
        addresses = [x.get('ip-address') for x in interface.get('ip-addresses', [])]
        addresses += [interface.get('inet')]
        for addr in addresses:
            ip = usable_ip(addr)
            if ip:
                result.add(ip)
    allowed = [ipaddress.ip_network(n) for n in cfg.get('allowed_cidrs', [])]
    return sorted(ip for ip in result if not allowed or any(ipaddress.ip_address(ip) in n for n in allowed))


def select_ip(addresses, cfg):
    if len(addresses) == 1:
        return addresses[0]
    for subnet in cfg.get('preferred_cidrs', []):
        matches = [ip for ip in addresses if ipaddress.ip_address(ip) in ipaddress.ip_network(subnet)]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            return None
    return None


def select_ip_interactive(name, addresses):
    if not sys.stdin.isatty():
        return None
    print('\nMehrere IPv4-Adressen fuer %s gefunden:' % name, file=sys.stderr)
    for number, address in enumerate(addresses, 1):
        print('  %s) %s' % (number, address), file=sys.stderr)
    while True:
        print('Auswahl [1-%s] oder q zum Abbrechen: ' % len(addresses), end='', file=sys.stderr, flush=True)
        answer = sys.stdin.readline().strip().lower()
        if answer in ('q', 'quit', 'exit') or not answer:
            raise InventoryError('%s: IP-Auswahl abgebrochen; Inventory unveraendert' % name)
        if answer.isdigit() and 1 <= int(answer) <= len(addresses):
            return addresses[int(answer) - 1]
        print('Ungueltige Auswahl.', file=sys.stderr)


def collect(api, cfg, static, source_name, interactive=False):
    resources = api.get('/cluster/resources?type=vm')
    if not isinstance(resources, list) or not resources:
        raise InventoryError('API liefert keine VMs/LXC; bestehendes Inventory bleibt erhalten')
    hosts, notes, skipped, seen, selected_overrides = {}, [], [], set(), {}
    overrides = cfg.get('host_overrides', {})
    for vm in sorted(resources, key=lambda x: int(x.get('vmid', 0))):
        kind = vm.get('type')
        if kind not in ('qemu', 'lxc'):
            continue
        name = vm.get('name')
        if not name or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', name):
            raise InventoryError('VM %s: gueltiger eindeutiger Name fehlt' % vm.get('vmid'))
        if name in seen:
            raise InventoryError('Doppelter VM/LXC-Name: %s' % name)
        seen.add(name)
        def skip(reason):
            skipped.append({'source': source_name, 'host': name, 'vmid': vm['vmid'], 'reason': reason})
        if vm.get('template'):
            skip('Template'); continue
        if cfg.get('running_only', True) and vm.get('status') != 'running':
            skip('Nicht gestartet'); continue
        path = '/nodes/%s/%s/%s' % (urllib.parse.quote(vm['node'], safe=''), kind, int(vm['vmid']))
        config = api.get(path + '/config')
        if not isinstance(config, dict):
            raise InventoryError('%s: VM-Konfiguration fehlt' % name)
        if config.get('template'):
            skip('Template'); continue
        raw_tags = tags(config.get('tags', vm.get('tags')))
        excluded_tags = set(raw_tags).intersection(cfg.get('exclude_tags', ['delete']))
        if excluded_tags:
            skip('Ausschluss-Tag: ' + ', '.join(sorted(excluded_tags))); continue
        ostype = str(config.get('ostype', '')).lower()
        family = 'linux' if kind == 'lxc' or ostype in ('l24', 'l26') else (
            'windows' if ostype.startswith(('win', 'w2k')) or ostype in ('wxp', 'wvista') else 'unknown')
        values = {'proxmox_source': source_name,
                  'proxmox_vmid': vm['vmid'], 'proxmox_node': vm['node'], 'proxmox_type': kind,
                  'proxmox_status': vm.get('status'), 'proxmox_ostype': ostype,
                  'proxmox_tags': ';'.join(raw_tags), 'inventory_os_family': family}
        values = merge(values, overrides.get(name, {}))
        values = merge(values, static.get(name, {}))  # explicit static settings win
        if values.get('inventory_os_family') == 'linux' and cfg.get('default_script_path'):
            values.setdefault('script_path', str(cfg['default_script_path']))
        if values.get('script_path') and not str(values['script_path']).startswith('/'):
            raise InventoryError('%s: script_path muss ein absoluter Pfad sein' % name)
        if values.get('ansible_host'):
            ip = usable_ip(values['ansible_host'])
            if not ip:
                raise InventoryError('%s: ansible_host muss eine gueltige IPv4 sein' % name)
            source, addresses = 'static_or_override', [ip]
        else:
            interfaces = None
            if vm.get('status') == 'running':
                response = api.get(path + ('/agent/network-get-interfaces' if kind == 'qemu' else '/interfaces'), optional=True)
                interfaces = response.get('result') if kind == 'qemu' and isinstance(response, dict) else response
            if interfaces is not None and not isinstance(interfaces, list):
                raise InventoryError('%s: ungueltige Netzwerkantwort' % name)
            addresses = candidates(interfaces, cfg)
            source = 'qemu_agent' if kind == 'qemu' else 'lxc_runtime'
            if not addresses and kind == 'lxc':
                interfaces = []
                for key, value in config.items():
                    if re.fullmatch(r'net\d+', key):
                        props = dict(part.split('=', 1) for part in value.split(',') if '=' in part)
                        interfaces.append({'name': props.get('name', key), 'inet': props.get('ip')})
                addresses = candidates(interfaces, cfg)
                source = 'lxc_config'
            ip = select_ip(addresses, cfg)
            if not ip and len(addresses) > 1 and interactive:
                ip = select_ip_interactive(name, addresses)
                selected_overrides[name] = ip
                source = 'interactive_override'
                notes.append({
                    'source': source_name,
                    'host': name,
                    'reason': 'IPv4 %s interaktiv ausgewaehlt und in host_overrides gespeichert' % ip,
                })
        if not ip:
            skip('Keine eindeutige IPv4 (Agent/LXC pruefen oder host_overrides/preferred_cidrs setzen): ' + ', '.join(addresses))
            continue
        values.update(ansible_host=ip, inventory_ip_source=source, proxmox_ipv4_addresses=addresses)
        if values.get('inventory_os_family') not in ('linux', 'windows', 'unknown'):
            raise InventoryError('%s: inventory_os_family ungueltig' % name)
        hosts[name] = values
    return hosts, notes, skipped, selected_overrides


def proxmox_sources(cfg, secrets):
    """Return validated independent Proxmox API sources with resolved secrets."""
    configured = cfg.get('proxmox_sources')
    if configured is None:
        legacy = cfg.get('proxmox')
        if not isinstance(legacy, dict):
            raise InventoryError('proxmox_sources muss eine Liste mit mindestens einer Quelle sein')
        configured = [dict(legacy, name='default', credential='default')]
    if not isinstance(configured, list) or not configured:
        raise InventoryError('proxmox_sources muss eine nicht leere Liste sein')
    token_secrets = secrets.get('proxmox_token_secrets', {})
    if token_secrets is None:
        token_secrets = {}
    if not isinstance(token_secrets, dict):
        raise InventoryError('proxmox_token_secrets muss ein Mapping sein')
    result, names = [], set()
    for position, raw in enumerate(configured, 1):
        if not isinstance(raw, dict):
            raise InventoryError('Proxmox-Quelle %s muss ein Mapping sein' % position)
        source = copy.deepcopy(raw)
        name = str(source.get('name', '')).strip()
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', name):
            raise InventoryError('Proxmox-Quelle %s: ungueltiger eindeutiger name' % position)
        if name in names:
            raise InventoryError('Doppelte Proxmox-Quelle: %s' % name)
        names.add(name)
        credential = str(source.get('credential', name)).strip()
        secret = token_secrets.get(credential)
        if not secret and len(configured) == 1:
            secret = secrets.get('proxmox_token_secret') or secrets.get('proxmox_api_token')
        if not secret:
            raise InventoryError(
                'Proxmox-Quelle %s: Token fehlt unter proxmox_token_secrets.%s' % (name, credential)
            )
        for required in ('url', 'user', 'token_id'):
            if not str(source.get(required, '')).strip():
                raise InventoryError('Proxmox-Quelle %s: %s fehlt' % (name, required))
        source['credential'] = credential
        source['token_secret'] = secret
        result.append(source)
    return result


def validate_with_ansible(path, root, expected):
    executable = shutil.which('ansible-inventory')
    if not executable:
        raise InventoryError('ansible-inventory fehlt im PATH')
    env = dict(os.environ, ANSIBLE_INVENTORY_UNPARSED_FAILED='True',
               ANSIBLE_INVENTORY_ANY_UNPARSED_IS_FAILED='True', ANSIBLE_NOCOLOR='1')
    proc = subprocess.run([executable, '-i', str(path), '--playbook-dir', str(root), '--list'],
                          env=env, capture_output=True, text=True)
    if proc.returncode:
        raise InventoryError('Ansible-Pruefung fehlgeschlagen; Inventory/host_vars/group_vars mit ansible-inventory pruefen')
    try:
        actual = set(json.loads(proc.stdout)['_meta']['hostvars'])
    except (ValueError, KeyError):
        raise InventoryError('Ansible liefert kein gueltiges Inventory') from None
    if actual != set(expected):
        raise InventoryError('Ansible-Hostliste weicht vom generierten Inventory ab')


def publish(root, documents, check=False):
    """Validate everything first; replace each file atomically and roll back on error."""
    root = Path(root)
    with tempfile.TemporaryDirectory(prefix='.inventory-build-', dir=root) as tmp:
        staged = []
        for relative, document in documents:
            source = Path(tmp) / Path(relative).name
            source.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding='utf-8')
            source.chmod(0o600)
            if 'all' in document:
                validate_with_ansible(source, root, static_hosts(document))
            staged.append((source, root / relative))
        changed = [(source, dest) for source, dest in staged if not dest.exists() or source.read_bytes() != dest.read_bytes()]
        if check:
            return bool(changed)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        backups = {}
        backup_dir = root / 'x/backups'
        for source, dest in changed:
            dest.parent.mkdir(parents=True, exist_ok=True)
            backups[dest] = dest.read_bytes() if dest.exists() else None
            if dest.exists():
                backup_dir.mkdir(parents=True, exist_ok=True)
                relative_name = str(dest.relative_to(root)).replace('/', '__')
                backup = backup_dir / (relative_name + '.' + stamp + '.bak')
                backup.write_bytes(backups[dest]); backup.chmod(0o600)
        replaced = []
        try:
            for source, dest in changed:
                os.replace(source, dest)
                replaced.append(dest)
        except OSError:
            for dest in reversed(replaced):
                if backups[dest] is None:
                    dest.unlink()
                else:
                    rollback = Path(tmp) / 'rollback'
                    rollback.write_bytes(backups[dest]); rollback.chmod(0o600)
                    os.replace(rollback, dest)
            raise
        return bool(changed)


def run(args):
    root = Path(args.root).resolve()
    config_path = Path(args.config or root / 'inventory_config.yml').resolve()
    cfg = read_yaml(config_path)
    if cfg.get('inventory_mode', 'static') != 'proxmox':
        print(json.dumps({'changed': False, 'check_mode': args.check,
                          'mode': 'static', 'message': 'Statisches YAML-Inventory bleibt unveraendert'},
                         ensure_ascii=False))
        return
    secrets_path = root / 'group_vars/all/secrets.yml'
    secrets = read_yaml(secrets_path) if secrets_path.is_file() else {}
    static_inventory = read_yaml(root / 'inventory/10_static.yml')
    static = static_hosts(static_inventory)
    with open(root / '.inventory-update.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        hosts, notes, skipped, selected_overrides = {}, [], [], {}
        for source in proxmox_sources(cfg, secrets):
            source_hosts, source_notes, source_skipped, source_overrides = collect(
                API(source), cfg, static, source['name'], interactive=args.interactive
            )
            duplicates = sorted(set(hosts).intersection(source_hosts))
            if duplicates:
                raise InventoryError(
                    'Doppelte VM-/LXC-Namen in mehreren Proxmox-Quellen: ' + ', '.join(duplicates)
                )
            hosts.update(source_hosts)
            notes.extend(source_notes)
            skipped.extend(source_skipped)
            for name, address in source_overrides.items():
                if name in selected_overrides and selected_overrides[name] != address:
                    raise InventoryError('Widerspruechliche interaktive IP-Auswahl fuer %s' % name)
                selected_overrides[name] = address
        if not hosts and not cfg.get('allow_empty_generated', False):
            raise InventoryError(
                'Kein API-Host mit eindeutiger IPv4 ermittelt; kein Inventory ersetzt. '
                + json.dumps(skipped, ensure_ascii=False)
            )
        if selected_overrides:
            overrides = cfg.setdefault('host_overrides', {})
            for name, address in selected_overrides.items():
                overrides.setdefault(name, {})['ansible_host'] = address
        generated = make_inventory(copy.deepcopy(hosts), cfg, [])
        merged_hosts = merge(hosts, static)
        report = {'generated_hosts': len(hosts), 'combined_hosts': len(merged_hosts),
                  'skipped': skipped, 'notes': notes,
                  'hosts': {n: {k: v.get(k) for k in ('ansible_host', 'inventory_ip_source', 'inventory_os_family', 'checkmk_hostname', 'checkmk_target_folder', 'checkmk_device_type', 'checkmk_exclude')}
                            for n, v in sorted(merged_hosts.items())}}
        documents = [('inventory/20_proxmox.yml', generated),
                     ('x/reports/inventory_report.yml', report)]
        if selected_overrides:
            try:
                config_relative = config_path.relative_to(root)
            except ValueError:
                raise InventoryError('Interaktive Auswahl kann nur in einer Konfiguration unter %s gespeichert werden' % root)
            documents.append((config_relative, copy.deepcopy(cfg)))
        changed = publish(root, documents, args.check)
        print(json.dumps({'changed': changed, 'check_mode': args.check, 'generated_hosts': len(hosts),
                          'combined_hosts': len(merged_hosts), 'skipped': skipped, 'notes': notes}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument('--config')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--interactive', action='store_true',
                        help='Bei mehreren IPv4-Adressen Auswahl abfragen und als host_override speichern')
    args = parser.parse_args()
    if args.check and args.interactive:
        parser.error('--check und --interactive koennen nicht kombiniert werden')
    try:
        run(args)
    except (InventoryError, OSError, KeyError, TypeError, ValueError) as exc:
        print('Inventory-Fehler: %s' % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
