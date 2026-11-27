import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'artifacts/script-library/lib/python'))
from job_store import Store
spec=importlib.util.spec_from_file_location('job_local_check',ROOT/'scripts/job_local_check.py')
checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)


class LocalChecks(unittest.TestCase):
    def test_status_and_thresholds(self):
        entry={'job':'fixture','max_age_seconds':100,'max_runtime_seconds':50}
        self.assertEqual(checks.check_job(None,entry,200)[0],3)
        self.assertEqual(checks.check_job({'status':'success','started':150,'finished':160},entry,200)[0],0)
        self.assertEqual(checks.check_job({'status':'success','started':0,'finished':1},entry,200)[0],2)
        self.assertEqual(checks.check_job({'status':'running','started':100},entry,200)[0],2)
        self.assertEqual(checks.check_job({'status':'running','started':180},entry,200)[0],0)
    def test_only_explicit_jobs_and_no_raw_summaries(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'jobs.sqlite3';store=Store(path)
            try:
                run=store.begin('selected');store.update(run,'failed','private-context',exit_code=3)
                other=store.begin('excluded');store.update(other,'success',exit_code=0)
                config={'database':str(path),'jobs':[{'job':'selected','max_age_seconds':86400,'max_runtime_seconds':60}]}
                result=list(checks.checks(config));self.assertEqual(result,['2 "Script job selected" - Job failed'])
            finally:store.close()
    def test_configuration_does_not_create_a_missing_database(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'missing.sqlite3'
            with self.assertRaises(Exception):list(checks.checks({'database':str(path)}))
            self.assertFalse(path.exists())
    def test_configuration_validation(self):
        for value in ([{'job':'bad"name'}],[{'job':'valid','max_age_seconds':True,'max_runtime_seconds':5}]):
            with self.assertRaises(ValueError):checks.normalize(value)


if __name__=='__main__':unittest.main()
