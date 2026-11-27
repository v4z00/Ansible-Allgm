"""Use the same validation for deployment and the Linux local check."""
import importlib.util
from pathlib import Path


def validate(entries):
    path=Path(__file__).resolve().parents[3]/'scripts/job_local_check.py'
    spec=importlib.util.spec_from_file_location('job_local_check',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.normalize(entries)


class FilterModule:
    def filters(self):return {'script_jobs_checkmk_entries':validate}
