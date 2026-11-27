"""Signing metadata and mocked Authenticode workflow; actual signing needs Windows."""
import datetime
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID,ExtendedKeyUsageOID

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('windows_signing_bundle',ROOT/'scripts/windows_signing_bundle.py')
bundle=importlib.util.module_from_spec(spec);spec.loader.exec_module(bundle)
PWSH=os.environ.get('PWSH') or shutil.which('pwsh')


class Signing(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve()
        key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Synthetic code signer')])
        now=datetime.datetime.now(datetime.timezone.utc)
        cert=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
              .serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(days=1))
              .not_valid_after(now+datetime.timedelta(days=1))
              .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CODE_SIGNING]),critical=False)
              .sign(key,hashes.SHA256()))
        self.certificate=self.root/'public.cer';self.certificate.write_bytes(cert.public_bytes(serialization.Encoding.DER))
        self.code=self.root/'code.ps1';self.code.write_text('Write-Output "synthetic"')
    def tearDown(self):self.tmp.cleanup()
    def test_code_batch_and_environment_identity_are_reproducible(self):
        rows=[{'path':'programs/code.ps1','source':str(self.code)}]
        first=bundle.prepare(rows,self.certificate,self.root/'cache')
        second=bundle.prepare(rows,self.certificate,self.root/'cache')
        self.assertEqual(first['batch_id'],second['batch_id'])
        third=bundle.prepare(rows,self.certificate,self.root/'cache','https://timestamp.example.invalid')
        self.assertNotEqual(first['batch_id'],third['batch_id'])
        self.assertTrue(bundle.certificate_info(self.certificate)['code_signing'])
        self.assertTrue(bundle.certificate_info(self.certificate)['self_issued'])
    def test_pfx_is_not_read_by_artifact_preparation(self):
        private=self.root/'key.pfx';private.write_bytes(b'synthetic placeholder')
        original=Path.read_bytes
        def read(path):
            if path.suffix=='.pfx':self.fail('Private key was opened by artifact builder')
            return original(path)
        with patch.object(Path,'read_bytes',read),self.assertRaises(ValueError):bundle.certificate_identity(private)
    def test_invalid_paths_collisions_configs_and_symlinks_are_refused(self):
        for path in ('../bad.ps1','C:\\bad.ps1','x:stream.ps1','lib/bad.ps1 '):
            with self.subTest(path=path),self.assertRaises(ValueError):bundle.relative(path)
        rows=[{'path':'A.ps1','source':str(self.code)},{'path':'a.ps1','source':str(self.code)}]
        with self.assertRaises(ValueError):bundle.prepare(rows,self.certificate,self.root/'cache')
        source=self.root/'secret.json';source.write_text('{}')
        with self.assertRaises(ValueError):bundle.prepare([{'path':'config/secret.json','source':str(source)}],self.certificate,self.root/'cache')
        linked=self.root/'linked.ps1';linked.symlink_to(self.code)
        with self.assertRaises(ValueError):bundle.prepare([{'path':'linked.ps1','source':str(linked)}],self.certificate,self.root/'cache')
    def test_returned_byte_mapping_is_verified(self):
        result=bundle.prepare([{'path':'code.ps1','source':str(self.code)}],self.certificate,self.root/'cache')
        root=Path(result['signed_root']);(root/'code.ps1').write_bytes(self.code.read_bytes())
        receipt={'schema':1,'certificate_thumbprint':result['certificate_thumbprint'],
                 'files':[{'path':'code.ps1','source_sha256':result['files'][0]['sha256'],'signed_sha256':result['files'][0]['sha256']}]}
        (root/'signed-manifest.json').write_text(json.dumps(receipt))
        expected=json.loads(Path(result['source_manifest']).read_text())
        self.assertTrue(bundle.verify(root,expected))
        (root/'code.ps1').write_text('tampered')
        with self.assertRaises(ValueError):bundle.verify(root,expected)
    @unittest.skipUnless(PWSH,'Portable PowerShell runtime required')
    def test_signer_control_flow_with_mock_authenticode_cmdlets(self):
        path=self.root/'fixture';path.mkdir()
        result=subprocess.run([PWSH,'-NoLogo','-NoProfile','-NonInteractive','-File',str(Path(__file__).with_name('signing_fixture.ps1')),
                               '-Root',str(ROOT),'-Directory',str(path)],text=True,capture_output=True,timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':unittest.main()
