function Export-JobEvents {
    param(
        [Parameter(Mandatory)]$Store,
        [ValidateRange(0,[long]::MaxValue)][long]$After = 0,
        [ValidateRange(1,500)][int]$Limit = 100,
        [string]$Epoch
    )
    $floorRows = @(Invoke-JobSql -Store $Store -Sql "SELECT value FROM meta WHERE key='floor';")
    $floor = if ($floorRows.Count) { [long]$floorRows[0].value } else { 0 }
    $topRows = @(Invoke-JobSql -Store $Store -Sql "SELECT seq FROM sqlite_sequence WHERE name='events';")
    $top = if ($topRows.Count) { [long]$topRows[0].seq } else { 0 }
    $events = @(Invoke-JobSql -Store $Store -Sql "SELECT id,kind,created,payload FROM events WHERE id>$After ORDER BY id LIMIT $Limit;")
    foreach ($event in $events) { $event.payload = $event.payload | ConvertFrom-Json }
    $next = if ($events.Count) { [long]$events[-1].id } else { $After }
    $expected = @(Invoke-JobSql -Store $Store -Sql "SELECT value FROM meta WHERE key='expectations';")
    $expectations = if ($expected.Count) { @($expected[0].value | ConvertFrom-Json) } else { @() }
    return @{
        schema = 1
        epoch = $Store.Epoch
        floor = $floor
        reset_required = [bool](($Epoch -and $Epoch -ne $Store.Epoch) -or $After -gt $top)
        gap = [bool](($After -lt $floor -and $After -ne 0) -or ($After -eq 0 -and $floor -gt 0))
        events = @($events)
        next = $next
        expectations = @($expectations)
    }
}
