#Requires -Version 5.1
param(
    [Parameter(Mandatory)][string]$ConfigPath,
    [string]$Sqlite = (Join-Path (Split-Path -Parent $PSScriptRoot) 'runtime/sqlite3.exe')
)
$ErrorActionPreference = 'Stop'
try {
    Import-Module (Join-Path (Split-Path -Parent $PSScriptRoot) 'lib/ScriptLibrary.psm1') -DisableNameChecking
    $config = Get-JobConfig -Path $ConfigPath
    $store = Open-JobStore -Database $config['database'] -Sqlite $Sqlite
    Get-JobLocalCheck -Store $store -Jobs $config['jobs'] -SecurityOutbox:$config['security_outbox']
}
catch { '3 "Script jobs data" - Configuration or local database unavailable' }
