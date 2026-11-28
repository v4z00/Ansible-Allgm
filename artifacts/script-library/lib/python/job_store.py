"""Local SQLite job/event store. No network access; no raw task output storage."""
import contextlib
import datetime
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import time
import uuid

SCHEMA = 1
STATUSES = {'running', 'success', 'warning', 'failed', 'skipped'}
TERMINAL = STATUSES - {'running'}
CATEGORIES = {'general', 'vzdump', 'ansible', 'administration', 'security'}

def utc():
    return time.time()

def safe_text(value, limit=1000):
    text=str(value)
    # Known private config values are removed before messages enter the database.
    paths=[]
    try:paths=json.loads(os.environ.get('HM_JOB_CONFIGFILES','[]'))
    except ValueError:pass
    for path in paths:
        try:
            with open(path,encoding='utf8') as handle:values=json.load(handle)
            for key,secret in values.items():
                if re.search(r'PASSWORD|PASSPHRASE|SECRET|TOKEN|API_KEY',key,re.I) and isinstance(secret,str) and len(secret)>3:
                    text=text.replace(secret,'[redacted]')
        except (OSError,ValueError,AttributeError):pass
    text=re.sub(r'(?i)(?:https?://)?api\.telegram\.org/bot[^/\s]+', '[telegram]', text)
    text=re.sub(r'(?i)(password|passwd|secret|token|authorization|api[_-]?key)\s*[:=]\s*[^\s,;]+',r'\1=[redacted]',text)
    text=re.sub(r'([a-z][a-z0-9+.-]*://)[^\s/@]+:[^\s/@]+@',r'\1[redacted]@',text)
    return ''.join(c for c in text if c in '\n\t' or ord(c)>=32)[:limit]

class Store:
    def __init__(self,path,host=None):
        self.path=Path(path).expanduser().absolute()
        self.path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        if self.path.is_symlink(): raise ValueError('Database symlink refused')
        if self.path.exists():
            s=self.path.stat()
            if not stat.S_ISREG(s.st_mode) or s.st_uid not in (0,os.geteuid()) or stat.S_IMODE(s.st_mode)&0o077:
                raise ValueError('Database requires private owner permissions')
        self.db=sqlite3.connect(str(self.path),timeout=10,isolation_level=None)
        os.chmod(self.path,0o600)
        self.db.row_factory=sqlite3.Row
        for attempt in range(20):
            try:self.db.execute('PRAGMA journal_mode=WAL');break
            except sqlite3.OperationalError:
                if attempt==19:raise
                time.sleep(0.05)
        self.db.execute('PRAGMA foreign_keys=ON')
        schema = Path(__file__).resolve().parents[1] / 'data/job-schema.sql'
        self.db.executescript(schema.read_text(encoding='utf-8'))
        with self.transaction():
            if 'duration_seconds' not in {r[1] for r in self.db.execute('PRAGMA table_info(runs)')}:self.db.execute('ALTER TABLE runs ADD COLUMN duration_seconds REAL')
            self.db.execute('INSERT OR IGNORE INTO meta VALUES(?,?)',('schema',str(SCHEMA)))
            self.db.execute('INSERT OR IGNORE INTO meta VALUES(?,?)',('epoch',str(uuid.uuid4())))
            self.db.execute('INSERT OR IGNORE INTO meta VALUES(?,?)',('host',host or os.uname().nodename))
            self.db.execute('INSERT OR IGNORE INTO meta VALUES(?,?)',('floor','0'))
        if int(self.meta('schema'))!=SCHEMA:raise ValueError('Unsupported database schema')
        self.epoch=self.meta('epoch');self.host=self.meta('host')
    def meta(self,key):return self.db.execute('SELECT value FROM meta WHERE key=?',(key,)).fetchone()[0]
    @contextlib.contextmanager
    def transaction(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:yield
        except BaseException:self.db.execute('ROLLBACK');raise
        else:self.db.execute('COMMIT')
    def close(self):self.db.close()
    def _key(self,run):return (self.host,self.epoch,run)
    def _event(self,run,kind):
        key=self._key(run)
        row=self.db.execute('SELECT * FROM runs WHERE source=? AND epoch=? AND run_id=?',key).fetchone()
        items=[dict(x) for x in self.db.execute('SELECT item_id,status,message,updated FROM items WHERE source=? AND epoch=? AND run_id=?',key)]
        payload={'run':dict(row),'items':items}
        self.db.execute('INSERT INTO events(source,epoch,run_id,created,kind,payload) VALUES(?,?,?,?,?,?)',(*key,utc(),kind,json.dumps(payload)))
    def begin(self,job,category='general'):
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',job):raise ValueError('Invalid job name')
        if category not in CATEGORIES:raise ValueError('Invalid category')
        run=str(uuid.uuid4());now=utc()
        with self.transaction():
            self.db.execute('INSERT INTO runs(source,epoch,run_id,job,category,status,started,activity) VALUES(?,?,?,?,?,?,?,?)',(*self._key(run),job,category,'running',now,now))
            self._event(run,'start')
        return run
    def update(self,run,status=None,summary='',item=None,exit_code=None,duration_seconds=None):
        if status is not None and status not in STATUSES:raise ValueError('Invalid status')
        if item is None and status in TERMINAL:
            if exit_code is None or (status in ('success','warning','skipped') and exit_code!=0) or (status=='failed' and exit_code==0):raise ValueError('Status and exit code disagree')
        with self.transaction():
            key=self._key(run);row=self.db.execute('SELECT status FROM runs WHERE source=? AND epoch=? AND run_id=?',key).fetchone()
            if not row or row[0]!='running':raise ValueError('Run is not running')
            now=utc();msg=safe_text(summary)
            if item is not None:
                if not str(item) or len(str(item))>160:raise ValueError('Invalid item ID')
                self.db.execute('INSERT OR REPLACE INTO items VALUES(?,?,?,?,?,?,?)',(*key,str(item),status or 'running',msg,now))
                self.db.execute('UPDATE runs SET activity=? WHERE source=? AND epoch=? AND run_id=?',(now,*key))
            else:
                terminal=status in TERMINAL
                self.db.execute('UPDATE runs SET status=?,activity=?,finished=?,exit_code=?,summary=?,duration_seconds=COALESCE(?,duration_seconds) WHERE source=? AND epoch=? AND run_id=?',(status or 'running',now,now if terminal else None,exit_code if terminal else None,msg,duration_seconds,*key))
            self._event(run,'item' if item is not None else ('finish' if status in TERMINAL else 'progress'))
    def recover(self,job):
        # Called only after obtaining the exclusive local job lock.
        rows=self.db.execute('SELECT run_id FROM runs WHERE source=? AND epoch=? AND job=? AND status=?',(self.host,self.epoch,job,'running')).fetchall()
        for row in rows:self.update(row[0],'failed','Previous process ended without completion',exit_code=255)
    def runs(self,job=None,status=None,category=None,limit=100,source=None,since=None,until=None,item=None):
        conditions=[];params=[]
        for k,v in [('job',job),('status',status),('category',category),('source',source)]:
            if v:conditions.append(k+'=?');params.append(v)
        if since is not None:conditions.append('started>=?');params.append(float(since))
        if until is not None:conditions.append('started<=?');params.append(float(until))
        if item is not None:
            conditions.append('EXISTS(SELECT 1 FROM items i WHERE i.source=runs.source AND i.epoch=runs.epoch AND i.run_id=runs.run_id AND i.item_id=?)');params.append(str(item))
        sql='SELECT * FROM runs'+(' WHERE '+' AND '.join(conditions) if conditions else '')+' ORDER BY started DESC LIMIT ?'
        return [dict(r) for r in self.db.execute(sql,(*params,min(max(int(limit),1),1000)))]
    def details(self,run):
        rows=[dict(r) for r in self.db.execute('SELECT * FROM runs WHERE run_id=?',(run,))]
        for row in rows:row['items']=[dict(i) for i in self.db.execute('SELECT item_id,status,message,updated FROM items WHERE source=? AND epoch=? AND run_id=?',(row['source'],row['epoch'],run))]
        return rows
    def latest(self,job=None,category=None,source=None):
        """Latest state per source/job, including a newer running job."""
        where=['NOT EXISTS (SELECT 1 FROM runs n WHERE n.source=r.source AND n.job=r.job AND (n.started>r.started OR (n.started=r.started AND n.rowid>r.rowid)))']
        params=[]
        for key,value in [('job',job),('category',category),('source',source)]:
            if value is not None:where.append('r.'+key+'=?');params.append(value)
        return [dict(row) for row in self.db.execute('SELECT r.* FROM runs r WHERE '+' AND '.join(where)+' ORDER BY r.source,r.job',params)]
    def export(self,after=0,epoch=None,limit=200):
        after=int(after);floor=int(self.meta('floor'))
        sequence=self.db.execute("SELECT seq FROM sqlite_sequence WHERE name='events'").fetchone()
        mismatch=(epoch is not None and epoch!=self.epoch) or after>(sequence[0] if sequence else 0)
        gap=(after<floor and after!=0) or (after==0 and floor>0)
        rows=[dict(r) for r in self.db.execute('SELECT id,kind,created,payload FROM events WHERE id>? ORDER BY id LIMIT ?',(after,min(max(int(limit),1),500)))]
        for row in rows:row['payload']=json.loads(row['payload'])
        return {'schema':SCHEMA,'epoch':self.epoch,'floor':floor,'reset_required':mismatch,'gap':gap,
                'events':rows,'next':rows[-1]['id'] if rows else after, 'expectations':json.loads(self.db.execute("SELECT value FROM meta WHERE key='expectations'").fetchone()[0]) if self.db.execute("SELECT 1 FROM meta WHERE key='expectations'").fetchone() else []}
    def cursor(self,source):
        row=self.db.execute('SELECT epoch,last_id FROM cursors WHERE source=?',(source,)).fetchone()
        return dict(row) if row else {'epoch':None,'last_id':0}
    def health(self,source,status,message='',category='general'):
        if category not in ('general','vzdump'):raise ValueError('Invalid health category')
        with self.transaction():
            self.db.execute('INSERT OR REPLACE INTO collection_health VALUES(?,?,?,?)',(source,status,utc(),safe_text(message)))
            self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('health_category:'+source,category))
    def ingest(self,source,batch,accept_gap=False):
        if batch.get('schema')!=SCHEMA:raise ValueError('Unsupported event schema')
        previous=self.cursor(source);epoch=batch['epoch']
        if previous['epoch'] and previous['epoch']!=epoch:
            self.health(source,'generation-changed');raise ValueError('Source database generation changed; explicit reset required')
        acknowledged=self.db.execute('SELECT value FROM meta WHERE key=?',('accept-gap:'+source,)).fetchone()
        accept_gap=accept_gap or bool(acknowledged)
        if (batch.get('gap') or batch.get('reset_required')) and not accept_gap:
            self.health(source,'gap');raise ValueError('Event history gap; explicit reset required')
        events=batch['events'];expected=previous['last_id']
        if not isinstance(events,list) or len(events)>500:raise ValueError('Invalid batch size')
        with self.transaction():
            current=self.cursor(source)
            if current['epoch'] and current['epoch']!=epoch:raise ValueError('Generation changed concurrently')
            expected=current['last_id']
            if batch['next']<expected:return 0
            for event in events:
                if not isinstance(event,dict):raise ValueError('Invalid event record')
                if not isinstance(event['id'],int) or event['id']<=expected:continue
                payload=event['payload'];run=payload['run']
                if run['status'] not in STATUSES or run['category'] not in CATEGORIES:raise ValueError('Invalid event status')
                key=(source,epoch,run['run_id'])
                self.db.execute('INSERT OR REPLACE INTO runs(source,epoch,run_id,job,category,status,started,activity,finished,exit_code,summary,duration_seconds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(*key,safe_text(run['job'],160),run['category'],run['status'],float(run['started']),float(run['activity']),run['finished'],run['exit_code'],safe_text(run['summary']),run.get('duration_seconds')))
                if event.get('kind') == 'systemd-observation':
                    self.db.execute('INSERT OR REPLACE INTO run_observations VALUES(?,?,?,?)', (*key, 'systemd'))
                for item in payload.get('items',[]):
                    if item['status'] not in STATUSES:raise ValueError('Invalid item status')
                    self.db.execute('INSERT OR REPLACE INTO items VALUES(?,?,?,?,?,?,?)',(*key,safe_text(item['item_id'],160),item['status'],safe_text(item['message']),float(item['updated'])))
                expected=event['id']
            if batch['next']!=expected:raise ValueError('Cursor did not match imported events')
            self.db.execute('INSERT OR REPLACE INTO cursors VALUES(?,?,?,?)',(source,epoch,expected,utc()))
            self.db.execute('DELETE FROM meta WHERE key=?',('accept-gap:'+source,))
            self.db.execute('INSERT OR REPLACE INTO collection_health VALUES(?,?,?,?)',(source,'ok',utc(),''))
        return len(events)
    def reset_cursor(self,source):
        with self.transaction():
            self.db.execute('DELETE FROM cursors WHERE source=?',(source,))
            self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',('accept-gap:'+source,'1'))
    def prune(self,days=90):
        if int(days)<1:raise ValueError('Retention must be positive')
        cutoff=utc()-int(days)*86400
        with self.transaction():
            old=[tuple(r) for r in self.db.execute('SELECT source,epoch,run_id FROM runs WHERE finished IS NOT NULL AND finished<?',(cutoff,))]
            removed=0
            for key in old:
                top=self.db.execute('SELECT MAX(id) FROM events WHERE source=? AND epoch=? AND run_id=?',key).fetchone()[0]
                if top:self.db.execute('UPDATE meta SET value=? WHERE key=?',(str(max(int(self.meta('floor')),top)),'floor'))
                self.db.execute('DELETE FROM events WHERE source=? AND epoch=? AND run_id=?',key)
                self.db.execute('DELETE FROM report_runs WHERE source=? AND epoch=? AND run_id=?',key)
                removed+=self.db.execute('DELETE FROM runs WHERE source=? AND epoch=? AND run_id=?',key).rowcount
            self.db.execute("DELETE FROM reports WHERE created<? AND NOT EXISTS(SELECT 1 FROM report_runs WHERE report_id=reports.id) AND NOT EXISTS(SELECT 1 FROM deliveries WHERE report_id=reports.id AND status!='sent')",(cutoff,))
        for source,epoch,identifier in old:
            if source!=self.host or epoch!=self.epoch:continue
            try:uuid.UUID(identifier)
            except ValueError:continue
            log=self.path.parent/'logs'/(identifier+'.log')
            if log.is_file() and not log.is_symlink():
                try:log.unlink()
                except OSError:
                    import sys
                    print('One expired private job log could not be removed.',file=sys.stderr)
        return removed
    @staticmethod
    def _failure_job_names(names):
        if not isinstance(names, (list, tuple)) or any(
            not isinstance(name, str) or not name or len(name) > 160 for name in names
        ) or len(names) > 100:
            raise ValueError('Invalid list of separately reported jobs')
        return tuple(dict.fromkeys(names))

    def failure_reports(self, jobs, *, reserve=True, labels=None, channels=()):
        """Keep each failed run and each delivery independently retryable."""
        from job_report import format_report

        jobs = self._failure_job_names(jobs)
        if not isinstance(channels, (list, tuple)) or any(channel not in ('mail', 'telegram') for channel in channels):
            raise ValueError('Invalid report channels')
        if reserve and not channels:
            raise ValueError('At least one delivery channel is required')
        if not jobs:
            return []
        with self.transaction():
            pending = [dict(row) for row in self.db.execute("""
                SELECT p.id, p.body FROM reports p
                WHERE p.category='job-failure' AND EXISTS (
                    SELECT 1 FROM deliveries d WHERE d.report_id=p.id AND d.status!='sent'
                )
                ORDER BY p.created, p.id LIMIT 50
            """)]
            placeholders = ','.join('?' for _ in jobs)
            rows = self.db.execute(f"""
                SELECT r.* FROM runs r
                WHERE r.category='general' AND r.status='failed' AND r.job IN ({placeholders})
                AND NOT EXISTS (
                    SELECT 1 FROM report_runs p
                    WHERE p.source=r.source AND p.epoch=r.epoch AND p.run_id=r.run_id
                )
                ORDER BY r.finished, r.source, r.run_id LIMIT ?
            """, (*jobs, 50-len(pending))).fetchall()
            for row in rows:
                run = dict(row)
                key = (run['source'], run['epoch'], run['run_id'])
                items = {key: [dict(item) for item in self.db.execute(
                    'SELECT item_id,status,message FROM items WHERE source=? AND epoch=? AND run_id=?', key
                )]}
                identifier = str(uuid.uuid4())
                body = format_report([run], items, [], 'job-failure', labels)
                if reserve:
                    now = utc()
                    self.db.execute("INSERT INTO reports VALUES(?,'job-failure',?,?)", (identifier, now, body))
                    self.db.execute('INSERT INTO report_runs VALUES(?,?,?,?)', (identifier, *key))
                    self.db.executemany('INSERT INTO deliveries VALUES(?,?,?,0,0,?)',
                                        [(identifier, channel, 'pending', now) for channel in dict.fromkeys(channels)])
                pending.append({'id':identifier, 'body':body})
            return pending

    def report(self,category='general',run_id=None,reserve=True,labels=None,channels=None,separate_failures=()):
        from job_report import format_report,legacy_health,clean_legacy_body
        if channels is not None and (not isinstance(channels,(list,tuple)) or any(channel not in ('mail','telegram') for channel in channels)):
            raise ValueError('Invalid report channels')
        def prepare_channels(identifier):
            # Persist every intended channel in the same transaction as report
            # reservation, before any external delivery can be acknowledged.
            if reserve:
                self.db.executemany('INSERT OR IGNORE INTO deliveries VALUES(?,?,?,0,0,?)',
                                    [(identifier,channel,'pending',utc()) for channel in (channels or [])])
        cats=('general','ansible') if category=='general' else (category,)
        with self.transaction():
            pending=self.db.execute("SELECT p.id,p.body FROM reports p WHERE p.category=? AND (NOT EXISTS(SELECT 1 FROM deliveries d WHERE d.report_id=p.id) OR EXISTS(SELECT 1 FROM deliveries d WHERE d.report_id=p.id AND d.status!='sent')) ORDER BY p.created LIMIT 1",(category,)).fetchone()
            if pending:
                report=dict(pending)
                rows=[dict(r) for r in self.db.execute('SELECT r.* FROM runs r JOIN report_runs p ON p.source=r.source AND p.epoch=r.epoch AND p.run_id=r.run_id WHERE p.report_id=? ORDER BY r.started',(report['id'],))]
                health=[dict(r) for r in self.db.execute('SELECT source,status,message FROM report_health WHERE report_id=?',(report['id'],))]
                if report['body'].startswith('📋') or report['body'].startswith('📦'):
                    health=health or legacy_health(report['body'])
                if rows or health:
                    items={}
                    for row in rows:
                        key=(row['source'],row['epoch'],row['run_id'])
                        items[key]=[dict(r) for r in self.db.execute('SELECT item_id,status,message FROM items WHERE source=? AND epoch=? AND run_id=?',key)]
                    report['body']=format_report(rows,items,health,category,labels)
                else:report['body']=clean_legacy_body(report['body'])
                if reserve:self.db.execute('UPDATE reports SET body=? WHERE id=?',(report['body'],report['id']))
                prepare_channels(report['id'])
                return report
            params=list(cats);where='r.category IN ('+','.join('?'*len(cats))+') AND r.status!=?';params.append('running')
            separate_failures = self._failure_job_names(separate_failures)
            if category == 'general' and separate_failures:
                placeholders = ','.join('?' for _ in separate_failures)
                where += f" AND NOT (r.category='general' AND r.status='failed' AND r.job IN ({placeholders}))"
                params.extend(separate_failures)
            # Service snapshots remain queryable, but healthy/optional inactive
            # units are not completed jobs. Use their recorded provenance, not
            # unit/job names (profiles may assign arbitrary observation names).
            where += """ AND NOT (
                r.status IN ('success','skipped')
                AND EXISTS(SELECT 1 FROM run_observations o WHERE o.source=r.source
                    AND o.epoch=r.epoch AND o.run_id=r.run_id AND o.kind='systemd')
                AND NOT EXISTS(SELECT 1 FROM items i WHERE i.source=r.source
                    AND i.epoch=r.epoch AND i.run_id=r.run_id AND i.status IN ('failed','warning'))
            )"""
            if run_id:where+=' AND r.run_id=?';params.append(run_id)
            rows=[dict(r) for r in self.db.execute('SELECT r.* FROM runs r WHERE '+where+' AND NOT EXISTS(SELECT 1 FROM report_runs p WHERE p.source=r.source AND p.epoch=r.epoch AND p.run_id=r.run_id) ORDER BY r.started LIMIT 2001',params)]
            health=[dict(r) for r in self.db.execute("SELECT h.source,h.status FROM collection_health h LEFT JOIN meta m ON m.key='health_category:'||h.source WHERE h.status!='ok' AND COALESCE(m.value,'general')=? ORDER BY h.source",(category,))]
            if len(rows)>2000:
                rows=rows[:2000]
                health.append({'source':'controller:reports','status':'backlog-remains'})
            fingerprint=json.dumps(health,sort_keys=True)
            health_key='health_report:'+category
            prior=self.db.execute('SELECT value FROM meta WHERE key=?',(health_key,)).fetchone()
            if not rows and not health:
                if reserve:self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',(health_key,fingerprint))
                return None
            if not rows and prior and prior[0]==fingerprint:return None
            if reserve:self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',(health_key,fingerprint))
            identifier=str(uuid.uuid4());items={}
            for row in rows:
                key=(row['source'],row['epoch'],row['run_id'])
                items[key]=[dict(r) for r in self.db.execute('SELECT item_id,status,message FROM items WHERE source=? AND epoch=? AND run_id=?',key)]
            body=format_report(rows,items,health,category,labels)
            if not reserve:return {'id':identifier,'body':body}
            self.db.execute('INSERT INTO reports VALUES(?,?,?,?)',(identifier,category,utc(),body))
            for row in rows:self.db.execute('INSERT INTO report_runs VALUES(?,?,?,?)',(identifier,row['source'],row['epoch'],row['run_id']))
            for state in health:self.db.execute('INSERT INTO report_health VALUES(?,?,?,?)',(identifier,state['source'],state['status'],state.get('message','')))
            prepare_channels(identifier)
            return {'id':identifier,'body':body}
    def claim(self,report,channel):
        with self.transaction():
            self.db.execute('INSERT OR IGNORE INTO deliveries VALUES(?,?,?,0,0,?)',(report,channel,'pending',utc()))
            result=self.db.execute("UPDATE deliveries SET status='sending',attempts=attempts+1,lease_until=?,updated=? WHERE report_id=? AND channel=? AND status!='sent' AND lease_until<?",(utc()+300,utc(),report,channel,utc()))
            return result.rowcount==1
    def delivered(self,report,channel,ok):
        with self.transaction():self.db.execute('UPDATE deliveries SET status=?,lease_until=0,updated=? WHERE report_id=? AND channel=?',('sent' if ok else 'pending',utc(),report,channel))


class Systemd:
    """Explicit profile-based service observations; no unit/script-file discovery."""
    import subprocess
    UNIT = re.compile(r'[A-Za-z0-9_][A-Za-z0-9_.:@\\-]*\.service\Z')
    PROPERTIES = ('LoadState', 'ActiveState', 'SubState', 'Type', 'Result',
                  'ExecMainCode', 'ExecMainStatus', 'ExecMainStartTimestampMonotonic',
                  'ExecMainExitTimestampMonotonic')


    @classmethod
    def normalize(cls, entries):
        if not isinstance(entries, list) or len(entries) > 128:
            raise ValueError('Expected at most 128 explicit systemd bindings')
        result = []
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) - {'unit', 'mode', 'name'}:
                raise ValueError('Invalid systemd binding fields')
            unit = entry.get('unit')
            if not isinstance(unit, str) or not cls.UNIT.fullmatch(unit) or '@.service' in unit:
                raise ValueError('Explicit system service instance required')
            mode = entry.get('mode')
            if mode not in ('active', 'oneshot', 'observe'):
                raise ValueError('Explicit systemd observation mode required')
            name = entry.get('name', 'systemd:' + unit[:-8].replace('@', ':').replace('\\', ':'))
            if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}', name):
                raise ValueError('Invalid observation job name')
            result.append({'unit': unit, 'mode': mode, 'name': name})
        if len({row['unit'] for row in result}) != len(result) or len({row['name'] for row in result}) != len(result):
            raise ValueError('Duplicate systemd binding')
        return result


    @classmethod
    def resolve_profiles(cls, profiles, selected):
        if not isinstance(profiles, dict) or not isinstance(selected, list):
            raise ValueError('Systemd profiles require an object and explicit selection list')
        if any(not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', name)
               for name in profiles):
            raise ValueError('Invalid systemd profile name')
        if any(not isinstance(name, str) or name not in profiles for name in selected) or len(set(selected)) != len(selected):
            raise ValueError('Unknown or duplicate selected systemd profile')
        entries = []
        for name in selected:
            profile = profiles[name]
            if isinstance(profile, dict):
                services = profile.get('services')
                if not isinstance(services, list):raise ValueError('Explicit profile services required')
                profile = [{key: row[key] for key in ('unit', 'mode', 'name') if key in row} for row in services if isinstance(row, dict)]
                if len(profile) != len(services):raise ValueError('Invalid profile service')
            entries.extend(cls.normalize(profile))
        return cls.normalize(entries)


    @classmethod
    def load(cls, path):
        path = Path(path)
        if path.is_symlink() or path.stat().st_mode & 0o077:
            raise ValueError('Private systemd binding file required')
        return cls.normalize(json.loads(path.read_text(encoding='utf8')))


    @classmethod
    def assess(cls, binding, properties):
        """Interpret only enumerated states and numeric fields; no raw text escapes."""
        mode = binding['mode']
        load_state = properties.get('LoadState')
        active = properties.get('ActiveState')
        result = properties.get('Result')
        if load_state != 'loaded':
            return 'failed', 'Systemd-Dienst fehlt oder konnte nicht geladen werden.'
        if active == 'failed' or result not in ('success', ''):
            reasons = {'timeout': 'Zeitlimit erreicht.', 'start-limit-hit': 'Neustartlimit erreicht.',
                       'watchdog': 'Watchdog hat einen Fehler erkannt.', 'oom-kill': 'Prozess wegen Speichermangel beendet.',
                       'exit-code': 'Dienstprozess mit Fehler beendet.', 'signal': 'Dienstprozess durch Signal beendet.',
                       'core-dump': 'Dienstprozess abgestuerzt.'}
            message = reasons.get(result, 'Systemd meldet einen Dienstfehler; lokales Dienstprotokoll pruefen.')
            code = properties.get('ExecMainStatus', '')
            if properties.get('ExecMainCode') == '1' and re.fullmatch(r'[0-9]{1,5}', code) and int(code):
                message += ' Prozess-Exitstatus: ' + str(int(code)) + '.'
            return 'failed', message
        if active in ('activating', 'deactivating', 'reloading', 'refreshing'):
            return 'warning', 'Systemd-Dienst befindet sich im Zustandswechsel.'
        if mode == 'oneshot':
            if properties.get('Type') != 'oneshot':
                return 'failed', 'Konfigurierte Oneshot-Zuordnung passt nicht zum Diensttyp.'
            def number(key):
                value = properties.get(key, '')
                return int(value) if re.fullmatch(r'[0-9]{1,20}', value) else None
            start = number('ExecMainStartTimestampMonotonic')
            end = number('ExecMainExitTimestampMonotonic')
            if start == 0 and active == 'inactive':
                return 'skipped', 'In diesem Boot noch kein Oneshot-Lauf beobachtet.'
            if start is not None and start > 0 and end is not None and end >= start and number('ExecMainCode') == 1 and number('ExecMainStatus') == 0 and result == 'success' and active in ('active', 'inactive'):
                return 'success', 'Letzter von systemd gespeicherter Oneshot-Abschluss erfolgreich.'
            return 'warning', 'Kein eindeutiger erfolgreicher Oneshot-Abschluss vorhanden.'
        if active == 'active' and result == 'success':
            return 'success', 'Systemd-Dienst zum Abfragezeitpunkt aktiv.'
        if active == 'inactive':
            if mode == 'observe':
                return 'skipped', 'Systemd-Dienst inaktiv; keine Dauerlaufpflicht konfiguriert.'
            return 'failed', 'Erwarteter dauerhaft aktiver Systemd-Dienst ist inaktiv.'
        return 'warning', 'Systemd-Dienstzustand nicht eindeutig auswertbar.'


    @classmethod
    def observe(cls, entries):
        entries = cls.normalize(entries)
        rows = []
        env = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'SYSTEMD_PAGER': ''}
        for entry in entries:
            try:
                completed = cls.subprocess.run(['/usr/bin/systemctl', '--no-pager', 'show', entry['unit'],
                                            '--property=' + ','.join(cls.PROPERTIES)],
                                           capture_output=True, text=True, timeout=10, env=env)
                if completed.returncode:
                    raise ValueError('Status query failed')
                properties = {key: value for line in completed.stdout.splitlines()
                              for key, sep, value in [line.partition('=')]
                              if sep and key in cls.PROPERTIES}
                status, summary = cls.assess(entry, properties)
            except (OSError, ValueError, cls.subprocess.TimeoutExpired):
                status, summary = 'failed', 'Systemd-Status konnte nicht abgefragt werden.'
            rows.append({**entry, 'status': status, 'summary': summary})
        return rows


    @classmethod
    def record(cls, store, entries, sample):
        """One atomic observation per job/sample, including repeated export pages."""
        sample = str(uuid.UUID(sample))
        rows = cls.observe(entries)
        now = utc()
        with store.transaction():
            for row in rows:
                run = str(uuid.uuid5(uuid.UUID(store.epoch), sample + ':' + row['name']))
                key = store._key(run)
                if store.db.execute('SELECT 1 FROM runs WHERE source=? AND epoch=? AND run_id=?', key).fetchone():
                    continue
                store.db.execute('INSERT INTO runs(source,epoch,run_id,job,category,status,started,activity,finished,exit_code,summary,duration_seconds) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
                                 (*key, row['name'], 'general', row['status'], now, now, now,
                                  1 if row['status'] == 'failed' else 0, row['summary'], 0))
                store.db.execute('INSERT INTO run_observations VALUES(?,?,?,?)', (*key, 'systemd'))
                store._event(run, 'systemd-observation')
        store.prune(90)
        return rows
