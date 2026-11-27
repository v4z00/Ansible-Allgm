function Get-GpoRegistrySnapshot {
    param([Parameter(Mandatory)][string]$Root)
    # An inaccessible SYSVOL is a failure, never evidence of an empty policy.
    $null = Get-Item -LiteralPath $Root -ErrorAction Stop
    $path = Join-Path $Root 'Machine\Registry.pol'
    try { $bytes = [IO.File]::ReadAllBytes($path) }
    catch [IO.FileNotFoundException] { return @{} }
    catch [IO.DirectoryNotFoundException] { return @{} }
    return Read-GpoRegistryPolicy -Bytes $bytes
}
