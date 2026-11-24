import concurrent.futures,datetime,importlib.util,json,os,subprocess,sys,tempfile,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];LIB=ROOT/'artifacts/script-library';sys.path.insert(0,str(LIB/'lib/python'))
from job_store import Store
import job_expectations
spec=importlib.util.spec_from_file_location('cron',ROOT/'scripts/job_cron_guard.py');cron=importlib.util.module_from_spec(spec);spec.loader.exec_module(cron)
class Jobs(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.store=Store(self.root/'jobs.db','fixture')
 def tearDown(self):self.store.close();self.tmp.cleanup()
 def cli(self,*args):return subprocess.run([sys.executable,str(LIB/'bin/script-jobs'),'--db',str(self.root/'jobs.db'),*args],text=True,capture_output=True)
 def test_lifecycle(self):
  r=self.store.begin('backup');self.store.update(r,'failed','secret=fixture-secret',item='101');self.store.update(r,'failed',exit_code=2)
  self.assertEqual(self.store.details(r)[0]['items'][0]['status'],'failed');self.assertNotIn('fixture-secret',json.dumps(self.store.export()))
  with self.assertRaises(ValueError):self.store.update(r,'success')
 def test_import_replay_rollback_generation(self):
  r=self.store.begin('backup');self.store.update(r,'success',exit_code=0);batch=self.store.export();other=Store(self.root/'controller.db','controller')
  try:
   other.ingest('host',batch);other.ingest('host',batch);self.assertEqual(len(other.runs()),1)
   broken=json.loads(json.dumps(batch));broken['next']+=1
   with self.assertRaises(ValueError):other.ingest('host',broken)
   self.assertEqual(other.cursor('host')['last_id'],batch['next']);broken['epoch']='new'
   with self.assertRaises(ValueError):other.ingest('host',broken)
  finally:other.close()
 def test_retention_and_gaps(self):
  r=self.store.begin('old');self.store.update(r,'success',exit_code=0);self.store.db.execute('UPDATE runs SET finished=? WHERE run_id=?',(time.time()-91*86400,r))
  active=self.store.begin('active');self.assertEqual(self.store.prune(),1);self.assertEqual(self.store.details(active)[0]['status'],'running');self.assertTrue(self.store.export()['gap'])
 def test_reports_and_channel_ack(self):
  r=self.store.begin('daily');self.store.update(r,'success',exit_code=0);w=self.store.begin('weekly','vzdump');self.store.update(w,'failed','failed',item='101');self.store.update(w,'failed',exit_code=1)
  report=self.store.report();self.assertNotIn('weekly',report['body']);self.assertEqual(self.store.report()['id'],report['id'])
  self.assertTrue(self.store.claim(report['id'],'telegram'));self.assertFalse(self.store.claim(report['id'],'telegram'))
  self.store.delivered(report['id'],'telegram',False);self.assertTrue(self.store.claim(report['id'],'telegram'));self.store.delivered(report['id'],'telegram',True)
  self.assertIsNone(self.store.report());self.assertIn('101',self.store.report('vzdump')['body'])
 def test_concurrent_writes(self):
  def writer(i):
   s=Store(self.root/'jobs.db')
   try:r=s.begin('job-'+str(i));s.update(r,'success',exit_code=0)
   finally:s.close()
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(writer,range(30)))
  self.assertEqual(len(self.store.runs()),30)
 def test_runner_failure_and_overlap(self):
  p=self.root/'bad.sh';p.write_text('#!/bin/bash\nexit 7\n');result=self.cli('run','--job','bad','--program',str(p));self.assertEqual(result.returncode,7,result.stderr);self.assertEqual(self.store.runs()[0]['status'],'failed')
  p.write_text('#!/bin/bash\nsleep 2\n');cmd=[sys.executable,str(LIB/'bin/script-jobs'),'--db',str(self.root/'jobs.db'),'run','--job','same','--program',str(p)];proc=subprocess.Popen(cmd)
  try:
   for _ in range(50):
    if self.store.runs(job='same'):break
    time.sleep(.02)
   self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,75)
  finally:proc.wait(timeout=5)
 def test_ndjson_private_database(self):
  result=self.cli('watch','--seconds','0');self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(result.stdout)['schema'],1);self.assertEqual((self.root/'jobs.db').stat().st_mode&0o777,0o600)
 def test_monday_only(self):
  from zoneinfo import ZoneInfo
  cfg={'job':'weekly','timezone':'Europe/Berlin','start':'08:00','weekdays':[0],'deadline_minutes':60,'max_runtime_minutes':600,'configured_at':0};now=datetime.datetime(2026,11,23,10,tzinfo=ZoneInfo('Europe/Berlin'))
  self.assertEqual(job_expectations.evaluate(cfg,[],now),'missing-expected-run');rows=[{'job':'weekly','started':now.replace(hour=8).timestamp(),'status':'success'}]
  for day in range(7):self.assertEqual(job_expectations.evaluate(cfg,rows,now+datetime.timedelta(days=day)),'ok')
 def test_cron_conflicts(self):
  text='0 8 * * 1 /old/backup.sh\n0 9 * * * /other/task.sh\n'
  with self.assertRaises(ValueError):cron.plan(text,'backup','backup.sh')
  cleaned,count=cron.plan(text,'backup','backup.sh','/old/backup.sh');self.assertEqual(count,1);self.assertIn('/other/task.sh',cleaned)
  self.assertEqual(cron.plan('#Ansible: script-jobs:backup\n0 8 * * 1 /new/backup.sh\n','backup','backup.sh')[1],0)
 def test_missing_transport_no_fake_delivery(self):
  r=self.store.begin('test');self.store.update(r,'success',exit_code=0);self.assertNotEqual(self.cli('report').returncode,0);self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM deliveries').fetchone()[0],0)
 def test_preview_does_not_reserve_and_filters(self):
  r=self.store.begin('daily');self.store.update(r,'success','ok',item='101');self.store.update(r,'success',exit_code=0)
  self.store.report(reserve=False)
  self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM reports').fetchone()[0],0)
  self.assertEqual(len(self.store.runs(source='fixture',item='101',since=0)),1)
  self.assertEqual(self.store.runs(item='102'),[])
 def test_gap_can_only_be_accepted_explicitly(self):
  r=self.store.begin('old');self.store.update(r,'success',exit_code=0);self.store.db.execute('UPDATE runs SET finished=1 WHERE run_id=?',(r,));self.store.prune()
  n=self.store.begin('new');self.store.update(n,'success',exit_code=0);batch=self.store.export();other=Store(self.root/'controller.db','controller')
  try:
   with self.assertRaises(ValueError):other.ingest('source',batch)
   other.reset_cursor('source');other.ingest('source',batch);self.assertEqual(len(other.runs()),1)
  finally:other.close()
 def test_status_cannot_claim_success_with_failed_exit(self):
  r=self.store.begin('bad')
  with self.assertRaises(ValueError):self.store.update(r,'success',exit_code=3)
 def test_timeout_is_failure_even_if_child_handles_term(self):
  p=self.root/'slow.sh';p.write_text("#!/bin/bash\ntrap 'exit 0' TERM\nsleep 10\n")
  result=self.cli('run','--job','slow','--program',str(p),'--max-runtime','1')
  self.assertEqual(result.returncode,143,result.stderr);self.assertEqual(self.store.runs()[0]['status'],'failed')
 def test_known_secret_value_not_in_events(self):
  from unittest.mock import patch
  cfg=self.root/'cfg.json';cfg.write_text('{"BOT_TOKEN":"fixture-sensitive-value"}');cfg.chmod(0o600)
  with patch.dict(os.environ,{'HM_JOB_CONFIGFILES':json.dumps([str(cfg)])}):
   r=self.store.begin('private');self.store.update(r,summary='value: fixture-sensitive-value')
  self.assertNotIn('fixture-sensitive-value',json.dumps(self.store.export()))
 def test_manual_job_retains_a_controlling_terminal(self):
  import pty,select,signal
  script=self.root/'interactive.sh';script.write_text('#!/bin/bash\nprintf READY\nread -r answer </dev/tty\n[[ "$answer" == fixture ]]\n')
  pid,fd=pty.fork()
  if pid==0:
   os.execv(sys.executable,[sys.executable,str(LIB/'bin/script-jobs'),'--db',str(self.root/'jobs.db'),'run','--job','interactive','--program',str(script)])
  output=b'';sent=False;status=None
  try:
   end=time.monotonic()+8
   while time.monotonic()<end:
    if select.select([fd],[],[],0.1)[0]:
     try:output+=os.read(fd,4096)
     except OSError:pass
    if b'READY' in output and not sent:os.write(fd,b'fixture\n');sent=True
    observed,state=os.waitpid(pid,os.WNOHANG)
    if observed:status=state;break
   self.assertTrue(sent,output)
   self.assertIsNotNone(status,output)
   self.assertTrue(os.WIFEXITED(status),output);self.assertEqual(os.WEXITSTATUS(status),0,output)
  finally:
   if status is None:
    os.kill(pid,signal.SIGTERM);os.waitpid(pid,0)
   os.close(fd)
if __name__=='__main__':unittest.main(verbosity=2)
