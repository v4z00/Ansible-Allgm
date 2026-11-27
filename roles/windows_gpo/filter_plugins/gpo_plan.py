"""Compile typed, environment-neutral GPO profiles; no inventory discovery or I/O."""
import re

# Settings with None/missing values remain unmanaged. False is an explicit value.
CATALOG = {
    'winrm_basic': (r'HKLM\Software\Policies\Microsoft\Windows\WinRM\Service', 'AllowBasic'),
    'winrm_unencrypted': (r'HKLM\Software\Policies\Microsoft\Windows\WinRM\Service', 'AllowUnencryptedTraffic'),
    'smb_client_signing': (r'HKLM\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters', 'RequireSecuritySignature'),
    'smb_server_signing': (r'HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters', 'RequireSecuritySignature'),
}
NTLM_KEY = r'HKLM\SYSTEM\CurrentControlSet\Control\Lsa\MSV1_0'


def plan(profiles, prefix='Ansible: ', transport='ntlm'):
    if not isinstance(prefix, str) or not prefix.strip() or len(prefix)>80 or re.search(r'[\x00-\x1f]',prefix):
        raise ValueError('A short, printable GPO prefix is required')
    if not isinstance(profiles,list) or len(profiles)>40:
        raise ValueError('A bounded list of GPO profiles is required')
    output=[]; ids=set(); names=set()
    transports=transport if isinstance(transport,list) else [transport]
    if any(not isinstance(t,str) for t in transports):raise ValueError('Invalid WinRM transport')
    for profile in profiles:
        if not isinstance(profile,dict) or set(profile)-{'id','name','settings'}:
            raise ValueError('Unknown GPO profile fields')
        identity=profile.get('id','');name=profile.get('name','')
        if not isinstance(identity,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',identity):
            raise ValueError('Stable GPO profile id required')
        if not isinstance(name,str) or not name.strip() or len(name)>100 or re.search(r'[\x00-\x1f]',name):
            raise ValueError('Printable GPO topic name required')
        full=prefix+name
        if identity in ids or full.casefold() in names:raise ValueError('Duplicate GPO profile')
        ids.add(identity);names.add(full.casefold())
        settings=profile.get('settings',{})
        if not isinstance(settings,dict) or set(settings)-CATALOG.keys()-{'ntlm_outgoing'}:
            raise ValueError('Unknown GPO setting')
        values=[]
        for feature,(key,value_name) in CATALOG.items():
            value=settings.get(feature)
            if value is None:continue
            if type(value) is not bool:raise ValueError('GPO switches must be real booleans')
            values.append({'feature':feature,'key':key,'name':value_name,'type':'DWord','value':int(value)})
        mode=settings.get('ntlm_outgoing','unmanaged')
        if mode not in ('unmanaged','allow','audit','deny'):raise ValueError('Invalid NTLM outgoing mode')
        if mode!='unmanaged':
            if mode=='deny' and any(t.lower() in ('ntlm','credssp') for t in transports):
                raise ValueError('Prepare and verify a non-NTLM management path before denying NTLM')
            values.append({'feature':'ntlm_outgoing','key':NTLM_KEY,'name':'RestrictSendingNTLMTraffic',
                           'type':'DWord','value':{'allow':0,'audit':1,'deny':2}[mode]})
        if values:output.append({'id':identity,'name':full,'values':values})
    return {'schema':1,'profiles':output}


class FilterModule:
    def filters(self):return {'windows_gpo_plan':plan}
