function Send-SecurityAlertQueue {
    param(
        [Parameter(Mandatory)]$Store,
        [Parameter(Mandatory)][hashtable]$Config,
        [string]$ReportId,
        [ValidateRange(1,1000)][int]$Limit = 100
    )
    $channels = @(Get-SecurityAlertChannels -Config $Config | ForEach-Object { ConvertTo-JobSqlLiteral $_ }) -join ','
    $pendingFilter = "p.category='security' AND d.status!='sent' AND d.channel COLLATE NOCASE IN ($channels)"
    $now = ConvertTo-JobSqlLiteral (Get-JobTimestamp)
    $selection = if ($ReportId) { ' AND p.id=' + (ConvertTo-JobSqlLiteral $ReportId) } else { '' }
    $rows = @(Invoke-JobSql -Store $Store -Sql "SELECT p.id,p.body,d.channel FROM reports p JOIN deliveries d ON d.report_id=p.id WHERE $pendingFilter AND d.lease_until<$now$selection ORDER BY p.created,d.channel LIMIT $Limit;")
    $failed = $false
    foreach ($row in $rows) {
        $id = ConvertTo-JobSqlLiteral $row.id
        $channel = ConvertTo-JobSqlLiteral $row.channel
        $now = ConvertTo-JobSqlLiteral (Get-JobTimestamp)
        $lease = ConvertTo-JobSqlLiteral ((Get-JobTimestamp) + 300)
        $claimed = @(Invoke-JobSql -Store $Store -Sql "BEGIN IMMEDIATE; UPDATE deliveries SET status='sending',attempts=attempts+1,lease_until=$lease,updated=$now WHERE report_id=$id AND channel=$channel AND status!='sent' AND lease_until<$now; SELECT changes() AS claimed; COMMIT;")
        if ($claimed[0].claimed -ne 1) { continue }
        $state = 'sent'
        try { Send-JobNotification -Channel $row.channel -Body $row.body -Config $Config }
        catch { $state = 'pending'; $failed = $true }
        $now = ConvertTo-JobSqlLiteral (Get-JobTimestamp)
        $null = Invoke-JobSql -Store $Store -Sql "UPDATE deliveries SET status='$state',lease_until=0,updated=$now WHERE report_id=$id AND channel=$channel;"
    }
    $count = @(Invoke-JobSql -Store $Store -Sql "SELECT COUNT(*) AS pending FROM deliveries d JOIN reports p ON p.id=d.report_id WHERE $pendingFilter;")
    return @{ pending = [int]$count[0].pending; failed = $failed }
}
