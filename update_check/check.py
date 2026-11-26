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
from staging_manifest import public_library
import local_extensions
try:
    import yaml
except ImportError:
    raise SystemExit('FEHLER: Python-Paket PyYAML fehlt. Den Python-Interpreter der Ansible-Umgebung verwenden.')

CHECKER_VERSION = '1.3.0'
VERSION_RE = re.compile(r'(?<![A-Za-z0-9])\d+\.\d+\.\d+(?:[a-zA-Z][A-Za-z0-9.-]*)?')
class AuditError(Exception): pass
class UniqueLoader(yaml.SafeLoader): pass

def unique_mapping(loader, node, deep=False):
    seen = set()
    for k,v in node.value:
        if k.tag == 'tag:yaml.org,2002:merge': continue
        key = loader.construct_object(k, deep=deep)
        if key in seen: raise AuditError('DOPPELTE_YAML_SCHLUESSEL')
        seen.add(key)
    loader.flatten_mapping(node)
    return yaml.SafeLoader.construct_mapping(loader,node,deep=deep)
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)

def guarded(root, relative):
    if not isinstance(relative,str) or not relative or '\\' in relative:
        raise AuditError('UNGUELTIGER_RELATIVPFAD')
    path=Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise AuditError('UNGUELTIGER_RELATIVPFAD')
    target=(root/path).resolve()
    if not target.is_relative_to(root): raise AuditError('PFAD_AUSSERHALB_PROJEKT')
    return target

def sha(path):
    value=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''): value.update(block)
    return value.hexdigest()

def load_json(path):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d: raise AuditError('DOPPELTE_JSON_SCHLUESSEL')
            d[k]=v
        return d
    try: return json.loads(path.read_text(),object_pairs_hook=unique)
    except (OSError,ValueError,UnicodeError): raise AuditError('JSON_UNLESBAR') from None

def read_yaml(path):
    try:
        value=yaml.load(path.read_text(),Loader=UniqueLoader)
        if not isinstance(value,dict): raise AuditError('YAML_KEINE_ZUORDNUNG')
        return value
    except AuditError: raise
    except (OSError,UnicodeError,yaml.YAMLError,TypeError,ValueError):
        raise AuditError('YAML_UNLESBAR') from None

def field(values,key):
    value=values
    for part in key.split('.'):
        if not isinstance(value,dict) or part not in value: return False,None
        value=value[part]
    return True,value

def dynamic(value):
    return isinstance(value,str) and ('{{' in value or '{%' in value)

def good_type(value,kind):
    return {'boolean':lambda:isinstance(value,bool), 'integer':lambda:isinstance(value,int) and not isinstance(value,bool), 'string':lambda:isinstance(value,str), 'list':lambda:isinstance(value,list), 'mapping':lambda:isinstance(value,dict), 'duration':lambda:isinstance(value,(str,int)) and not isinstance(value,bool), 'scalar_id':lambda:isinstance(value,(str,int)) and not isinstance(value,bool), 'any':lambda:True}.get(kind,lambda:False)()

def resolve_literal(value,values,seen=None):
    """Nur Dictionary-Aliase und bekannte Ansible-Kontexte erkennen; nie Jinja ausfuehren."""
    if not dynamic(value):return value,'LITERAL'
    seen=set() if seen is None else set(seen)
    m=re.fullmatch(r"\s*\{\{\s*([A-Za-z_][A-Za-z0-9_.]*)(?:\s*\|\s*(int|string|bool))?\s*\}\}\s*",value)
    if m:
        key,conversion=m.groups()
        if key in seen:return None,'ALIAS_ZYKLUS'
        found,item=field(values,key)
        if not found:
            if key.startswith('ansible_') or key in {'inventory_hostname','playbook_dir','inventory_dir'}:return None,'ANSIBLE_KONTEXT'
            return None,'ALIAS_ZIEL_FEHLT'
        resolved,status=resolve_literal(item,values,seen|{key})
        if status not in {'LITERAL','OK_ALIAS'}:return None,status
        try:
            if conversion=='int':resolved=int(resolved)
            elif conversion=='string':resolved=str(resolved)
            elif conversion=='bool':
                if isinstance(resolved,bool):pass
                elif isinstance(resolved,str) and resolved.lower() in {'true','false','yes','no','1','0'}:resolved=resolved.lower() in {'true','yes','1'}
                else:return None,'ALIAS_FILTER_UNGEPRUEFT'
        except (ValueError,TypeError):return None,'ALIAS_FILTER_UNGUELTIG'
        return resolved,'OK_ALIAS'
    if re.fullmatch(r"\s*\{\{\s*(playbook_dir|inventory_dir)\s*\}\}[^{}]*",value):return None,'ANSIBLE_KONTEXT'
    if re.fullmatch(r"\s*\{\{\s*lookup\(\s*['\"](?:ansible\.builtin\.)?env['\"]\s*,\s*['\"]HOME['\"]\s*\)\s*\}\}[^{}]*",value):return None,'ANSIBLE_KONTEXT'
    return None,'DYNAMISCH_UNGEPRUEFT'


def setting_severity(row):
    status=row['status']
    if status in {'OK','OK_ALIAS','ROLLENDEFAULT','OPTIONALER_DEFAULT'}:return 'ok'
    if status in {'ANSIBLE_KONTEXT','BEISPIELWERT_ABWEICHEND','UNBEKANNTE_TLS_AUFGABE','UNBEKANNT_ABER_TEXTTREFFER','UNBEKANNT_OHNE_STATISCHEN_TREFFER'}:return 'info'
    if status in {'HOSTBEZOGEN_UNGEPRUEFT','DYNAMISCH_UNGEPRUEFT'}:return 'warning' if row.get('required') else 'info'
    if status in {'FEHLT','LEER'}:return 'warning'
    return 'error'

def version_hint(root,paths,variables=None):
    versions=set()
    for rel in paths:
        try:
            p=guarded(root,rel)
            if p.is_file():
                # Nur gezielte Marker, niemals gesamte Settings oder Ausgaben anzeigen.
                if p.suffix=='.toml':
                    text=p.read_text()[:16384]
                    matches=re.findall(r'^version\s*=\s*"([^"]+)"',text,re.M)
                elif p.name=='__init__.py':
                    matches=re.findall(r'^__version__\s*=\s*[\'"]([^\'"]+)',p.read_text()[:4096],re.M)
                elif p.suffix in ('.yml','.yaml'):
                    text=p.read_text()[:16384]
                    matches=[]
                    for variable in variables or []:
                        if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',variable):matches+=re.findall(r'^'+re.escape(variable)+r':\s*[\'"]?([^\s\'"]+)',text,re.M)
                else: matches=VERSION_RE.findall(p.read_text()[:4096])[:1]
                versions.update(v for v in matches if VERSION_RE.fullmatch(v))
        except (OSError,UnicodeError): continue
    return sorted(versions)

def file_enabled(manifest,rel,features):
    gates=manifest.get('file_features',{}).get(rel,[])
    if not gates:return True
    # Mehrere bekannte Verbraucher: OR. Unbekannte Schalter bleiben pruefpflichtig.
    return not all(features.get(key) is False for key in gates)

def check_component(root,manifest,features=None):
    if manifest.get('schema')!=1:raise AuditError('MANIFEST_SCHEMA_UNGUELTIG')
    identifier=manifest['id'];expected=manifest['version'];features=features or {}
    if not re.fullmatch(r'[a-z0-9_-]+',identifier):raise AuditError('KOMPONENTEN_ID_UNGUELTIG')
    files=manifest['files']
    if not isinstance(files,dict) or not files:raise AuditError('LEERES_KOMPONENTENMANIFEST')
    issues=[];rows=[];matched=0;active=0;active_matched=0
    for rel,wanted in sorted(files.items()):
        if not public_library(rel) and any(part in {'group_vars','host_vars','inventory','x','_local','.git','.ssh','artifacts'} for part in Path(rel).parts):
            raise AuditError('KONFIGURATION_ODER_SECRET_IM_SHA_MANIFEST')
        if not re.fullmatch(r'[a-f0-9]{64}',wanted):raise AuditError('SHA_UNGUELTIG')
        enabled=file_enabled(manifest,rel,features);active+=int(enabled)
        path=guarded(root,rel);actual=None
        lexical=root/rel
        if any(p.is_symlink() for p in (lexical, *lexical.parents) if p.is_relative_to(root)):
            status='UNSAFE_SYMLINK'
        elif not path.is_file():status='FEHLT'
        else:
            try:actual=sha(path);status='OK' if actual==wanted else 'SHA_ABWEICHUNG'
            except OSError:status='UNLESBAR'
        if status=='OK':matched+=1;active_matched+=int(enabled)
        elif enabled:issues.append({'path':rel,'status':status})
        rows.append({'path':rel,'status':status if enabled else 'DEAKTIVIERT_'+status,'required':enabled,'features':manifest.get('file_features',{}).get(rel,[]),'expected_sha256':wanted,'actual_sha256':actual})
    exact=matched==len(files)
    detected=expected if exact else None
    if issues:
        for old in manifest.get('known_versions',[]):
            if old.get('files') and all(guarded(root,p).is_file() and sha(guarded(root,p))==h for p,h in old['files'].items()):detected=old['version'];break
    hints=version_hint(root,manifest.get('version_files',[]),manifest.get('version_variables',[]))
    if manifest.get('check_version_markers') and exact and hints and any(v!=expected for v in hints):issues.append({'path':'Versionsmarker','status':'WIDERSPRUCH_ZUM_SHA_STAND'});exact=False;detected=None
    status='ABWEICHEND' if issues else 'OK' if exact else 'AKTIVER_UMFANG_OK'
    return {'id':identifier,'expected_version':expected,'verified_version':detected,'status':status,'matched':matched,'tracked':len(files),'active_tracked':active,'active_matched':active_matched,'issues':issues,'files':rows,'declared_versions':hints,'scope':manifest.get('scope','Lokaler Controller-Code')}

def variable_base(root,kind='group_vars'):
    bases=[]
    for rel in [kind,'inventory/'+kind]:
        p=guarded(root,rel)
        if p.is_dir() and p not in bases:bases.append(p)
    if len(bases)>1:raise AuditError('ZWEI_GETRENNTE_VARIABLENABLAGEN_'+kind.upper())
    return bases[0] if bases else guarded(root,kind)


def global_settings(root):
    values={}; sources={}; errors=[]
    base=variable_base(root)/'all'
    files=sorted(p for p in base.iterdir() if p.suffix in ('.yml','.yaml') and p.is_file()) if base.is_dir() else []
    for p in files:
        rel=str(p.relative_to(root))
        if not p.resolve().is_relative_to(root): errors.append({'path':rel,'status':'PFAD_AUSSERHALB_PROJEKT'}); continue
        if '.example' in p.name or '.sample' in p.name:
            errors.append({'path':rel,'status':'BEISPIEL_IN_AKTIVER_KONFIGURATION'}); continue
        try: data=read_yaml(p)
        except AuditError as e: errors.append({'path':rel,'status':str(e)}); continue
        # Ansible ersetzt Dictionaries bei normalem hash_behaviour=replace.
        # Ueberlappungen werden sichtbar gemeldet, nicht still als gueltig angenommen.
        for key,value in data.items():
            if not isinstance(key,str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',key):
                errors.append({'path':rel,'status':'UNGUELTIGER_VARIABLENNAME'}); continue
            if key in values:
                errors.append({'key':key,'status':'MEHRFACH_GLOBAL_DEFINIERT','path':rel})
            values[key]=value; sources[key]=rel
    if not files: errors.append({'path':'group_vars/all','status':'GLOBALE_SETTINGS_FEHLEN'})
    return values,errors

def scoped_definitions(root):
    # Nur Namen von alternativen Definitionen sammeln, keine Inhalte ausgeben.
    definitions=set()
    for base in ('group_vars','host_vars'):
        d=variable_base(root,base)
        if not d.is_dir(): continue
        for p in d.rglob('*'):
            if not p.is_file() or p.suffix not in ('.yml','.yaml') or '.example' in p.name: continue
            if base=='group_vars' and p.relative_to(d).parts[0]=='all': continue
            try:
                if not p.resolve().is_relative_to(root): continue
                definitions.update(read_yaml(p).keys())
            except AuditError: continue
    return definitions

def find_usage(root,key):
    if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*',key):
        raise AuditError('UNGUELTIGER_VARIABLENNAME')
    parts=key.split('.')
    expression=r'\b'+re.escape(key)+r'\b'
    if len(parts)==2:
        parent,child=parts
        expression+=r'|\b'+re.escape(parent)+r"(?:\[['\"]"+re.escape(child)+r"['\"]\]|\.get\(['\"]"+re.escape(child)+r"['\"])"
    if len(parts)==2 and parts[0]=='features':expression+=r'|[\"\']feature[\"\']\s*:\s*[\"\']'+re.escape(parts[1])+r'[\"\']'
    pattern=re.compile(expression)
    hits=[]
    for directory in ['bin','scripts','lib','roles','playbooks','templates','config','filter_plugins','plugins']:
        base=guarded(root,directory)
        if not base.is_dir():continue
        for p in sorted(base.rglob('*')):
            if not p.is_file() or any(part in {'__pycache__','x','backups','_local','.git','tests'} for part in p.parts):continue
            if p.suffix not in {'.py','.sh','.j2','.yml','.yaml','.json','.cfg','.toml','.zsh','.ps1','.js','.html'} and p.name not in {'control','bashrc'}:continue
            if not p.resolve().is_relative_to(root):continue
            try:
                if p.stat().st_size>1024*1024:continue
                for number,line in enumerate(p.read_text().splitlines(),1):
                    if pattern.search(line):hits.append({'path':str(p.relative_to(root)),'line':number})
            except (OSError,UnicodeError):continue
    seen_files=set()
    for directory in ['group_vars','host_vars','inventory']:
        base=guarded(root,directory)
        if not base.is_dir():continue
        for p in sorted(base.rglob('*')):
            if not p.is_file() or p.suffix not in ('.yml','.yaml') or '.example' in p.name:continue
            resolved=p.resolve()
            if not resolved.is_relative_to(root) or resolved in seen_files:continue
            seen_files.add(resolved)
            try:node=yaml.compose(p.read_text())
            except (OSError,UnicodeError,yaml.YAMLError):continue
            visited=set()
            def walk(value):
                if value is None or id(value) in visited:return
                visited.add(id(value))
                if isinstance(value,yaml.MappingNode):
                    for k,v in value.value:walk(v)
                elif isinstance(value,yaml.SequenceNode):
                    for v in value.value:walk(v)
                elif isinstance(value,yaml.ScalarNode) and dynamic(value.value) and pattern.search(value.value):
                    hits.append({'path':str(p.relative_to(root)),'line':value.start_mark.line+1})
            walk(node)
    return hits


def unknown_settings(root,values,contract):
    known={r['key'] for r in contract.get('fields',[])}
    roots={key.split('.')[0] for key in known}
    # Ansible-interne Verbindungsvariablen sind normale bekannte Plattformvariablen.
    roots.update({'ansible_user','ansible_port','ansible_password','ansible_become','ansible_become_user','ansible_become_method','ansible_become_password','ansible_python_interpreter','managed_access_effective_user'})
    candidates=[key for key in values if key not in roots]
    features=values.get('features',{})
    if isinstance(features,dict):
        candidates += ['features.'+key for key in features if isinstance(key,str) and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',key) and 'features.'+key not in known]
    result=[]
    for key in sorted(candidates):
        hits=find_usage(root,key)
        result.append({'key':key,'status':'UNBEKANNT_ABER_TEXTTREFFER' if hits else 'UNBEKANNT_OHNE_STATISCHEN_TREFFER','usage':hits,'deletion_allowed':False})
    return result

def check_settings(root,contract,code_root=None,report_unknown=True,check_links=True):
    values,errors=global_settings(root); rows=[]; scoped=scoped_definitions(root)
    for rule in contract.get('fields',[]):
        key=rule['key']; feature=rule.get('feature')
        if feature:
            present,enabled=field(values,'features.'+feature)
            if present and enabled is False: continue
            if not present or not isinstance(enabled,bool):
                # Features selbst werden separat geprueft; kein falscher Pflichtfehler.
                continue
        exists,value=field(values,key)
        if not exists:
            if key.split('.')[0] in scoped:
                status='HOSTBEZOGEN_UNGEPRUEFT'
            elif rule.get('default_source'):
                try:
                    default_data=read_yaml(guarded(code_root or root,rule['default_source']))
                    exists_default,default_value=field(default_data,key)
                    status='ROLLENDEFAULT' if exists_default and good_type(default_value,rule['type']) else 'FEHLT'
                except AuditError: status='FEHLT'
            else:
                status='FEHLT' if rule.get('required') else 'OPTIONALER_DEFAULT'

        else:
            checked,alias_status=resolve_literal(value,values)
            if alias_status not in {'LITERAL','OK_ALIAS'}:status=alias_status
            elif not good_type(checked,rule['type']):status='FALSCHER_TYP'
            elif rule.get('nonempty') and checked in ('',[],{},None):status='LEER'
            else:status='OK_ALIAS' if alias_status=='OK_ALIAS' else 'OK'
        rows.append({'key':key,'status':status,'expected_type':rule['type'],'required':bool(rule.get('required'))})
    # TLS-Eintraege einzeln pruefen, neue/vergessene Aufgabennamen erkennen.
    tls=values.get('tls_validate_certs',{})
    if isinstance(tls,dict):
        allowed=set(contract.get('tls_tasks',[]))
        existing_keys={row['key'] for row in rows}
        for key,v in tls.items():
            if 'tls_validate_certs.'+str(key) in existing_keys: continue
            label=key if isinstance(key,str) and re.fullmatch(r'[a-z0-9_]+',key) else 'UNGUELTIGER_SCHLUESSEL'
            status='UNBEKANNTE_TLS_AUFGABE' if key not in allowed else 'DYNAMISCH_UNGEPRUEFT' if dynamic(v) else 'OK' if isinstance(v,bool) else 'FALSCHER_TYP'
            rows.append({'key':'tls_validate_certs.'+label,'status':status,'expected_type':'boolean','required':False})
    # Alias-Pfade pruefen, ohne Inventory oder dessen Plugins auszufuehren.
    for rel,target in [('inventory/group_vars','group_vars'),('inventory/host_vars','host_vars')]:
        p=root/rel
        if check_links and (root/target).is_dir():
            if not p.exists(): errors.append({'path':rel,'status':'VARIABLEN_VERLINKUNG_FEHLT'})
            elif p.resolve()!=(root/target).resolve(): errors.append({'path':rel,'status':'ZWEITE_VARIABLENABLAGE'})
    for row in rows:row['severity']=setting_severity(row)
    rows.sort(key=lambda x:x['key'])
    return {'fields':rows,'errors':errors,'unknown_variables':unknown_settings(root,values,contract) if report_unknown else [],'scope':'Nur lokal lesbare globale YAML-Werte; Jinja/Lookups und Host-/Gruppenpraezedenz werden nicht ausgefuehrt.'}

def check_registry(root,features=None,settings_root=None):
    names=set(); aliases={}; issues=[]; count=0
    values,_=global_settings(settings_root or root)
    directory=guarded(root,'bin/control.d')
    for p in sorted(directory.glob('*.json')):
        if not p.resolve().is_relative_to(root): raise AuditError('REGISTRY_PFAD_AUSSERHALB_PROJEKT')
        doc=load_json(p)
        commands=doc.get('commands')
        if not isinstance(commands,list): raise AuditError('REGISTRY_SCHEMA_UNGUELTIG')
        for cmd in commands:
            name=cmd.get('name','')
            if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*',name): raise AuditError('REGISTRY_NAME_UNGUELTIG')
            if name in names: issues.append({'command':name,'status':'DOPPELTER_BEFEHL'})
            names.add(name); count+=1
            for alias in cmd.get('aliases',[]):
                a=alias.get('name','')
                if not isinstance(a,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*',a): raise AuditError('ALIAS_NAME_UNGUELTIG')
                if a in aliases and aliases[a]!=name: issues.append({'command':name,'status':'DOPPELTER_ALIAS'})
                aliases[a]=name
            feature=cmd.get('feature')
            if feature:
                present,enabled=field(values,'features.'+feature)
                if not present:enabled=(features or {}).get(feature,cmd.get('feature_default',False))
                if enabled is False:continue
            for rel in [cmd.get('handler','')]+cmd.get('requires',[]):
                if not guarded(root,rel).is_file(): issues.append({'command':name,'status':'MODULDATEI_FEHLT','path':rel})
    for alias,name in aliases.items():
        if alias in names and alias!=name: issues.append({'command':name,'status':'ALIAS_KOLLIDIERT_MIT_BEFEHL'})
    return {'commands':count,'issues':issues,'executed':False}

def audit(root,here,only=None):
    installed = root / ".controller-install.json"
    receipt = load_json(installed) if installed.is_file() and not installed.is_symlink() else {}
    live_manifest = receipt.get("files") if receipt.get("schema") in (1, 2) and receipt.get("source") in ("main", "staging") else None
    addon_manifests = []
    if receipt.get("schema") == 2:
        modules = receipt.get("modules", {})
        owners = receipt.get("owners", {})
        files = receipt.get("files", {})
        if (not isinstance(modules, dict) or not isinstance(owners, dict)
                or not isinstance(files, dict) or owners.keys() != files.keys()
                or not all(name in modules for name in owners.values())):
            raise AuditError("INVALID_MODULE_OWNERSHIP")
        for name, meta in modules.items():
            if meta["kind"] != "addon":
                continue
            addon_files = {p: files[p] for p, owner in owners.items() if owner == name}
            addon_manifests.append({"schema": 1, "id": "addon-" + name.lower(), "version": meta["version"],
                                    "files": addon_files, "scope": name})
        if live_manifest is not None:
            live_manifest = {p: h for p, h in live_manifest.items() if modules[owners[p]]["kind"] != "addon"}
    if live_manifest is None:
        seal=load_json(here/'integrity.json')
        for rel,wanted in seal.get('files',{}).items():
            p=guarded(here,rel)
            if not p.is_file() or sha(p)!=wanted: raise AuditError('PRUEFER_ODER_MANIFEST_SHA_ABWEICHUNG')
    release=load_json(here/'release.json')
    if live_manifest is None:
        expected_paths=set(release['manifests']+['check.py','check.sh','configure.py','probes.py','release.json','settings_contract.json','settings_catalog.json','VERSION.txt','cleanup.py','cleanup_plan.json'])
        if not expected_paths.issubset(seal['files']): raise AuditError('UNVERSIEGELTE_PRUEFDATEN')
    report={'schema':1,'checker_version':CHECKER_VERSION,'controller_profile':release['profile'],
            'expected_controller_release':release['controller_release'],'delivery_scope':release.get('delivery_scope','combined_update'),'controller_release_verified':False,
            'read_only':True,'network_accessed':False,'remote_runtime_checked':False,
            'components':[],'extensions':[],'settings':None,'registry':None,'errors':[]}
    values,config_errors=global_settings(root)
    features=dict(release.get('feature_defaults',{}))
    if isinstance(values.get('features',{}),dict):features.update(values.get('features',{}))
    report['features']={k:('aktiv' if v is True else 'deaktiviert' if v is False else 'ungeprueft') for k,v in features.items()}
    if live_manifest is not None:
        report['controller_profile']=receipt['profile']
        report['expected_controller_release']=receipt['source']
        if only in (None,'controller_basis'):
            report['components'].append(check_component(root,{
                'schema':1,'id':'controller_basis','version':receipt['source'],'files':live_manifest,
            }))
    else:
        for rel in release['manifests']:
            result=check_component(root,load_json(guarded(here,rel)),features)
            if only is None or only==result['id']: report['components'].append(result)
    if only is None or only=='settings':
        report['settings']=check_settings(root,load_json(here/'settings_contract.json'))
    extension_manifests = list(addon_manifests)
    for module in addon_manifests:
        if only is None or only == module["id"]:
            report["extensions"].append(check_component(root, module, features))
    for extension in sorted((here/'extensions').glob('*')):
        if not extension.is_dir():continue
        if extension.is_symlink() or not extension.resolve().is_relative_to(here):raise AuditError('ADDON_PFAD_UNGUELTIG')
        ext_seal=load_json(extension/'integrity.json')
        if sha(extension/'manifest.json')!=ext_seal.get('manifest_sha256'):raise AuditError('ADDON_MANIFEST_SHA_ABWEICHUNG')
        manifest=load_json(extension/'manifest.json')
        if manifest.get('id') in {r['id'] for r in report['components']+extension_manifests}:raise AuditError('DOPPELTE_ADDON_ID')
        extension_manifests.append(manifest)
        if only==manifest['id'] or (only is None and live_manifest is None):
            report['extensions'].append(check_component(root,manifest,features))
    if only is None or only=='registry': report['registry']=check_registry(root,features)
    known={x['id'] for x in report['components']+extension_manifests}|{'settings','registry','cleanup','local'}
    if only and only not in known: raise AuditError('UNBEKANNTE_KOMPONENTE')
    code_ok=bool(report['components']) and all(c['status']=='OK' for c in report['components'])
    report['controller_release_verified']=only is None and code_ok and all(c['status']=='OK' for c in report['extensions'])
    report['active_scope_verified']=all(c['status'] in ('OK','AKTIVER_UMFANG_OK') for c in report['components']+report['extensions'])
    bad=any(c.get('status') not in ('OK','AKTIVER_UMFANG_OK') for c in report['components']+report['extensions'])
    if report['settings']:
        bad=bad or bool(report['settings']['errors']) or any(x['severity'] in ('warning','error') for x in report['settings']['fields'])
    if report['registry']: bad=bad or bool(report['registry']['issues'])
    if only is None or only=='cleanup':
        import importlib.util
        spec=importlib.util.spec_from_file_location('controller_cleanup_preview',here/'cleanup.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        try:
            plan=load_json(here/'cleanup_plan.json');report['cleanup']=module.preview(root,plan,external=False)
            report['cleanup']['receipt']=module.receipt_status(root,plan)
        except module.CleanupError:raise AuditError('BEREINIGUNGSPLAN_ODER_PROJEKT_UNGUELTIG') from None
    if only in (None, 'local'):
        report['local_extensions'] = local_extensions.inspect(root)
        bad = bad or not local_extensions.passed(report['local_extensions'])
    report['status']='PRUEFBEDARF' if bad else 'OK'
    return report

def display(report,details,color='auto'):
    if 'local_extensions' in report:
        local_extensions.display(report['local_extensions'])
    import os
    enabled=color=='always' or (color=='auto' and sys.stdout.isatty() and 'NO_COLOR' not in os.environ)
    palette={'ok':'32','info':'36','warning':'33','error':'31'}
    def line(text,severity='info'):
        print(('\033['+palette[severity]+'m'+text+'\033[0m') if enabled else text)
    line('CONTROLLER-VERSIONSPRUEFUNG '+report['checker_version']+' (Prueflauf)', 'info')
    print('Profil: '+report['controller_profile']+' | Sollkatalog: '+report['expected_controller_release'])
    if report.get('delivery_scope')=='checker_only':print('Lieferumfang: nur Checker; andere Komponenten werden nicht aktualisiert.')
    line('Release-Dateiabgleich: '+('VOLLSTAENDIG PASSEND' if report['controller_release_verified'] else 'AKTIVER UMFANG PASSEND' if report.get('active_scope_verified') else 'PRUEFBEDARF'),'ok' if report.get('active_scope_verified') else 'warning')
    states=report.get('features',{})
    if states:
        print('Features: '+str(sum(v=='aktiv' for v in states.values()))+' aktiv, '+str(sum(v=='deaktiviert' for v in states.values()))+' deaktiviert.')
        if details:
            for name,state in sorted(states.items()):print('  '+name+': '+state)
    for row in report['components']+report['extensions']:
        status=row['status'];severity='ok' if status=='OK' else 'info' if status=='AKTIVER_UMFANG_OK' else 'info' if status=='NICHT_INSTALLIERT' else 'warning' if status in ('PRUEFMODUL_FEHLT','BEKANNTER_AELTERER_STAND') else 'error'
        line('  '+row['id']+': '+status+' | SHA-bestaetigt: '+str(row.get('verified_version') or 'nicht belegt')+' | Soll: '+str(row.get('expected_version','-')),severity)
        if details and row.get('declared_versions'):print('    Versionsmarker (unbestaetigt): '+', '.join(row['declared_versions']))
        if 'matched' in row:print('    Aktive Dateien passend: '+str(row['matched'])+'/'+str(row['tracked']))
        for issue in row.get('issues',[]):line('    '+issue['status']+' '+issue['path'],'error')
        if details:
            for item in row.get('files',[]):
                if not item['required']:line('    '+item['status']+' '+item['path'],'info')
    if report['settings']:
        settings=report['settings'];counts={level:sum(row.get('severity',setting_severity(row))==level for row in settings['fields']) for level in ['error','warning','info']}
        counts['error']+=len(settings['errors'])
        print('Settings: '+str(len(settings['fields']))+' Felder; '+str(counts['error'])+' Fehler, '+str(counts['warning'])+' Warnungen, '+str(counts['info'])+' Informationen.')
        for row in settings['errors']:line('  '+row['status']+' '+row.get('key',row.get('path','')),'error')
        for row in settings['fields']:
            severity=row.get('severity',setting_severity(row))
            if details or severity in ('warning','error'):line('  '+row['key']+': '+row['status'],severity)
        if counts['info'] and not details:line('  Kontextabhaengige Informationen mit --details anzeigen.','info')
        unknown=settings.get('unknown_variables',[])
        line('Unbekannte Variablen (nur Informationen, nie automatisch loeschen): '+str(len(unknown)),'info')
        for row in unknown:
            line('  '+row['key']+': '+row['status']+'; Texttreffer: '+str(len(row['usage'])),'info')
            if details:
                for hit in row['usage']:print('    '+hit['path']+':'+str(hit['line']))
    if report['registry']:
        registry=report['registry'];line('Registry: '+str(registry['commands'])+' Befehle; '+str(len(registry['issues']))+' Befunde.','error' if registry['issues'] else 'ok')
        for row in registry['issues']:line('  '+row['status']+' '+row['command']+' '+row.get('path',''),'error')
    if report.get('extended_checks'):
        print('Erweiterte Konfigurations-/API-Pruefung:')
        for row in report['extended_checks']['configuration_and_api_checks']:
            line('  '+row['id']+': '+row['status'],'ok' if row['status']=='OK' else 'info' if row['status'].startswith('SKIP_') else 'warning')
            for issue in row.get('issues',[]):line('    '+issue['status']+' '+issue['path'],'warning')
        print('API-Aufrufe: '+str(report['extended_checks']['network_requests'])+'. Keine Nachrichten oder Aenderungen gesendet.')
    line('Ergebnis: '+report['status']+'. Prueflauf ohne Deployment oder Dienst-Aenderungen.','ok' if report['status']=='OK' else 'warning')
    if report.get('cleanup'):
        cleanup=report['cleanup'];line('Bereinigung: '+cleanup['status']+' | Kandidaten nach Projektpruefung: '+str(cleanup['candidates'])+' | erhalten: '+str(cleanup['retained']),'info')
        print('  Laufnachweis: '+cleanup.get('receipt','NOCH_KEIN_LAUFNACHWEIS')+'. System-/Cronverweise werden vor Ausfuehrung zusaetzlich geprueft.')
        if cleanup['candidates']:print('  Bereinigung pruefen/ausfuehren: bin/control update-check --cleanup (Vorschau und YES).')
        if details:
            for row in cleanup['files']:print('  '+row['status']+' '+row['path'])


def main():
    if "--versions" in sys.argv[1:]:
        from rollout import show_versions
        parser = argparse.ArgumentParser(description="Installierte Module und Versionen anzeigen")
        parser.add_argument("--versions", action="store_true")
        parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
        return show_versions(parser.parse_args().root)
    if any(arg in {"--remote", "--apply", "--auto", "--rollback", "--staging"} for arg in sys.argv[1:]):
        import rollout
        return rollout.main(sys.argv[1:])
    parser=argparse.ArgumentParser(description=__doc__,
        epilog="Git-Update: --remote für main, --staging für staging. Mit --apply übernehmen. --auto verwendet immer main.")
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--json',action='store_true',help='Strukturierter Bericht ohne Settings-/Credentialwerte')
    parser.add_argument('--details',action='store_true',help='Auch passende und optionale Settingsfelder auflisten')
    parser.add_argument('--only',help='Nur Komponente/Add-on, settings, registry oder cleanup pruefen')
    parser.add_argument('--configure',action='store_true',help='Interaktiv fehlende bekannte Variablen erklaeren/erfragen, Vorschau und YES vor Speicherung')
    parser.add_argument('--color',choices=['auto','always','never'],default='auto',help='Terminalfarben; auto nutzt TTY und respektiert NO_COLOR. JSON bleibt ohne ANSI.')
    parser.add_argument('--no-prompt',action='store_true',help='Keine optionale Bereinigungsfrage im normalen interaktiven Prueflauf')
    parser.add_argument('--cleanup',action='store_true',help='Freigegebenen Altbestand pruefen, Vorschau/YES/Archiv; aktive/abhaengige Dateien erhalten')
    parser.add_argument('--check',action='store_true',help='Erweiterte lokale Konfigurationspruefung und lesende GET-APIs fuer konfigurierte Dienste')
    parser.add_argument('--offline',action='store_true',help='Mit --check keine Netzwerkaufrufe; nur lokale Struktur/Artefakte pruefen')
    parser.add_argument('--timeout',type=int,default=8,help='API-Timeout pro Aufruf in Sekunden (1 bis 30, Standard 8)')
    parser.add_argument('--field',action='append',default=[],help='Mit --configure gezielt diese bekannte Variable abfragen (mehrfach moeglich)')
    parser.add_argument('--find-usage',metavar='VARIABLE',help='Nur lokale Textfundstellen anzeigen; keine Inhalte, keine automatische Loeschung')
    parser.add_argument('--sort-settings',action='store_true',help='Settings-Bloecke nach Katalog ordnen, Vorschau und YES; keine Variablen abfragen')
    args=parser.parse_args()
    try:
        if args.cleanup and (args.json or args.configure or args.sort_settings or args.check or args.only or args.find_usage):raise AuditError('BEREINIGUNG_GETRENNT_AUFRUFEN')
        if args.offline and not args.check:raise AuditError('OFFLINE_BENOETIGT_CHECK')
        if not 1<=args.timeout<=30:raise AuditError('TIMEOUT_MUSS_1_BIS_30_SEIN')
        root=args.root.resolve();here=Path(__file__).resolve().parent
        report=audit(root,here,args.only)
        if args.cleanup:
            import importlib.util
            spec=importlib.util.spec_from_file_location('controller_cleanup_action',here/'cleanup.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            try:module.interactive(root,load_json(here/'cleanup_plan.json'))
            except (module.CleanupError,EOFError,KeyboardInterrupt):raise AuditError('BEREINIGUNG_ABGEBROCHEN_ODER_NICHT_SICHER') from None
            report=audit(root,here,args.only);report['read_only']=False;report['cleanup_executed']=True
        if args.find_usage:
            hits=find_usage(root,args.find_usage)
            result={'variable':args.find_usage,'usage':hits,'deletion_allowed':False,'note':'Texttreffer sind kein vollstaendiger Nachweis dynamischer Verwendung.'}
            if args.json:print(json.dumps(result,ensure_ascii=False,indent=2))
            else:
                print(args.find_usage+': '+str(len(hits))+' lokale Textfundstellen. Keine Loeschfreigabe.')
                for hit in hits:print('  '+hit['path']+':'+str(hit['line']))
            return 0
        if args.field and not args.configure:raise AuditError('FIELD_BENOETIGT_CONFIGURE')
        if args.configure or args.sort_settings:
            if args.json or args.only not in (None,'settings'):
                raise AuditError('INTERAKTIV_NICHT_MIT_JSON_ODER_KOMPONENTENFILTER_KOMBINIEREN')
            if not sys.stdin.isatty():raise AuditError('KONFIGURATION_BENOETIGT_INTERAKTIVES_TERMINAL')
            if not (root/'bin/control').is_file() and not (root/'ansible.cfg').is_file():raise AuditError('ANSIBLE_PROJEKTROOT_NICHT_ERKANNT')
            import importlib.util
            spec=importlib.util.spec_from_file_location('controller_settings_wizard',here/'configure.py')
            wizard=importlib.util.module_from_spec(spec);spec.loader.exec_module(wizard)
            display(report,False,args.color)
            try:changed=wizard.configure(root,here,sys.modules[__name__],sort_only=not args.configure,selected_keys=args.field or None)
            except (wizard.ConfigureError,EOFError,KeyboardInterrupt):raise AuditError('KONFIGURATION_ABGEBROCHEN_ODER_NICHT_SICHER_AENDERBAR') from None
            report=audit(root,here,args.only);report['read_only']=not changed;report['configuration_changed']=changed
        if args.check:
            import importlib.util
            spec=importlib.util.spec_from_file_location('controller_readonly_probes',here/'probes.py')
            probes=importlib.util.module_from_spec(spec);spec.loader.exec_module(probes)
            report['extended_checks']=probes.run(root,sys.modules[__name__],offline=args.offline,timeout=args.timeout,active_files={r['path']:r['required'] for c in report['components']+report['extensions'] for r in c.get('files',[])},progress=lambda label:print('Pruefe '+label+' ...',file=sys.stderr,flush=True))
            report['network_accessed']=report['extended_checks']['network_requests']>0
            if any(row['status']!='OK' and not row['status'].startswith('SKIP_') for row in report['extended_checks']['configuration_and_api_checks']):report['status']='PRUEFBEDARF'
        print(json.dumps(report,ensure_ascii=False,indent=2)) if args.json else display(report,args.details,args.color)
        if not args.json and not args.no_prompt and not any([args.cleanup,args.check,args.configure,args.sort_settings,args.only,args.find_usage]) and report.get('cleanup',{}).get('candidates',0) and sys.stdin.isatty() and sys.stdout.isatty():
            if input('Freigegebene Altreste jetzt zur Bereinigung anzeigen? [j/N]: ').strip().lower() in {'j','ja','y','yes'}:
                import importlib.util
                spec=importlib.util.spec_from_file_location('controller_cleanup_prompt',here/'cleanup.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
                try:module.interactive(root,load_json(here/'cleanup_plan.json'))
                except (module.CleanupError,EOFError,KeyboardInterrupt):raise AuditError('BEREINIGUNG_ABGEBROCHEN_ODER_NICHT_SICHER') from None
                report=audit(root,here,args.only);report['read_only']=False;report['cleanup_executed']=True;display(report,args.details,args.color)
        return 0 if report['status']=='OK' else 1
    except (AuditError,OSError,ValueError,KeyError,TypeError,UnicodeError,RecursionError) as exc:
        code=str(exc) if isinstance(exc,AuditError) else 'LOKALE_PRUEFDATEN_UNLESBAR'
        if args.json: print(json.dumps({'status':'FEHLER','error':code,'read_only':not (args.cleanup or args.configure or args.sort_settings)}))
        else: print('FEHLER: '+code+'. Pruefung/Aktion abgebrochen; vorhandene Sicherungen/Nachweise pruefen.',file=sys.stderr)
        return 2
if __name__=='__main__': raise SystemExit(main())
