function Save-SecurityAlert {
    param(
        [Parameter(Mandatory)]$Store,
        [Parameter(Mandatory)][ValidateLength(1,256)][string]$EventKey,
        [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9_.:-]{1,160}$')][string]$Job,
        [Parameter(Mandatory)][string]$Summary,
        [string]$Details = '',
        [Parameter(Mandatory)][ValidateSet('mail','telegram')][string[]]$Channels
    )
    if ($EventKey -match '[\x00-\x1F]') { throw 'Invalid stable event key.' }
    $eventSql = ConvertTo-JobSqlLiteral $EventKey
    $reportId = [Guid]::NewGuid().ToString()
    $report = ConvertTo-JobSqlLiteral $reportId
    $runId = [Guid]::NewGuid().ToString()
    $run = ConvertTo-JobSqlLiteral $runId
    $source = ConvertTo-JobSqlLiteral $Store.Source
    $epoch = ConvertTo-JobSqlLiteral $Store.Epoch
    $name = ConvertTo-JobSqlLiteral $Job
    $now = ConvertTo-JobSqlLiteral (Get-JobTimestamp)
    $safeSummary = ConvertTo-JobSafeText $Summary -Limit 200
    $text = ConvertTo-JobSqlLiteral $safeSummary
    $body = 'Security alert ' + [char]::ConvertFromUtf32(0x274C) + "`n" + (ConvertTo-JobSafeText $Store.Source -Limit 160) + ' / ' + $Job + "`n" + $safeSummary
    if ($Details) { $body += "`n" + (ConvertTo-JobSafeText $Details) }
    $bodySql = ConvertTo-JobSqlLiteral $body
    $event = Get-JobEventSql -Store $Store -RunId $runId -Kind finish -OnlyAfterChange
    $deliverySql = @($Channels | Select-Object -Unique | ForEach-Object {
        $channel = ConvertTo-JobSqlLiteral $_
        "INSERT INTO deliveries SELECT $report,$channel,'pending',0,0,$now WHERE EXISTS(SELECT 1 FROM reports WHERE id=$report);"
    }) -join "`n"
    $sql = @"
BEGIN IMMEDIATE;
INSERT INTO runs(source,epoch,run_id,job,category,status,started,activity,finished,exit_code,summary,duration_seconds)
SELECT $source,$epoch,$run,$name,'security','failed',$now,$now,$now,1,$text,0
WHERE NOT EXISTS(SELECT 1 FROM security_alerts WHERE event_key=$eventSql);
$event
INSERT INTO reports SELECT $report,'security',$now,$bodySql
WHERE NOT EXISTS(SELECT 1 FROM security_alerts WHERE event_key=$eventSql);
INSERT INTO report_runs SELECT $report,$source,$epoch,$run WHERE EXISTS(SELECT 1 FROM reports WHERE id=$report);
$deliverySql
INSERT INTO security_alerts SELECT $eventSql,$report WHERE EXISTS(SELECT 1 FROM reports WHERE id=$report);
SELECT report_id FROM security_alerts WHERE event_key=$eventSql;
COMMIT;
"@
    $rows = @(Invoke-JobSql -Store $Store -Sql $sql)
    return [string]$rows[0].report_id
}
