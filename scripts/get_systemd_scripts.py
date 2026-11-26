#!/usr/bin/env python3
"""Standalone, read-only Ansible inventory of custom systemd script services.

Copy this one file outside the controller checkout if desired. Secrets and script
contents are never exported. Exec command arguments are filtered on the host.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

REMOTE = r'''
import datetime,json,os,re,shlex,subprocess,sys,time
from pathlib import Path

PROPERTIES=('Id','FragmentPath','DropInPaths','Type','User','Group','ActiveState',
 'SubState','UnitFileState','Restart','RemainAfterExit','MainPID','ControlPID',
 'Result','TriggeredBy','Triggers','TimersCalendar','TimersMonotonic','WorkingDirectory')
UNIT=re.compile(r'^[A-Za-z0-9_.:@\\-]+\.(?:service|timer)$')
SCRIPT=re.compile(r'/[A-Za-z0-9_.@%/+:-]+\.sh\b')
DENIED=re.compile(r'(?:^|[/_.-])(?:secrets?|credentials?|passwords?|tokens?|\.env)(?:$|[/_.-])',re.I)
ENV={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LANG':'C','LC_ALL':'C','SYSTEMD_PAGER':''}

def command(arguments):
 try:
  result=subprocess.run(['systemctl','--no-pager',*arguments],capture_output=True,text=True,
                        timeout=15,env=ENV)
  return result.returncode,result.stdout if result.returncode==0 else ''
 except (OSError,subprocess.TimeoutExpired):return 1,''

def properties(name):
 # Environment, EnvironmentFiles, credentials, descriptions and raw unit text
 # are deliberately not requested. Commands are queried separately below.
 rc,text=command(['show',name,'--property='+','.join(PROPERTIES)])
 if rc:return None
 allowed=set(PROPERTIES)
 return {key:value for line in text.splitlines() for key,separator,value in [line.partition('=')]
         if separator and key in allowed}

def references(name):
 # Raw Exec* values stay inside this host-side function. Only script paths and
 # command shape leave it. Arguments and environment values are never returned.
 rc,text=command(['show',name,'--property=ExecStart,ExecStartPre,ExecStartPost,ExecStop,ExecStopPost,ExecReload'])
 if rc:return {'query_failed':True,'scripts':[],'start_kind':'review'}
 found=[];kind='review';start_script=None;extra=[]
 for line in text.splitlines():
  key,separator,value=line.partition('=')
  if not separator:continue
  if key!='ExecStart' and value:extra.append(key)
  match=re.fullmatch(r'\{ path=([^;{}]+) ; argv\[\]=([^{}]*?) ; ignore_errors=(?:yes|no) ;[^{}]*\}',value)
  if not match:continue
  try:args=shlex.split(match[2])
  except ValueError:args=[]
  executable=match[1].strip()
  candidate=None;shape='review'
  if args and SCRIPT.fullmatch(executable) and executable==args[0]:
   candidate=executable
   if len(args)==1:shape='direct-script'
  elif len(args)>=2 and executable in ('/bin/sh','/bin/bash','/usr/bin/sh','/usr/bin/bash') and args[0]==executable and SCRIPT.fullmatch(args[1]):
   candidate=args[1]
   if len(args)==2:shape='shell-script'
  # Never search arbitrary arguments for path-looking values: those can be
  # secrets too. Only the executable or the immediate shell script is allowed.
  if candidate and not DENIED.search(candidate):
   found.append({'directive':key,'path':candidate})
   if key=='ExecStart':kind=shape;start_script=candidate if shape!='review' else None
 if start_script and DENIED.search(start_script):kind='review';start_script=None
 return {'scripts':list({(row['directive'],row['path']):row for row in found}.values()),
         'start_kind':kind,'start_script':start_script,'extra_command_directives':extra}

def main():
 started=time.monotonic();roots=json.loads(sys.argv[1]);names=set();errors=[]
 for kind in ('service','timer'):
  rc,text=command(['list-unit-files','--type='+kind,'--no-legend','--plain'])
  if rc:errors.append('list-unit-files:'+kind)
  for line in text.splitlines():
   fields=line.lstrip('● ').split()
   if fields and UNIT.fullmatch(fields[0]):names.add(fields[0])
  # Include loaded template instances. Descriptions never leave this function.
  rc,text=command(['list-units','--all','--type='+kind,'--no-legend','--plain'])
  if rc:errors.append('list-units:'+kind)
  for line in text.splitlines():
   fields=line.lstrip('● ').split()
   if fields and UNIT.fullmatch(fields[0]):names.add(fields[0])
 services={};timers={};total=len(names)
 for name in sorted(names):
  if len(services)+len(timers)>4096 or time.monotonic()-started>120:
   errors.append('query-budget-exceeded');break
  if DENIED.search(name):continue
  data=properties(name)
  if data is None:errors.append('unit-query-failed:'+name);continue
  fragment=data.get('FragmentPath','');drops=data.get('DropInPaths','').split()
  custom=fragment.startswith(('/etc/systemd/','/run/systemd/','/usr/local/lib/systemd/')) or any(p.startswith(('/etc/systemd/','/run/systemd/')) for p in drops) or os.path.lexists('/etc/systemd/system/'+name)
  entry={'unit':name,'custom':custom,'properties':data}
  if name.endswith('.service'):
   entry.update(references(name))
   if entry.get('query_failed'):errors.append('exec-query-failed:'+name)
   matches=[row for row in entry['scripts'] if any(row['path'].startswith(root.rstrip('/')+'/') for root in roots)]
   if custom or matches:services[name]=entry
  else:timers[name]=entry
 selected=[]
 for name,entry in timers.items():
  targets=entry['properties'].get('Triggers','').split()
  if entry['custom'] or any(target in services for target in targets):selected.append(entry)
 # Inactive user managers cannot be inferred from system units. Only list unit
 # filenames here; do not read their contents or any home configuration files.
 user_units=[]
 import pwd
 homes={Path(p.pw_dir) for p in pwd.getpwall() if p.pw_dir.startswith('/')}
 directories=[Path('/etc/systemd/user')]+[home/'.config/systemd/user' for home in homes]
 for directory in directories:
  if directory.is_dir():
   for path in sorted(directory.glob('*')):
    if path.suffix in ('.service','.timer') and not DENIED.search(path.name):user_units.append(str(path))
 result={'schema':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'scope':'system-manager','complete':not errors,'installed_or_loaded_units':total,
         'services':list(services.values()),'timers':selected,'errors':errors,
         'user_unit_files_require_review':user_units,
         'privacy':'no script/config contents, environment values, credentials or command arguments exported',
         'limitations':['User-manager units require separate review; filenames only.',
                        'Complex ExecStart commands require review; no automatic binding.']}
 print(json.dumps(result,ensure_ascii=False))
 return 0 if not errors else 1

if __name__=='__main__':sys.exit(main())
'''

PLAY = '''---
- name: Read custom systemd script bindings without changing units
  hosts: all_linux_systems
  gather_facts: false
  become: true
  tasks:
    - name: Validate the output hostname
      ansible.builtin.assert:
        that: inventory_hostname is match('^[A-Za-z0-9][A-Za-z0-9_.-]*$')
    - name: Query selected systemd properties with host-side filtering
      ansible.builtin.script:
        cmd: "{{ systemd_reader | quote }} {{ ([script_path | default('/scripte'), '/root'] | to_json) | quote }}"
        executable: "{{ script_jobs_python | default('/usr/bin/python3') }}"
      register: systemd_read
      changed_when: false
      failed_when: false
      ignore_unreachable: true
      no_log: true
    - name: Create a private directory per hostname on the controller
      ansible.builtin.file:
        path: "{{ systemd_output }}/{{ inventory_hostname }}"
        state: directory
        mode: '0700'
      delegate_to: localhost
      become: false
      vars:
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
        ansible_become: false
    - name: Save only the filtered systemd observation
      ansible.builtin.copy:
        content: "{{ (systemd_read.stdout | from_json) if (systemd_read.rc | default(255)) in [0,1] else {'schema': 1, 'complete': false, 'errors': ['unreachable-or-query-failed']} }}"
        dest: "{{ systemd_output }}/{{ inventory_hostname }}/systemd.json"
        mode: '0600'
      delegate_to: localhost
      become: false
      vars:
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
        ansible_become: false
      no_log: true
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version='GET_SYSTEMD_SCRIPTS 0.1.0')
    parser.add_argument('--project', type=Path, default=Path('/root/ansible'))
    parser.add_argument('--inventory')
    parser.add_argument('--limit', required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--list-hosts', action='store_true')
    args = parser.parse_args()
    project = args.project.resolve()
    if not (project / 'ansible.cfg').is_file():
        parser.error('Existing controller ansible.cfg required')
    binary = next((str(p) for p in (project / '.venv/bin/ansible-playbook', project / 'venv/bin/ansible-playbook') if p.is_file()), None) or shutil.which('ansible-playbook')
    if not binary:
        parser.error('Existing Ansible environment required')
    os.umask(0o077)
    output = (args.output or Path.cwd() / ('systemd-script-export-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))).resolve()
    if not args.list_hosts:
        output.mkdir(mode=0o700, parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix='get-systemd-scripts-') as temporary:
        stage = Path(temporary)
        for name in ('group_vars', 'host_vars'):
            if (project / name).exists():
                (stage / name).symlink_to(project / name, target_is_directory=True)
        (stage / 'reader.py').write_text(REMOTE)
        (stage / 'playbook.yml').write_text(PLAY)
        (stage / 'vars.json').write_text(json.dumps({'systemd_reader': str(stage / 'reader.py'), 'systemd_output': str(output)}))
        command = [binary, str(stage / 'playbook.yml'), '--limit', args.limit, '-e', '@' + str(stage / 'vars.json')]
        if args.inventory:
            command += ['-i', args.inventory]
        if args.list_hosts:
            command += ['--list-hosts']
        env = dict(os.environ, ANSIBLE_CONFIG=str(project / 'ansible.cfg'), SCRIPT_JOBS_CALLBACK='0', ANSIBLE_NOCOLOR='1')
        result = subprocess.run(command, cwd=project, env=env, capture_output=True, text=True)
        if args.list_hosts:
            # Only inventory host names, never raw Ansible diagnostics.
            import re
            for line in result.stdout.splitlines():
                if re.fullmatch(r'\s{6}[A-Za-z0-9][A-Za-z0-9_.-]*', line):
                    print(line.strip())
            return result.returncode
    complete = result.returncode == 0
    count = 0
    for path in sorted(output.glob('*/systemd.json')):
        data = json.loads(path.read_text())
        complete = complete and data.get('complete', False) and not data.get('user_unit_files_require_review')
        print('%s: %d script/custom services, %d timers, %s' %
              (path.parent.name, len(data.get('services', [])), len(data.get('timers', [])),
               'complete' if data.get('complete') and not data.get('user_unit_files_require_review') else 'review needed'))
        for service in data.get('services', []):
            properties = service['properties']
            scripts = ', '.join(dict.fromkeys(row['path'] for row in service['scripts'])) or '(no exported script reference)'
            print('  %s [%s, %s/%s, %s] -> %s' %
                  (service['unit'], properties.get('Type', '?'), properties.get('ActiveState', '?'),
                   properties.get('UnitFileState', '?'), service['start_kind'], scripts))
        for timer in data.get('timers', []):
            print('  %s -> %s' % (timer['unit'], timer['properties'].get('Triggers', '?')))
        if data.get('user_unit_files_require_review'):
            print('  User-manager unit files require separate review.')
        count += 1
    print('Filtered output: ' + str(output))
    if not count:
        print('No host results. Check inventory selection and connectivity; raw diagnostics were discarded.')
    return 0 if complete and count else 1


if __name__ == '__main__':
    raise SystemExit(main())
