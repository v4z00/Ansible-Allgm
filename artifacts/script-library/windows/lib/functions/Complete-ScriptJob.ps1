function Complete-ScriptJob {
    param(
        [Parameter(Mandatory)]$Job,
        [Parameter(Mandatory)][ValidateSet('success','warning','failed','skipped')][string]$Status,
        [Parameter(Mandatory)][int]$ExitCode,
        [string]$Summary = ''
    )
    $Status = $Status.ToLowerInvariant()
    if (($Status -eq 'failed') -eq ($ExitCode -eq 0)) { throw 'Job status and exit code disagree.' }
    $store = $Job.Store
    $source = ConvertTo-JobSqlLiteral $store.Source
    $epoch = ConvertTo-JobSqlLiteral $store.Epoch
    $run = ConvertTo-JobSqlLiteral $Job.RunId
    $state = ConvertTo-JobSqlLiteral $Status
    $message = ConvertTo-JobSqlLiteral (ConvertTo-JobSafeText $Summary)
    $now = ConvertTo-JobSqlLiteral (Get-JobTimestamp)
    $duration = ConvertTo-JobSqlLiteral ([Math]::Max(0, (Get-JobTimestamp) - $Job.Started))
    $event = Get-JobEventSql -Store $store -RunId $Job.RunId -Kind finish -OnlyAfterChange
    $sql = @"
BEGIN IMMEDIATE;
UPDATE runs SET status=$state,finished=$now,activity=$now,exit_code=$ExitCode,
 summary=$message,duration_seconds=$duration
WHERE source=$source AND epoch=$epoch AND run_id=$run AND status='running';
$event
SELECT changes() AS updated;
COMMIT;
"@
    $result = @(Invoke-JobSql -Store $store -Sql $sql)
    if ($result.Count -ne 1 -or $result[0].updated -ne 1) { throw 'Job is not running.' }
}
