function Test-JobSignedBundle {
    param(
        [Parameter(Mandatory)][string]$Root,
        [Parameter(Mandatory)][object[]]$Files,
        [Parameter(Mandatory)][string]$Thumbprint
    )
    try {
        $receiptPath = Join-Path $Root 'signed-manifest.json'
        $receipt = [IO.File]::ReadAllText($receiptPath, [Text.Encoding]::UTF8) | ConvertFrom-Json
        if ($receipt.schema -ne 1 -or $receipt.certificate_thumbprint -ne $Thumbprint -or @($receipt.files).Count -ne $Files.Count) { return $false }
        foreach ($expected in $Files) {
            $rows = @($receipt.files | Where-Object path -CEQ $expected.path)
            if ($rows.Count -ne 1 -or $rows[0].source_sha256 -ne $expected.sha256) { return $false }
            $path = Resolve-JobSigningPath -Root $Root -RelativePath $expected.path
            if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $rows[0].signed_sha256) { return $false }
            if ([IO.Path]::GetExtension($path) -in @('.ps1','.psm1','.psd1','.ps1xml')) {
                $signature = Get-AuthenticodeSignature -LiteralPath $path
                if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Thumbprint -ne $Thumbprint) { return $false }
            }
        }
        return $true
    }
    catch { return $false }
}
