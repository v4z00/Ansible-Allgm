function Start-ScriptJob {
    param(
        [Parameter(Mandatory)]$Store,
        [Parameter(Mandatory)][ValidatePattern('^[A-Za-z0-9_.:-]{1,160}$')][string]$Name,
        [ValidateSet('general','vzdump','ansible','administration','security')][string]$Category = 'general'
    )
    $Category = $Category.ToLowerInvariant()
    $runId = [Guid]::NewGuid().ToString()
    $values = @($Store.Source, $Store.Epoch, $runId, $Name, $Category, 'running', (Get-JobTimestamp))
    $quoted = @($values | ForEach-Object { ConvertTo-JobSqlLiteral $_ })
    $event = Get-JobEventSql -Store $Store -RunId $runId -Kind start
    $sql = @"
BEGIN IMMEDIATE;
INSERT INTO runs(source,epoch,run_id,job,category,status,started,activity)
VALUES($($quoted[0]),$($quoted[1]),$($quoted[2]),$($quoted[3]),$($quoted[4]),$($quoted[5]),$($quoted[6]),$($quoted[6]));
$event
COMMIT;
"@
    $null = Invoke-JobSql -Store $Store -Sql $sql
    return @{ Store = $Store; RunId = $runId; Started = [double]$values[6] }
}
