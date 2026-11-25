"""Opt-in aggregate Ansible results. Never persist task arguments or hostvars."""
import os
import time
from pathlib import Path
import sys
from ansible.plugins.callback import CallbackBase

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'artifacts/script-library/lib/python'))

class CallbackModule(CallbackBase):
    CALLBACK_VERSION=2.0
    CALLBACK_TYPE='aggregate'
    CALLBACK_NAME='script_job_results'
    CALLBACK_NEEDS_ENABLED=True
    def __init__(self):
        super().__init__();self.store=None;self.run=None
    def v2_playbook_on_start(self,playbook):
        if os.environ.get('SCRIPT_JOBS_CALLBACK')!='1':return
        if Path(playbook._file_name).resolve() in {ROOT/'playbooks/scripts/summary_jobs.yml',ROOT/'playbooks/scripts/show_status.yml'}:return
        from job_store import Store
        self.store=Store(os.environ.get('SCRIPT_JOBS_CONTROLLER_DB','/var/lib/script-jobs/controller.sqlite3'))
        self.started=time.monotonic()
        self.run=self.store.begin('ansible:'+Path(playbook._file_name).name,'ansible')
    def v2_playbook_on_stats(self,stats):
        if not self.store:return
        failed=False
        for host in stats.processed:
            state=stats.summarize(host)
            bad=state.get('failures',0)>0 or state.get('unreachable',0)>0
            failed|=bad
            self.store.update(self.run,'failed' if bad else 'success',
                              'Unreachable' if state.get('unreachable',0) else 'Ansible host result',item=host)
        if not stats.processed:failed=True
        self.store.update(self.run,'failed' if failed else 'success','Ansible playbook completed',exit_code=1 if failed else 0,duration_seconds=time.monotonic()-self.started)
        self.store.close();self.store=None
