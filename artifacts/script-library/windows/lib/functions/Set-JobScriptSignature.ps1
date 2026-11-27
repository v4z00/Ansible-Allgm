function Set-JobScriptSignature {
    param(
        [Parameter(Mandatory)][string]$Root,
        [Parameter(Mandatory)][object[]]$Files,
        [Parameter(Mandatory)]$Certificate,
        [string]$TimestampServer = ''
    )
    if (-not $Certificate.HasPrivateKey) { throw 'Signing requires the declared private key.' }
    if (Test-JobSignedBundle -Root $Root -Files $Files -Thumbprint $Certificate.Thumbprint) {
        return [IO.File]::ReadAllText((Join-Path $Root 'signed-manifest.json'), [Text.Encoding]::UTF8) | ConvertFrom-Json
    }
    if ($TimestampServer) {
        $uri = [Uri]$TimestampServer
        if (-not $uri.IsAbsoluteUri -or $uri.Scheme -notin @('http','https') -or $uri.UserInfo) { throw 'Invalid timestamp service URI.' }
    }
    # Validate every source hash before changing the first artifact.
    $seen = @{}
    foreach ($entry in $Files) {
        if ($entry.sha256 -notmatch '^[a-fA-F0-9]{64}$' -or $seen.ContainsKey([string]$entry.path)) { throw 'Invalid or duplicate artifact manifest entry.' }
        $seen[[string]$entry.path] = $true
        $path = Resolve-JobSigningPath -Root $Root -RelativePath $entry.path
        if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $entry.sha256) { throw 'Unsigned source hash differs from the reviewed manifest.' }
    }
    $result = @()
    foreach ($entry in $Files) {
        $path = Resolve-JobSigningPath -Root $Root -RelativePath $entry.path
        $signed = [IO.Path]::GetExtension($path) -in @('.ps1','.psm1','.psd1','.ps1xml')
        if ($signed) {
            $options = @{ LiteralPath=$path; Certificate=$Certificate; HashAlgorithm='SHA256'; IncludeChain='NotRoot'; ErrorAction='Stop' }
            if ($TimestampServer) { $options.TimestampServer = $TimestampServer }
            $signature = Set-AuthenticodeSignature @options
            if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Thumbprint -ne $Certificate.Thumbprint) {
                throw 'A signed artifact failed Authenticode validation.'
            }
        }
        $result += @{ path=$entry.path; source_sha256=$entry.sha256; signed_sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant(); signed=$signed }
    }
    $receipt = @{ schema=1; certificate_thumbprint=$Certificate.Thumbprint; files=@($result) }
    $destination = Join-Path $Root 'signed-manifest.json'
    $temporary = $destination + '.' + [Guid]::NewGuid().ToString('N') + '.tmp'
    try {
        [IO.File]::WriteAllText($temporary, (ConvertTo-Json -InputObject $receipt -Depth 20), (New-Object Text.UTF8Encoding($false)))
        if ([IO.File]::Exists($destination)) { [IO.File]::Replace($temporary,$destination,[NullString]::Value) }
        else { [IO.File]::Move($temporary,$destination) }
    }
    finally { if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary -Force } }
    return $receipt
}
