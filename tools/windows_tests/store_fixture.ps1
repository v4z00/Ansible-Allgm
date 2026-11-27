param([string]$Root, [string]$Directory, [string]$Sqlite, [string]$Case = 'store', [int]$Port)
$ErrorActionPreference = 'Stop'
Import-Module (Join-Path $Root 'artifacts/script-library/windows/lib/ScriptLibrary.psm1') -Force -DisableNameChecking
[Threading.Thread]::CurrentThread.CurrentCulture = 'de-DE'
$database = Join-Path $Directory "job ' fixture.sqlite3"
$store = New-JobStore -Database $database -Sqlite $Sqlite -Source 'fixture.example.invalid'
if ($Case -eq 'store') {
    $missing = Join-Path $Directory 'missing.sqlite3'
    try { $null = Open-JobStore -Database $missing -Sqlite $Sqlite; throw 'Expected failure.' }
    catch { if (Test-Path -LiteralPath $missing) { throw 'Read query created a database.' } }
    $job = Start-ScriptJob -Store $store -Name 'fixture-job' -Category General
    $text = "value '); DROP TABLE runs; -- " + [char]0x00FC
    Set-JobItem -Job $job -Item "quote'item" -Status Success -Message $text
    Complete-ScriptJob -Job $job -Status Success -ExitCode 0 -Summary 'Completed'
    $duplicateRejected = $false
    try { Complete-ScriptJob -Job $job -Status success -ExitCode 0 }
    catch { $duplicateRejected = $true }
    if (-not $duplicateRejected) { throw 'Terminal result was overwritten.' }
    $read = Open-JobStore -Database $database -Sqlite $Sqlite
    $batch = Export-JobEvents -Store $read -Limit 2
    $batch | ConvertTo-Json -Depth 20 -Compress | Set-Content -LiteralPath (Join-Path $Directory 'first.json') -Encoding utf8
    Export-JobEvents -Store $read -After $batch.next -Epoch $read.Epoch |
        ConvertTo-Json -Depth 20 -Compress | Set-Content -LiteralPath (Join-Path $Directory 'next.json') -Encoding utf8
    $latest = @(Get-JobState -Store $read)
    if ($latest.Count -ne 1 -or $latest[0].status -ne 'success') { throw 'Latest state failed.' }
}
elseif ($Case -eq 'writer') {
    $job = Start-ScriptJob -Store $store -Name ('writer-' + [Guid]::NewGuid().ToString())
    Complete-ScriptJob -Job $job -Status success -ExitCode 0
}
elseif ($Case -eq 'security') {
    $config = @{ SECURITY_CHANNELS = @('mail','telegram') }
    $module = Get-Module ScriptLibrary
    & $module {
        $script:sent = @()
        $script:telegramFails = $true
        function script:Send-JobNotification {
            param($Channel, $Body, $Config)
            if ($Channel -eq 'telegram' -and $script:telegramFails) { throw 'Synthetic outage.' }
            $script:sent += $Channel
        }
    }
    $first = Send-SecurityAlert -Store $store -Config $config -EventKey "provider:42:'" -Job 'event-check' -Summary 'Attention' -Details 'secret=synthetic-value'
    if ($first.pending -ne 1) { throw 'Failed channel was acknowledged.' }
    & $module { $script:telegramFails = $false }
    $second = Send-SecurityAlert -Store $store -Config $config -EventKey "provider:42:'" -Job 'event-check' -Summary 'Duplicate'
    if ($second.pending -ne 0) { throw 'Retry did not drain queue.' }
    $sent = @(& $module { $script:sent })
    if (($sent -join ',') -ne 'mail,telegram') { throw 'A successful channel was resent.' }
    $rows = @(Invoke-JobSql -Store $store -Sql 'SELECT COUNT(*) AS total FROM security_alerts;')
    if ($rows[0].total -ne 1) { throw 'Duplicate alert persisted.' }
    Export-JobEvents -Store (Open-JobStore -Database $database -Sqlite $Sqlite) |
        ConvertTo-Json -Depth 20 -Compress | Set-Content -LiteralPath (Join-Path $Directory 'security.json') -Encoding utf8
}
elseif ($Case -eq 'retention') {
    $job = Start-ScriptJob -Store $store -Name 'old-job'
    Complete-ScriptJob -Job $job -Status success -ExitCode 0
    $null = Invoke-JobSql -Store $store -Sql 'UPDATE runs SET finished=1;'
    $null = Start-ScriptJob -Store $store -Name 'running-job'
    $removed = Remove-JobHistory -Store $store
    if ($removed -ne 1) { throw 'Retention deleted unexpected rows.' }
    $batch = Export-JobEvents -Store $store
    if (-not $batch.gap) { throw 'Pruned history gap was hidden.' }
    $latest = @(Get-JobState -Store $store)
    if ($latest.Count -ne 1 -or $latest[0].status -ne 'running') { throw 'Running job was pruned.' }
}
elseif ($Case -eq 'runner') {
    $program = Join-Path $Directory "program ' fixture.ps1"
    [IO.File]::WriteAllText($program, 'Write-Output "secret=only-in-private-log"; exit 7', [Text.Encoding]::UTF8)
    $spec = Join-Path $Directory 'runner.json'
    @{ name='process-job'; program=$program; arguments=@(); config_files=@(); max_runtime_seconds=10 } |
        ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $spec -Encoding utf8
    $code = Invoke-ScriptJob -Store $store -SpecFile $spec -PowerShell (Get-Process -Id $PID).Path
    if ($code -ne 7) { throw 'Child exit code was lost.' }
    $latest = @(Get-JobState -Store $store)
    if ($latest[0].status -ne 'failed' -or $latest[0].exit_code -ne 7) { throw 'Process failure was not recorded.' }
    $batch = Export-JobEvents -Store $store | ConvertTo-Json -Depth 20
    if ($batch.Contains('only-in-private-log')) { throw 'Raw output leaked into events.' }
    [IO.File]::WriteAllText($program, 'Start-Sleep -Seconds 20', [Text.Encoding]::UTF8)
    @{ name='process-job'; program=$program; max_runtime_seconds=1 } |
        ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $spec -Encoding utf8
    $code = Invoke-ScriptJob -Store $store -SpecFile $spec -PowerShell (Get-Process -Id $PID).Path
    if ($code -ne 124) { throw 'Timeout was not a failure.' }
}
elseif ($Case -eq 'local-check') {
    $job = Start-ScriptJob -Store $store -Name 'successful-job'
    Complete-ScriptJob -Job $job -Status success -ExitCode 0
    $entries = @(
        @{ job='successful-job'; max_age_seconds=3600; max_runtime_seconds=60 },
        @{ job='missing-job'; max_age_seconds=3600; max_runtime_seconds=60 }
    )
    $lines = @(Get-JobLocalCheck -Store (Open-JobStore -Database $database -Sqlite $Sqlite) -Jobs $entries -SecurityOutbox)
    [IO.File]::WriteAllLines((Join-Path $Directory 'checks.txt'), [string[]]$lines)
}
elseif ($Case -in @('smtp','smtp-starttls')) {
    $mode = if ($Case -eq 'smtp') { 'none' } else { 'starttls' }
    $cfg = @{ SMTP_HOST = '127.0.0.1'; SMTP_PORT = $Port; SMTP_TLS = $mode; SMTP_AUTH = 'none'; SMTP_FROM = 'sender@example.invalid'; MAIL_TO = 'receiver@example.invalid' }
    $body = [string][char]0x00C4 + [char]0x00D6 + [char]0x00DC + [char]0x00E4 + [char]0x00F6 + [char]0x00FC + [char]0x00DF
    Send-JobNotification -Channel mail -Body $body -Config $cfg
}
'FIXTURE_OK'
