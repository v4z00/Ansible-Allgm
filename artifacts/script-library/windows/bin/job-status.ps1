#requires -Version 5.1
param(
    [string]$Database = 'C:\ProgramData\ScriptJobs\jobs.sqlite3',
    [string]$Sqlite = (Join-Path (Split-Path -Parent $PSScriptRoot) 'runtime/sqlite3.exe'),
    [string]$Job,
    [switch]$AsJson
)
$ErrorActionPreference = 'Stop'
try {
    Import-Module (Join-Path (Split-Path -Parent $PSScriptRoot) 'lib/ScriptLibrary.psm1') -DisableNameChecking
    $store = Open-JobStore -Database $Database -Sqlite $Sqlite
    $filter = if ($Job) { @{ Name = $Job } } else { @{} }
    $rows = @(Get-JobState -Store $store @filter)
    if ($AsJson) { ConvertTo-Json -InputObject $rows -Depth 20 -Compress; exit 0 }
    $symbols = @{ success = 0x2705; failed = 0x274C; warning = 0x26A0; skipped = 0x23ED; running = 0x23F3 }
    foreach ($row in $rows) {
        $stamp = [DateTimeOffset]::FromUnixTimeMilliseconds([long]($row.started * 1000)).UtcDateTime.ToString('yyyy-MM-ddTHH:mm:ssZ', [Globalization.CultureInfo]::InvariantCulture)
        $symbol = [char]::ConvertFromUtf32($symbols[[string]$row.status])
        '{0}  {1} / {2} {3}  Exit: {4}' -f $stamp,$row.source,$row.job,$symbol,$row.exit_code
    }
    if (-not $rows.Count) { 'No job results recorded.' }
}
catch { 'Job database/helper unavailable.'; exit 3 }
