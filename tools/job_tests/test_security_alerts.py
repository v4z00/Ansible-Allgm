"""Immediate security outbox and SMTP relay semantics, using synthetic data."""
import concurrent.futures
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'artifacts/script-library/lib/python'))
from job_store import Store
from job_security import record,retry,channels
from job_notify import deliver


class SecurityAlerts(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.directory=Path(self.tmp.name)
        self.store=Store(self.directory/'jobs.sqlite3','fixture-host')
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def alert(self,event='event:42'):
        return record(self.store,event,'security-event','Attention','secret=synthetic-sensitive',['mail','telegram'])
    def test_per_channel_retry_and_event_deduplication(self):
        identifier=self.alert();sent=[]
        def sender(channel,*args):
            sent.append(channel)
            if channel=='telegram':raise OSError('synthetic outage')
        with patch('job_security.deliver',side_effect=sender):
            self.assertEqual(retry(self.store,{},ROOT)['pending'],1)
        self.assertEqual(self.alert(),identifier)
        with patch('job_security.deliver') as sender:
            self.assertEqual(retry(self.store,{},ROOT)['pending'],0)
            self.assertEqual(sender.call_args[0][0],'telegram');self.assertEqual(sender.call_count,1)
        self.assertEqual(len(self.store.runs()),1)
        self.assertNotIn('synthetic-sensitive',str(self.store.export()))
        self.assertIsNone(self.store.report())
    def test_atomic_concurrent_event_deduplication(self):
        def create(_):
            store=Store(self.directory/'jobs.sqlite3')
            try:return record(store,'same-event','security-event','Attention','',['mail'])
            finally:store.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:ids=list(pool.map(create,range(12)))
        self.assertEqual(len(set(ids)),1)
        self.assertEqual(len(self.store.runs()),1)
    def test_expired_lease_and_pending_retention(self):
        identifier=self.alert();self.assertTrue(self.store.claim(identifier,'mail'))
        self.store.db.execute('UPDATE deliveries SET lease_until=1')
        self.store.db.execute('UPDATE reports SET created=1')
        self.store.db.execute('UPDATE runs SET finished=1')
        self.store.prune()
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM security_alerts').fetchone()[0],1)
        with patch('job_security.deliver'):
            self.assertEqual(retry(self.store,{},ROOT)['pending'],0)
        self.store.prune()
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM security_alerts').fetchone()[0],0)
    def test_new_alert_is_sent_before_an_old_backlog(self):
        self.alert('older');new=self.alert('newer')
        with patch('job_security.deliver') as sender:
            retry(self.store,{},ROOT,report=new)
            self.assertEqual({call.args[1]['id'] for call in sender.call_args_list},{new})
    def test_channel_configuration_is_explicit(self):
        self.assertEqual(channels({'MAIL_TO':'receiver@example.invalid'}),['mail'])
        for value in ({},{'SECURITY_CHANNELS':[]},{'SECURITY_CHANNELS':['bogus']}):
            with self.assertRaises(ValueError):channels(value)
    def test_smtp_without_login_and_fixed_table(self):
        cfg={'MAIL_TO':'receiver@example.invalid','SMTP_HOST':'relay.example.invalid',
             'SMTP_FROM':'sender@example.invalid','SMTP_TLS':'none','SMTP_AUTH':'none'}
        with patch('job_notify.smtplib.SMTP') as smtp:
            deliver('mail',{'body':'ÄÖÜäöüß\nCompleted'},cfg,ROOT/'artifacts/script-library')
            client=smtp.return_value.__enter__.return_value
            # The context manager intentionally uses the original client object.
            smtp.return_value.login.assert_not_called();smtp.return_value.starttls.assert_not_called()
            message=smtp.return_value.send_message.call_args[0][0]
            self.assertEqual(str(message['Subject']),'AEOEUEaeoeuess')
            self.assertIn('Completed',message.get_content())
    def test_starttls_failure_does_not_send_plaintext(self):
        cfg={'MAIL_TO':'receiver@example.invalid','SMTP_HOST':'relay.example.invalid','SMTP_FROM':'sender@example.invalid'}
        with patch('job_notify.smtplib.SMTP') as smtp:
            smtp.return_value.starttls.side_effect=OSError('TLS unavailable')
            with self.assertRaises(OSError):deliver('mail',{'body':'Attention'},cfg,ROOT/'artifacts/script-library')
            smtp.return_value.send_message.assert_not_called()


if __name__=='__main__':unittest.main()
