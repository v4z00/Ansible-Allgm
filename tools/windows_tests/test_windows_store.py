"""Portable PowerShell/real SQLite protocol tests, without Windows host contact."""
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import socketserver
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'artifacts/script-library/lib/python'))
from job_store import Store

PWSH=os.environ.get('PWSH') or shutil.which('pwsh')
SQLITE=os.environ.get('SQLITE3') or shutil.which('sqlite3')


class Relay(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b'220 fixture\r\n')
        while True:
            line=self.rfile.readline()
            if not line:return
            command=line.decode('ascii','replace').strip()
            self.server.commands.append(command.split(' ',1)[0])
            if command.upper().startswith(('EHLO','HELO')):self.wfile.write(b'250 fixture\r\n')
            elif command.upper()=='DATA':
                self.wfile.write(b'354 body\r\n');body=b''
                while True:
                    part=self.rfile.readline()
                    if part in (b'.\r\n',b''):break
                    body+=part
                self.server.messages.append(body);self.wfile.write(b'250 accepted\r\n')
            elif command.upper()=='QUIT':self.wfile.write(b'221 bye\r\n');return
            else:self.wfile.write(b'250 ok\r\n')


@unittest.skipUnless(PWSH and SQLITE,'PowerShell and SQLite executables required')
class WindowsStore(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.directory=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def fixture(self,case,port=0,check=True):
        command=[PWSH,'-NoLogo','-NoProfile','-NonInteractive','-File',str(Path(__file__).with_name('store_fixture.ps1')),
                 '-Root',str(ROOT),'-Directory',str(self.directory),'-Sqlite',SQLITE,'-Case',case,'-Port',str(port)]
        result=subprocess.run(command,capture_output=True,text=True,timeout=60)
        if check:self.assertEqual(result.returncode,0,result.stderr)
        return result
    def test_protocol_import_unicode_sql_injection_and_read_queries(self):
        self.fixture('store')
        store=Store(self.directory/'controller.sqlite3','controller')
        try:
            first=json.loads((self.directory/'first.json').read_text(encoding='utf-8-sig'))
            rest=json.loads((self.directory/'next.json').read_text(encoding='utf-8-sig'))
            store.ingest('windows-host',first);store.ingest('windows-host',rest);store.ingest('windows-host',rest)
            self.assertEqual(store.cursor('windows-host')['last_id'],3)
            row=store.latest()[0];self.assertEqual(row['status'],'success')
            message=store.details(row['run_id'])[0]['items'][0]['message']
            self.assertIn("'); DROP TABLE runs; --",message);self.assertIn('ü',message)
            self.assertIsInstance(row['started'],float)
        finally:store.close()
    def test_concurrent_writers(self):
        # Initialize once, then overlap independent PowerShell processes.
        self.fixture('writer')
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(lambda _:self.fixture('writer'),range(8)))
        with sqlite3.connect(self.directory/"job ' fixture.sqlite3") as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM runs WHERE status='success'").fetchone()[0],9)
    def test_security_retry_ack_dedup_and_import(self):
        self.fixture('security')
        batch=json.loads((self.directory/'security.json').read_text(encoding='utf-8-sig'))
        self.assertNotIn('synthetic-value',json.dumps(batch))
        store=Store(self.directory/'controller.sqlite3','controller')
        try:
            store.ingest('windows-host',batch)
            self.assertEqual(len(store.runs(category='security')),1)
            self.assertIsNone(store.report())
        finally:store.close()
    def test_retention_preserves_running_and_reports_gaps(self):self.fixture('retention')
    def test_process_runner_failure_timeout_and_private_logs(self):self.fixture('runner')
    def test_local_checks_match_linux(self):
        self.fixture('local-check')
        sys.path.insert(0,str(ROOT/'scripts'))
        from job_local_check import checks
        entries=[{'job':name,'max_age_seconds':3600,'max_runtime_seconds':60} for name in ('successful-job','missing-job')]
        expected=list(checks({'database':str(self.directory/"job ' fixture.sqlite3"),'jobs':entries,'security_outbox':True}))
        self.assertEqual((self.directory/'checks.txt').read_text(encoding='utf-8-sig').splitlines(),expected)
    def relay_test(self,case):
        with socketserver.TCPServer(('127.0.0.1',0),Relay) as relay:
            relay.messages=[];relay.commands=[]
            thread=threading.Thread(target=relay.serve_forever,daemon=True);thread.start()
            try:result=self.fixture(case,relay.server_address[1],check=False)
            finally:relay.shutdown();thread.join(timeout=5)
        return result,relay
    def test_smtp_relay_without_login_and_fixed_mail_table(self):
        result,relay=self.relay_test('smtp');self.assertEqual(result.returncode,0,result.stderr)
        self.assertNotIn('AUTH',relay.commands);self.assertEqual(len(relay.messages),1)
        self.assertIn(b'AEOEUEaeoeuess',relay.messages[0])
    def test_missing_starttls_never_falls_back_to_plaintext(self):
        result,relay=self.relay_test('smtp-starttls');self.assertNotEqual(result.returncode,0)
        self.assertEqual(relay.messages,[])


if __name__=='__main__':unittest.main()
