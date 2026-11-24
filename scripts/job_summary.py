#!/usr/bin/env python3
"""Run the local summary play without turning a host filter into a localhost limit."""
import argparse,json,os,subprocess,tempfile
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--limit');a=p.parse_args();root=Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='summary-') as tmp:
        path=Path(tmp)/'vars.json';path.write_text(json.dumps({'script_jobs_targets':a.limit} if a.limit else {}));path.chmod(0o600)
        env=os.environ.copy();env['SCRIPT_JOBS_CALLBACK']='0'
        return subprocess.call(['ansible-playbook','playbooks/scripts/summary_jobs.yml','-e','@'+str(path)],cwd=root,env=env)
if __name__=='__main__':raise SystemExit(main())
