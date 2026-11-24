"""Isolated local Ansible integration; no real host, Cron, SMTP or Telegram actions."""
import grp,hashlib,json,os,pwd,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
@unittest.skipUnless(os.environ.get('ANSIBLE_JOBS_INTEGRATION')=='1','explicit local Ansible integration')
class Integration(unittest.TestCase):
 def test_deploy_run_collect_and_idempotence(self):
  with tempfile.TemporaryDirectory(prefix='jobs-integration-') as td:
   d=Path(td);source=d/'source/fixture';target=d/'target';db=d/'data/jobs.db';source.mkdir(parents=True)
   files={'demo.sh':'''#!/usr/bin/env bash
D="$(cd "$(dirname "$0")" && pwd)"
exec "$D/bin/script-jobs" run --job demo --program "$D/programs/demo.sh" --config "$D/config/common.json" -- "$@"
''','programs/demo.sh':'''#!/usr/bin/env bash
D="$(cd "$(dirname "$0")/.." && pwd)"
. "$D/lib/load.sh"
hm_job_event 'Synthetic phase'
hm_job_item 101 success 'Synthetic item'
''','config/common.json':json.dumps({'LABEL':'$(touch '+str(d/'executed')+')','TEMPLATE':"{{ lookup('pipe', 'touch "+str(d/'executed-template')+"') }}"})+'\n'}
   manifest=[]
   for name,text in files.items():
    p=source/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);p.chmod(0o600)
    manifest.append({'path':name,'kind':'config' if name.endswith('.json') else 'script','sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
   (source/'deployment.json').write_text(json.dumps({'files':manifest}))
   inventory={'all':{'children':{'all_linux_systems':{'hosts':{'fixture':{'ansible_connection':'local','ansible_become':False,'ansible_python_interpreter':sys.executable,'script_jobs_python':sys.executable,'script_jobs_source_root':str(d/'source'),'script_jobs_target_root':str(target),'script_library_root':str(target),'script_jobs_database_path':str(db),'script_jobs_owner':pwd.getpwuid(os.getuid()).pw_name,'script_jobs_group':grp.getgrgid(os.getgid()).gr_name}}}}}}
   (d/'inventory.json').write_text(json.dumps(inventory));(d/'ansible.cfg').write_text('[defaults]\ninventory='+str(d/'inventory.json')+'\nlocal_tmp='+str(d/'local-tmp')+'\nremote_tmp='+str(d/'remote-tmp')+'\nroles_path='+str(ROOT/'roles')+'\n')
   env=dict(os.environ,ANSIBLE_CONFIG=str(d/'ansible.cfg'),SCRIPT_JOBS_CALLBACK='0')
   command=['ansible-playbook',str(ROOT/'playbooks/scripts/deploy_jobs.yml'),'-l','fixture']
   first=subprocess.run(command,env=env,capture_output=True,text=True);self.assertEqual(first.returncode,0,first.stdout+first.stderr)
   second=subprocess.run(command,env=env,capture_output=True,text=True);self.assertEqual(second.returncode,0,second.stdout+second.stderr);self.assertRegex(second.stdout,r'changed=0\s')
   self.assertFalse((d/'executed').exists());self.assertFalse((d/'executed-template').exists())
   run=subprocess.run(['bash',str(target/'demo.sh')],capture_output=True,text=True);self.assertEqual(run.returncode,0,run.stderr)
   query=subprocess.run([sys.executable,str(ROOT/'scripts/job_console.py'),'--project',str(d),'--db',str(d/'controller.db'),'--limit','fixture','collect'],env=env,capture_output=True,text=True)
   self.assertEqual(query.returncode,0,query.stderr+query.stdout);self.assertEqual(json.loads(query.stdout)[0]['status'],'ok')
   sys.path.insert(0,str(ROOT/'artifacts/script-library/lib/python'));from job_store import Store
   state=Store(d/'controller.db');rows=state.runs();self.assertEqual(rows[0]['status'],'success');self.assertEqual(state.details(rows[0]['run_id'])[0]['items'][0]['item_id'],'101');state.close()
 def test_actual_callback_records_only_host_statuses(self):
  with tempfile.TemporaryDirectory(prefix='callback-integration-') as td:
   d=Path(td);(d/'inventory').write_text('fixture ansible_connection=local\n');(d/'ansible.cfg').write_text('[defaults]\ninventory='+str(d/'inventory')+'\nlocal_tmp='+str(d/'local-tmp')+'\nremote_tmp='+str(d/'remote-tmp')+'\n')
   (d/'play.yml').write_text('- hosts: all\n  gather_facts: false\n  tasks:\n    - debug:\n        msg: fixture-private-task-argument\n')
   env=dict(os.environ,ANSIBLE_CONFIG=str(d/'ansible.cfg'),ANSIBLE_CALLBACK_PLUGINS=str(ROOT/'tools/callbacks'),ANSIBLE_CALLBACKS_ENABLED='script_job_results',SCRIPT_JOBS_CALLBACK='1',SCRIPT_JOBS_CONTROLLER_DB=str(d/'jobs.db'))
   result=subprocess.run(['ansible-playbook',str(d/'play.yml')],env=env,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   sys.path.insert(0,str(ROOT/'artifacts/script-library/lib/python'));from job_store import Store
   state=Store(d/'jobs.db');rows=state.runs();self.assertEqual(rows[0]['category'],'ansible');self.assertEqual(rows[0]['status'],'success');self.assertNotIn('fixture-private-task-argument',json.dumps(state.export()));state.close()
if __name__=='__main__':unittest.main(verbosity=2)
