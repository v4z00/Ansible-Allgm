"""Plan explicit private source folders and service definitions, without discovery."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

SERVICE_KEYS = {'unit', 'mode', 'name', 'description', 'type', 'exec_start', 'exec_stop',
                'exec_start_pre', 'exec_start_post', 'exec_stop_post', 'working_directory',
                'user', 'group', 'restart', 'restart_sec', 'remain_after_exit',
                'timeout_start_sec', 'timeout_stop_sec', 'pid_file', 'kill_mode',
                'after', 'before', 'wants', 'requires', 'conflicts', 'wanted_by',
                'default_dependencies', 'environment_files', 'enabled', 'state'}


def text(value):
    if not isinstance(value, str) or not value or len(value) > 4096 or any(ord(c) < 32 for c in value):
        raise ValueError('Expected a nonempty single-line profile value')
    return value


def relative(value):
    value = text(value)
    path = PurePosixPath(value)
    if value == '.' or path.is_absolute() or str(path) != value or any(p in ('.', '..') for p in path.parts) or not re.fullmatch(r'[A-Za-z0-9_./-]+', value):
        raise ValueError('Expected a canonical relative source/destination path')
    return value


def absolute(value):
    value = text(value)
    if not value.startswith('/') or str(PurePosixPath(value)) != value or '..' in PurePosixPath(value).parts:
        raise ValueError('Expected a canonical absolute destination path')
    return value


def account(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', value):
        raise ValueError('Invalid profile owner/group')
    return value


def fixed(value, target, library):
    return text(value).replace('{target}', target).replace('{library_root}', library)


def quote(value, arguments=False):
    value = text(value).replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%')
    if arguments:value = value.replace('$', '$$')
    return '"' + value + '"'


def dependencies(values):
    if not isinstance(values, list) or len(values) > 64:
        raise ValueError('Expected a unit dependency list')
    if any(not isinstance(v, str) or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.:@\\-]*\.(?:service|target|socket|mount|path)', v) for v in values):
        raise ValueError('Invalid unit dependency')
    return ' '.join(values)


def command(argv, target, library):
    if not isinstance(argv, list) or not argv or len(argv) > 128:
        raise ValueError('Commands require an explicit argument list')
    values = [fixed(value, target, library) for value in argv]
    absolute(values[0])
    return ' '.join(quote(value, arguments=True) for value in values)


def service(spec, target, library, owner, group):
    if not isinstance(spec, dict) or set(spec) - SERVICE_KEYS:
        raise ValueError('Unknown service profile fields')
    unit = spec.get('unit')
    if not isinstance(unit, str) or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.:@-]*\.service', unit) or '@.service' in unit:
        raise ValueError('A concrete service name is required')
    if spec.get('mode') not in ('active', 'oneshot', 'observe'):
        raise ValueError('Explicit observation mode required')
    kind = spec.get('type', 'simple')
    if kind not in ('simple', 'exec', 'oneshot', 'notify', 'forking', 'dbus', 'idle'):
        raise ValueError('Unsupported service type')
    if kind == 'dbus':raise ValueError('BusName service profiles need a separate explicit extension')
    if (spec['mode'] == 'oneshot') != (kind == 'oneshot'):
        raise ValueError('Oneshot execution and observation mode must agree')
    sections = {'Unit': [('Description', text(spec.get('description', 'Managed script service')).replace('%', '%%'))],
                'Service': [('Type', kind), ('User', account(spec.get('user', owner))),
                            ('Group', account(spec.get('group', group))),
                            ('WorkingDirectory', quote(absolute(fixed(spec.get('working_directory', '{target}'), target, library)))),
                            ('Environment', quote('SCRIPT_LIBRARY_ROOT=' + library))]}
    for key in ('after', 'before', 'wants', 'requires', 'conflicts'):
        if key in spec:sections['Unit'].append((key.title(), dependencies(spec[key])))
    for key, directive, section in (('default_dependencies', 'DefaultDependencies', 'Unit'),
                                    ('remain_after_exit', 'RemainAfterExit', 'Service')):
        if key in spec:
            if type(spec[key]) is not bool:raise ValueError('Service flags must be booleans')
            sections[section].append((directive, 'yes' if spec[key] else 'no'))
    sections['Service'].append(('ExecStart', command(spec['exec_start'], target, library)))
    if 'exec_stop' in spec:sections['Service'].append(('ExecStop', command(spec['exec_stop'], target, library)))
    for key, directive in (('exec_start_pre', 'ExecStartPre'), ('exec_start_post', 'ExecStartPost'), ('exec_stop_post', 'ExecStopPost')):
        if key in spec:
            if not isinstance(spec[key], list):raise ValueError('Expected a command list')
            sections['Service'].extend((directive, command(argv, target, library)) for argv in spec[key])
    restart = spec.get('restart', 'no')
    if restart not in ('no', 'always', 'on-success', 'on-failure', 'on-abnormal', 'on-watchdog', 'on-abort'):
        raise ValueError('Invalid restart policy')
    if kind == 'oneshot' and restart in ('always', 'on-success'):
        raise ValueError('Oneshot restart policy is not supported by systemd')
    sections['Service'].append(('Restart', restart))
    for key, directive in (('restart_sec', 'RestartSec'), ('timeout_start_sec', 'TimeoutStartSec'), ('timeout_stop_sec', 'TimeoutStopSec')):
        if key in spec:
            value = spec[key]
            if type(value) not in (int, float) or not 0 <= value <= 86400:
                raise ValueError('Timeout values require finite seconds between 0 and 86400')
            sections['Service'].append((directive, str(value)))
    if 'pid_file' in spec:sections['Service'].append(('PIDFile', quote(absolute(fixed(spec['pid_file'], target, library)))))
    if 'kill_mode' in spec:
        if spec['kill_mode'] not in ('control-group', 'mixed', 'process', 'none'):raise ValueError('Invalid kill mode')
        sections['Service'].append(('KillMode', spec['kill_mode']))
    if 'environment_files' in spec and not isinstance(spec['environment_files'], list):raise ValueError('Expected environment file list')
    for value in spec.get('environment_files', []):
        sections['Service'].append(('EnvironmentFile', quote(absolute(fixed(value, target, library)))))
    if spec.get('wanted_by'):
        sections['Install'] = [('WantedBy', dependencies(spec['wanted_by']))]
    if 'enabled' in spec:
        if type(spec['enabled']) is not bool:raise ValueError('Enabled must be a boolean')
        if spec['enabled'] and not spec.get('wanted_by'):raise ValueError('Enable requires explicit WantedBy targets')
    if 'state' in spec and spec['state'] not in ('started', 'stopped', 'restarted', 'reloaded'):
        raise ValueError('Invalid explicit service action')
    action = {'unit': unit, **{key: spec[key] for key in ('enabled', 'state') if key in spec}}
    return {'unit': unit, 'sections': sections, 'action': action}


def no_links(path, stop):
    for parent in [path, *path.parents]:
        if parent.is_symlink():raise ValueError('Source links are not accepted')
        if parent == stop:break


def deployment(profiles, selected, host_source, library, owner='root', group='root', unit_dir='/etc/systemd/system', database=None):
    if not isinstance(profiles, dict) or not isinstance(selected, list) or any(not isinstance(v, str) or v not in profiles for v in selected):
        raise ValueError('Explicit known profile selection required')
    if len(set(selected)) != len(selected):raise ValueError('Duplicate selected profile')
    base = Path(absolute(host_source));library = absolute(library);unit_dir = absolute(unit_dir)
    result = {'files': [], 'directories': [], 'services': [], 'libraries': []}
    destinations = set();units = set();directories = {}
    library_roots = {library}
    for name in selected:
        profile = profiles[name]
        if isinstance(profile, dict) and profile.get('library') is True:
            library_roots.add(absolute(profile['target']))
    for name in selected:
        profile = profiles[name]
        if isinstance(profile, list):continue  # Existing explicit status-only profiles.
        if not isinstance(profile, dict) or set(profile) - {'source', 'target', 'owner', 'group', 'services', 'library'}:
            raise ValueError('Invalid deployment profile')
        if 'library' in profile and type(profile['library']) is not bool:
            raise ValueError('Profile library must be a boolean')
        source = base / relative(profile['source']);target = absolute(profile['target'])
        if target in ('/', '/root', '/etc', '/usr', '/var', '/opt', '/home', '/root/ansible'):
            raise ValueError('Choose a dedicated destination folder')
        if PurePosixPath('/root/ansible') in PurePosixPath(target).parents:
            raise ValueError('Host programs cannot overwrite controller code')
        who = account(profile.get('owner', owner));team = account(profile.get('group', group))
        profile_library = target if profile.get('library', False) else library
        if profile.get('library', False):
            if any(target == root or PurePosixPath(root) in PurePosixPath(target).parents or PurePosixPath(target) in PurePosixPath(root).parents for root in library_roots if root != target) or target == library:
                raise ValueError('Profile libraries require separate nonoverlapping roots')
            if any(row['path'] == target for row in result['libraries']):
                raise ValueError('Duplicate profile library')
            result['libraries'].append({'path': target, 'owner': who, 'group': team})
        manifest = source / 'deployment.json';no_links(manifest, base)
        data = json.loads(manifest.read_text(encoding='utf8'))
        if not isinstance(data.get('files'), list) or len(data['files']) > 1024:raise ValueError('Explicit source manifest required')
        if data.get('review_required') or data.get('sanitized_import'):
            raise ValueError('Imported sources need review before deployment')
        entries = data['files']
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) - {'path', 'dest', 'sha256', 'kind', 'config_key'}:
                raise ValueError('Invalid manifest file fields')
            local = source / relative(entry['path']);no_links(local, base)
            rel = relative(entry.get('dest', entry['path']));dest = str(PurePosixPath(target) / rel)
            if dest in destinations:raise ValueError('Profiles target the same file')
            protected = [str(PurePosixPath(root) / p) for root in library_roots for p in ('bin', 'lib/common', 'lib/python', 'lib/data', 'lib/load.sh')]
            if any(dest == p or dest.startswith(p + '/') for p in protected):
                raise ValueError('Private profiles cannot replace the shared library')
            if entry.get('kind') not in ('script', 'config', 'library', 'data'):
                raise ValueError('Invalid file kind')
            wanted = entry.get('sha256')
            if not isinstance(wanted, str) or not re.fullmatch('[a-f0-9]{64}', wanted) or not local.is_file() or hashlib.sha256(local.read_bytes()).hexdigest() != wanted:
                raise ValueError('Source missing or hash differs from the reviewed manifest')
            if local.suffix in ('.service', '.timer') or PurePosixPath(dest).suffix in ('.service', '.timer'):
                raise ValueError('Define units in profiles rather than copying them from files')
            destinations.add(dest)
            row = {'source': str(local), 'dest': dest, 'sha256': wanted,
                   'mode': '0700' if entry['kind'] == 'script' else '0600', 'owner': who, 'group': team}
            if 'config_key' in entry:
                key = entry['config_key']
                if entry['kind'] != 'config' or local.suffix != '.json' or not isinstance(key, str) or not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]*', key):
                    raise ValueError('Rendered configuration requires a JSON config and an explicit key')
                defaults = json.loads(local.read_text(encoding='utf8'))
                if not isinstance(defaults, dict):raise ValueError('Profile configuration must be an object')
                row['config_key'] = key
            result['files'].append(row)
            for parent in [PurePosixPath(dest).parent, *PurePosixPath(dest).parent.parents]:
                if parent == PurePosixPath(target).parent:break
                key = str(parent)
                if key in directories and directories[key] != (who, team):raise ValueError('Conflicting directory ownership')
                directories[key] = (who, team)
        if not entries:directories[target] = (who, team)
        services = profile.get('services')
        if not isinstance(services, list) or not services:raise ValueError('Deployment profile requires explicit services')
        for spec in services:
            row = service(spec, target, profile_library, who, team)
            if row['unit'] in units:raise ValueError('Duplicate managed unit')
            row['dest'] = str(PurePosixPath(unit_dir) / row['unit'])
            units.add(row['unit']);result['services'].append(row)
    result['directories'] = [{'path': path, 'owner': who, 'group': team}
                             for path, (who, team) in sorted(directories.items(), key=lambda row: (len(PurePosixPath(row[0]).parts), row[0]))]
    files = destinations | {row['dest'] for row in result['services']}
    if len(files) != len(destinations) + len(result['services']):
        raise ValueError('A private file would overwrite a generated unit')
    for path in files:
        if any(str(parent) in files for parent in PurePosixPath(path).parents):
            raise ValueError('A destination file would also be used as a directory')
        if database and path in (absolute(database), str(PurePosixPath(database).parent / 'systemd.json')):
            raise ValueError('Private files cannot overwrite runtime observations')
    result['checks'] = ([['directory', row['path']] for row in result['directories']] +
                        [['file', row['dest']] for row in result['files']] +
                        ([['directory', unit_dir]] if result['services'] else []) +
                        [['file', row['dest']] for row in result['services']])
    for row in result['libraries']:
        result['checks'].extend(['directory', str(PurePosixPath(row['path']) / p)] for p in ('bin', 'lib', 'lib/common', 'lib/python', 'lib/data'))
    return result


class FilterModule:
    def filters(self):
        return {'script_jobs_systemd_deployment': deployment}
