#!/usr/bin/env python3
"""Controller queries over Ansible's inventory/connection/become machinery."""
import argparse
import json
import os
from pathlib import Path, PureWindowsPath
import shutil
import subprocess
import sys
import tempfile
import uuid

from controller_i18n import cli_args, tr
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'artifacts/script-library/lib/python'))
from job_store import Store

PLAY='''- name: Read local host job events without executing jobs
  hosts: "{{ job_targets }}"
  gather_facts: false
  become: "{{ not job_is_windows }}"
  become_user: "{{ script_jobs_owner | default('root') }}"
  vars:
    job_is_windows: "{{ ansible_connection | default('ssh') in ['winrm','psrp'] or inventory_hostname in groups.get('all_windows_systems', []) }}"
  tasks:
    - name: Verify Windows authentication prerequisites
      ansible.builtin.include_role:
        name: windows_connection_guard
      when: job_is_windows
    - name: Observe explicitly configured systemd services without running jobs
      ansible.builtin.command:
        argv: "{{ [script_jobs_python | default('/usr/bin/python3'), job_source_overrides.get(inventory_hostname, {}).get('root', script_jobs_target_root | default(script_path | default('/scripte'))) ~ '/bin/script-jobs', '--db', job_source_overrides.get(inventory_hostname, {}).get('database', script_jobs_database_path | default('/var/lib/script-jobs/jobs.sqlite3')), 'systemd-record', '--config', (job_source_overrides.get(inventory_hostname, {}).get('database', script_jobs_database_path | default('/var/lib/script-jobs/jobs.sqlite3'))) | dirname ~ '/systemd.json', '--sample', job_systemd_sample, '--expect-profiles', ({'profiles': script_jobs_systemd_profiles | default({}), 'selected': script_jobs_systemd_selected_profiles} | to_json)] }}"
      when: not job_is_windows and script_jobs_systemd_selected_profiles | default([]) | length > 0
      register: job_systemd_query
      changed_when: false
      ignore_errors: true
      ignore_unreachable: true
      no_log: true
    - name: Query existing local SQLite helper
      ansible.builtin.command:
        argv: "{{ [script_jobs_python | default('/usr/bin/python3'), job_source_overrides.get(inventory_hostname, {}).get('root', script_jobs_target_root | default(script_path | default('/scripte'))) ~ '/bin/script-jobs', '--db', job_source_overrides.get(inventory_hostname, {}).get('database', script_jobs_database_path | default('/var/lib/script-jobs/jobs.sqlite3')), 'export', '--after', (job_cursors.get(inventory_hostname, {}).get('last_id', 0) | string), '--limit', '100'] + (['--epoch', job_cursors[inventory_hostname]['epoch']] if job_cursors.get(inventory_hostname, {}).get('epoch') else []) }}"
      register: job_query
      when: not job_is_windows
      changed_when: false
      ignore_errors: true
      ignore_unreachable: true
      no_log: true
    - name: Refuse stale results after a failed systemd observation
      ansible.builtin.set_fact:
        job_query: "{{ job_query | combine({'rc': 1}) }}"
      when: not job_is_windows and not (job_systemd_query.skipped | default(false)) and job_systemd_query.rc | default(255) != 0
      no_log: true
    - name: Read Windows SQLite events through the local PowerShell library
      ansible.windows.win_powershell:
        depth: 10
        script: |
          param([string]$Root, [string]$Database, [string]$Sqlite, [long]$After, [string]$Epoch)
          $ErrorActionPreference = 'Stop'
          $Ansible.Changed = $false
          Import-Module (Join-Path $Root 'lib/ScriptLibrary.psm1') -DisableNameChecking
          $store = Open-JobStore -Database $Database -Sqlite $Sqlite
          $Ansible.Result = Export-JobEvents -Store $store -After $After -Epoch $Epoch -Limit 100
        parameters:
          Root: "{{ job_source_overrides.get(inventory_hostname, {}).get('root', windows_script_root | default('C:\\\\Scripte')) }}"
          Database: "{{ job_source_overrides.get(inventory_hostname, {}).get('database', windows_job_database | default('C:\\\\ProgramData\\\\ScriptJobs\\\\jobs.sqlite3')) }}"
          Sqlite: "{{ windows_sqlite_exe | default(job_source_overrides.get(inventory_hostname, {}).get('root', windows_script_root | default('C:\\\\Scripte')) ~ '\\\\runtime\\\\sqlite3.exe') }}"
          After: "{{ job_cursors.get(inventory_hostname, {}).get('last_id', 0) }}"
          Epoch: "{{ job_cursors.get(inventory_hostname, {}).get('epoch', '') }}"
      become: false
      when: job_is_windows
      register: windows_job_query
      ignore_errors: true
      ignore_unreachable: true
      no_log: true
    - name: Normalize the Windows result for the common importer
      ansible.builtin.set_fact:
        job_query:
          rc: "{{ 0 if not windows_job_query.failed | default(false) and not windows_job_query.unreachable | default(false) else 1 }}"
          unreachable: "{{ windows_job_query.unreachable | default(false) }}"
          stdout: "{{ windows_job_query.result | default({}) | to_json }}"
      when: job_is_windows
      no_log: true
    - name: Transfer only structured job data to temporary local spool
      ansible.builtin.copy:
        content: "{{ {'host': inventory_hostname, 'ok': (job_query.rc | default(255) == 0), 'unreachable': job_query.unreachable | default(false), 'data': (job_query.stdout | from_json if job_query.rc | default(255) == 0 else none)} | to_json }}"
        dest: "{{ job_spool }}/{{ inventory_hostname | hash('sha256') }}.json"
        mode: '0600'
      delegate_to: localhost
      become: false
      vars:
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
        ansible_become: false
      no_log: true
'''

def transport(project,limit,cursors,inventory=None,source_overrides=None,systemd_sample=None):
    if not limit:raise ValueError(tr('jobs.limit'))
    if not (project/'ansible.cfg').is_file():raise ValueError(tr('jobs.config_required'))
    binary=shutil.which('ansible-playbook')
    if not binary:
        binary=next((str(p) for p in (project/'.venv/bin/ansible-playbook',project/'venv/bin/ansible-playbook') if p.is_file()),None)
    if not binary:raise ValueError(tr('jobs.environment'))
    with tempfile.TemporaryDirectory(prefix='job-query-') as tmp:
        stage=Path(tmp);spool=stage/'spool';spool.mkdir(mode=0o700)
        for name in ('group_vars','host_vars'):
            if (project/name).exists():(stage/name).symlink_to(project/name,target_is_directory=True)
        (stage/'query.yml').write_text(PLAY)
        (stage/'params.json').write_text(json.dumps({'job_targets':limit,'job_cursors':cursors,'job_spool':str(spool),'job_source_overrides':source_overrides or {},'job_systemd_sample':systemd_sample or str(uuid.uuid4())}))
        env=os.environ.copy();env.update(ANSIBLE_CONFIG=str(project/'ansible.cfg'),ANSIBLE_VERBOSITY='0',ANSIBLE_DEBUG='0',ANSIBLE_NOCOLOR='1')
        # Do not recursively record this internal collection as an Ansible job.
        env['SCRIPT_JOBS_CALLBACK']='0'
        command=[binary,str(stage/'query.yml'),'--limit',limit,'-e','@'+str(stage/'params.json')]
        if inventory:command+=['-i',inventory]
        result=subprocess.run(command,cwd=str(project),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
        if result.returncode!=0:raise ValueError('Ansible collection did not complete; partial spool refused')
        records=[]
        for file in spool.glob('*.json'):
            if file.stat().st_size>20*1024*1024:raise ValueError(tr('jobs.response_size'))
            records.append(json.loads(file.read_text()))
        if not records:raise ValueError(tr('jobs.no_results'))
        return records


def collect(store,project,limit,inventory=None,source_overrides=None):
    output=[];systemd_sample=str(uuid.uuid4())
    for page in range(20):
        cursors={r['source']:dict(r) for r in store.db.execute('SELECT source,epoch,last_id FROM cursors')}
        try:records=transport(project,limit,cursors,inventory,source_overrides,systemd_sample)
        except Exception:
            store.health('controller:collection','query-failed')
            return output+[{'host':'controller:collection','status':'query-failed'}]
        store.health('controller:collection','ok');more=False
        for record in records:
            host=record['host']
            if not record['ok']:
                state='unreachable' if record.get('unreachable') else 'not-attached-or-query-failed'
                store.health(host,state);output.append({'host':host,'status':state});continue
            try:
                store.ingest(host,record['data'])
                from job_expectations import evaluate
                rows=[dict(r) for r in store.db.execute('SELECT * FROM runs WHERE source=?',(host,))]
                expected_keys=set()
                for expected in record['data'].get('expectations',[]):
                    key=host+'/'+expected['job'];expected_keys.add(key)
                    try:state=evaluate(expected,rows)
                    except (ValueError,KeyError):state='schedule-unconfigured'
                    store.health(key,state,category=expected.get('category','vzdump' if expected['job'].startswith('vzdump') else 'general'))
                for previous in store.db.execute('SELECT source FROM collection_health').fetchall():
                    if previous[0].startswith(host+'/') and previous[0] not in expected_keys:store.health(previous[0],'ok')
                output.append({'host':host,'status':'ok','events':record['data']['events'],'cursor':record['data']['next']})
                more=more or len(record['data']['events'])>=100
            except ValueError:
                store.health(host,'gap-or-schema-error');output.append({'host':host,'status':'gap-or-schema-error'})
        if not more:return output
    store.health('controller:collection','backlog-remains')
    return output+[{'host':'controller:collection','status':'backlog-remains'}]


def table(rows):
    icons={'success':'✅','failed':'❌','warning':'⚠️','skipped':'⏭️','running':'⏳'}
    for row in rows:
        print('%s %s %-20s %-28s %s %s'%(icons.get(row['status'],'⚠️'),time.strftime('%d.%m %H:%M',time.localtime(row['started'])),row['source'],row['job'],row['status'],row['run_id']))
    if not rows:print(tr('jobs.no_rows'))


def show_live(records,machine=False):
    symbols={'success':'✅','failed':'❌','warning':'⚠️','skipped':'⏭️','running':'⏳'}
    for record in records:
        if record['status']!='ok':
            data={'schema':1,'type':'host_status','host':record['host'],'status':record['status']}
            print(json.dumps(data) if machine else '🚫 '+record['host']+': '+record['status'],flush=True);continue
        for event in record['events']:
            data={'schema':1,'type':'event','host':record['host'],**event}
            if machine:print(json.dumps(data,ensure_ascii=False),flush=True)
            else:
                run=event['payload']['run']
                print('%s %s / %s [%s] %s'%(symbols.get(run['status'],'⚠️'),record['host'],run['job'],event['kind'],run['summary']),flush=True)
        if machine:print(json.dumps({'schema':1,'type':'heartbeat','host':record['host'],'cursor':record['cursor']}),flush=True)

def main():
    os.umask(0o077)
    argv=cli_args(sys.argv[1:], root=ROOT)
    p=argparse.ArgumentParser(description=tr("jobs.help"))
    p.add_argument('--project',type=Path,default=ROOT);p.add_argument('--db');p.add_argument('--config',type=Path)
    p.add_argument('--inventory');p.add_argument('--limit');p.add_argument('--json',action='store_true')
    p.add_argument('view',choices=['menu','collect','live','runs','latest','running','errors','details','reports','reset-cursor'],nargs='?',default='menu')
    p.add_argument('--job');p.add_argument('--run');p.add_argument('--source');p.add_argument('--since',type=float);p.add_argument('--until',type=float);p.add_argument('--item');p.add_argument('--seconds',type=int,default=60)
    a=p.parse_args(argv)
    if a.view=='latest' and any(value is not None for value in (a.since,a.until,a.item)):
        p.error(tr('jobs.latest_filter'))
    configuration=a.config or a.project/'config/script_jobs_controller.json'
    if a.config and not configuration.is_file():raise ValueError(tr('jobs.config_missing'))
    settings=json.loads(configuration.read_text()) if configuration.is_file() else {}
    if a.db is None:a.db=settings.get('database',os.environ.get('SCRIPT_JOBS_CONTROLLER_DB','/var/lib/script-jobs/controller.sqlite3'))
    source_overrides=settings.get('source_overrides',{})
    if not isinstance(source_overrides,dict):raise ValueError(tr('jobs.source_overrides'))
    for host,value in source_overrides.items():
        if not isinstance(value,dict) or set(value)-{'root','database'}:raise ValueError(tr('jobs.source_keys'))
        for path in value.values():
            windows=PureWindowsPath(path) if isinstance(path,str) else None
            absolute=isinstance(path,str) and (path.startswith('/') or bool(windows.drive and windows.root and not windows.drive.startswith('\\\\')))
            if not absolute or any(c in path for c in '\r\n') or '..' in Path(path).parts or '..' in windows.parts:raise ValueError(tr('jobs.absolute_paths'))
    store=Store(a.db)
    try:
        view=a.view
        if view=='menu':
            while True:
                print(tr('jobs.menu'))
                choice=input(tr('jobs.choice')).strip()
                if choice=='0':return 0
                if choice=='1':table(store.runs(status='running'))
                elif choice=='2':table(store.latest())
                elif choice=='3':table([r for r in store.runs(limit=1000) if r['status'] in ('failed','warning')])
                elif choice=='4':print(json.dumps(store.details(input(tr('jobs.run_id')).strip()),ensure_ascii=False,indent=2))
                elif choice=='6':
                    print(json.dumps([dict(r) for r in store.db.execute('SELECT p.id,p.category,d.channel,d.status,d.attempts FROM reports p LEFT JOIN deliveries d ON p.id=d.report_id ORDER BY p.created DESC LIMIT 100')],ensure_ascii=False,indent=2))
                elif choice in ('5','7'):
                    target=a.limit or input(tr('jobs.inventory')).strip()
                    if not target:continue
                    until=time.monotonic()+(60 if choice=='5' else 0)
                    while True:
                        show_live(collect(store,a.project,target,a.inventory,source_overrides),a.json)
                        if time.monotonic()>=until:break
                        time.sleep(2)
        elif view in ('collect','live'):
            if not a.limit:p.error(tr('jobs.remote_limit'))
            end=time.monotonic()+(max(0,min(a.seconds,3600)) if view=='live' else 0)
            while True:
                result=collect(store,a.project,a.limit,a.inventory,source_overrides)
                if view=='live':show_live(result,a.json)
                else:print(json.dumps(result,ensure_ascii=False),flush=True)
                if time.monotonic()>=end:return 0 if all(x['status']=='ok' for x in result) else 1
                time.sleep(2)
        elif view=='reset-cursor':
            if not a.source:p.error(tr('jobs.source_required'))
            store.reset_cursor(a.source)
        elif view=='details':
            if not a.run:p.error(tr('jobs.run_required'))
            print(json.dumps(store.details(a.run),ensure_ascii=False,indent=2))
        elif view=='reports':print(json.dumps([dict(r) for r in store.db.execute('SELECT * FROM deliveries ORDER BY updated DESC LIMIT 100')],indent=2))
        else:
            rows=store.latest(a.job,source=a.source) if view=='latest' else store.runs(a.job,'running' if view=='running' else None,limit=1000,source=a.source,since=a.since,until=a.until,item=a.item)
            if view=='errors':rows=[r for r in rows if r['status'] in ('failed','warning')]
            if a.source:rows=[r for r in rows if r['source']==a.source]
            if a.json:print(json.dumps(rows,ensure_ascii=False))
            else:table(rows)
        return 0
    finally:store.close()

if __name__=='__main__':
    try:sys.exit(main())
    except KeyboardInterrupt:sys.exit(130)
    except Exception:
        print(tr('jobs.query_error'),file=sys.stderr);sys.exit(1)
