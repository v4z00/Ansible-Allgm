function Get-JobSigningCertificate {
    param(
        [Parameter(Mandatory)][ValidatePattern('^[A-Fa-f0-9]{40}$')][string]$Thumbprint,
        [ValidateSet('CurrentUser','LocalMachine')][string]$StoreLocation = 'LocalMachine'
    )
    $certificate = Get-Item -LiteralPath ('Cert:\' + $StoreLocation + '\My\' + $Thumbprint) -ErrorAction Stop
    $now = [DateTime]::UtcNow
    if (-not $certificate.HasPrivateKey -or $certificate.NotBefore.ToUniversalTime() -gt $now -or $certificate.NotAfter.ToUniversalTime() -le $now) {
        throw 'The selected signing certificate requires a usable, current private key.'
    }
    $codeSigning = @($certificate.Extensions | Where-Object { $_.Oid.Value -eq '2.5.29.37' } |
        ForEach-Object { $_.EnhancedKeyUsages } | Where-Object Value -eq '1.3.6.1.5.5.7.3.3')
    if (-not $codeSigning.Count) { throw 'The selected certificate has no code-signing EKU.' }
    return $certificate
}
