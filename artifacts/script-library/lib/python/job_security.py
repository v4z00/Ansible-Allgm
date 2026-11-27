"""Immediate host security alerts; durable, deduplicated, channel-specific retry."""
import json
import re
import uuid

from job_store import safe_text, utc
from job_notify import deliver


def channels(cfg):
    selected=cfg.get('SECURITY_CHANNELS')
    if selected is None:
        selected=[]
        if cfg.get('EMAIL') or cfg.get('MAIL_TO'):selected.append('mail')
        if (cfg.get('BOT_TOKEN') or cfg.get('TELEGRAM_BOT_TOKEN')) and (cfg.get('CHAT_ID') or cfg.get('TELEGRAM_CHAT_ID')):
            selected.append('telegram')
    if not isinstance(selected,list) or not selected or len(set(selected))!=len(selected) or any(c not in ('mail','telegram') for c in selected):
        raise ValueError('Explicit security notification channels required')
    return selected


def record(store,event_key,job,summary,details,selected):
    """Commit the alert and intended deliveries before contacting any service."""
    if not isinstance(event_key,str) or not 1<=len(event_key)<=256 or any(ord(c)<32 for c in event_key):
        raise ValueError('Stable security event key required')
    if not isinstance(job,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',job):
        raise ValueError('Invalid security job name')
    if not selected or any(c not in ('mail','telegram') for c in selected):raise ValueError('Invalid security channels')
    summary=safe_text(summary,200);details=safe_text(details,1000)
    with store.transaction():
        previous=store.db.execute('SELECT report_id FROM security_alerts WHERE event_key=?',(event_key,)).fetchone()
        if previous:return previous[0]
        identifier=str(uuid.uuid4());run=str(uuid.uuid4());now=utc()
        store.db.execute("INSERT INTO runs(source,epoch,run_id,job,category,status,started,activity,finished,exit_code,summary,duration_seconds) VALUES(?,?,?,?,'security','failed',?,?,?,1,?,0)",(*store._key(run),job,now,now,now,summary))
        store._event(run,'finish')
        body='Security alert ❌\n%s / %s\n%s'%(safe_text(store.host,160),job,summary)
        if details:body+='\n'+details
        store.db.execute('INSERT INTO reports VALUES(?,?,?,?)',(identifier,'security',now,body))
        store.db.execute('INSERT INTO security_alerts VALUES(?,?)',(event_key,identifier))
        store.db.execute('INSERT INTO report_runs VALUES(?,?,?,?)',(identifier,*store._key(run)))
        store.db.executemany('INSERT INTO deliveries VALUES(?,?,?,0,0,?)',[(identifier,c,'pending',now) for c in selected])
        return identifier


def retry(store,cfg,root,limit=100,report=None):
    """A failed channel stays pending; successful channels are never resent."""
    rows=store.db.execute("SELECT p.id,p.body,d.channel FROM reports p JOIN deliveries d ON d.report_id=p.id WHERE p.category='security' AND d.status!='sent' AND d.lease_until<? AND (? IS NULL OR p.id=?) ORDER BY p.created,d.channel LIMIT ?",(utc(),report,report,min(max(int(limit),1),1000))).fetchall()
    failed=False
    for row in rows:
        if not store.claim(row['id'],row['channel']):continue
        try:deliver(row['channel'],dict(row),cfg,root)
        except Exception:
            store.delivered(row['id'],row['channel'],False);failed=True
        else:store.delivered(row['id'],row['channel'],True)
    pending=store.db.execute("SELECT COUNT(*) FROM deliveries d JOIN reports p ON p.id=d.report_id WHERE p.category='security' AND d.status!='sent'").fetchone()[0]
    return {'pending':pending,'failed':failed}
