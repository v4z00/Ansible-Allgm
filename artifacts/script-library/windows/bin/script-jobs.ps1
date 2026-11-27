#requires -Version 5.1
param(
    [Parameter(Mandatory)][ValidateSet('init','latest','export','prune','security-alert','security-retry')][string]$Command,
    [string]$Database = 'C:\ProgramData\ScriptJobs\jobs.sqlite3',
    [string]$Sqlite = (Join-Path (Split-Path -Parent $PSScriptRoot) 'runtime/sqlite3.exe'),
    [string[]]$ConfigFile = @(),
    [string]$EventKey,
    [string]$Job,
    [string]$Epoch,
    [long]$After = 0,
    [int]$Limit = 100,
    [int]$Days = 90
)
$ErrorActionPreference = 'Stop'
try {
    Import-Module (Join-Path (Split-Path -Parent $PSScriptRoot) 'lib/ScriptLibrary.psm1') -DisableNameChecking
    if ($Command -in @('latest','export')) {
        if (-not (Test-Path -LiteralPath $Database -PathType Leaf)) {
            '{"status":"not_attached","schema":1}'
            exit 3
        }
        $store = Open-JobStore -Database $Database -Sqlite $Sqlite
    }
    else { $store = New-JobStore -Database $Database -Sqlite $Sqlite }
    $exitCode = 0
    switch ($Command) {
        init { $result = @{ schema = 1; epoch = $store.Epoch } }
        latest {
            $filter = if ($Job) { @{ Name = $Job } } else { @{} }
            $result = @(Get-JobState -Store $store @filter)
        }
        export { $result = Export-JobEvents -Store $store -After $After -Limit $Limit -Epoch $Epoch }
        prune { $result = @{ removed = Remove-JobHistory -Store $store -Days $Days } }
        security-alert {
            $config = Get-JobConfig -Path $ConfigFile
            # Alert details are data on stdin, never executable script/command arguments.
            $text = [Console]::In.ReadToEnd()
            if ($text.Length -gt 65536) { throw 'Security message too large.' }
            $event = $text | ConvertFrom-Json
            $details = if ($event.PSObject.Properties['details']) { [string]$event.details } else { '' }
            $result = Send-SecurityAlert -Store $store -Config $config -EventKey $EventKey -Job $event.job -Summary $event.summary -Details $details
            if ($result.pending) { $exitCode = 1 }
        }
        security-retry {
            $config = Get-JobConfig -Path $ConfigFile
            $result = Send-SecurityAlertQueue -Store $store -Config $config
            if ($result.pending) { $exitCode = 1 }
        }
    }
    ConvertTo-Json -InputObject $result -Depth 30 -Compress
    exit $exitCode
}
catch {
    # No raw exceptions: WinRM, HTTP and SMTP errors can include credentials.
    '{"status":"job_helper_failed","schema":1}'
    exit 1
}
