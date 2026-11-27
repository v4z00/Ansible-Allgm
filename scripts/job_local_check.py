#!/usr/bin/env python3
"""Read-only Checkmk local checks for selected jobs and the security outbox."""
import argparse
import json
from pathlib import Path
import re
import sqlite3
import time
import urllib.parse


def check_job(row,entry,now):
    if row is None:return 3,'No recorded run'
    status=row['status']
    if status=='running':
        overdue=now-float(row['started'])>entry['max_runtime_seconds']
        return (2,'Runtime exceeded') if overdue else (0,'Running')
    if now-float(row['finished'] or row['started'])>entry['max_age_seconds']:return 2,'Result overdue'
    return {'success':(0,'Completed'),'warning':(1,'Job warning'),'failed':(2,'Job failed'),'skipped':(0,'Skipped')}.get(status,(3,'Invalid stored state'))


def normalize(entries):
    if not isinstance(entries,list) or len(entries)>128:raise ValueError('At most 128 selected jobs required')
    result=[]
    for entry in entries:
        if not isinstance(entry,dict) or set(entry)-{'job','max_age_seconds','max_runtime_seconds'}:raise ValueError('Invalid check fields')
        if not re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',str(entry.get('job',''))):raise ValueError('Invalid check job')
        for key in ('max_age_seconds','max_runtime_seconds'):
            if not isinstance(entry.get(key),int) or isinstance(entry[key],bool) or entry[key]<1:raise ValueError('Explicit positive check thresholds required')
        result.append(entry)
    if len({entry['job'] for entry in result})!=len(result):raise ValueError('Duplicate check jobs')
    return result


def checks(config,now=None):
    entries=normalize(config.get('jobs',[]));now=time.time() if now is None else now
    path=Path(config['database']).absolute()
    # mode=ro prevents a missing database from being silently created.
    connection=sqlite3.connect('file:'+urllib.parse.quote(str(path))+'?mode=ro',uri=True,timeout=5)
    connection.row_factory=sqlite3.Row
    try:
        for entry in entries:
            row=connection.execute('SELECT * FROM runs WHERE job=? ORDER BY started DESC,rowid DESC LIMIT 1',(entry['job'],)).fetchone()
            state,message=check_job(row,entry,now)
            yield '%d "Script job %s" - %s'%(state,entry['job'],message)
        if config.get('security_outbox',False):
            pending=connection.execute("SELECT COUNT(*) FROM deliveries d JOIN reports p ON p.id=d.report_id WHERE p.category='security' AND d.status!='sent'").fetchone()[0]
            yield '%d "Script security delivery" pending=%d %s'%(2 if pending else 0,pending,'Notifications pending' if pending else 'Queue empty')
    finally:connection.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--config',type=Path,required=True);args=parser.parse_args()
    try:
        config=json.loads(args.config.read_text());lines=list(checks(config))
    except (OSError,ValueError,KeyError,sqlite3.Error):
        print('3 "Script jobs data" - Configuration or local database unavailable');return 0
    print('\n'.join(lines));return 0


if __name__=='__main__':raise SystemExit(main())
