function Assert-JobPrivatePath {
    param([Parameter(Mandatory)][string]$Path)
    $entry = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
    if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Private paths must not be reparse points.' }
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) { return }
    $allowed = @('S-1-5-18', 'S-1-5-32-544', [Security.Principal.WindowsIdentity]::GetCurrent().User.Value)
    $acl = Get-Acl -LiteralPath $Path
    foreach ($rule in $acl.GetAccessRules($true, $true, [Security.Principal.SecurityIdentifier])) {
        if ($rule.AccessControlType -eq 'Allow' -and $rule.IdentityReference.Value -notin $allowed) {
            throw 'Private job data permits access by an undeclared principal.'
        }
    }
}
