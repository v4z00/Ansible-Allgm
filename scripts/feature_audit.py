#!/usr/bin/env python3
"""Read-only feature audit. Reads local YAML only; never runs inventory plugins."""
import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader,node,deep=False):
    seen=set()
    for key,value in node.value:
        if key.tag=='tag:yaml.org,2002:merge':continue
        k=loader.construct_object(key,deep=deep)
        if k in seen:raise ValueError('Duplicate YAML key')
        seen.add(k)
    loader.flatten_mapping(node)
    return yaml.SafeLoader.construct_mapping(loader,node,deep=deep)


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)


def read_yaml(path):
    try:
        if not path.is_file():return None,'FEHLENDE_DATEI'
        value=yaml.load(path.read_text(),Loader=UniqueLoader)
        return ({} if value is None else value),None
    except (OSError,UnicodeError,ValueError,TypeError,yaml.YAMLError):
        # No exception snippets: they could contain private settings.
        return None,'UNLESBARE_SETTINGS'


def local_path(root,rel):
    path=(root/rel).resolve()
    if Path(rel).is_absolute() or not path.is_relative_to(root):
        raise ValueError('Pfad ausserhalb des Projekts')
    return path


def environment_hints(root):
    hints=[]
    cfg,error=read_yaml(root/'inventory_config.yml')
    if not error and isinstance(cfg,dict):
        if cfg.get('inventory_mode')=='proxmox' or cfg.get('proxmox_sources') or cfg.get('proxmox_url'):
            hints.append({'feature':'proxmox','source':'inventory_config.yml','reason':'Proxmox-Inventarkonfiguration vorhanden'})
    for p in sorted((root/'inventory').glob('*')):
        if p.is_symlink() or p.suffix not in {'.yml','.yaml'} or not p.is_file():continue
        obj,error=read_yaml(p)
        if error or not isinstance(obj,dict):continue
        source=str(p.relative_to(root))
        plugin=obj.get('plugin','')
        if isinstance(plugin,str) and 'proxmox' in plugin.lower():
            hints.append({'feature':'proxmox','source':source,'reason':'Lokale Proxmox-Plugin-Konfiguration vorhanden (nicht ausgefuehrt)'})
        def walk(value):
            if isinstance(value,dict):
                for key,item in value.items():
                    if isinstance(key,str) and isinstance(item,dict) and item.get('hosts'):
                        if 'proxmox' in key.lower():hints.append({'feature':'proxmox','source':source,'reason':'Nichtleere Proxmox-Hostgruppe vorhanden'})
                        if 'docker' in key.lower():hints.append({'feature':'docker','source':source,'reason':'Nichtleere Docker-Hostgruppe vorhanden'})
                    if key=='tags':
                        tags=item if isinstance(item,list) else re.split(r'[,;\s]+',item) if isinstance(item,str) else []
                        for tag in tags:
                            if tag in {'proxmox','docker'}:hints.append({'feature':tag,'source':source,'reason':'Lokales Inventory enthaelt entsprechendes Infrastruktur-Tag'})
                    walk(item)
            elif isinstance(value,list):
                for item in value:walk(item)
        walk(obj)
    unique={(x['feature'],x['source'],x['reason']):x for x in hints}
    return list(unique.values())


def flag_value(value):
    if isinstance(value,bool):return 'AKTIV' if value else 'DEAKTIVIERT'
    if isinstance(value,str):
        if value.lower() in {'true','yes','on','1'}:return 'AKTIV'
        if value.lower() in {'false','no','off','0'}:return 'DEAKTIVIERT'
        if '{{' in value or '{%' in value:return 'DYNAMISCH'
    return 'UNGUELTIGER_TYP'


def collect(root,commands,catalog_path=None):
    root=Path(root).resolve()
    catalog_path=Path(catalog_path) if catalog_path else root/'scripts/feature_catalog.json'
    catalog=json.loads(catalog_path.read_text())
    expected={}
    for feature,info in catalog['features'].items():
        expected[('group_vars/all/settings.yml',('features',feature))]={'feature':feature,'sources':info.get('sources',[]),'commands':[]}
    for name,c in commands.items():
        feature=c.get('feature')
        if not feature:continue
        path=c.get('settings','group_vars/all/settings.yml');keys=tuple(c.get('setting_path',['features',feature]))
        slot=expected.setdefault((path,keys),{'feature':feature,'sources':[],'commands':[]})
        slot['commands'].append(name)
        if c.get('feature_default') is True:slot['legacy_default']=True
    cache={};rows=[]
    for (path,keys),info in sorted(expected.items()):
        if path not in cache:
            try:cache[path]=read_yaml(local_path(root,path))
            except ValueError:cache[path]=(None,'UNGUELTIGER_PFAD')
        obj,error=cache[path];status=error;missing=False
        if not error:
            value=obj
            for key in keys:
                if not isinstance(value,dict):status='UNGUELTIGE_STRUKTUR';break
                if key not in value:status='FEHLENDER_SCHALTER';missing=True;break
                value=value[key]
            else:status=flag_value(value)
        row=dict(info,path=path,key='.'.join(keys),status=status)
        row['warning']=status not in {'AKTIV','DEAKTIVIERT'}
        if missing and info.get('legacy_default'):row['note']='Bisheriger manueller Standard bleibt verfuegbar; Schalter fehlt dennoch.'
        rows.append(row)
    hints=environment_hints(root);warnings=[]
    for hint in hints:
        row=next((x for x in rows if x['feature']==hint['feature'] and x['key']=='features.'+hint['feature']),None)
        if row and row['status']!='AKTIV':
            reason='Schalter fehlt in Settings' if row['status']=='FEHLENDER_SCHALTER' else 'Settings-Datei fehlt' if row['status']=='FEHLENDE_DATEI' else 'Funktion ist ausdruecklich deaktiviert' if row['status']=='DEAKTIVIERT' else 'Aktivierung aus Settings nicht sicher lesbar'
            warnings.append({'feature':hint['feature'],'message':hint['feature'].capitalize()+'-Umgebung aus lokalen Dateien erkennbar, aber '+row['key']+' nicht aktiv: '+reason+'.','source':hint['source']})
    return {'settings_modified':False,'inventory_executed':False,'live_hosts_contacted':False,'features':rows,'environment_hints':hints,'environment_warnings':warnings,'warning_count':sum(x['warning'] for x in rows)+len(warnings)}


def display(report):
    print('Feature-Pruefung (nur lokale Dateien; Einstellungen unveraendert):')
    labels={'FEHLENDER_SCHALTER':'FEHLT: Schalter ist in den Settings nicht vorhanden',
            'FEHLENDE_DATEI':'FEHLT: Settings-Datei ist nicht vorhanden',
            'UNLESBARE_SETTINGS':'FEHLER: YAML unlesbar oder doppelte Schluessel',
            'UNGUELTIGE_STRUKTUR':'FEHLER: Settings-Struktur ist kein passendes Mapping',
            'UNGUELTIGER_TYP':'FEHLER: Feature ist kein boolescher Schalter',
            'UNGUELTIGER_PFAD':'FEHLER: Settings-Pfad ausserhalb des Projekts',
            'DYNAMISCH':'HINWEIS: dynamischer Ausdruck; wird hier nicht ausgewertet'}
    for row in report['features']:
        print('  '+row['key']+' – '+labels.get(row['status'],row['status'])+' ['+row['path']+']')
        if row.get('note'):print('    '+row['note'])
    for hint in report['environment_warnings']:print('  HINWEIS: '+hint['message']+' Quelle: '+hint['source'])
    print('Hinweise/fehlende Definitionen: '+str(report['warning_count'])+'. Keine Schalter gesetzt.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json',action='store_true')
    parser.add_argument('--strict',action='store_true',help='Bei fehlenden/unlesbaren Definitionen Exit 1')
    args=parser.parse_args();root=args.project_root.resolve();commands={}
    for p in (root/'bin/control.d').glob('*.json'):
        for c in json.loads(p.read_text()).get('commands',[]):commands[c['name']]=c
    report=collect(root,commands)
    if args.json:print(json.dumps(report,indent=2))
    else:display(report)
    return 1 if args.strict and report['warning_count'] else 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError,TypeError):raise SystemExit('Feature-Pruefung konnte lokale Struktur/Metadaten nicht lesen; keine Einstellungen veraendert.')
