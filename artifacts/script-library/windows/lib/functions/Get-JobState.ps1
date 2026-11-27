function Get-JobState {
    param(
        [Parameter(Mandatory)]$Store,
        [ValidateLength(1,160)][string]$Name
    )
    $filter = if ($Name) { ' AND r.job=' + (ConvertTo-JobSqlLiteral $Name) } else { '' }
    $sql = @"
SELECT r.* FROM runs r WHERE NOT EXISTS(
 SELECT 1 FROM runs n WHERE n.source=r.source AND n.job=r.job
 AND (n.started>r.started OR (n.started=r.started AND n.rowid>r.rowid)))
$filter ORDER BY r.source,r.job;
"@
    Invoke-JobSql -Store $Store -Sql $sql
}
