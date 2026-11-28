[CmdletBinding(SupportsShouldProcess)]
param([string]$Base, [string]$Directories, [string]$Files, [string]$TaskName, [string]$TaskDescription)

$ErrorActionPreference = 'Stop'
$knownDirectories = ConvertFrom-Json $Directories
foreach ($target in @($knownDirectories) + @(ConvertFrom-Json $Files)) {
    $path = $target
    while ($path -and $path.TrimEnd('\') -ne $Base.TrimEnd('\')) {
        if ($path -eq $target) {
            $item = Get-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue
            if ($item -and $item.PSIsContainer -ne ($target -in $knownDirectories)) {
                throw 'An existing object has the wrong type.'
            }
        }
        else {
            $item = Get-Item -LiteralPath $path -Force -ErrorAction SilentlyContinue
        }
        if ($item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw 'A profile destination contains a reparse point.'
        }
        $path = [IO.Path]::GetDirectoryName($path)
    }
    if (-not $path) { throw 'A profile destination is outside the allowed directory.' }
}
if ($TaskName) {
    $task = Get-ScheduledTask -TaskPath '\Ansible\PrivateScripts\' -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task -and $task.Description -cne $TaskDescription) {
        throw 'The requested task name belongs to an unmanaged task.'
    }
}
$Ansible.Changed = $false
