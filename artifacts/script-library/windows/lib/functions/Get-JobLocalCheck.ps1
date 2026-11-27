function Get-JobLocalCheck {
    param(
        [Parameter(Mandatory)]$Store,
        [object[]]$Jobs = @(),
        [switch]$SecurityOutbox
    )
    if ($Jobs.Count -gt 128) { throw 'At most 128 selected jobs required.' }
    $seen = @{}
    $now = Get-JobTimestamp
    foreach ($entry in $Jobs) {
        $name = [string]$entry.job
        if ($name -notmatch '^[A-Za-z0-9_.:-]{1,160}$' -or $seen.ContainsKey($name)) { throw 'Invalid or duplicate check job.' }
        $seen[$name] = $true
        if ($entry.max_age_seconds -lt 1 -or $entry.max_runtime_seconds -lt 1) { throw 'Explicit check thresholds required.' }
        $jobSql = ConvertTo-JobSqlLiteral $name
        $rows = @(Invoke-JobSql -Store $Store -Sql "SELECT * FROM runs WHERE job=$jobSql ORDER BY started DESC,rowid DESC LIMIT 1;")
        $state = 3
        $message = 'No recorded run'
        if ($rows.Count) {
            $row = $rows[0]
            switch ($row.status) {
                success { $state = 0; $message = 'Completed' }
                warning { $state = 1; $message = 'Job warning' }
                failed { $state = 2; $message = 'Job failed' }
                skipped { $state = 0; $message = 'Skipped' }
                running { $state = 0; $message = 'Running' }
                default { $state = 3; $message = 'Invalid stored state' }
            }
            if ($row.status -eq 'running') {
                if ($now - $row.started -gt $entry.max_runtime_seconds) { $state = 2; $message = 'Runtime exceeded' }
            }
            else {
                $finished = if ($row.finished) { $row.finished } else { $row.started }
                if ($now - $finished -gt $entry.max_age_seconds) { $state = 2; $message = 'Result overdue' }
            }
        }
        '{0} "Script job {1}" - {2}' -f $state,$name,$message
    }
    if ($SecurityOutbox) {
        $rows = @(Invoke-JobSql -Store $Store -Sql "SELECT COUNT(*) AS pending FROM deliveries d JOIN reports p ON p.id=d.report_id WHERE p.category='security' AND d.status!='sent';")
        $pending = [int]$rows[0].pending
        $state = if ($pending) { 2 } else { 0 }
        $message = if ($pending) { 'Notifications pending' } else { 'Queue empty' }
        '{0} "Script security delivery" pending={1} {2}' -f $state,$pending,$message
    }
}
