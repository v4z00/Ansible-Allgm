function Open-JobStore {
    param(
        [Parameter(Mandatory)][string]$Database,
        [Parameter(Mandatory)][string]$Sqlite
    )
    if (-not (Test-Path -LiteralPath $Database -PathType Leaf)) {
        throw 'The existing job database is missing.'
    }
    Assert-JobPrivatePath -Path $Database
    $store = @{ Database = $Database; Sqlite = $Sqlite; ReadOnly = $true }
    $metadata = @{}
    foreach ($row in @(Invoke-JobSql -Store $store -Sql 'SELECT key,value FROM meta;')) {
        $metadata[$row.key] = $row.value
    }
    if ($metadata['schema'] -ne '1' -or -not $metadata['epoch'] -or -not $metadata['host']) {
        throw 'The existing job database metadata is invalid.'
    }
    $store.Source = $metadata['host']
    $store.Epoch = $metadata['epoch']
    return $store
}
