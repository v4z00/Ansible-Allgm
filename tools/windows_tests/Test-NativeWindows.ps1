#requires -Version 5.1
param([Parameter(Mandatory)][string]$Root)
$ErrorActionPreference = 'Stop'
$directory = Join-Path ([IO.Path]::GetTempPath()) ('script-library-test-' + [Guid]::NewGuid().ToString('N'))
$null = New-Item -ItemType Directory -Path $directory
$certificate = $null
try {
    # Limit fixture state to the runner identity, SYSTEM and built-in Administrators.
    $acl = New-Object Security.AccessControl.DirectorySecurity
    $acl.SetAccessRuleProtection($true,$false)
    $ids = @('S-1-5-18','S-1-5-32-544',[Security.Principal.WindowsIdentity]::GetCurrent().User.Value)
    foreach ($id in $ids) {
        $sid = New-Object Security.Principal.SecurityIdentifier($id)
        $rule = New-Object Security.AccessControl.FileSystemAccessRule($sid,'FullControl','ContainerInherit,ObjectInherit','None','Allow')
        $acl.AddAccessRule($rule)
    }
    Set-Acl -LiteralPath $directory -AclObject $acl
    $sqlite = Join-Path $Root 'artifacts/sqlite/windows/sqlite3.exe'
    foreach ($case in @('store','security','retention','runner','local-check')) {
        $target = Join-Path $directory $case
        $null = New-Item -ItemType Directory -Path $target
        & (Join-Path $Root 'tools/windows_tests/store_fixture.ps1') -Root $Root -Directory $target -Sqlite $sqlite -Case $case
        if (-not $?) { throw 'Windows store fixture failed.' }
    }
    Import-Module (Join-Path $Root 'artifacts/script-library/windows/lib/ScriptLibrary.psm1') -Force -DisableNameChecking
    $certificate = New-SelfSignedCertificate -Type CodeSigningCert -Subject ('CN=EphemeralRuntimeTest-' + [Guid]::NewGuid().ToString('N')) -CertStoreLocation Cert:\CurrentUser\My -NotAfter (Get-Date).AddDays(1) -KeyExportPolicy NonExportable
    $public = Join-Path $directory 'publisher.cer'
    $null = Export-Certificate -Cert $certificate -FilePath $public
    $null = Import-Certificate -FilePath $public -CertStoreLocation Cert:\CurrentUser\Root
    $null = Import-Certificate -FilePath $public -CertStoreLocation Cert:\CurrentUser\TrustedPublisher
    $key = Get-JobSigningCertificate -Thumbprint $certificate.Thumbprint -StoreLocation CurrentUser
    $signing = Join-Path $directory 'signing'
    $null = New-Item -ItemType Directory -Path $signing
    $path = Join-Path $signing 'fixture.ps1'
    [IO.File]::WriteAllText($path, '# Native signing fixture', (New-Object Text.UTF8Encoding($false)))
    $files = @(@{ path='fixture.ps1'; sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() })
    $null = Set-JobScriptSignature -Root $signing -Files $files -Certificate $key
    if (-not (Test-JobSignedBundle -Root $signing -Files $files -Thumbprint $key.Thumbprint)) { throw 'Native Authenticode verification failed.' }
    [IO.File]::AppendAllText($path, "`n# tamper")
    if (Test-JobSignedBundle -Root $signing -Files $files -Thumbprint $key.Thumbprint) { throw 'Tampered signature was accepted.' }
    'NATIVE_WINDOWS_RUNTIME_OK'
}
finally {
    if ($certificate) {
        foreach ($store in @('Root','TrustedPublisher','My')) {
            $path = 'Cert:\CurrentUser\' + $store + '\' + $certificate.Thumbprint
            if (Test-Path -LiteralPath $path) {
                if ($store -eq 'My') { Remove-Item -LiteralPath $path -DeleteKey -Force }
                else { Remove-Item -LiteralPath $path -Force }
            }
        }
    }
    if (Test-Path -LiteralPath $directory) { Remove-Item -LiteralPath $directory -Recurse -Force }
}
