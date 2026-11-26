#!/usr/bin/env python3
"""Expliziter interaktiver Settingsmodus; kein Netzwerk, keine Playbookausfuehrung."""
import sys
from pathlib import Path
import datetime
import getpass
import json
import os
import re
import stat
import tempfile
import urllib.parse
import yaml
from yaml.tokens import AliasToken,AnchorToken

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from controller_i18n import language, tr

class ConfigureError(Exception):pass

def _dump(value):
    return '\n'.join(line for line in yaml.safe_dump(value,sort_keys=False,allow_unicode=True).splitlines() if line!='...')

def _end(node):
    if isinstance(node,yaml.MappingNode) and node.value and not node.flow_style:return _end(node.value[-1][1])
    if isinstance(node,yaml.SequenceNode) and node.value and not node.flow_style:return _end(node.value[-1])
    return node.end_mark

def _parse(text,loader):
    try:
        data=yaml.load(text,Loader=loader)
        if data is None:return {}
        if not isinstance(data,dict):raise ConfigureError(tr("wizard.not_mapping"))
        return data
    except ConfigureError:raise
    except Exception:raise ConfigureError(tr("wizard.invalid_yaml")) from None

def set_field(text,key,value,loader):
    """Nur den betroffenen YAML-Wert/Eintrag bearbeiten; restliche Zeilen erhalten."""
    current=_parse(text,loader)
    parts=key.split('.')
    if not text.strip() or current=={}:
        data=value
        for part in reversed(parts):data={part:data}
        return text.rstrip()+'\n'+_dump(data)+'\n'
    node=yaml.compose(text);parent_key=None
    for index,part in enumerate(parts):
        if not isinstance(node,yaml.MappingNode):raise ConfigureError(tr("wizard.nested_mapping"))
        hits=[(k,v) for k,v in node.value if k.value==part]
        if not hits:
            nested=value
            for rest in reversed(parts[index+1:]):nested={rest:nested}
            addition={part:nested}
            if node.flow_style:
                data=yaml.safe_load(yaml.serialize(node));data[part]=nested
                start,end=node.start_mark.index,node.end_mark.index
                indent=parent_key.start_mark.column+2 if parent_key is not None else 0
                lines=_dump(data).splitlines()
                replacement='\n'+'\n'.join(' '*indent+line for line in lines)
                out=text[:start]+replacement+text[end:]
            else:
                end=_end(node).index
                newline=text.find('\n',end)
                insert=len(text) if newline<0 else newline+1
                indent=node.value[0][0].start_mark.column if node.value else (parent_key.start_mark.column+2 if parent_key else 0)
                rendered='\n'.join(' '*indent+line for line in _dump(addition).splitlines())+'\n'
                prefix='' if insert==0 or text[insert-1:insert]=='\n' else '\n'
                out=text[:insert]+prefix+rendered+text[insert:]
            _parse(out,loader)
            return out
        k,v=hits[0]
        if v.start_mark.index<k.end_mark.index:raise ConfigureError(tr("wizard.yaml_alias"))
        if index<len(parts)-1:
            parent_key=k;node=v;continue
        rendered=_dump(value)
        if isinstance(value,(dict,list)) and value:
            indent=k.start_mark.column+2
            rendered='\n'+'\n'.join(' '*indent+line for line in rendered.splitlines())
        out=text[:v.start_mark.index]+rendered+text[_end(v).index:]
        checked=_parse(out,loader)
        found=checked
        for p in parts:found=found[p]
        if found!=value:raise ConfigureError(tr("wizard.verify_value"))
        return out
    raise ConfigureError(tr("wizard.unknown_value"))

def remove_top_field(text,key,loader):
    if '.' in key:raise ConfigureError(tr("wizard.nested_secret"))
    _parse(text,loader);node=yaml.compose(text)
    for k,v in node.value:
        if k.value!=key:continue
        start=text.rfind('\n',0,k.start_mark.index)+1
        end=_end(v).index
        lineend=text.find('\n',end)
        lineend=len(text) if lineend<0 else lineend+1
        tail=text[end:lineend].strip()
        preserved=(tail+'\n') if tail.startswith('#') else ''
        out=text[:start]+preserved+text[lineend:]
        _parse(out,loader)
        return out
    return text

def sort_settings(text,catalog,loader):
    _parse(text,loader)
    # YAML-Anker sind reihenfolgeabhaengig: niemals vor ihre Definition verschieben.
    if any(isinstance(token,(AliasToken,AnchorToken)) for token in yaml.scan(text)):
        return text,False
    node=yaml.compose(text)
    if not node or not node.value:return text,True
    lines=text.splitlines(keepends=True);starts=[];last_end=0
    for i,(key,value) in enumerate(node.value):
        start=key.start_mark.line
        if i:
            while start>last_end and (not lines[start-1].strip() or lines[start-1].lstrip().startswith('#')):start-=1
        starts.append(start)
        marker=_end(value);last_end=marker.line+(1 if marker.column else 0)
    prefix=''.join(lines[:starts[0]])
    order={key:i for i,key in enumerate(catalog.get('top_level_order',[]))}
    blocks=[]
    for i,(key,value) in enumerate(node.value):
        end=starts[i+1] if i+1<len(starts) else len(lines)
        blocks.append((order.get(key.value,len(order)),i,''.join(lines[starts[i]:end])))
    result=prefix+''.join(block[2] for block in sorted(blocks,key=lambda x:(x[0],x[1])))
    if _parse(result,loader)!=_parse(text,loader):raise ConfigureError(tr("wizard.sort_changes"))
    return result,True

def _sensitive(key,value=None):
    if re.search(r'password|secret|credentials|private_key|telegram_bot_token',key,re.I):return True
    if isinstance(value,str) and re.match(r'^[a-zA-Z]+://[^/\s]*:[^/\s]*@',value):return True
    if isinstance(value,dict):return any(_sensitive(str(k),v) for k,v in value.items())
    return False

def _safe_write(path,data,old_stat=None,secret=False):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=None
    try:
        with tempfile.NamedTemporaryFile('wb',dir=path.parent,prefix='.update-check-',delete=False) as f:
            temporary=Path(f.name);f.write(data);f.flush();os.fsync(f.fileno())
            mode=0o600 if secret or old_stat is None else stat.S_IMODE(old_stat.st_mode)
            os.fchmod(f.fileno(),mode)
            if old_stat:os.fchown(f.fileno(),old_stat.st_uid,old_stat.st_gid)
        os.replace(temporary,path);temporary=None
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)

def _transaction(root,plans,expected_originals=None):
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup=root/'x/backups/update_check'/stamp
    originals={};stats={}
    for path,new,secret in plans:
        if path.is_symlink():raise ConfigureError(tr("wizard.symlink"))
        originals[path]=path.read_bytes() if path.exists() else None
        if expected_originals is not None and originals[path]!=expected_originals[path]:raise ConfigureError(tr("wizard.concurrent_edit"))
        stats[path]=path.stat() if path.exists() else None
    # Erst komplette Backups, dann Aenderungen. Backupinhalte nie protokollieren.
    backup.mkdir(parents=True,exist_ok=True,mode=0o700)
    for path,data in originals.items():
        if data is None:continue
        dest=backup/path.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        with dest.open('xb') as f:
            os.chmod(dest,0o600);f.write(data);f.flush();os.fsync(f.fileno())
    written=[]
    try:
        for path,new,secret in plans:
            before=path.read_bytes() if path.exists() else None
            if before!=originals[path]:raise ConfigureError(tr("wizard.concurrent_save"))
            _safe_write(path,new,stats[path],secret);written.append((path,new))
    except BaseException:
        for path,new in reversed(written):
            # Keine zwischenzeitlichen fremden Aenderungen zuruecksetzen.
            if path.read_bytes()!=new:continue
            if originals[path] is None:path.unlink()
            else:_safe_write(path,originals[path],stats[path],secret=path.name=='secrets.yml')
        raise ConfigureError(tr("wizard.save_failed")) from None
    return backup

def configure(root,here,api,sort_only=False,input_fn=input,secret_fn=getpass.getpass,print_fn=print,selected_keys=None):
    """api ist das bereits SHA-gepruefte gemeinsame Pruefmodul; Eingaben explizit."""
    catalog=api.load_json(here/'settings_catalog.json')
    contract=api.load_json(here/'settings_contract.json')
    varbase=api.variable_base(root)/'all'
    if (varbase/'settings.yml').is_symlink() or (varbase/'secrets.yml').is_symlink():raise ConfigureError(tr("wizard.config_link"))
    settings=api.guarded(root,str((varbase/'settings.yml').relative_to(root)))
    secrets=api.guarded(root,str((varbase/'secrets.yml').relative_to(root)))
    if settings.is_symlink() or secrets.is_symlink():raise ConfigureError(tr("wizard.config_link"))
    original_raw=settings.read_bytes() if settings.exists() else None
    secret_raw=secrets.read_bytes() if secrets.exists() else None
    original=original_raw.decode() if original_raw is not None else ''
    original_secret=secret_raw.decode() if secret_raw is not None else ''
    _parse(original,api.UniqueLoader);_parse(original_secret,api.UniqueLoader)
    values,errors=api.global_settings(root)
    fatal=[e for e in errors if e['status'] not in {'GLOBALE_SETTINGS_FEHLEN','BEISPIEL_IN_AKTIVER_KONFIGURATION'}]
    if fatal:raise ConfigureError(tr("wizard.invalid_global"))
    scoped=api.scoped_definitions(root)
    fields=catalog['fields'];changes=[];new=original;new_secret=original_secret
    rules={r['key']:r for r in contract.get('fields',[])}
    if selected_keys and any(key not in rules for key in selected_keys):raise ConfigureError(tr("wizard.unknown_setting"))
    sequence=sorted(rules,key=lambda key:(not key.startswith('features.'),list(rules).index(key)))
    if selected_keys:sequence=[key for key in sequence if key in selected_keys]
    translated_fields = {}
    if language() == "en":
        # Use the same field descriptions as the TUI. A profile may omit translations.
        reference = root / "descriptions/configurations/group_vars__all__settings.md"
        if reference.is_file() and not reference.is_symlink() and reference.resolve().is_relative_to(root.resolve()):
            match = re.search(r"```json\s*\n(.*?)\n```", reference.read_text(encoding="utf-8"), flags=re.S)
            if match:
                try:
                    document = json.loads(match[1])
                    fields_en = document.get("i18n", {}).get("en", {}).get("fields", {})
                    if isinstance(fields_en, dict):
                        translated_fields = {key: data for key, data in fields_en.items() if isinstance(data, dict)}
                except (ValueError, AttributeError):
                    pass  # A missing translation must not prevent the operator from repairing settings.
    if not sort_only:
        for key in sequence:
            rule=rules[key];feature=rule.get('feature');force=bool(selected_keys)
            if feature and not force:
                present,enabled=api.field(values,'features.'+feature)
                if not present or enabled is not True:continue
            present,old=api.field(values,key)
            local_settings=_parse(new,api.UniqueLoader);local_secrets=_parse(new_secret,api.UniqueLoader)
            in_settings,_=api.field(local_settings,key);in_secrets,_=api.field(local_secrets,key)
            if not present and key.split('.')[0] in scoped:
                print_fn(key+tr("wizard.host_value"));continue
            if present:
                if api.dynamic(old) and not force:continue
                valid=api.good_type(old,rule['type']) and not (rule.get('nonempty') and old in ('',[],{},None))

                if valid and (not rule.get('choices') or old in rule['choices']) and not force:continue
                if not (in_settings or in_secrets):
                    print_fn(key+tr("wizard.other_file"));continue
            else:
                if rule.get('default_source') and not force:
                    try:
                        d=api.read_yaml(api.guarded(root,rule['default_source']))
                        if api.field(d,key)[0]:continue
                    except Exception:pass
                if not force and not rule.get('required'):continue

            info=dict(fields.get(key,{}));secret=_sensitive(key)
            source=info.get('source','')
            if source.startswith('examples/') and not secret:
                expected=catalog.get('example_sources',{}).get(source)
                try:
                    example_path=api.guarded(root,source)
                    if not expected or api.sha(example_path)!=expected:
                        info.pop('default',None);info.pop('example',None)
                        print_fn(key+tr("wizard.example_changed"))
                    else:
                        example_data=api.read_yaml(example_path)
                        found,sample=api.field(example_data,key)
                        if found:
                            info['example']=sample
                            if not info.get('example_only',False):info['default']=sample
                except Exception:
                    info.pop('default',None);info.pop('example',None)
            prose = translated_fields.get(key, {}) if language() == "en" else info
            print_fn('\n'+key+' – '+prose.get('description',tr("wizard.variable")))
            print_fn(tr("wizard.type")+rule['type']+tr("wizard.source")+info.get('source','settings_contract.json'))
            if prose.get('help'):print_fn(prose['help'])
            default=old if present and api.good_type(old,rule['type']) and not _sensitive(key,old) else info.get('default')
            has_default=('default' in info or (present and not _sensitive(key,old))) and not secret and not info.get('example_only',False)
            if has_default and not api.good_type(default,rule['type']):has_default=False
            if not has_default and 'example' in info and not secret:
                print_fn(tr("wizard.example")+_dump(info['example']))
            while True:
                suffix=(tr("wizard.default", value=_dump(default).replace("\n"," "))) if has_default else ''
                prompt=tr("wizard.prompt", default=suffix)
                answer=secret_fn(prompt) if secret else input_fn(prompt)
                if answer.strip().lower()=='q':raise ConfigureError(tr("wizard.cancelled"))
                if answer.strip().lower()=='s':break
                if not answer.strip() and has_default:value=default
                else:
                    if not answer.strip():
                        print_fn(tr("wizard.required_input"));continue
                    if rule['type']=='string':value=answer
                    elif rule['type']=='boolean' and answer.strip().lower() in {'j','ja','y','yes','true','1','n','nein','no','false','0'}:
                        value=answer.strip().lower() in {'j','ja','y','yes','true','1'}
                    else:
                        try:value=yaml.safe_load(answer)
                        except yaml.YAMLError:print_fn(tr("wizard.bad_input"));continue
                if not api.good_type(value,rule['type']):print_fn(tr("wizard.bad_type"));continue
                if rule.get('nonempty') and value in ('',[],{},None):print_fn(tr("wizard.empty"));continue
                if isinstance(value,str) and (key.endswith('_url') or key=='checkmk_download_base_url'):
                    try:
                        parsed=urllib.parse.urlsplit(value)
                        valid_url=parsed.scheme in ('http','https') and bool(parsed.netloc) and parsed.password is None
                    except ValueError:valid_url=False
                    if not valid_url:
                        print_fn(tr("wizard.url"));continue
                if info.get('choices') and value not in info['choices']:print_fn(tr("wizard.choices")+', '.join(str(x) for x in info['choices']));continue

                # Unterstuetzt nur bekannte Variablen, keine pauschale Beispieluebernahme.
                if secret:
                    if in_settings:new=remove_top_field(new,key,api.UniqueLoader)
                    new_secret=set_field(new_secret,key,value,api.UniqueLoader)
                else:
                    if in_secrets and not in_settings:
                        print_fn(tr("wizard.secret_location"));break
                    new=set_field(new,key,value,api.UniqueLoader)
                target=values
                for part in key.split('.')[:-1]:target=target.setdefault(part,{})
                target[key.split('.')[-1]]=value
                changes.append((key,value,secret));break
    new,sorted_ok=sort_settings(new,catalog,api.UniqueLoader)
    if not sorted_ok:print_fn(tr("wizard.anchor"))
    plans=[]
    if new!=original:plans.append((settings,new.encode(),False))
    if new_secret!=original_secret:plans.append((secrets,new_secret.encode(),True))
    if not plans:print_fn(tr("wizard.no_changes"));return False
    print_fn(tr("wizard.preview"))
    for key,value,secret in changes:
        print_fn('  '+key+' = '+(tr("wizard.hidden") if secret or _sensitive(key,value) else _dump(value).replace('\n',' ')))
    for path,data,secret in plans:print_fn(tr("wizard.edit_file")+str(path.relative_to(root))+(' (0600)' if secret else ''))
    if new!=original and not changes:print_fn(tr("wizard.order_only"))
    if input_fn(tr("wizard.confirm")).strip()!='YES':
        print_fn(tr("wizard.unsaved"));return False
    # Wiederholte Validierung unmittelbar vor Speicherung.
    for path,data,secret in plans:_parse(data.decode(),api.UniqueLoader)
    if settings.exists() and settings.read_text()!=original:raise ConfigureError(tr("wizard.settings_changed"))
    if secrets.exists() and secrets.read_text()!=original_secret:raise ConfigureError(tr("wizard.secrets_changed"))
    backup=_transaction(root,plans,{settings:original_raw,secrets:secret_raw})
    print_fn(tr("wizard.saved")+str(backup)+tr("wizard.no_services"))
    return True
