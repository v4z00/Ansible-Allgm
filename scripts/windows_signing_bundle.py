#!/usr/bin/env python3
"""Prepare explicit code-only signing batches; verify returned bytes without keys."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import ssl
import sys
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import ExtendedKeyUsageOID


def relative(value):
    if not isinstance(value,str):raise ValueError('Artifact path must be text')
    path=PurePosixPath(value)
    if not isinstance(value,str) or path.is_absolute() or path.as_posix()!=value or not path.parts:
        raise ValueError('Explicit relative artifact path required')
    for part in path.parts:
        if part in ('.','..') or re.search(r'[\\:*?"<>|\x00-\x1f]',part) or part.rstrip(' .')!=part:
            raise ValueError('Unsafe Windows artifact path')
    return value


def source_files(library):
    """Only the public Windows code tree and two declared shared data files."""
    result=[]
    for source in sorted((library/'windows').rglob('*')):
        if source.is_file():
            path=source.relative_to(library/'windows').as_posix()
            if source.suffix.lower() not in ('.ps1','.psm1','.psd1','.ps1xml'):raise ValueError('Non-PowerShell source in Windows code tree')
            result.append({'source':str(source),'path':path})
    for name in ('job-schema.sql','mail-translations.json'):
        result.append({'source':str(library/'lib/data'/name),'path':'lib/data/'+name})
    return result


def certificate_identity(path):
    if Path(path).suffix.lower() not in ('.cer','.crt','.pem'):raise ValueError('Public certificate file required; PFX is not a bundle input')
    if any(item.is_symlink() for item in (Path(path).absolute(),*Path(path).absolute().parents)):
        raise ValueError('Public certificate symlink refused')
    data=Path(path).read_bytes()
    if b'PRIVATE KEY' in data:raise ValueError('Only a public certificate may enter the artifact workflow')
    if b'-----BEGIN CERTIFICATE-----' in data:
        if data.count(b'-----BEGIN CERTIFICATE-----')!=1:raise ValueError('One publisher certificate required')
        data=ssl.PEM_cert_to_DER_cert(data.decode('ascii'))
    certificate=x509.load_der_x509_certificate(data)
    if certificate.public_bytes(serialization.Encoding.DER)!=data:raise ValueError('Certificate contains trailing non-certificate data')
    # Thumbprint selects the exact Windows certificate, not a subject-name match.
    return hashlib.sha1(data,usedforsecurity=False).hexdigest().upper(),hashlib.sha256(data).hexdigest()


def certificate_info(path):
    thumbprint,digest=certificate_identity(path)
    data=Path(path).read_bytes()
    certificate=x509.load_pem_x509_certificate(data) if b'-----BEGIN CERTIFICATE-----' in data else x509.load_der_x509_certificate(data)
    try:code_signing=ExtendedKeyUsageOID.CODE_SIGNING in certificate.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value
    except x509.ExtensionNotFound:code_signing=False
    try:is_ca=certificate.extensions.get_extension_for_class(x509.BasicConstraints).value.ca
    except x509.ExtensionNotFound:is_ca=False
    return {'thumbprint':thumbprint,'sha256':digest,'self_issued':certificate.subject==certificate.issuer,'code_signing':code_signing,'is_ca':is_ca}


def private_directory(path):
    path=Path(path).absolute()
    if any(parent.is_symlink() for parent in (path,*path.parents)):raise ValueError('Signing cache symlink refused')
    path.mkdir(mode=0o700,parents=True,exist_ok=True)
    if path.stat().st_mode&0o077:raise ValueError('Signing cache requires private permissions')
    return path


def prepare(entries,certificate,cache,timestamp_server=''):
    if not isinstance(entries,list) or not entries or len(entries)>2000:raise ValueError('Explicit bounded code manifest required')
    thumbprint,certificate_sha=certificate_identity(certificate)
    files=[];seen=set();total=0
    for entry in entries:
        path=relative(entry['path']);source=Path(entry['source']).absolute()
        if path.casefold() in seen:raise ValueError('Case-insensitive artifact collision')
        seen.add(path.casefold())
        if any(parent.is_symlink() for parent in (source,*source.parents)) or not source.is_file():raise ValueError('Regular source files required')
        if source.stat().st_size>8*1024*1024:raise ValueError('Signing source file too large')
        if source.suffix.lower() not in ('.ps1','.psm1','.psd1','.ps1xml') and path not in ('lib/data/job-schema.sql','lib/data/mail-translations.json'):
            raise ValueError('Only code and declared shared library data enter signing batches')
        data=source.read_bytes();digest=hashlib.sha256(data).hexdigest()
        total+=len(data)
        if total>32*1024*1024:raise ValueError('Signing batch too large')
        if entry.get('sha256',digest)!=digest:raise ValueError('Approved source hash changed')
        files.append({'path':path,'sha256':digest,'content_base64':base64.b64encode(data).decode('ascii')})
    files.sort(key=lambda value:value['path'])
    identity={'schema':1,'certificate_thumbprint':thumbprint,'certificate_sha256':certificate_sha,
              'timestamp_server':timestamp_server,'files':[{k:f[k] for k in ('path','sha256')} for f in files]}
    batch=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    directory=private_directory(private_directory(cache)/batch)
    signed=private_directory(directory/'signed')
    for entry in files:private_directory(signed/PurePosixPath(entry['path']).parent)
    expected=directory/'source-manifest.json'
    if expected.is_symlink():raise ValueError('Signing source manifest symlink refused')
    expected.write_text(json.dumps(identity,indent=2)+'\n');expected.chmod(0o600)
    return {**identity,'batch_id':batch,'files':files,'signed_root':str(signed),'source_manifest':str(expected)}


def verify(directory,expected):
    directory=Path(directory)
    receipt_path=directory/'signed-manifest.json'
    if receipt_path.is_symlink():raise ValueError('Signing receipt symlink refused')
    receipt=json.loads(receipt_path.read_text())
    if receipt.get('schema')!=1 or receipt.get('certificate_thumbprint')!=expected['certificate_thumbprint']:
        raise ValueError('Signing receipt identity mismatch')
    rows=receipt.get('files',[])
    if not isinstance(rows,list) or len(rows)!=len(expected['files']):raise ValueError('Signing receipt file set mismatch')
    indexed={relative(row['path']):row for row in rows}
    if len(indexed)!=len(rows):raise ValueError('Duplicate signed artifact')
    for source in expected['files']:
        row=indexed.get(source['path']);path=directory/relative(source['path'])
        if row is None or row.get('source_sha256')!=source['sha256']:raise ValueError('Signing source identity mismatch')
        if any(parent.is_symlink() for parent in (path,*path.parents)):raise ValueError('Signed artifact symlink refused')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=row.get('signed_sha256'):raise ValueError('Signed artifact transport checksum mismatch')
    # Authenticode is verified on the signer and again on the execution host.
    # This controller-side check verifies receipt/source mapping and byte transport.
    return True


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    prepare_args=sub.add_parser('prepare');group=prepare_args.add_mutually_exclusive_group(required=True)
    group.add_argument('--library',type=Path);group.add_argument('--manifest',type=Path)
    prepare_args.add_argument('--certificate',type=Path,required=True);prepare_args.add_argument('--cache',type=Path,required=True)
    prepare_args.add_argument('--timestamp-server',default='')
    verify_args=sub.add_parser('verify');verify_args.add_argument('--directory',type=Path,required=True);verify_args.add_argument('--expected',type=Path,required=True)
    cert_args=sub.add_parser('certificate');cert_args.add_argument('--path',type=Path,required=True)
    args=parser.parse_args();os.umask(0o077)
    if args.command=='prepare':
        entries=source_files(args.library) if args.library else json.loads(args.manifest.read_text())
        print(json.dumps(prepare(entries,args.certificate,args.cache,args.timestamp_server)))
    elif args.command=='verify':
        verify(args.directory,json.loads(args.expected.read_text()));print('{"verified":true}')
    else:print(json.dumps(certificate_info(args.path)))
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError,KeyError):print('Signing artifact preparation/verification failed; no key material was read.',file=sys.stderr);sys.exit(1)
