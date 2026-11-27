"""Select only the credentials needed by explicitly enabled host alarm channels."""


def configuration(values,channels,windows=False):
    if not isinstance(values,dict) or not isinstance(channels,list) or not channels or len(channels)!=len(set(channels)):
        raise ValueError('Explicit security channels/configuration required')
    if set(channels)-{'mail','telegram'}:raise ValueError('Unknown security channel')
    result={'SECURITY_CHANNELS':channels}
    if 'telegram' in channels:
        import re
        if not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+',str(values.get('BOT_TOKEN',''))) or not values.get('CHAT_ID'):
            raise ValueError('Telegram security channel incomplete')
        result.update({key:values[key] for key in ('BOT_TOKEN','CHAT_ID')})
    if 'mail' in channels:
        recipient=values.get('MAIL_TO','')
        if not isinstance(recipient,str) or not recipient or any(c in recipient for c in '\r\n'):
            raise ValueError('Security mail recipient required')
        result['MAIL_TO']=recipient
        if values.get('SMTP_HOST'):
            for key in ('SMTP_HOST','SMTP_FROM'):
                if not isinstance(values.get(key),str) or not values[key] or any(c in values[key] for c in '\r\n'):
                    raise ValueError('SMTP host and sender required')
            tls=values.get('SMTP_TLS','starttls');auth=values.get('SMTP_AUTH','none')
            if tls not in ('none','starttls','tls') or windows and tls=='tls' or auth not in ('none','password'):
                raise ValueError('Unsupported SMTP security settings')
            result.update({key:values[key] for key in ('SMTP_HOST','SMTP_FROM')})
            result.update(SMTP_PORT=int(values.get('SMTP_PORT',465 if tls=='tls' else 25 if tls=='none' else 587)),SMTP_TLS=tls,SMTP_AUTH=auth)
            if not 1<=result['SMTP_PORT']<=65535:raise ValueError('Invalid SMTP port')
            if auth=='password':
                if not values.get('SMTP_USERNAME') or not values.get('SMTP_PASSWORD'):raise ValueError('SMTP credentials incomplete')
                result.update({key:values[key] for key in ('SMTP_USERNAME','SMTP_PASSWORD')})
        elif windows:raise ValueError('Windows security mail requires an SMTP relay')
    return result


class FilterModule:
    def filters(self):return {'script_security_config':configuration}
