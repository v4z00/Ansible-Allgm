"""Offline GPO contract tests. Real AD/GPMC execution remains a separate pilot."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from jinja2 import Environment, StrictUndefined

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gpo_plan',ROOT/'roles/windows_gpo/filter_plugins/gpo_plan.py')
gpo=importlib.util.module_from_spec(spec);spec.loader.exec_module(gpo)
PWSH=os.environ.get('PWSH') or shutil.which('pwsh')

class Gpo(unittest.TestCase):
    def test_only_explicit_typed_values_and_topic_names(self):
        data=gpo.plan([{'id':'security','name':'Security','settings':{'winrm_basic':False,'smb_client_signing':True}}])
        self.assertEqual(data['profiles'][0]['name'],'Ansible: Security')
        self.assertEqual([v['value'] for v in data['profiles'][0]['values']],[0,1])
        self.assertEqual(gpo.plan([{'id':'windows','name':'Windows','settings':{}}])['profiles'],[])
        for value in ('false',0,1,[],{}):
            with self.subTest(value=value),self.assertRaises(ValueError):gpo.plan([{'id':'security','name':'Security','settings':{'winrm_basic':value}}])
    def test_unknown_settings_duplicate_names_and_ntlm_lockout_are_rejected(self):
        for profiles in ([{'id':'security','name':'Security','settings':{'typo':True}}],
                         [{'id':'a','name':'Security'},{'id':'b','name':'security'}],
                         [{'id':'security','name':'Security','settings':{'ntlm_outgoing':'deny'}}]):
            with self.assertRaises(ValueError):gpo.plan(profiles)
        self.assertEqual(gpo.plan([{'id':'security','name':'Security','settings':{'ntlm_outgoing':'deny'}}],transport='kerberos')['profiles'][0]['values'][0]['value'],2)
    @unittest.skipUnless(PWSH,'PowerShell runtime required')
    def test_native_parser_and_mocked_gpo_lifecycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            role=ROOT/'roles/windows_gpo'
            text=(role/'templates/manage.ps1.j2').read_text()
            # Keep the fixture's snapshot mock; production uses its actual read-only function.
            def lookup(kind,path,rstrip=False):
                return '' if path.endswith('/Get-GpoRegistrySnapshot.ps1') else Path(path).read_text()
            rendered=Environment(undefined=StrictUndefined).from_string(text).render(role_path=str(role),lookup=lookup)
            manager=directory/'manage.ps1';manager.write_text(rendered)
            result=subprocess.run([PWSH,'-NoProfile','-NonInteractive','-File',str(Path(__file__).with_name('gpo_fixture.ps1')),'-Root',str(ROOT),'-Directory',str(directory),'-Manager',str(manager)],capture_output=True,text=True,timeout=30)
            self.assertEqual(result.returncode,0,result.stderr+result.stdout)

if __name__=='__main__':unittest.main()
