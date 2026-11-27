function New-JobStore {
    param(
        [Parameter(Mandatory)][string]$Database,
        [Parameter(Mandatory)][string]$Sqlite,
        [string]$Source = [Environment]::MachineName,
        [string]$SchemaPath
    )
    if (-not (Test-Path -LiteralPath $Sqlite -PathType Leaf)) {
        throw 'The declared SQLite executable is missing.'
    }
    if (-not $SchemaPath) {
        $SchemaPath = Join-Path $script:LibraryRoot 'data/job-schema.sql'
        if (-not (Test-Path -LiteralPath $SchemaPath -PathType Leaf)) {
            $artifactRoot = Split-Path -Parent (Split-Path -Parent $script:LibraryRoot)
            $SchemaPath = Join-Path $artifactRoot 'lib/data/job-schema.sql'
        }
    }
    $parent = Split-Path -Parent $Database
    $null = New-Item -ItemType Directory -Path $parent -Force
    Assert-JobPrivatePath -Path $parent
    if (Test-Path -LiteralPath $Database) { Assert-JobPrivatePath -Path $Database }
    $store = @{ Database = $Database; Sqlite = $Sqlite }
    $null = Invoke-JobSql -Store $store -Sql 'PRAGMA journal_mode=WAL;'
    $schema = [IO.File]::ReadAllText($SchemaPath, [Text.Encoding]::UTF8)
    $epoch = [Guid]::NewGuid().ToString()
    $sourceSql = ConvertTo-JobSqlLiteral $Source
    $epochSql = ConvertTo-JobSqlLiteral $epoch
    $sql = @"
$schema
BEGIN IMMEDIATE;
INSERT OR IGNORE INTO meta VALUES('schema','1');
INSERT OR IGNORE INTO meta VALUES('epoch',$epochSql);
INSERT OR IGNORE INTO meta VALUES('host',$sourceSql);
INSERT OR IGNORE INTO meta VALUES('floor','0');
COMMIT;
"@
    $null = Invoke-JobSql -Store $store -Sql $sql
    $metadata = @{}
    foreach ($row in @(Invoke-JobSql -Store $store -Sql 'SELECT key,value FROM meta;')) {
        $metadata[$row.key] = $row.value
    }
    if ($metadata['schema'] -ne '1') { throw 'Unsupported job database schema.' }
    $store.Source = $metadata['host']
    $store.Epoch = $metadata['epoch']
    return $store
}
