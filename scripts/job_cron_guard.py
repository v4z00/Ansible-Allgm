#!/usr/bin/env python3
"""Reject duplicate cron jobs; migrate only an explicitly supplied exact command."""
import argparse
import fcntl
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

def plan(text,name,script,legacy=None):
    lines=text.splitlines(keepends=True);matches=[];managed=False;tag='#Ansible: script-jobs:'+name
    for index,line in enumerate(lines):
        stripped=line.strip()
        if stripped.startswith('#'):
            managed=stripped==tag;continue
        if not stripped:continue
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*=',stripped):continue
        parts=stripped.split(None,1) if stripped.startswith('@') else stripped.split(None,5)
        command=parts[-1] if len(parts)==(2 if stripped.startswith('@') else 6) else ''
        if managed:managed=False;continue
        if re.search(r'(?<![A-Za-z0-9_.-])'+re.escape(script)+r'(?![A-Za-z0-9_.-])',command):
            if legacy is None or command!=legacy:raise ValueError('Unmanaged conflicting cron invocation; review and supply exact legacy command')
            matches.append(index)
    if len(matches)>1:raise ValueError('Multiple legacy invocations require manual review')
    return ''.join(line for i,line in enumerate(lines) if i not in matches),len(matches)

def validate_schedule(value):
    if not isinstance(value,dict):raise ValueError('Cron mapping required')
    if value.get('special_time'):
        if value['special_time'] not in ('reboot','hourly','daily','weekly','monthly','yearly','annually'):raise ValueError('Invalid special time')
        if any(k in value for k in ('minute','hour','day','month','weekday')):raise ValueError('Special time cannot be combined with calendar fields')
        return
    definitions={'minute':(0,59,{}),'hour':(0,23,{}),'day':(1,31,{}),'month':(1,12,{n:i+1 for i,n in enumerate(('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'))}),'weekday':(0,7,{n:i for i,n in enumerate(('sun','mon','tue','wed','thu','fri','sat'))})}
    for key,(low,high,aliases) in definitions.items():
        expression=str(value.get(key,'*')).lower()
        for part in expression.split(','):
            base,*step=part.split('/')
            if len(step)>1 or step and (not step[0].isdigit() or int(step[0])<1):raise ValueError('Invalid Cron step')
            if base=='*':continue
            bounds=base.split('-')
            if len(bounds)>2:raise ValueError('Invalid Cron range')
            numbers=[]
            for bound in bounds:
                if bound in aliases:n=aliases[bound]
                elif bound.isdigit():n=int(bound)
                else:raise ValueError('Invalid Cron field')
                if not low<=n<=high:raise ValueError('Cron field outside range')
                numbers.append(n)
            if len(numbers)==2 and numbers[0]>numbers[1]:raise ValueError('Invalid Cron range order')

def main():
    p=argparse.ArgumentParser();p.add_argument('--user',required=True);p.add_argument('--name',required=True);p.add_argument('--script',required=True);p.add_argument('--legacy');p.add_argument('--remove-legacy',action='store_true');p.add_argument('--schedule-json');a=p.parse_args()
    if a.schedule_json:
        import json
        validate_schedule(json.loads(a.schedule_json))
    if not re.fullmatch(r'[A-Za-z0-9_.-]+',a.user):raise ValueError('Invalid user')
    def read():
        result=subprocess.run(['crontab','-u',a.user,'-l'],capture_output=True,text=True)
        if result.returncode and 'no crontab' not in result.stderr.lower():raise ValueError('Cannot inspect crontab')
        return result.stdout
    # Refuse an in-place code/Cron switch while this exact script is executing.
    proc=Path('/proc')
    if proc.is_dir():
        for entry in proc.iterdir():
            if not entry.name.isdigit() or int(entry.name)==os.getpid():continue
            try:
                argv=(entry/'cmdline').read_bytes().split(b'\0')
                candidates=argv[:2]
                if any(Path(x.decode(errors='replace')).name==a.script for x in candidates):
                    raise RuntimeError('Target job is currently running')
            except (FileNotFoundError,PermissionError,ProcessLookupError):continue
    # System crontabs/periodic jobs are outside this managed user-crontab migration.
    # Refuse a duplicate rather than modifying a foreign schedule.
    references=[]
    system=[Path('/etc/crontab')]+list(Path('/etc/cron.d').glob('*'))
    pattern=re.compile(r'(?<![A-Za-z0-9_.-])'+re.escape(a.script)+r'(?![A-Za-z0-9_.-])')
    for file in system:
        if not file.is_file():continue
        for line in file.read_text(errors='replace').splitlines():
            if line.strip() and not line.lstrip().startswith('#') and pattern.search(line):references.append(file)
    for directory in ('/etc/cron.hourly','/etc/cron.daily','/etc/cron.weekly','/etc/cron.monthly'):
        for file in Path(directory).glob('*'):
            if file.is_file() and (file.name==a.script or pattern.search(file.read_text(errors='replace'))):references.append(file)
    if references:raise ValueError('Conflicting system Cron invocation requires explicit separate migration')
    lock=Path('/tmp')/('script-cron-'+str(os.getuid())+'-'+hashlib.sha256(a.user.encode()).hexdigest()+'.lock')
    descriptor=os.open(str(lock),os.O_CREAT|os.O_RDWR|getattr(os,'O_NOFOLLOW',0),0o600)
    if os.fstat(descriptor).st_uid!=os.geteuid():os.close(descriptor);raise ValueError('Cron lock owner mismatch')
    with os.fdopen(descriptor,'w') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        text=read();new,count=plan(text,a.name,a.script,a.legacy)
        if a.remove_legacy and count:
            if read()!=text:raise ValueError('Crontab changed during review')
            subprocess.run(['crontab','-u',a.user,'-'],input=new,text=True,check=True)
        print('Legacy entries matched: '+str(count))
if __name__=='__main__':
    try:main()
    except Exception:print('Cron conflict or inspection error; no blind overwrite performed.',file=sys.stderr);sys.exit(1)
