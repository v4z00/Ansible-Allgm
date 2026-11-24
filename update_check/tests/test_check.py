"""Offline-Selbsttests auf temporaeren Dateien; keine produktiven Settings."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SOURCE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('controller_check_test_module',SOURCE/'check.py')
check=importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

class CheckerTest(unittest.TestCase):
    def test_valid_type(self):
        self.assertTrue(check.good_type(False,'boolean'))
        self.assertFalse(check.good_type('false','boolean'))
        self.assertFalse(check.good_type(True,'integer'))
    def test_dynamic_is_not_executed(self):
        self.assertTrue(check.dynamic('{{ lookup("pipe", "false") }}'))
    def test_version_marker_not_sha(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'scripts').mkdir()
            p=root/'scripts/test.py';p.write_text('# known\n')
            manifest={'schema':1,'id':'test','version':'1.0.0','version_files':['VERSION.txt'],'files':{'scripts/test.py':check.sha(p)}}
            self.assertEqual(check.check_component(root,manifest)['verified_version'],'1.0.0')
            (root/'VERSION.txt').write_text('1.0.0\n');p.write_text('# modified\n')
            self.assertIsNone(check.check_component(root,manifest)['verified_version'])
    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as td:
            report=check.check_component(Path(td).resolve(),{'schema':1,'id':'test','version':'1','files':{'scripts/missing.py':'0'*64}})
            self.assertEqual(report['issues'][0]['status'],'FEHLT')
    def test_secret_not_hashed(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(check.AuditError):
                check.check_component(Path(td).resolve(),{'schema':1,'id':'test','version':'1','files':{'group_vars/all/secrets.yml':'0'*64}})
    def test_path_escape(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(check.AuditError):check.guarded(Path(td).resolve(),'../../secret')
    def test_duplicate_yaml_is_safe(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'settings.yml';p.write_text('secret: first\nsecret: second\n')
            with self.assertRaises(check.AuditError):check.read_yaml(p)
    def test_unsafe_yaml_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'settings.yml';p.write_text('secret: !!python/object/apply:os.system ["false"]\n')
            with self.assertRaises(check.AuditError):check.read_yaml(p)
    def test_no_credentials_in_report(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'group_vars/all').mkdir(parents=True)
            (root/'group_vars/all/secrets.yml').write_text('password: NEVER_PRINT_THIS\n')
            report=check.check_settings(root,{'fields':[{'key':'password','type':'string','required':True}],'tls_tasks':[]})
            self.assertNotIn('NEVER_PRINT_THIS',json.dumps(report))
    def test_site_values_are_not_enforced(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'group_vars/all').mkdir(parents=True)
            (root/'group_vars/all/settings.yml').write_text('tls_validate_certs_default: true\n')
            contract={'fields':[{'key':'tls_validate_certs_default','type':'boolean','required':False,'expected_constant':False,'implicit_default':True}]}
            self.assertEqual(check.check_settings(root,contract)['fields'][0]['status'],'OK')



class ConfigurationTests(unittest.TestCase):
    def module(self):
        spec=importlib.util.spec_from_file_location('controller_config_test_module',SOURCE/'configure.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module
    def test_sort_keeps_values_comments_unknown(self):
        module=self.module()
        text='# title\nunknown: keep # retained\nfeatures:\n  baseline: false\n'
        changed,done=module.sort_settings(text,{'top_level_order':['features']},check.UniqueLoader)
        self.assertTrue(done);self.assertIn('# retained',changed)
        self.assertEqual(check.yaml.safe_load(text),check.yaml.safe_load(changed))
    def test_nested_edit_preserves_other_values(self):
        module=self.module()
        changed=module.set_field('features: {}\nunknown: keep\n','features.checkmk',False,check.UniqueLoader)
        self.assertEqual(check.yaml.safe_load(changed),{'features':{'checkmk':False},'unknown':'keep'})
    def test_yaml_anchors_are_not_reordered(self):
        module=self.module();text='a: &defaults\n  value: true\nb: *defaults\n'
        self.assertEqual(module.sort_settings(text,{'top_level_order':['b','a']},check.UniqueLoader),(text,False))

class PatchTests(unittest.TestCase):
    def test_literal_alias_resolution(self):
        self.assertEqual(check.resolve_literal('{{ compose_timeout }}',{'compose_timeout':30}),(30,'OK_ALIAS'))
    def test_alias_cycles(self):
        self.assertEqual(check.resolve_literal('{{ a }}',{'a':'{{ b }}','b':'{{ a }}'})[1],'ALIAS_ZYKLUS')
    def test_context_not_executed(self):
        self.assertEqual(check.resolve_literal('{{ playbook_dir }}/../artifacts/test',{})[1],'ANSIBLE_KONTEXT')
        self.assertEqual(check.resolve_literal('{{ lookup("pipe", "touch /tmp/never-run") }}',{})[1],'DYNAMISCH_UNGEPRUEFT')
    def test_disabled_parent(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'group_vars/all').mkdir(parents=True)
            (root/'group_vars/all/settings.yml').write_text('features: {kerberos: false}\n')
            self.assertEqual(check.check_settings(root,{'fields':[{'key':'features.kerberos_keytabs','type':'boolean','required':True,'feature':'kerberos'}]})['fields'],[])
    def test_configuration_usage_only_values(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'group_vars/all').mkdir(parents=True)
            p=root/'group_vars/all/settings.yml';p.write_text('network_device_credentials: {}\nport: "{{ network_device_credentials.port }}"\n')
            hits=check.find_usage(root,'network_device_credentials')
            self.assertEqual([r['line'] for r in hits],[2]);self.assertNotIn('port',json.dumps(hits))
    def test_historical_file_optional(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td).resolve();(root/'active.py').write_text('# active\n')
            m={'schema':1,'id':'test','version':'1','files':{'active.py':check.sha(root/'active.py')},'historical_files':[{'path':'old.py'}]}
            self.assertEqual(check.check_component(root,m)['status'],'OK')
            (root/'old.py').write_text('# old\n');self.assertEqual(check.check_component(root,m)['status'],'OK')
            (root/'active.py').write_text('# drift\n');self.assertEqual(check.check_component(root,m)['status'],'ABWEICHEND')

if __name__=='__main__':unittest.main()
