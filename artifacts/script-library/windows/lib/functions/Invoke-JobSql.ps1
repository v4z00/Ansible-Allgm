function Invoke-JobSql {
    param(
        [Parameter(Mandatory)]$Store,
        [Parameter(Mandatory)][string]$Sql
    )
    if ($Store.Database -match '["\r\n]' -or -not [IO.Path]::IsPathRooted($Store.Database)) {
        throw 'An absolute database path without quotes or line breaks is required.'
    }
    $process = New-Object Diagnostics.Process
    $process.StartInfo.FileName = $Store.Sqlite
    $readOnly = if ($Store['ReadOnly']) { '-readonly ' } else { '' }
    $process.StartInfo.Arguments = $readOnly + '-noinit -batch -bail -json -cmd ".timeout 10000" "' + $Store.Database + '"'
    $process.StartInfo.UseShellExecute = $false
    $process.StartInfo.CreateNoWindow = $true
    $process.StartInfo.RedirectStandardInput = $true
    $process.StartInfo.RedirectStandardOutput = $true
    $process.StartInfo.RedirectStandardError = $true
    $process.StartInfo.StandardOutputEncoding = New-Object Text.UTF8Encoding($false)
    $process.StartInfo.StandardErrorEncoding = New-Object Text.UTF8Encoding($false)
    try {
        if (-not $process.Start()) { throw 'SQLite could not be started.' }
        $outputTask = $process.StandardOutput.ReadToEndAsync()
        $errorTask = $process.StandardError.ReadToEndAsync()
        # Write explicit UTF-8 bytes. StandardInputEncoding is not available in
        # every .NET Framework used by Windows PowerShell 5.1.
        $bytes = [Text.Encoding]::UTF8.GetBytes("PRAGMA foreign_keys=ON;`n" + $Sql + "`n")
        $process.StandardInput.BaseStream.Write($bytes, 0, $bytes.Length)
        $process.StandardInput.BaseStream.Close()
        if (-not $process.WaitForExit(30000)) {
            $process.Kill()
            throw 'SQLite operation timed out.'
        }
        $output = $outputTask.GetAwaiter().GetResult()
        $null = $errorTask.GetAwaiter().GetResult()
        if ($process.ExitCode -ne 0) {
            # SQLite diagnostics can contain input data. Keep them out of reports.
            throw 'SQLite operation failed.'
        }
        if (-not [string]::IsNullOrWhiteSpace($output)) {
            return $output | ConvertFrom-Json
        }
    }
    finally { $process.Dispose() }
}
