function Resolve-JobSigningPath {
    param([Parameter(Mandatory)][string]$Root, [Parameter(Mandatory)][string]$RelativePath, [switch]$AllowMissing)
    $parts = $RelativePath -split '/'
    if (-not $parts.Count) { throw 'An explicit artifact path is required.' }
    foreach ($part in $parts) {
        if (-not $part -or $part -in @('.','..') -or $part -match '[\\:*?"<>|\x00-\x1F]' -or $part -ne $part.TrimEnd(' ','.')) {
            throw 'Invalid signing artifact path.'
        }
    }
    $base = [IO.Path]::GetFullPath($Root).TrimEnd([char[]]@('\','/'))
    $path = [IO.Path]::GetFullPath((Join-Path $base ($parts -join [IO.Path]::DirectorySeparatorChar)))
    if (-not $path.StartsWith($base + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Signing path escapes the selected root.'
    }
    $currentPath = $path
    while ($currentPath.Length -ge $base.Length) {
        if (Test-Path -LiteralPath $currentPath) {
            $current = Get-Item -LiteralPath $currentPath -Force -ErrorAction Stop
            if ($currentPath -eq $path -and $current.PSIsContainer) { throw 'Only files can be signed.' }
            if ($current.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Signing paths must not contain reparse points.' }
        }
        elseif ($currentPath -eq $path -and -not $AllowMissing) { throw 'Signing source file is missing.' }
        if ($currentPath -eq $base) { break }
        $parent = [IO.Directory]::GetParent($currentPath)
        if (-not $parent) { throw 'Signing root was not reached.' }
        $currentPath = $parent.FullName
    }
    return [IO.Path]::GetFullPath((Join-Path $base ($parts -join [IO.Path]::DirectorySeparatorChar)))
}
