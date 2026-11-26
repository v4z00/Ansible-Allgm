"""Real cron windows across multi-daily, frequent and weekly jobs."""
import datetime
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'artifacts/script-library/lib/python'))
from job_expectations import normalize,evaluate


class Windows(unittest.TestCase):
    def spec(self,hour,minute='0',weekday='*'):
        with patch('job_expectations.time.time',return_value=1):
            return normalize([{'job':'fixture','timezone':'Europe/Berlin','cron':{'hour':hour,'minute':minute,'weekday':weekday},
                               'expected':{'deadline_minutes':10,'max_runtime_minutes':60}}])[0]
    def now(self,day=26,hour=13,minute=0):return datetime.datetime(2026,11,day,hour,minute,tzinfo=ZoneInfo('Europe/Berlin'))
    def row(self,when,status='success'):return {'job':'fixture','started':when.timestamp(),'status':status}
    def test_second_daily_slot_needs_its_own_result(self):
        spec=self.spec('0,12');morning=self.row(self.now(hour=0))
        self.assertEqual(evaluate(spec,[morning],self.now()),'missing-expected-run')
        self.assertEqual(evaluate(spec,[morning,self.row(self.now(hour=12))],self.now()),'ok')
    def test_five_minute_calendar_uses_latest_slot_and_grace_period(self):
        spec=self.spec('*','5,10,15,20,25,30,35,40,45,50,55,0')
        self.assertEqual(len(spec['start']),288)
        self.assertEqual(evaluate(spec,[],self.now(hour=9,minute=1)),'ok')
        spec['deadline_minutes']=1
        self.assertEqual(evaluate(spec,[self.row(self.now(hour=8,minute=55))],self.now(hour=9,minute=2)),'missing-expected-run')
        self.assertEqual(evaluate(spec,[self.row(self.now(hour=9))],self.now(hour=9,minute=2)),'ok')
    def test_weekly_success_remains_valid_through_sunday(self):
        spec=self.spec('6',weekday='1');row=self.row(self.now(day=23,hour=6))
        for day in range(23,30):self.assertEqual(evaluate(spec,[row],self.now(day=day)),'ok')
        self.assertEqual(evaluate(spec,[row],self.now(day=30)),'missing-expected-run')
    def test_running_job_is_not_lost_when_another_slot_becomes_due(self):
        spec=self.spec('0,12');row=self.row(self.now(hour=0),'running')
        self.assertEqual(evaluate(spec,[row],self.now()),'overdue-running')
        spec['max_runtime_minutes']=1440
        self.assertEqual(evaluate(spec,[row],self.now()),'ok')
    def test_unsupported_or_partial_schedules_remain_unconfigured(self):
        spec=self.spec('invalid');self.assertEqual(evaluate(spec,[],self.now()),'schedule-unconfigured')
        spec=self.spec('5');spec.pop('timezone');self.assertEqual(evaluate(spec,[],self.now()),'schedule-unconfigured')
        self.assertEqual(self.spec('5','*/15')['start'],['05:00','05:15','05:30','05:45'])
    def test_unchanged_calendar_preserves_activation_boundary(self):
        spec=self.spec('0,12')
        entry={'job':'fixture','timezone':'Europe/Berlin','cron':{'hour':'0,12','minute':'0','weekday':'*'},'expected':{'deadline_minutes':10,'max_runtime_minutes':60}}
        with patch('job_expectations.time.time',return_value=999):self.assertEqual(normalize([entry],[spec])[0]['configured_at'],1)


if __name__=='__main__':unittest.main(verbosity=2)
