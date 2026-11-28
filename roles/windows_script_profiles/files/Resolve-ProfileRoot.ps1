[CmdletBinding(SupportsShouldProcess)]
param([string]$Mode, [string]$LocalRoot, [string]$SysvolSubdir)

$ErrorActionPreference = 'Stop'
$Ansible.Changed = $false
if ($Mode -eq 'sysvol') {
    $machine = Get-CimInstance Win32_ComputerSystem
    if ($machine.DomainRole -notin 4, 5) { throw 'Select a domain controller for SYSVOL.' }
    $dc = Get-ADDomainController -Identity $machine.DNSHostName -Server ($machine.DNSHostName + '.' + $machine.Domain)
    if ($dc.IsReadOnly) { throw 'A writable domain controller is required.' }
    $share = Get-SmbShare -Name SYSVOL
    $base = Join-Path $share.Path ($machine.Domain + '\scripts')
    if (-not (Test-Path -LiteralPath $base -PathType Container)) { throw 'The local domain scripts directory is unavailable.' }
    if ($SysvolSubdir -notmatch '^[A-Za-z][A-Za-z0-9_-]{0,47}$' -or $SysvolSubdir -match '^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])$') {
        throw 'Use a simple managed subdirectory name under SYSVOL scripts.'
    }
    $root = Join-Path $base $SysvolSubdir
}
else {
    if ($LocalRoot -notmatch '^[A-Za-z]:\\[^\\/:*?"<>|\x00-\x1F]+(?:\\[^\\/:*?"<>|\x00-\x1F]+)*$') {
        throw 'Specify an absolute local directory below a drive root.'
    }
    $segments = $LocalRoot.Substring(3).Split('\')
    foreach ($segment in $segments) {
        if ($segment.Trim(' ', '.') -cne $segment -or $segment -match '^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(\.|$)') {
            throw 'Invalid local Windows directory.'
        }
    }
    $root = Join-Path $LocalRoot 'AnsibleProfiles'
    $base = [IO.Path]::GetPathRoot($root)
}
$Ansible.Result = @{ root = $root; base = $base; policy = [string](Get-ExecutionPolicy); system_root = $env:SystemRoot }
