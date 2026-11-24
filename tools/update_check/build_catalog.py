"""Entwicklungshelfer: Katalog nur aus geprueften Beispiel-/Vorlagenquellen erzeugen."""
import hashlib,json,re
from pathlib import Path
import yaml

def build(package,template,home):
    examples=package/'examples';base=yaml.safe_load((template/'examples/first_run/settings.yml.example').read_text())
    base.setdefault('portainer_check_enabled', False)
    extra=yaml.safe_load((examples/'checkmk/settings.example.yml').read_text());base.update(extra)
    base.update(yaml.safe_load((examples/'checkmk/plugins.example.yml').read_text()))
    # Nur neutrale Beispiele; keine Secrets oder Standortsettings lesen.
    (examples/'settings').mkdir(exist_ok=True)
    (examples/'settings/all_settings.example.yml').write_text('# Neutrale Nachschlagewerte; keine aktive Konfiguration.\n# Werte mit example.invalid sind Platzhalter und werden nicht automatisch uebernommen.\n'+yaml.safe_dump(base,sort_keys=False,allow_unicode=True))
    contract=json.loads((package/'update_check/settings_contract.json').read_text())
    sources={};data={}
    files=['settings/all_settings.example.yml','checkmk/settings.example.yml','checkmk/plugins.example.yml','access/host_access.example.yml','access/credentials.example.yml','bootstrap/settings.example.yml','tls/settings.example.yml']
    if home:files.append('homelab/settings.example.yml')
    for rel in files:
        p=examples/rel;values=yaml.safe_load(p.read_text()) or {}
        sources['examples/'+rel]=hashlib.sha256(p.read_bytes()).hexdigest()
        def walk(obj,prefix=''):
            for key,value in obj.items():
                full=prefix+key;data[full]=(value,'examples/'+rel)
                if isinstance(value,dict):walk(value,full+'.')
        walk(values)
    descriptions={
      'portainer_check_enabled':'Zusätzlichen TCP-Test für Portainer nach dem Pflichtcheck aktivieren.',
      'portainer_check_host':'Optionales TCP-Ziel. Ohne Eintrag gilt die Ansible-Adresse des Docker-Hosts.',
      'portainer_check_port':'TCP-Port für den optionalen Portainer-Test.',
      'portainer_check_timeout':'Wartezeit für den Portainer-TCP-Test in Sekunden.',

      'checkmk_server':'Adresse und Port des Checkmk-Agent-Receivers fuer die TLS-Registrierung.',
      'checkmk_server_url':'HTTPS-Basisadresse der Checkmk-Weboberflaeche/API, ohne Site-Unterpfad.',
      'checkmk_site':'Name der Checkmk-Site; wird fuer API- und Agentregistrierung verwendet.',
      'checkmk_download_base_url':'Downloadverzeichnis fuer Agentpaket und Plugins auf deiner Checkmk-Site.',
      'checkmk_agent_version':'Exakte Agent-Paketversion fuer den Download. Das Paket muss auf der Site vorhanden sein.',
      'checkmk_linux_plugins':'Dateinamen fuer den Plugin-Download. Die Hostgruppen steuern weiterhin die Verteilung.',
      'checkmk_folders':'Liste der anzulegenden Checkmk-Ordner mit path und name.',
      'checkmk_api_password':'Automation-Secret fuer die Checkmk-REST-API. Neue Werte nur in lokale secrets.yml schreiben.',
      'checkmk_registration_password':'Secret fuer die Agentregistrierung; lokale secrets.yml, nicht Beispielordner.',
      'tls_validate_certs_default':'Standortstandard fuer die getrennten TLS-Aufgaben. Telegram wird getrennt konfiguriert.',
      'tls_validate_certs':'Gezielte boolesche Ausnahmen pro TLS-Aufgabe; vorhandene Schluessel erhalten.',
      'tls_validate_certs.telegram_notification':'TLS-Zertifikatspruefung beim Versand an die oeffentliche Telegram-API. Empfehlung true; lokale Ausnahmen bleiben erlaubt.',
      'tls_validate_certs.backup_telegram_notification':'TLS-Zertifikatspruefung fuer die getrennte Backup-Telegram-Nachricht. Empfehlung true; lokale Ausnahmen bleiben erlaubt.',
      'rsyslog_protocol':'Transportprotokoll der zentralen Syslog-Weiterleitung: tcp oder udp.',
      'rsyslog_target_host':'Zielserver fuer die zentrale Syslog-Weiterleitung.',
      'rsyslog_target_port':'Port des zentralen Syslog-Empfaengers.',
      'system_timezone':'Zeitzone fuer die verwalteten Systeme, zum Beispiel Europe/Berlin.',
      'chrony_ntp_servers':'Liste der Zeitserver. LXC-Ausnahmen der bestehenden Rolle bleiben erhalten.',
      'bootstrap_public_key_file':'Controller-Public-Key fuer den einmaligen Erstzugang; Jinja wird hier nicht ausgefuehrt.',
      'ansible_auth_mode':'SSH-Anmeldemodus der vorhandenen Zugangskonfiguration.',
      'host_updates_reboot':'Kein globaler Reboot-Opt-in: automatischer Neustart bleibt auf den expliziten Host-Update-Starter begrenzt.'}
    tls_help={}
    previous=''
    for line in (examples/'tls/settings.example.yml').read_text().splitlines():
        m=re.match(r'\s*#\s*([a-z0-9_]+):',line)
        if m:tls_help[m.group(1)]=previous.lstrip(' #')
        if line.strip():previous=line
    fields={}
    for rule in contract['fields']:
        key=rule['key'];info={'description':descriptions.get(key,('Funktionsschalter fuer '+key.split('.',1)[1]+'. Nur aktivieren, wenn dieses Modul eingerichtet werden soll.') if key.startswith('features.') else 'Konfigurationswert '+key+' fuer die bestehende Rolle; Bedeutung und Typ anhand des zugeordneten Beispiels pruefen.'),'source':'settings_contract.json'}
        if key in data:
            value,source=data[key];info['source']=source
            sensitive=bool(re.search(r'password|secret|credential|private_key|telegram_bot_token',key,re.I))
            if not sensitive:
                info['example']=value
                placeholder=(isinstance(value,str) and (not value or 'example.invalid' in value or value in ['template','Musterumgebung','IT-Administration']))
                info['example_only']=placeholder
                if not placeholder and value not in (None,):info['default']=value
        if key.startswith('tls_validate_certs.'):
            task=key.split('.',1)[1]
            info['description']='Zertifikatspruefung fuer: '+tls_help.get(task,task)+'. true prueft, false ueberspringt nur diese Aufgabe.'
            info['source']='examples/tls/settings.example.yml'
            info.pop('default',None) # Kein hart codierter Aufgaben-/Standortwert; nur vorhandene Beispieldaten verwenden.
            if key in data:info['default']=data[key][0]
            elif 'tls_validate_certs_default' in data:info['default']=data['tls_validate_certs_default'][0]
            info['example_only']=False
            if task=='proxmox_update_check':
                info.pop('default',None);info['example_only']=True
                info['description']='Nur TLS des lesenden API-Tests. Ohne Eintrag gilt validate_certs je Inventoryquelle. Produktive Quellenkonfiguration bleibt getrennt.'
        if key=='rsyslog_protocol':info['choices']=['tcp','udp']
        if key=='ansible_auth_mode':info['choices']=['password_all','key_only','password_users_only']
        if key=='managed_access_default_become_method':info['choices']=['sudo','su']
        fields[key]=info
    order=['site_id','site_name','site_managed_by','features','ansible_auth_mode','auth_method_description','managed_access_default_user','managed_access_default_port','managed_access_default_become','managed_access_default_become_method','managed_access_default_become_user','managed_host_access','bootstrap_targets','bootstrap_public_key_file','bootstrap_disable_password_auth_after_key','tls_validate_certs_default','tls_validate_certs']
    order += [key for key in base if key not in order]
    return {'schema':1,'fields':fields,'example_sources':sources,'top_level_order':order,'policy':'Nur gepruefte Beispiele als Vorgabe. Keine Platzhalter oder Zugangsdaten automatisch uebernehmen.'}
