function Remove-JobHistory {
    param([Parameter(Mandatory)]$Store, [ValidateRange(1,3650)][int]$Days = 90)
    $cutoff = ConvertTo-JobSqlLiteral ((Get-JobTimestamp) - $Days * 86400)
    $sql = @"
BEGIN IMMEDIATE;
CREATE TEMP TABLE expired_runs AS SELECT source,epoch,run_id FROM runs WHERE finished IS NOT NULL AND finished<$cutoff;
UPDATE meta SET value=CAST(MAX(CAST(value AS INTEGER),COALESCE((SELECT MAX(e.id) FROM events e JOIN expired_runs r ON r.source=e.source AND r.epoch=e.epoch AND r.run_id=e.run_id),0)) AS TEXT) WHERE key='floor';
DELETE FROM events WHERE EXISTS(SELECT 1 FROM expired_runs r WHERE r.source=events.source AND r.epoch=events.epoch AND r.run_id=events.run_id);
DELETE FROM report_runs WHERE EXISTS(SELECT 1 FROM expired_runs r WHERE r.source=report_runs.source AND r.epoch=report_runs.epoch AND r.run_id=report_runs.run_id);
DELETE FROM runs WHERE EXISTS(SELECT 1 FROM expired_runs r WHERE r.source=runs.source AND r.epoch=runs.epoch AND r.run_id=runs.run_id);
SELECT COUNT(*) AS removed,json_group_array(json_object('source',source,'epoch',epoch,'run_id',run_id)) AS expired FROM expired_runs;
DELETE FROM reports WHERE created<$cutoff AND NOT EXISTS(SELECT 1 FROM report_runs WHERE report_id=reports.id) AND NOT EXISTS(SELECT 1 FROM deliveries WHERE report_id=reports.id AND status!='sent');
COMMIT;
"@
    $rows = @(Invoke-JobSql -Store $Store -Sql $sql)
    $logs = Join-Path (Split-Path -Parent $Store.Database) 'logs'
    $expired = ConvertFrom-Json -InputObject $rows[0].expired
    foreach ($old in $expired) {
        if ($old.source -ne $Store.Source -or $old.epoch -ne $Store.Epoch -or
            $old.run_id -notmatch '^[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$') { continue }
        foreach ($suffix in @('.log','.stderr.log')) {
            $path = Join-Path $logs ($old.run_id + $suffix)
            if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { continue }
            Assert-JobPrivatePath -Path $path
            Remove-Item -LiteralPath $path -Force -ErrorAction Stop
        }
    }
    return [int]$rows[0].removed
}
