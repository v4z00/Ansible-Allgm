param([string]$Root,[string]$Directory)
$ErrorActionPreference = 'Stop'
Import-Module (Join-Path $Root 'artifacts/script-library/windows/lib/ScriptLibrary.psm1') -DisableNameChecking
$module = Get-Module ScriptLibrary
& $module {
    $script:signCount = 0
    $script:rejectSignature = $false
    function script:Set-AuthenticodeSignature {
        [CmdletBinding()]
        param($LiteralPath,$Certificate,$HashAlgorithm,$IncludeChain,$TimestampServer)
        $script:signCount++
        [IO.File]::AppendAllText($LiteralPath, "`n# synthetic signature", [Text.Encoding]::UTF8)
        $status = if ($script:rejectSignature) { 'NotTrusted' } else { 'Valid' }
        return [pscustomobject]@{ Status=$status; SignerCertificate=$Certificate }
    }
    function script:Get-AuthenticodeSignature {
        param($LiteralPath)
        return [pscustomobject]@{ Status='Valid'; SignerCertificate=[pscustomobject]@{Thumbprint=('A' * 40)} }
    }
}
$certificate = [pscustomobject]@{ HasPrivateKey=$true; Thumbprint=('A' * 40) }
$null = New-Item -ItemType Directory -Path (Join-Path $Directory 'lib/data') -Force
$rows = @()
foreach ($name in @("quote' script.ps1",'lib/module.psm1','lib/data/mail-translations.json')) {
    $path = Join-Path $Directory $name
    [IO.File]::WriteAllText($path, '# synthetic source', [Text.Encoding]::UTF8)
    $rows += @{ path=$name; sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() }
}
$receipt = Set-JobScriptSignature -Root $Directory -Files $rows -Certificate $certificate
if (@($receipt.files).Count -ne 3) { throw 'Signing receipt incomplete.' }
if (-not (Test-JobSignedBundle -Root $Directory -Files $rows -Thumbprint $certificate.Thumbprint)) { throw 'Signed bundle failed validation.' }
$null = Set-JobScriptSignature -Root $Directory -Files $rows -Certificate $certificate
if ((& $module { $script:signCount }) -ne 2) { throw 'Unchanged cache was re-signed.' }
[IO.File]::AppendAllText((Join-Path $Directory $rows[0].path), 'tamper')
if (Test-JobSignedBundle -Root $Directory -Files $rows -Thumbprint $certificate.Thumbprint) { throw 'Tampered artifact accepted.' }
$failed = $false
try { $null = Set-JobScriptSignature -Root $Directory -Files $rows -Certificate $certificate }
catch { $failed = $true }
if (-not $failed -or (& $module { $script:signCount }) -ne 2) { throw 'Source tampering was signed.' }
foreach ($path in @('../escape.ps1','lib/file.ps1:stream','C:\escape.ps1')) {
    $failed = $false
    try { $null = Resolve-JobSigningPath -Root $Directory -RelativePath $path -AllowMissing }
    catch { $failed = $true }
    if (-not $failed) { throw 'Unsafe signing path accepted.' }
}
$fresh = Join-Path $Directory 'fresh'
$null = New-Item -ItemType Directory -Path $fresh
$path = Join-Path $fresh 'script.ps1'
[IO.File]::WriteAllText($path, '# unsigned source', [Text.Encoding]::UTF8)
$entries = @(@{path='script.ps1';sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()})
& $module { $script:rejectSignature = $true }
$failed = $false
try { $null = Set-JobScriptSignature -Root $fresh -Files $entries -Certificate $certificate }
catch { $failed = $true }
if (-not $failed -or (Test-Path -LiteralPath (Join-Path $fresh 'signed-manifest.json'))) { throw 'Untrusted signing result was marked ready.' }
'SIGNING_FIXTURE_OK'
