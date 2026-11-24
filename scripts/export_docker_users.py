#!/usr/bin/env python3
"""Discover numeric Docker service users and merge them into host_vars YAML."""
import argparse
import copy
import os
from pathlib import Path
import re
import sys
import tempfile

import yaml


COMPOSE_RE = re.compile(r'^(?:docker-)?compose(?:[^/]*)?\.ya?ml$', re.IGNORECASE)
VARIABLE_RE = re.compile(r'^\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}$')


def scalar(value, variables):
    text = str(value).strip().strip('"\'')
    match = VARIABLE_RE.fullmatch(text)
    if match:
        text = variables.get(match.group(1), match.group(2) or '')
    return text


def env_file(path):
    result = {}
    if not path.is_file():
        return result
    for raw in path.read_text(encoding='utf-8', errors='replace').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def environment(service, compose_path, project_variables):
    result = dict(project_variables)
    configured_files = service.get('env_file', [])
    if isinstance(configured_files, str):
        configured_files = [configured_files]
    for configured in configured_files or []:
        if isinstance(configured, dict):
            configured = configured.get('path', '')
        if configured:
            result.update(env_file(compose_path.parent / str(configured)))
    configured_env = service.get('environment', {})
    if isinstance(configured_env, dict):
        for key, value in configured_env.items():
            if value is not None:
                result[str(key)] = scalar(value, result)
    elif isinstance(configured_env, list):
        for item in configured_env:
            if isinstance(item, str) and '=' in item:
                key, value = item.split('=', 1)
                result[key.strip()] = scalar(value, result)
    return result


def numeric(value, variables):
    if value is None:
        return None
    text = scalar(value, variables)
    return int(text) if text.isdigit() else None


def discover(source):
    found = {}
    errors = []
    host_directories = sorted(
        path for path in source.iterdir()
        if path.is_dir() and not path.name.startswith('.')
    )
    for host_dir in host_directories:
        host_users = {}
        compose_files = sorted(
            path for path in host_dir.rglob('*')
            if path.is_file()
            and COMPOSE_RE.match(path.name)
            and not any(part.startswith('.') for part in path.relative_to(host_dir).parts)
        )
        for compose in compose_files:
            try:
                document = yaml.safe_load(compose.read_text(encoding='utf-8', errors='replace')) or {}
            except yaml.YAMLError:
                errors.append('%s: ungueltiges YAML' % compose)
                continue
            services = document.get('services', {})
            if not isinstance(services, dict):
                continue
            project_vars = env_file(compose.parent / '.env')
            for service_name, service in services.items():
                if not isinstance(service, dict):
                    continue
                variables = environment(service, compose, project_vars)
                uid = numeric(variables.get('PUID', variables.get('UID')), variables)
                gid = numeric(variables.get('PGID', variables.get('GID')), variables)
                configured_user = scalar(service.get('user', ''), variables)
                if uid is None and re.fullmatch(r'\d+(?::\d+)?', configured_user):
                    uid_text, _, gid_text = configured_user.partition(':')
                    uid = int(uid_text)
                    gid = int(gid_text or uid_text)
                if uid is None or uid < 1000:
                    continue
                gid = gid if gid is not None else uid
                source_label = '%s:%s' % (compose.relative_to(host_dir), service_name)
                current = host_users.setdefault(uid, {'gids': set(), 'sources': set()})
                current['gids'].add(gid)
                current['sources'].add(source_label)
        found[host_dir.name] = host_users
    return found, errors


def existing_users(path):
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding='utf-8')) or {}
    users = loaded.get('docker_service_users', [])
    if not isinstance(users, list):
        raise ValueError('%s: docker_service_users muss eine Liste sein' % path)
    return {int(item['uid']): item for item in users if isinstance(item, dict) and 'uid' in item}


def build_users(discovered, previous):
    result = []
    all_uids = sorted(set(discovered).union(previous))
    for uid in all_uids:
        old = copy.deepcopy(previous.get(uid, {}))
        details = discovered.get(uid)
        gids = sorted(details['gids']) if details else []
        gid = old.get('gid', gids[0] if len(gids) == 1 else uid)
        entry = {
            'name': old.get('name', 'CHANGE_ME_%s' % uid),
            'uid': uid,
            'gid': int(gid),
            'managed': bool(old.get('managed', False)),
            'create_home': bool(old.get('create_home', False)),
            'shell': old.get('shell', '/usr/sbin/nologin'),
            'discovered': details is not None,
            'sources': sorted(details['sources']) if details else old.get('sources', []),
        }
        if len(gids) > 1:
            entry['discovered_gids'] = gids
        for key in ('comment', 'home', 'system', 'state'):
            if key in old:
                entry[key] = old[key]
        result.append(entry)
    return result


def render(users):
    header = (
        '---\n'
        '# Von scripts/export_docker_users.py gepflegte Uebersicht.\n'
        '# name pruefen und managed: true setzen, bevor ein Konto angelegt wird.\n'
    )
    return header + yaml.safe_dump({'docker_service_users': users}, sort_keys=False, allow_unicode=True)


def write_atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.chmod(0o600)
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument('--source', default=os.environ.get('ANSIBLE_DOCKER_CONFIG_ROOT', '/root/docker-configs'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    source = Path(args.source).resolve()
    if not source.is_dir():
        parser.error('Docker-Konfigurationsverzeichnis fehlt: %s' % source)
    discovered, errors = discover(source)
    changed = []
    for host, details in sorted(discovered.items()):
        target = root / 'host_vars' / host / 'docker_users.yml'
        content = render(build_users(details, existing_users(target)))
        if not target.exists() or target.read_text(encoding='utf-8') != content:
            changed.append(str(target.relative_to(root)))
            if not args.check:
                write_atomic(target, content)
    print(yaml.safe_dump({'source': str(source), 'changed': changed, 'warnings': errors}, sort_keys=False), end='')
    return 1 if args.check and changed else 0


if __name__ == '__main__':
    sys.exit(main())
