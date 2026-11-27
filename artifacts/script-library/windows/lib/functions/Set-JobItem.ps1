function Set-JobItem {
    param(
        [Parameter(Mandatory)]$Job,
        [Parameter(Mandatory)][ValidateLength(1,160)][string]$Item,
        [Parameter(Mandatory)][ValidateSet('running','success','warning','failed','skipped')][string]$Status,
        [string]$Message = ''
    )
    $Status = $Status.ToLowerInvariant()
    $store = $Job.Store
    $source = ConvertTo-JobSqlLiteral $store.Source
    $epoch = ConvertTo-JobSqlLiteral $store.Epoch
    $run = ConvertTo-JobSqlLiteral $Job.RunId
    $itemSql = ConvertTo-JobSqlLiteral $Item
    $state = ConvertTo-JobSqlLiteral $Status
    $text = ConvertTo-JobSqlLiteral (ConvertTo-JobSafeText $Message)
    $now = ConvertTo-JobSqlLiteral (Get-JobTimestamp)
    $event = Get-JobEventSql -Store $store -RunId $Job.RunId -Kind item -OnlyAfterChange
    $sql = @"
BEGIN IMMEDIATE;
INSERT OR REPLACE INTO items(source,epoch,run_id,item_id,status,message,updated)
SELECT $source,$epoch,$run,$itemSql,$state,$text,$now
WHERE EXISTS(SELECT 1 FROM runs WHERE source=$source AND epoch=$epoch AND run_id=$run AND status='running');
UPDATE runs SET activity=$now WHERE source=$source AND epoch=$epoch AND run_id=$run AND status='running';
$event
SELECT changes() AS updated;
COMMIT;
"@
    $result = @(Invoke-JobSql -Store $store -Sql $sql)
    if ($result.Count -ne 1 -or $result[0].updated -ne 1) { throw 'Job is not running.' }
}
