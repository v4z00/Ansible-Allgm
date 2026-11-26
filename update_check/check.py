#!/usr/bin/env python3
"""Lokaler Controller-Pruefer; Schreibmodus nur mit --configure oder --sort-settings."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import local_extensions
from controller_i18n import cli_args, machine_report, status_text, tr
from staging_manifest import public_library

try:
    import yaml
except ImportError:
    cli_args(sys.argv[1:], Path(__file__).resolve().parents[1])
    raise SystemExit(tr('audit.dependency'))

CHECKER_VERSION = '1.5.2'
VERSION_RE = re.compile(r'(?<![A-Za-z0-9])\d+\.\d+\.\d+(?:[a-zA-Z][A-Za-z0-9.-]*)?')


class AuditError(Exception):
    pass


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    seen = set()
    for key_node, _value_node in node.value:
        if key_node.tag == 'tag:yaml.org,2002:merge':
            continue
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise AuditError('DOPPELTE_YAML_SCHLUESSEL')
        seen.add(key)
    loader.flatten_mapping(node)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def guarded(root, relative):
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise AuditError('UNGUELTIGER_RELATIVPFAD')
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise AuditError('UNGUELTIGER_RELATIVPFAD')
    target = (root / path).resolve()
    if not target.is_relative_to(root):
        raise AuditError('PFAD_AUSSERHALB_PROJEKT')
    return target


def sha(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def load_json(path):
    def unique(pairs):
        mapping = {}
        for key, value in pairs:
            if key in mapping:
                raise AuditError('DOPPELTE_JSON_SCHLUESSEL')
            mapping[key] = value
        return mapping

    try:
        return json.loads(path.read_text(), object_pairs_hook=unique)
    except (OSError, ValueError, UnicodeError):
        raise AuditError('JSON_UNLESBAR') from None


def read_yaml(path):
    try:
        value = yaml.load(path.read_text(), Loader=UniqueLoader)
        if not isinstance(value, dict):
            raise AuditError('YAML_KEINE_ZUORDNUNG')
        return value
    except AuditError:
        raise
    except (OSError, UnicodeError, yaml.YAMLError, TypeError, ValueError):
        raise AuditError('YAML_UNLESBAR') from None


def field(values, key):
    value = values
    for part in key.split('.'):
        if not isinstance(value, dict) or part not in value:
            return False, None
        value = value[part]
    return True, value


def dynamic(value):
    return isinstance(value, str) and ('{{' in value or '{%' in value)


def good_type(value, kind):
    return {
        'boolean': lambda: isinstance(value, bool),
        'integer': lambda: isinstance(value, int) and not isinstance(value, bool),
        'string': lambda: isinstance(value, str),
        'list': lambda: isinstance(value, list),
        'mapping': lambda: isinstance(value, dict),
        'duration': lambda: isinstance(value, (str, int)) and not isinstance(value, bool),
        'scalar_id': lambda: isinstance(value, (str, int)) and not isinstance(value, bool),
        'any': lambda: True,
    }.get(kind, lambda: False)()


def resolve_literal(value, values, seen=None):
    """Nur Dictionary-Aliase und bekannte Ansible-Kontexte erkennen; nie Jinja ausfuehren."""
    if not dynamic(value):
        return value, 'LITERAL'
    seen = set() if seen is None else set(seen)
    match = re.fullmatch(
        r"\s*\{\{\s*([A-Za-z_][A-Za-z0-9_.]*)(?:\s*\|\s*(int|string|bool))?\s*\}\}\s*", value
    )
    if not match:
        if re.fullmatch(r"\s*\{\{\s*(playbook_dir|inventory_dir)\s*\}\}[^{}]*", value):
            return None, 'ANSIBLE_KONTEXT'
        if re.fullmatch(
            r"\s*\{\{\s*lookup\(\s*['\"](?:ansible\.builtin\.)?env['\"]\s*,\s*['\"]HOME['\"]\s*\)\s*\}\}[^{}]*",
            value,
        ):
            return None, 'ANSIBLE_KONTEXT'
        return None, 'DYNAMISCH_UNGEPRUEFT'
    key, conversion = match.groups()
    if key in seen:
        return None, 'ALIAS_ZYKLUS'
    found, item = field(values, key)
    if not found:
        if key.startswith('ansible_') or key in {
            'inventory_hostname',
            'playbook_dir',
            'inventory_dir',
        }:
            return None, 'ANSIBLE_KONTEXT'
        return None, 'ALIAS_ZIEL_FEHLT'
    resolved, status = resolve_literal(item, values, seen | {key})
    if status not in {'LITERAL', 'OK_ALIAS'}:
        return None, status
    try:
        if conversion == 'int':
            resolved = int(resolved)
        elif conversion == 'string':
            resolved = str(resolved)
        elif conversion == 'bool':
            if isinstance(resolved, bool):
                pass
            elif isinstance(resolved, str) and resolved.lower() in {
                'true',
                'false',
                'yes',
                'no',
                '1',
                '0',
            }:
                resolved = resolved.lower() in {'true', 'yes', '1'}
            else:
                return None, 'ALIAS_FILTER_UNGEPRUEFT'
    except (ValueError, TypeError):
        return None, 'ALIAS_FILTER_UNGUELTIG'
    return resolved, 'OK_ALIAS'


def setting_severity(row):
    status = row['status']
    if status in {'OK', 'OK_ALIAS', 'ROLLENDEFAULT', 'OPTIONALER_DEFAULT'}:
        return 'ok'
    if status in {
        'ANSIBLE_KONTEXT',
        'BEISPIELWERT_ABWEICHEND',
        'UNBEKANNTE_TLS_AUFGABE',
        'UNBEKANNT_ABER_TEXTTREFFER',
        'UNBEKANNT_OHNE_STATISCHEN_TREFFER',
    }:
        return 'info'
    if status in {'HOSTBEZOGEN_UNGEPRUEFT', 'DYNAMISCH_UNGEPRUEFT'}:
        return 'warning' if row.get('required') else 'info'
    if status in {'FEHLT', 'LEER'}:
        return 'warning'
    return 'error'


def _read_version_markers(marker_path, variables):
    # Nur gezielte Marker, niemals gesamte Settings oder Ausgaben anzeigen.
    if marker_path.suffix == '.toml':
        text = marker_path.read_text()[:16384]
        matches = re.findall(r'^version\s*=\s*"([^"]+)"', text, re.M)
    elif marker_path.name == '__init__.py':
        matches = re.findall(
            r'^__version__\s*=\s*[\'"]([^\'"]+)', marker_path.read_text()[:4096], re.M
        )
    elif marker_path.suffix in ('.yml', '.yaml'):
        text = marker_path.read_text()[:16384]
        matches = []
        for variable in variables or []:
            if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', variable):
                matches += re.findall(
                    r'^' + re.escape(variable) + r':\s*[\'"]?([^\s\'"]+)',
                    text,
                    re.M,
                )
    else:
        matches = VERSION_RE.findall(marker_path.read_text()[:4096])[:1]
    return matches


def version_hint(root, paths, variables=None):
    versions = set()
    for rel in paths:
        try:
            marker_path = guarded(root, rel)
            if not marker_path.is_file():
                continue
            matches = _read_version_markers(marker_path, variables)
            versions.update(version for version in matches if VERSION_RE.fullmatch(version))
        except (OSError, UnicodeError):
            continue
    return sorted(versions)


def file_enabled(manifest, rel, features):
    gates = manifest.get('file_features', {}).get(rel, [])
    if not gates:
        return True
    # Mehrere bekannte Verbraucher: OR. Unbekannte Schalter bleiben pruefpflichtig.
    return not all(features.get(key) is False for key in gates)


def check_component(root, manifest, features=None):
    if manifest.get('schema') != 1:
        raise AuditError('MANIFEST_SCHEMA_UNGUELTIG')
    identifier = manifest['id']
    expected = manifest['version']
    features = features or {}
    if not re.fullmatch(r'[a-z0-9_-]+', identifier):
        raise AuditError('KOMPONENTEN_ID_UNGUELTIG')
    files = manifest['files']
    if not isinstance(files, dict) or not files:
        raise AuditError('LEERES_KOMPONENTENMANIFEST')
    issues = []
    rows = []
    matched = 0
    active = 0
    active_matched = 0
    for rel, wanted in sorted(files.items()):
        if not public_library(rel) and any(
            part
            in {
                'group_vars',
                'host_vars',
                'inventory',
                'x',
                '_local',
                '.git',
                '.ssh',
                'artifacts',
            }
            for part in Path(rel).parts
        ):
            raise AuditError('KONFIGURATION_ODER_SECRET_IM_SHA_MANIFEST')
        if not re.fullmatch(r'[a-f0-9]{64}', wanted):
            raise AuditError('SHA_UNGUELTIG')
        enabled = file_enabled(manifest, rel, features)
        active += int(enabled)
        path = guarded(root, rel)
        actual = None
        lexical = root / rel
        if any(
            file_path.is_symlink()
            for file_path in (lexical, *lexical.parents)
            if file_path.is_relative_to(root)
        ):
            status = 'UNSAFE_SYMLINK'
        elif not path.is_file():
            status = 'FEHLT'
        else:
            try:
                actual = sha(path)
                status = 'OK' if actual == wanted else 'SHA_ABWEICHUNG'
            except OSError:
                status = 'UNLESBAR'
        if status == 'OK':
            matched += 1
            active_matched += int(enabled)
        elif enabled:
            issues.append({'path': rel, 'status': status})
        rows.append(
            {
                'path': rel,
                'status': status if enabled else 'DEAKTIVIERT_' + status,
                'required': enabled,
                'features': manifest.get('file_features', {}).get(rel, []),
                'expected_sha256': wanted,
                'actual_sha256': actual,
            }
        )
    exact = matched == len(files)
    detected = expected if exact else None
    if issues:
        for old in manifest.get('known_versions', []):
            if old.get('files') and all(
                guarded(root, file_path).is_file()
                and sha(guarded(root, file_path)) == expected_hash
                for file_path, expected_hash in old['files'].items()
            ):
                detected = old['version']
                break
    hints = version_hint(
        root, manifest.get('version_files', []), manifest.get('version_variables', [])
    )
    if (
        manifest.get('check_version_markers')
        and exact
        and hints
        and any(version != expected for version in hints)
    ):
        issues.append({'path': 'Versionsmarker', 'status': 'WIDERSPRUCH_ZUM_SHA_STAND'})
        exact = False
        detected = None
    status = 'ABWEICHEND' if issues else 'OK' if exact else 'AKTIVER_UMFANG_OK'
    return {
        'id': identifier,
        'expected_version': expected,
        'verified_version': detected,
        'status': status,
        'matched': matched,
        'tracked': len(files),
        'active_tracked': active,
        'active_matched': active_matched,
        'issues': issues,
        'files': rows,
        'declared_versions': hints,
        'scope': manifest.get('scope', 'Lokaler Controller-Code'),
    }


def variable_base(root, kind='group_vars'):
    bases = []
    for rel in [kind, 'inventory/' + kind]:
        candidate = guarded(root, rel)
        if candidate.is_dir() and candidate not in bases:
            bases.append(candidate)
    if len(bases) > 1:
        raise AuditError('ZWEI_GETRENNTE_VARIABLENABLAGEN_' + kind.upper())
    return bases[0] if bases else guarded(root, kind)


def global_settings(root):
    values = {}
    sources = {}
    errors = []
    base = variable_base(root) / 'all'
    files = (
        sorted(
            settings_path
            for settings_path in base.iterdir()
            if settings_path.suffix in ('.yml', '.yaml') and settings_path.is_file()
        )
        if base.is_dir()
        else []
    )
    for settings_path in files:
        rel = str(settings_path.relative_to(root))
        if not settings_path.resolve().is_relative_to(root):
            errors.append({'path': rel, 'status': 'PFAD_AUSSERHALB_PROJEKT'})
            continue
        if '.example' in settings_path.name or '.sample' in settings_path.name:
            errors.append({'path': rel, 'status': 'BEISPIEL_IN_AKTIVER_KONFIGURATION'})
            continue
        try:
            data = read_yaml(settings_path)
        except AuditError as error:
            errors.append({'path': rel, 'status': str(error)})
            continue
        # Ansible ersetzt Dictionaries bei normalem hash_behaviour=replace.
        # Report overlapping definitions explicitly.
        for key, value in data.items():
            if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key):
                errors.append({'path': rel, 'status': 'UNGUELTIGER_VARIABLENNAME'})
                continue
            if key in values:
                errors.append({'key': key, 'status': 'MEHRFACH_GLOBAL_DEFINIERT', 'path': rel})
            values[key] = value
            sources[key] = rel
    if not files:
        errors.append({'path': 'group_vars/all', 'status': 'GLOBALE_SETTINGS_FEHLEN'})
    return values, errors


def _collect_definitions(root, base, directory, definitions):
    for settings_path in directory.rglob('*'):
        if (
            not settings_path.is_file()
            or settings_path.suffix not in ('.yml', '.yaml')
            or '.example' in settings_path.name
        ):
            continue
        if base == 'group_vars' and settings_path.relative_to(directory).parts[0] == 'all':
            continue
        try:
            if settings_path.resolve().is_relative_to(root):
                definitions.update(read_yaml(settings_path).keys())
        except AuditError:
            continue


def scoped_definitions(root):
    # Collect alternate definition names without exposing their values.
    definitions = set()
    for base in ('group_vars', 'host_vars'):
        directory = variable_base(root, base)
        if not directory.is_dir():
            continue
        _collect_definitions(root, base, directory, definitions)
    return definitions


def _find_text_references(source_path, root, pattern, hits):
    try:
        if source_path.stat().st_size > 1024 * 1024:
            return
        for number, line in enumerate(source_path.read_text().splitlines(), 1):
            if pattern.search(line):
                hits.append({'path': str(source_path.relative_to(root)), 'line': number})
    except (OSError, UnicodeError):
        return


def _find_yaml_references(node, pattern, relative_path, hits):
    visited = set()

    def walk(value):
        if value is None or id(value) in visited:
            return
        visited.add(id(value))
        if isinstance(value, yaml.MappingNode):
            for _key_node, child_node in value.value:
                walk(child_node)
        elif isinstance(value, yaml.SequenceNode):
            for child_node in value.value:
                walk(child_node)
        elif (
            isinstance(value, yaml.ScalarNode)
            and dynamic(value.value)
            and pattern.search(value.value)
        ):
            hits.append(
                {
                    'path': str(relative_path),
                    'line': value.start_mark.line + 1,
                }
            )

    walk(node)


def find_usage(root, key):
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', key):
        raise AuditError('UNGUELTIGER_VARIABLENNAME')
    parts = key.split('.')
    expression = r'\b' + re.escape(key) + r'\b'
    if len(parts) == 2:
        parent, child = parts
        expression += (
            r'|\b'
            + re.escape(parent)
            + r"(?:\[['\"]"
            + re.escape(child)
            + r"['\"]\]|\.get\(['\"]"
            + re.escape(child)
            + r"['\"])"
        )
    if len(parts) == 2 and parts[0] == 'features':
        expression += r'|[\"\']feature[\"\']\s*:\s*[\"\']' + re.escape(parts[1]) + r'[\"\']'
    pattern = re.compile(expression)
    hits = []
    for directory in [
        'bin',
        'scripts',
        'lib',
        'roles',
        'playbooks',
        'templates',
        'config',
        'filter_plugins',
        'plugins',
    ]:
        base = guarded(root, directory)
        if not base.is_dir():
            continue
        for source_path in sorted(base.rglob('*')):
            if not source_path.is_file() or any(
                part in {'__pycache__', 'x', 'backups', '_local', '.git', 'tests'}
                for part in source_path.parts
            ):
                continue
            if source_path.suffix not in {
                '.py',
                '.sh',
                '.j2',
                '.yml',
                '.yaml',
                '.json',
                '.cfg',
                '.toml',
                '.zsh',
                '.ps1',
                '.js',
                '.html',
            } and source_path.name not in {'control', 'bashrc'}:
                continue
            if not source_path.resolve().is_relative_to(root):
                continue
            _find_text_references(source_path, root, pattern, hits)
    seen_files = set()
    for directory in ['group_vars', 'host_vars', 'inventory']:
        base = guarded(root, directory)
        if not base.is_dir():
            continue
        for source_path in sorted(base.rglob('*')):
            if (
                not source_path.is_file()
                or source_path.suffix not in ('.yml', '.yaml')
                or '.example' in source_path.name
            ):
                continue
            resolved = source_path.resolve()
            if not resolved.is_relative_to(root) or resolved in seen_files:
                continue
            seen_files.add(resolved)
            try:
                node = yaml.compose(source_path.read_text())
            except (OSError, UnicodeError, yaml.YAMLError):
                continue
            _find_yaml_references(node, pattern, source_path.relative_to(root), hits)
    return hits


def unknown_settings(root, values, contract):
    known = {rule['key'] for rule in contract.get('fields', [])}
    roots = {key.split('.')[0] for key in known}
    # Ansible-interne Verbindungsvariablen sind normale bekannte Plattformvariablen.
    roots.update(
        {
            'ansible_user',
            'ansible_port',
            'ansible_password',
            'ansible_become',
            'ansible_become_user',
            'ansible_become_method',
            'ansible_become_password',
            'ansible_python_interpreter',
            'managed_access_effective_user',
        }
    )
    candidates = [key for key in values if key not in roots]
    features = values.get('features', {})
    if isinstance(features, dict):
        candidates += [
            'features.' + key
            for key in features
            if isinstance(key, str)
            and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key)
            and 'features.' + key not in known
        ]
    result = []
    for key in sorted(candidates):
        hits = find_usage(root, key)
        result.append(
            {
                'key': key,
                'status': 'UNBEKANNT_ABER_TEXTTREFFER'
                if hits
                else 'UNBEKANNT_OHNE_STATISCHEN_TREFFER',
                'usage': hits,
                'deletion_allowed': False,
            }
        )
    return result


def _missing_setting_status(rule, scoped, root):
    key = rule['key']
    if key.split('.')[0] in scoped:
        return 'HOSTBEZOGEN_UNGEPRUEFT'
    if not rule.get('default_source'):
        return 'FEHLT' if rule.get('required') else 'OPTIONALER_DEFAULT'
    try:
        defaults = read_yaml(guarded(root, rule['default_source']))
        exists, value = field(defaults, key)
        return 'ROLLENDEFAULT' if exists and good_type(value, rule['type']) else 'FEHLT'
    except AuditError:
        return 'FEHLT'


def check_settings(root, contract, code_root=None, report_unknown=True, check_links=True):
    values, errors = global_settings(root)
    rows = []
    scoped = scoped_definitions(root)
    for rule in contract.get('fields', []):
        key = rule['key']
        feature = rule.get('feature')
        if feature:
            present, enabled = field(values, 'features.' + feature)
            if present and enabled is False:
                continue
            if not present or not isinstance(enabled, bool):
                # Feature switches are checked separately.
                continue
        exists, value = field(values, key)
        if not exists:
            status = _missing_setting_status(rule, scoped, code_root or root)
        else:
            checked, alias_status = resolve_literal(value, values)
            if alias_status not in {'LITERAL', 'OK_ALIAS'}:
                status = alias_status
            elif not good_type(checked, rule['type']):
                status = 'FALSCHER_TYP'
            elif rule.get('choices') and checked not in rule['choices']:
                status = 'UNGUELTIGE_AUSWAHL'
            elif rule.get('nonempty') and checked in ('', [], {}, None):
                status = 'LEER'
            else:
                status = 'OK_ALIAS' if alias_status == 'OK_ALIAS' else 'OK'
        rows.append(
            {
                'key': key,
                'status': status,
                'expected_type': rule['type'],
                'required': bool(rule.get('required')),
            }
        )
    # TLS-Eintraege einzeln pruefen, neue/vergessene Aufgabennamen erkennen.
    tls = values.get('tls_validate_certs', {})
    if isinstance(tls, dict):
        allowed = set(contract.get('tls_tasks', []))
        existing_keys = {row['key'] for row in rows}
        for key, configured_value in tls.items():
            if 'tls_validate_certs.' + str(key) in existing_keys:
                continue
            label = (
                key
                if isinstance(key, str) and re.fullmatch(r'[a-z0-9_]+', key)
                else 'UNGUELTIGER_SCHLUESSEL'
            )
            status = (
                'UNBEKANNTE_TLS_AUFGABE'
                if key not in allowed
                else 'DYNAMISCH_UNGEPRUEFT'
                if dynamic(configured_value)
                else 'OK'
                if isinstance(configured_value, bool)
                else 'FALSCHER_TYP'
            )
            rows.append(
                {
                    'key': 'tls_validate_certs.' + label,
                    'status': status,
                    'expected_type': 'boolean',
                    'required': False,
                }
            )
    # Alias-Pfade pruefen, ohne Inventory oder dessen Plugins auszufuehren.
    for rel, target in [
        ('inventory/group_vars', 'group_vars'),
        ('inventory/host_vars', 'host_vars'),
    ]:
        link_path = root / rel
        if check_links and (root / target).is_dir():
            if not link_path.exists():
                errors.append({'path': rel, 'status': 'VARIABLEN_VERLINKUNG_FEHLT'})
            elif link_path.resolve() != (root / target).resolve():
                errors.append({'path': rel, 'status': 'ZWEITE_VARIABLENABLAGE'})
    for row in rows:
        row['severity'] = setting_severity(row)
    rows.sort(key=lambda entry: entry['key'])
    return {
        'fields': rows,
        'errors': errors,
        'unknown_variables': unknown_settings(root, values, contract) if report_unknown else [],
        'scope': 'Nur lokal lesbare globale YAML-Werte; Jinja/Lookups und Host-/Gruppenpraezedenz werden nicht ausgefuehrt.',
    }


def _registry_commands(root):
    directory = guarded(root, 'bin/control.d')
    for registry_path in sorted(directory.glob('*.json')):
        if not registry_path.resolve().is_relative_to(root):
            raise AuditError('REGISTRY_PFAD_AUSSERHALB_PROJEKT')
        doc = load_json(registry_path)
        commands = doc.get('commands')
        if not isinstance(commands, list):
            raise AuditError('REGISTRY_SCHEMA_UNGUELTIG')
        yield from commands


def check_registry(root, features=None, settings_root=None):
    names = set()
    aliases = {}
    issues = []
    count = 0
    values, _ = global_settings(settings_root or root)
    for cmd in _registry_commands(root):
        name = cmd.get('name', '')
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', name):
            raise AuditError('REGISTRY_NAME_UNGUELTIG')
        if name in names:
            issues.append({'command': name, 'status': 'DOPPELTER_BEFEHL'})
        names.add(name)
        count += 1
        for alias in cmd.get('aliases', []):
            alias_name = alias.get('name', '')
            if not isinstance(alias_name, str) or not re.fullmatch(
                r'[a-zA-Z0-9][a-zA-Z0-9_-]*', alias_name
            ):
                raise AuditError('ALIAS_NAME_UNGUELTIG')
            if alias_name in aliases and aliases[alias_name] != name:
                issues.append({'command': name, 'status': 'DOPPELTER_ALIAS'})
            aliases[alias_name] = name
        feature = cmd.get('feature')
        if feature:
            present, enabled = field(values, 'features.' + feature)
            if not present:
                enabled = (features or {}).get(feature, cmd.get('feature_default', False))
            if enabled is False:
                continue
        for rel in [cmd.get('handler', '')] + cmd.get('requires', []):
            if not guarded(root, rel).is_file():
                issues.append({'command': name, 'status': 'MODULDATEI_FEHLT', 'path': rel})
    for alias, name in aliases.items():
        if alias in names and alias != name:
            issues.append({'command': name, 'status': 'ALIAS_KOLLIDIERT_MIT_BEFEHL'})
    return {'commands': count, 'issues': issues, 'executed': False}


def audit(root, here, only=None):
    installed = root / ".controller-install.json"
    receipt = load_json(installed) if installed.is_file() and not installed.is_symlink() else {}
    live_manifest = (
        receipt.get("files")
        if receipt.get("schema") in (1, 2) and receipt.get("source") in ("main", "staging")
        else None
    )
    addon_manifests = []
    if receipt.get("schema") == 2:
        modules = receipt.get("modules", {})
        owners = receipt.get("owners", {})
        files = receipt.get("files", {})
        if (
            not isinstance(modules, dict)
            or not isinstance(owners, dict)
            or not isinstance(files, dict)
            or owners.keys() != files.keys()
            or not all(name in modules for name in owners.values())
        ):
            raise AuditError("INVALID_MODULE_OWNERSHIP")
        for name, meta in modules.items():
            if meta["kind"] != "addon":
                continue
            addon_files = {
                file_path: files[file_path]
                for file_path, owner in owners.items()
                if owner == name
            }
            addon_manifests.append(
                {
                    "schema": 1,
                    "id": "addon-" + name.lower(),
                    "version": meta["version"],
                    "files": addon_files,
                    "scope": name,
                }
            )
        if live_manifest is not None:
            live_manifest = {
                file_path: file_hash
                for file_path, file_hash in live_manifest.items()
                if modules[owners[file_path]]["kind"] != "addon"
            }
    if live_manifest is None:
        seal = load_json(here / 'integrity.json')
        for rel, wanted in seal.get('files', {}).items():
            file_path = guarded(here, rel)
            if not file_path.is_file() or sha(file_path) != wanted:
                raise AuditError('PRUEFER_ODER_MANIFEST_SHA_ABWEICHUNG')
    release = load_json(here / 'release.json')
    if live_manifest is None:
        expected_paths = set(
            release['manifests']
            + [
                'check.py',
                'check.sh',
                'configure.py',
                'probes.py',
                'release.json',
                'settings_contract.json',
                'settings_catalog.json',
                'VERSION.txt',
                'cleanup.py',
                'cleanup_plan.json',
            ]
        )
        if not expected_paths.issubset(seal['files']):
            raise AuditError('UNVERSIEGELTE_PRUEFDATEN')
    report = {
        'schema': 1,
        'checker_version': CHECKER_VERSION,
        'controller_profile': release['profile'],
        'expected_controller_release': release['controller_release'],
        'delivery_scope': release.get('delivery_scope', 'combined_update'),
        'controller_release_verified': False,
        'read_only': True,
        'network_accessed': False,
        'remote_runtime_checked': False,
        'components': [],
        'extensions': [],
        'settings': None,
        'registry': None,
        'errors': [],
    }
    values, config_errors = global_settings(root)
    features = dict(release.get('feature_defaults', {}))
    if isinstance(values.get('features', {}), dict):
        features.update(values.get('features', {}))
    report['features'] = {
        feature_key: (
            'aktiv'
            if flag_value is True
            else 'deaktiviert'
            if flag_value is False
            else 'ungeprueft'
        )
        for feature_key, flag_value in features.items()
    }
    if live_manifest is not None:
        report['controller_profile'] = receipt['profile']
        report['expected_controller_release'] = receipt['source']
        if only in (None, 'controller_basis'):
            report['components'].append(
                check_component(
                    root,
                    {
                        'schema': 1,
                        'id': 'controller_basis',
                        'version': receipt['source'],
                        'files': live_manifest,
                    },
                )
            )
    else:
        for rel in release['manifests']:
            result = check_component(root, load_json(guarded(here, rel)), features)
            if only is None or only == result['id']:
                report['components'].append(result)
    if only is None or only == 'settings':
        report['settings'] = check_settings(root, load_json(here / 'settings_contract.json'))
    extension_manifests = list(addon_manifests)
    for module in addon_manifests:
        if only is None or only == module["id"]:
            report["extensions"].append(check_component(root, module, features))
    for extension in sorted((here / 'extensions').glob('*')):
        if not extension.is_dir():
            continue
        if extension.is_symlink() or not extension.resolve().is_relative_to(here):
            raise AuditError('ADDON_PFAD_UNGUELTIG')
        ext_seal = load_json(extension / 'integrity.json')
        if sha(extension / 'manifest.json') != ext_seal.get('manifest_sha256'):
            raise AuditError('ADDON_MANIFEST_SHA_ABWEICHUNG')
        manifest = load_json(extension / 'manifest.json')
        if manifest.get('id') in {
            component_row['id'] for component_row in report['components'] + extension_manifests
        }:
            raise AuditError('DOPPELTE_ADDON_ID')
        extension_manifests.append(manifest)
        if only == manifest['id'] or (only is None and live_manifest is None):
            report['extensions'].append(check_component(root, manifest, features))
    if only is None or only == 'registry':
        report['registry'] = check_registry(root, features)
    known = {entry['id'] for entry in report['components'] + extension_manifests} | {
        'settings',
        'registry',
        'cleanup',
        'local',
    }
    if only and only not in known:
        raise AuditError('UNBEKANNTE_KOMPONENTE')
    code_ok = bool(report['components']) and all(
        component['status'] == 'OK' for component in report['components']
    )
    report['controller_release_verified'] = (
        only is None
        and code_ok
        and all(component['status'] == 'OK' for component in report['extensions'])
    )
    report['active_scope_verified'] = all(
        component['status'] in ('OK', 'AKTIVER_UMFANG_OK')
        for component in report['components'] + report['extensions']
    )
    bad = any(
        component.get('status') not in ('OK', 'AKTIVER_UMFANG_OK')
        for component in report['components'] + report['extensions']
    )
    if report['settings']:
        bad = (
            bad
            or bool(report['settings']['errors'])
            or any(
                entry['severity'] in ('warning', 'error')
                for entry in report['settings']['fields']
            )
        )
    if report['registry']:
        bad = bad or bool(report['registry']['issues'])
    if only is None or only == 'cleanup':
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            'controller_cleanup_preview', here / 'cleanup.py'
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            plan = load_json(here / 'cleanup_plan.json')
            report['cleanup'] = module.preview(root, plan, external=False)
            report['cleanup']['receipt'] = module.receipt_status(root, plan)
        except module.CleanupError:
            raise AuditError('BEREINIGUNGSPLAN_ODER_PROJEKT_UNGUELTIG') from None
    if only in (None, 'local'):
        report['local_extensions'] = local_extensions.inspect(root)
        bad = bad or not local_extensions.passed(report['local_extensions'])
    report['status'] = 'PRUEFBEDARF' if bad else 'OK'
    return report


def _print_usage(hits, indent):
    for hit in hits:
        print(indent + hit['path'] + ':' + str(hit['line']))


def display(report, details, color='auto'):
    if 'local_extensions' in report:
        local_extensions.display(report['local_extensions'])
    import os

    enabled = color == 'always' or (
        color == 'auto' and sys.stdout.isatty() and 'NO_COLOR' not in os.environ
    )
    palette = {'ok': '32', 'info': '36', 'warning': '33', 'error': '31'}

    def line(text, severity='info'):
        print(('\033[' + palette[severity] + 'm' + text + '\033[0m') if enabled else text)

    line(tr("audit.title", version=report["checker_version"]), 'info')
    print(
        tr(
            "audit.profile",
            profile=report["controller_profile"],
            release=report["expected_controller_release"],
        )
    )
    if report.get('delivery_scope') == 'checker_only':
        print(tr("audit.checker_only"))
    line(
        tr(
            "audit.release",
            status=tr("audit.complete")
            if report["controller_release_verified"]
            else tr("audit.active_scope")
            if report.get("active_scope_verified")
            else status_text("PRUEFBEDARF"),
        ),
        'ok' if report.get('active_scope_verified') else 'warning',
    )
    states = report.get('features', {})
    if states:
        print(
            tr(
                "audit.features",
                enabled=sum(feature_state == "aktiv" for feature_state in states.values()),
                disabled=sum(
                    feature_state == "deaktiviert" for feature_state in states.values()
                ),
            )
        )
        if details:
            for name, state in sorted(states.items()):
                print('  ' + name + ': ' + status_text(state))
    for row in report['components'] + report['extensions']:
        status = row['status']
        severity = (
            'ok'
            if status == 'OK'
            else 'info'
            if status == 'AKTIVER_UMFANG_OK'
            else 'info'
            if status == 'NICHT_INSTALLIERT'
            else 'warning'
            if status in ('PRUEFMODUL_FEHLT', 'BEKANNTER_AELTERER_STAND')
            else 'error'
        )
        line(
            tr(
                "audit.component",
                name=row["id"],
                status=status_text(status),
                verified=row.get("verified_version") or tr("audit.unverified"),
                expected=row.get("expected_version", "-"),
            ),
            severity,
        )
        if details and row.get('declared_versions'):
            print(tr("audit.markers", markers=", ".join(row["declared_versions"])))
        if 'matched' in row:
            print(tr("audit.matched", matched=row["matched"], tracked=row["tracked"]))
        for issue in row.get('issues', []):
            line('    ' + status_text(issue['status']) + ' ' + issue['path'], 'error')
        if not details:
            continue
        for item in row.get('files', []):
            if not item['required']:
                line('    ' + status_text(item['status']) + ' ' + item['path'], 'info')
    if report['settings']:
        settings = report['settings']
        counts = {
            level: sum(
                row.get('severity', setting_severity(row)) == level
                for row in settings['fields']
            )
            for level in ['error', 'warning', 'info']
        }
        counts['error'] += len(settings['errors'])
        print(tr("audit.settings", fields=len(settings["fields"]), **counts))
        for row in settings['errors']:
            line(
                '  ' + status_text(row['status']) + ' ' + row.get('key', row.get('path', '')),
                'error',
            )
        for row in settings['fields']:
            severity = row.get('severity', setting_severity(row))
            if details or severity in ('warning', 'error'):
                line('  ' + row['key'] + ': ' + status_text(row['status']), severity)
        if counts['info'] and not details:
            line(tr("audit.details_hint"), 'info')
        unknown = settings.get('unknown_variables', [])
        line(tr("audit.unknown", count=len(unknown)), 'info')
        for row in unknown:
            line(
                tr(
                    "audit.references",
                    key=row["key"],
                    status=status_text(row["status"]),
                    count=len(row["usage"]),
                ),
                'info',
            )
            if details:
                _print_usage(row['usage'], '    ')
    if report['registry']:
        registry = report['registry']
        line(
            tr("audit.registry", commands=registry["commands"], issues=len(registry["issues"])),
            'error' if registry['issues'] else 'ok',
        )
        for row in registry['issues']:
            line(
                '  '
                + status_text(row['status'])
                + ' '
                + row['command']
                + ' '
                + row.get('path', ''),
                'error',
            )
    if report.get('extended_checks'):
        print(tr("audit.extended_heading"))
        for row in report['extended_checks']['configuration_and_api_checks']:
            line(
                '  ' + row['id'] + ': ' + status_text(row['status']),
                'ok'
                if row['status'] == 'OK'
                else 'info'
                if row['status'].startswith('SKIP_')
                else 'warning',
            )
            for issue in row.get('issues', []):
                line('    ' + status_text(issue['status']) + ' ' + issue['path'], 'warning')
        print(tr("audit.requests", count=report["extended_checks"]["network_requests"]))
    line(
        tr("audit.result", status=status_text(report["status"])),
        'ok' if report['status'] == 'OK' else 'warning',
    )
    if report.get('cleanup'):
        cleanup = report['cleanup']
        line(
            tr(
                "audit.cleanup",
                status=status_text(cleanup["status"]),
                count=cleanup["candidates"],
                retained=cleanup["retained"],
            ),
            'info',
        )
        print(
            tr(
                "audit.receipt",
                status=status_text(cleanup.get("receipt", "NOCH_KEIN_LAUFNACHWEIS")),
            )
        )
        if cleanup['candidates']:
            print(tr("audit.cleanup_hint"))
        if details:
            for row in cleanup['files']:
                print('  ' + status_text(row['status']) + ' ' + row['path'])


def _run_cleanup(root, here, only, module_name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(module_name, here / 'cleanup.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        module.interactive(root, load_json(here / 'cleanup_plan.json'))
    except (module.CleanupError, EOFError, KeyboardInterrupt):
        raise AuditError('BEREINIGUNG_ABGEBROCHEN_ODER_NICHT_SICHER') from None
    report = audit(root, here, only)
    report['read_only'] = False
    report['cleanup_executed'] = True
    return report


def _show_blocked_extensions(local, as_json):
    if as_json:
        print(
            json.dumps(
                machine_report(
                    {
                        "status": local["status"],
                        "read_only": True,
                        "local_extensions": local,
                    }
                )
            )
        )
    else:
        local_extensions.display(local)


def main():
    argv = cli_args(sys.argv[1:], Path(__file__).resolve().parents[1])
    if "--versions" in argv:
        from rollout import show_versions

        parser = argparse.ArgumentParser(description=tr("audit.versions_help"))
        parser.add_argument("--versions", action="store_true")
        parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
        return show_versions(parser.parse_args(argv).root)
    if any(arg in {"--remote", "--apply", "--auto", "--rollback", "--staging"} for arg in argv):
        import rollout

        return rollout.main(argv)
    parser = argparse.ArgumentParser(
        description=tr("audit.description"), epilog=tr("audit.git_help")
    )
    parser.add_argument("--lang", choices=("de", "en"), help=tr("cli.lang"))
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--json', action='store_true', help=tr("audit.json_help"))
    parser.add_argument('--details', action='store_true', help=tr("audit.details_help"))
    parser.add_argument('--only', help=tr("audit.only_help"))
    parser.add_argument('--configure', action='store_true', help=tr("audit.configure_help"))
    parser.add_argument(
        '--color',
        choices=['auto', 'always', 'never'],
        default='auto',
        help=tr("audit.color_help"),
    )
    parser.add_argument('--no-prompt', action='store_true', help=tr("audit.no_prompt_help"))
    parser.add_argument('--cleanup', action='store_true', help=tr("audit.cleanup_help"))
    parser.add_argument('--check', action='store_true', help=tr("audit.check_help"))
    parser.add_argument('--offline', action='store_true', help=tr("audit.offline_help"))
    parser.add_argument('--timeout', type=int, default=8, help=tr("audit.timeout_help"))
    parser.add_argument('--field', action='append', default=[], help=tr("audit.field_help"))
    parser.add_argument('--find-usage', metavar='VARIABLE', help=tr("audit.usage_help"))
    parser.add_argument('--sort-settings', action='store_true', help=tr("audit.sort_help"))
    args = parser.parse_args(argv)
    try:
        if args.cleanup and (
            args.json
            or args.configure
            or args.sort_settings
            or args.check
            or args.only
            or args.find_usage
        ):
            raise AuditError('BEREINIGUNG_GETRENNT_AUFRUFEN')
        if args.offline and not args.check:
            raise AuditError('OFFLINE_BENOETIGT_CHECK')
        if not 1 <= args.timeout <= 30:
            raise AuditError('TIMEOUT_MUSS_1_BIS_30_SEIN')
        root = args.root.resolve()
        here = Path(__file__).resolve().parent
        if args.cleanup or args.configure or args.sort_settings:
            local = local_extensions.inspect(root)
            if not local_extensions.passed(local):
                _show_blocked_extensions(local, args.json)
                return 1
        report = audit(root, here, args.only)
        if args.cleanup:
            report = _run_cleanup(root, here, args.only, 'controller_cleanup_action')
        if args.find_usage:
            hits = find_usage(root, args.find_usage)
            result = {
                'variable': args.find_usage,
                'usage': hits,
                'deletion_allowed': False,
                'note': 'Texttreffer sind kein vollstaendiger Nachweis dynamischer Verwendung.',
            }
            if args.json:
                print(json.dumps(machine_report(result), ensure_ascii=False, indent=2))
            else:
                print(args.find_usage + ': ' + str(len(hits)) + tr("audit.matches"))
                _print_usage(hits, '  ')
            return 0
        if args.field and not args.configure:
            raise AuditError('FIELD_BENOETIGT_CONFIGURE')
        if args.configure or args.sort_settings:
            if args.json or args.only not in (None, 'settings'):
                raise AuditError('INTERAKTIV_NICHT_MIT_JSON_ODER_KOMPONENTENFILTER_KOMBINIEREN')
            if not sys.stdin.isatty():
                raise AuditError('KONFIGURATION_BENOETIGT_INTERAKTIVES_TERMINAL')
            if not (root / 'bin/control').is_file() and not (root / 'ansible.cfg').is_file():
                raise AuditError('ANSIBLE_PROJEKTROOT_NICHT_ERKANNT')
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                'controller_settings_wizard', here / 'configure.py'
            )
            wizard = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wizard)
            display(report, False, args.color)
            try:
                changed = wizard.configure(
                    root,
                    here,
                    sys.modules[__name__],
                    sort_only=not args.configure,
                    selected_keys=args.field or None,
                )
            except (wizard.ConfigureError, EOFError, KeyboardInterrupt):
                raise AuditError(
                    'KONFIGURATION_ABGEBROCHEN_ODER_NICHT_SICHER_AENDERBAR'
                ) from None
            report = audit(root, here, args.only)
            report['read_only'] = not changed
            report['configuration_changed'] = changed
        if args.check:
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                'controller_readonly_probes', here / 'probes.py'
            )
            probes = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(probes)
            report['extended_checks'] = probes.run(
                root,
                sys.modules[__name__],
                offline=args.offline,
                timeout=args.timeout,
                active_files={
                    file_entry['path']: file_entry['required']
                    for component in report['components'] + report['extensions']
                    for file_entry in component.get('files', [])
                },
                progress=lambda label: print(
                    tr('audit.probe', name=label), file=sys.stderr, flush=True
                ),
            )
            report['network_accessed'] = report['extended_checks']['network_requests'] > 0
            if any(
                row['status'] != 'OK' and not row['status'].startswith('SKIP_')
                for row in report['extended_checks']['configuration_and_api_checks']
            ):
                report['status'] = 'PRUEFBEDARF'
        if args.json:
            print(json.dumps(machine_report(report), ensure_ascii=False, indent=2))
        else:
            display(report, args.details, args.color)
        if (
            not args.json
            and not args.no_prompt
            and not any(
                [
                    args.cleanup,
                    args.check,
                    args.configure,
                    args.sort_settings,
                    args.only,
                    args.find_usage,
                ]
            )
            and local_extensions.passed(report['local_extensions'])
            and report.get('cleanup', {}).get('candidates', 0)
            and sys.stdin.isatty()
            and sys.stdout.isatty()
        ):
            if input(tr("audit.cleanup_prompt")).strip().lower() in {'j', 'ja', 'y', 'yes'}:
                report = _run_cleanup(root, here, args.only, 'controller_cleanup_prompt')
                display(report, args.details, args.color)
        return 0 if report['status'] == 'OK' else 1
    except (
        AuditError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        UnicodeError,
        RecursionError,
    ) as exc:
        code = str(exc) if isinstance(exc, AuditError) else 'LOKALE_PRUEFDATEN_UNLESBAR'
        if args.json:
            print(
                json.dumps(
                    machine_report(
                        {
                            'status': 'FEHLER',
                            'error': code,
                            'read_only': not (
                                args.cleanup or args.configure or args.sort_settings
                            ),
                        }
                    )
                )
            )
        else:
            print(
                tr("audit.error_label") + status_text(code) + tr("audit.error_hint"),
                file=sys.stderr,
            )
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
