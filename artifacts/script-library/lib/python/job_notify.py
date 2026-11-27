"""Private notification transport with fixed ASCII mail mapping and per-channel ACK."""
import json
from email.message import EmailMessage
import shutil
import smtplib
import ssl
import subprocess
import unicodedata
import urllib.parse
import urllib.request


def ascii_mail(text,root):
    with (root/'lib/data/mail-translations.json').open(encoding='utf8') as f:table=json.load(f)
    text=unicodedata.normalize('NFC',text)
    for source,target in table.items():text=text.replace(source,target)
    text=unicodedata.normalize('NFKD',text)
    return ''.join(c for c in text if not unicodedata.combining(c)).encode('ascii','replace').decode('ascii')


def smtp_mail(subject,body,recipient,cfg):
    """Explicit relay/TLS settings; authentication is independent of encryption."""
    host=cfg['SMTP_HOST'];sender=cfg.get('SMTP_FROM','')
    if not all(isinstance(value,str) and value and '\r' not in value and '\n' not in value
               for value in (host,sender,recipient)):
        raise ValueError('SMTP host, sender and recipient required')
    tls=cfg.get('SMTP_TLS','starttls')
    auth=cfg.get('SMTP_AUTH','none')
    if tls not in ('none','starttls','tls') or auth not in ('none','password'):
        raise ValueError('Invalid SMTP TLS/authentication mode')
    if auth=='password' and not (cfg.get('SMTP_USERNAME') and cfg.get('SMTP_PASSWORD')):
        raise ValueError('SMTP credentials incomplete')
    port=int(cfg.get('SMTP_PORT',465 if tls=='tls' else 25 if tls=='none' else 587))
    if not 1<=port<=65535:raise ValueError('Invalid SMTP port')
    message=EmailMessage();message['From']=sender;message['To']=recipient;message['Subject']=subject
    message.set_content(body,charset='us-ascii')
    context=ssl.create_default_context(cafile=cfg.get('SMTP_CA_FILE') or None)
    client=smtplib.SMTP_SSL(host,port,timeout=30,context=context) if tls=='tls' else smtplib.SMTP(host,port,timeout=30)
    with client:
        if tls=='starttls':client.starttls(context=context)
        if auth=='password':client.login(cfg['SMTP_USERNAME'],cfg['SMTP_PASSWORD'])
        client.send_message(message)


def deliver(channel,report,cfg,root):
    if channel=='mail':
        recipient=cfg.get('EMAIL') or cfg.get('MAIL_TO')
        if not isinstance(recipient,str) or not recipient or recipient.startswith('-') or '\n' in recipient or '\r' in recipient:raise ValueError('Mail configuration unavailable')
        subject=ascii_mail(report['body'].splitlines()[0] if report['body'] else 'Job-Zusammenfassung',root)
        body=ascii_mail(report['body'],root)
        if cfg.get('SMTP_HOST'):
            smtp_mail(subject,body,recipient,cfg)
            return
        binary=shutil.which('mail') or shutil.which('mailx')
        if not binary:raise ValueError('Local mail transport unavailable')
        subprocess.run([binary,'-s',subject,recipient],input=body.encode('ascii'),check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=60)
    elif channel=='telegram':
        token=cfg.get('BOT_TOKEN') or cfg.get('TELEGRAM_BOT_TOKEN');chat=cfg.get('CHAT_ID') or cfg.get('TELEGRAM_CHAT_ID')
        import re
        if not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+',str(token)):raise ValueError('Telegram configuration invalid')
        # Conservative chunks avoid exceeding Telegram character limits with emoji.
        body=report['body']
        for start in range(0,len(body),1800):
            data=urllib.parse.urlencode({'chat_id':chat,'text':body[start:start+1800]}).encode()
            req=urllib.request.Request('https://api.telegram.org/bot'+token+'/sendMessage',data=data)
            verify=cfg.get('TELEGRAM_VALIDATE_CERTS',True)
            if not isinstance(verify,bool):raise ValueError('TLS validation flag must be boolean')
            context=ssl.create_default_context() if verify else ssl._create_unverified_context()
            with urllib.request.urlopen(req,timeout=30,context=context) as response:result=json.load(response)
            if result.get('ok') is not True:raise ValueError('Notification rejected')
    else:raise ValueError('Unknown notification channel')
