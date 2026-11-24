#!/usr/bin/env python3
"""Explizite --check-Pruefungen: YAML/INI, Agentartefakt und ausschliesslich GET-APIs."""
import configparser
import json
from pathlib import Path
import re
import shutil
import socket
import ssl
import subprocess
import urllib.error
import urllib.parse
import urllib.request

class ProbeError(Exception):pass
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None

def get_json(url,headers,validate,timeout):
    try:parsed=urllib.parse.urlsplit(url)
    except ValueError:raise ProbeError('URL_UNGUELTIG') from None
    if parsed.scheme not in ('http','https') or not parsed.netloc or parsed.username is not None or parsed.password is not None:
        raise ProbeError('URL_UNGUELTIG_ODER_ENTHAELT_ZUGANGSDATEN')
    if not isinstance(validate,bool):raise ProbeError('TLS_SCHALTER_KEIN_BOOLEAN')
    context=ssl.create_default_context()
    if not validate:context.check_hostname=False;context.verify_mode=ssl.CERT_NONE
    opener=urllib.request.build_opener(NoRedirect(),urllib.request.HTTPSHandler(context=context))
    request=urllib.request.Request(url,headers={'Accept':'application/json',**headers},method='GET')
    try:
        with opener.open(request,timeout=timeout) as response:
            body=response.read(8*1024*1024+1)
            if len(body)>8*1024*1024:raise ProbeError('ANTWORT_ZU_GROSS')
            value=json.loads(body)
            if not isinstance(value,dict):raise ProbeError('ANTWORT_KEIN_JSON_OBJEKT')
            return value
    except urllib.error.HTTPError as exc:
        code=exc.code;exc.close()
        raise ProbeError('HTTP_'+str(code)+('_REDIRECT_NICHT_VERFOLGT' if code in (301,302,303,307,308) else '')) from None
    except urllib.error.URLError as exc:
        reason=exc.reason
        if isinstance(reason,ssl.SSLCertVerificationError):code='TLS_ZERTIFIKAT_UNGUELTIG'
        elif isinstance(reason,socket.gaierror):code='DNS_FEHLER'
        elif isinstance(reason,(TimeoutError,socket.timeout)):code='ZEITUEBERSCHREITUNG'
        else:code='VERBINDUNG_FEHLGESCHLAGEN'
        raise ProbeError(code) from None
    except (OSError,ValueError,UnicodeError):raise ProbeError('VERBINDUNGS_ODER_JSON_FEHLER') from None

def local_configuration(root,api,active_files=None):
    rows=[]
    cfg=root/'ansible.cfg'
    if cfg.is_file():
        try:
            parser=configparser.ConfigParser(interpolation=None);parser.read_string(cfg.read_text())
            rows.append({'id':'ansible_cfg','status':'OK'})
        except (OSError,configparser.Error,UnicodeError):rows.append({'id':'ansible_cfg','status':'INI_UNGUELTIG'})
    else:rows.append({'id':'ansible_cfg','status':'FEHLT'})
    paths=[]
    paths.extend(sorted((root/'inventory').glob('*.yml')));paths.extend(sorted((root/'inventory').glob('*.yaml')))
    for base in ['playbooks','roles']:
        directory=api.guarded(root,base)
        if directory.is_dir():
            paths.extend(p for p in directory.rglob('*') if p.is_file() and p.suffix in ('.yml','.yaml') and (base=='playbooks' or 'tasks' in p.parts or 'handlers' in p.parts or 'defaults' in p.parts) and 'tests' not in p.parts)
    errors=[];checked=0
    for p in paths:
        if active_files is not None and active_files.get(str(p.relative_to(root))) is False:continue
        if not p.resolve().is_relative_to(root):continue
        try:
            value=__import__('yaml').load(p.read_text(),Loader=api.UniqueLoader)
            if not isinstance(value,(dict,list)) and value is not None:errors.append({'path':str(p.relative_to(root)),'status':'YAML_STRUKTUR_UNGEWOEHNLICH'})
            checked+=1
        except Exception:errors.append({'path':str(p.relative_to(root)),'status':'YAML_UNGUELTIG_ODER_NICHT_UNTERSTUETZTES_TAG'})
    rows.append({'id':'yaml_struktur','status':'OK' if not errors else 'PRUEFBEDARF','files':checked,'issues':errors,'note':'Keine Ansible-Ausfuehrung/Module-/Jinja-/Inventorypluginvalidierung.'})
    return rows

def artifact_check(root,values,api,runner=subprocess.run):
    row={'id':'checkmk_agentartefakt','status':'SKIP_FEATURE_AUS'}
    if values.get('features',{}).get('checkmk') is not True:return row
    raw=values.get('checkmk_agent_package_src','artifacts/checkmk/check-mk-agent.deb')
    if not isinstance(raw,str):return {'id':row['id'],'status':'PFAD_UNGUELTIG'}
    if raw.startswith('{{ playbook_dir }}/../'):
        raw=raw[len('{{ playbook_dir }}/../'):]
    elif api.dynamic(raw):return {'id':row['id'],'status':'DYNAMISCH_UNGEPRUEFT'}
    p=Path(raw)
    try:
        if p.is_absolute():
            p=p.resolve()
            if not p.is_relative_to(root):return {'id':row['id'],'status':'ARTIFAKTPFAD_EXTERN_NICHT_GEPRUEFT'}
        else:p=api.guarded(root,raw)
    except Exception:return {'id':row['id'],'status':'PFAD_UNGUELTIG'}
    if not p.is_file():return {'id':row['id'],'status':'ARTIFAKT_FEHLT','hint':'bin/control checkmk-download'}
    tool=Path('/usr/bin/dpkg-deb')
    if not tool.is_file():return {'id':row['id'],'status':'DPKG_DEB_NICHT_VORHANDEN'}
    try:
        result=runner([str(tool),'-f',str(p),'Version'],capture_output=True,text=True,timeout=10)
        version=result.stdout.strip()
        if result.returncode or not re.fullmatch(r'[0-9][A-Za-z0-9.+~:-]{0,100}',version):return {'id':row['id'],'status':'PAKETMETADATEN_UNGUELTIG'}
        expected=values.get('checkmk_agent_version','')
        matches=isinstance(expected,str) and not api.dynamic(expected) and bool(re.fullmatch(re.escape(expected)+r'(?:-\d+)?',version))
        return {'id':row['id'],'status':'OK' if matches else 'PAKETVERSION_ABWEICHEND','version':version}
    except Exception:return {'id':row['id'],'status':'PAKETMETADATEN_NICHT_LESBAR'}

def run(root,api,offline=False,timeout=8,getter=get_json,progress=None,active_files=None):
    values,_=api.global_settings(root);features=values.get('features',{})
    if not isinstance(features,dict):features={}
    tls=values.get('tls_validate_certs',{});default=values.get('tls_validate_certs_default',True)
    if not isinstance(tls,dict):tls={}
    rows=local_configuration(root,api,active_files);rows.append(artifact_check(root,values,api))
    requests=0
    def call(label,url,headers,validate):
        nonlocal requests
        if offline:raise ProbeError('SKIP_OFFLINE')
        if progress:progress(label)
        requests+=1
        return getter(url,headers,validate,timeout)
    def required(*keys):
        data=[values.get(k) for k in keys]
        if any(not isinstance(x,str) or not x.strip() or api.dynamic(x) for x in data):raise ProbeError('ZUGANG_FEHLT_ODER_DYNAMISCH')
        return data
    if features.get('checkmk') is True:
        try:
            server,site,user,secret=required('checkmk_server_url','checkmk_site','checkmk_api_user','checkmk_api_password')
            validate=tls.get('checkmk_update_check',default)
            headers={'Authorization':'Bearer '+user+' '+secret}
            # Aktuelle stabile API, keine automatischen Schreiboperationen oder unstabilen Endpunkte.
            base=server.rstrip('/')+'/'+urllib.parse.quote(site,safe='')+'/check_mk/api/v1'
            version=call('Checkmk-Version',base+'/version',headers,validate)
            hosts=call('Checkmk-Lesezugriff',base+'/domain-types/host_config/collections/all',headers,validate)
            if not isinstance(hosts.get('value'),list):raise ProbeError('CHECKMK_ANTWORT_UNERWARTET')
            row={'id':'checkmk_api','status':'OK','tls_validate_certs':validate,'hosts_count':len(hosts['value'])}
            reported=version.get('versions',{}).get('checkmk') if isinstance(version.get('versions'),dict) else None
            if isinstance(reported,str) and re.fullmatch(r'\d+\.\d+\.\d+[A-Za-z0-9.-]*',reported):row['version']=reported
            rows.append(row)
        except ProbeError as exc:rows.append({'id':'checkmk_api','status':str(exc)})
    else:rows.append({'id':'checkmk_api','status':'SKIP_FEATURE_AUS'})
    if features.get('proxmox') is True:
        try:
            cfg=api.read_yaml(api.guarded(root,'inventory_config.yml'))
            sources=cfg.get('proxmox_sources')
            if sources is None and isinstance(cfg.get('proxmox'),dict):sources=[dict(cfg['proxmox'],name='default',credential='default')]
            if not isinstance(sources,list) or not sources:raise ProbeError('PROXMOX_QUELLEN_FEHLEN')
            token_secrets=values.get('proxmox_token_secrets',{})
            if not isinstance(token_secrets,dict):raise ProbeError('PROXMOX_SECRET_MAPPING_UNGUELTIG')
            for number,source in enumerate(sources,1):
                label='proxmox_api_'+str(number)
                try:
                    if not isinstance(source,dict):raise ProbeError('PROXMOX_QUELLE_UNGUELTIG')
                    name=source.get('name','');credential=source.get('credential',name)
                    secret=token_secrets.get(credential)
                    if not secret and len(sources)==1:secret=values.get('proxmox_token_secret') or values.get('proxmox_api_token')
                    parts=[source.get('url'),source.get('user'),source.get('token_id'),secret]
                    if any(not isinstance(x,str) or not x.strip() or api.dynamic(x) for x in parts):raise ProbeError('ZUGANG_FEHLT_ODER_DYNAMISCH')
                    url,user,token,secret=parts
                    if not url.startswith('https://'):raise ProbeError('PROXMOX_URL_MUSS_HTTPS_SEIN')
                    validate=tls.get('proxmox_update_check',source.get('validate_certs',True))
                    auth={'Authorization':'PVEAPIToken='+user+'!'+token+'='+secret}
                    version=call(label+'-Version',url.rstrip('/')+'/api2/json/version',auth,validate)
                    resources=call(label+'-Inventoryzugriff',url.rstrip('/')+'/api2/json/cluster/resources?type=vm',auth,validate)
                    if not isinstance(resources.get('data'),list):raise ProbeError('PROXMOX_ANTWORT_UNERWARTET')
                    row={'id':label,'status':'OK','tls_validate_certs':validate,'resources_count':len(resources['data'])}
                    reported=version.get('data',{}).get('version') if isinstance(version.get('data'),dict) else None
                    if isinstance(reported,str) and re.fullmatch(r'\d+(?:\.\d+)+(?:-\d+)?',reported):row['version']=reported
                    rows.append(row)
                except ProbeError as exc:rows.append({'id':label,'status':str(exc)})
        except (ProbeError,api.AuditError,OSError) as exc:rows.append({'id':'proxmox_api','status':str(exc) if isinstance(exc,ProbeError) else 'PROXMOX_KONFIGURATION_UNLESBAR'})
    else:rows.append({'id':'proxmox_api','status':'SKIP_FEATURE_AUS'})
    token=values.get('telegram_bot_token')
    if isinstance(token,str) and token and not api.dynamic(token):
        try:
            validate=tls.get('telegram_update_check',True)
            if not re.fullmatch(r'\d+:[A-Za-z0-9_-]+',token):raise ProbeError('TELEGRAM_TOKENFORMAT_UNGUELTIG')
            result=call('Telegram-Authentifizierung','https://api.telegram.org/bot'+token+'/getMe',{},validate)
            if result.get('ok') is not True:raise ProbeError('TELEGRAM_AUTHENTIFIZIERUNG_FEHLGESCHLAGEN')
            rows.append({'id':'telegram_getme','status':'OK','tls_validate_certs':validate,'message_sent':False})
        except ProbeError as exc:rows.append({'id':'telegram_getme','status':str(exc),'message_sent':False})
    else:rows.append({'id':'telegram_getme','status':'SKIP_NICHT_EINGERICHTET','message_sent':False})
    return {'configuration_and_api_checks':rows,'network_requests':requests,'offline':offline,'changes_activated':False,'messages_sent':False,'note':'Nur YAML-/INI-Struktur und lesende API-Aufrufe. Keine vollstaendige Ansible-/Dienstvalidierung.'}
