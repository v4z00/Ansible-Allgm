function Invoke-ScriptJob {
    param(
        [Parameter(Mandatory)]$Store,
        [Parameter(Mandatory)][string]$SpecFile,
        [string]$PowerShell = (Join-Path $env:SystemRoot 'System32/WindowsPowerShell/v1.0/powershell.exe')
    )
    Assert-JobPrivatePath -Path $SpecFile
    $spec = Get-JobConfig -Path @($SpecFile)
    $name = [string]$spec['name']
    if ($name -notmatch '^[A-Za-z0-9_.:-]{1,160}$') { throw 'Invalid job name.' }
    $program = [string]$spec['program']
    if (-not [IO.Path]::IsPathRooted($program) -or [IO.Path]::GetExtension($program) -ne '.ps1') {
        throw 'An explicit PowerShell program path is required.'
    }
    Assert-JobPrivatePath -Path $program
    $category = if ($spec['category']) { [string]$spec['category'] } else { 'general' }
    if ($category -notin @('general','administration')) { throw 'Unsupported scheduled job category.' }
    $maxRuntime = if ($spec['max_runtime_seconds']) { [int]$spec['max_runtime_seconds'] } else { 86400 }
    if ($maxRuntime -lt 1) { throw 'Maximum runtime must be positive.' }
    $stateRoot = Split-Path -Parent $Store.Database
    $lockDirectory = Join-Path $stateRoot 'locks'
    $logs = Join-Path $stateRoot 'logs'
    $null = New-Item -ItemType Directory -Path $lockDirectory,$logs -Force
    Assert-JobPrivatePath -Path $lockDirectory
    Assert-JobPrivatePath -Path $logs
    $hash = [Security.Cryptography.SHA256]::Create()
    try { $lockName = [BitConverter]::ToString($hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($name))).Replace('-','') }
    finally { $hash.Dispose() }
    $lockPath = Join-Path $lockDirectory ($lockName + '.lock')
    try { $lock = [IO.File]::Open($lockPath, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None) }
    catch [IO.IOException] { return 75 }
    $job = $null
    $process = $null
    $output = $null
    $errors = $null
    $started = $false
    try {
        $source = ConvertTo-JobSqlLiteral $Store.Source
        $epoch = ConvertTo-JobSqlLiteral $Store.Epoch
        $jobName = ConvertTo-JobSqlLiteral $name
        $unfinished = @(Invoke-JobSql -Store $Store -Sql "SELECT run_id,started FROM runs WHERE source=$source AND epoch=$epoch AND job=$jobName AND status='running';")
        foreach ($old in $unfinished) {
            Complete-ScriptJob -Job @{ Store=$Store; RunId=$old.run_id; Started=$old.started } -Status failed -ExitCode 255 -Summary 'Previous process ended without completion'
        }
        $job = Start-ScriptJob -Store $Store -Name $name -Category $category
        # Fixed wrapper: job paths and arguments remain JSON data, never source code.
        $wrapper = @'
$ErrorActionPreference = 'Stop'
$spec = [IO.File]::ReadAllText($env:SCRIPT_JOB_SPEC,[Text.Encoding]::UTF8) | ConvertFrom-Json
$arguments = @()
if ($spec.PSObject.Properties['arguments']) { $arguments = @($spec.arguments) }
$global:LASTEXITCODE = 0
& $spec.program @arguments
$completed = $?
if ($global:LASTEXITCODE -ne 0) { exit $global:LASTEXITCODE }
if (-not $completed) { exit 1 }
exit 0
'@
        $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($wrapper))
        $process = New-Object Diagnostics.Process
        $process.StartInfo.FileName = $PowerShell
        $process.StartInfo.Arguments = '-NoLogo -NoProfile -NonInteractive -EncodedCommand ' + $encoded
        $process.StartInfo.UseShellExecute = $false
        $process.StartInfo.CreateNoWindow = $true
        $process.StartInfo.RedirectStandardOutput = $true
        $process.StartInfo.RedirectStandardError = $true
        $process.StartInfo.WorkingDirectory = Split-Path -Parent $program
        $process.StartInfo.EnvironmentVariables['SCRIPT_JOB_SPEC'] = $SpecFile
        $process.StartInfo.EnvironmentVariables['HM_JOB_RUN_ID'] = $job.RunId
        $process.StartInfo.EnvironmentVariables['HM_JOB_DB'] = $Store.Database
        $process.StartInfo.EnvironmentVariables['HM_JOB_MANAGED'] = '1'
        $process.StartInfo.EnvironmentVariables['HM_JOB_CONFIGFILES'] = ConvertTo-Json -InputObject @($spec['config_files']) -Compress
        $output = [IO.File]::Create((Join-Path $logs ($job.RunId + '.log')))
        $errors = [IO.File]::Create((Join-Path $logs ($job.RunId + '.stderr.log')))
        $clock = [Diagnostics.Stopwatch]::StartNew()
        $null = $process.Start()
        $started = $true
        $stdoutTask = $process.StandardOutput.BaseStream.CopyToAsync($output)
        $stderrTask = $process.StandardError.BaseStream.CopyToAsync($errors)
        $timedOut = $false
        while (-not $process.WaitForExit(200)) {
            if ($clock.Elapsed.TotalSeconds -lt $maxRuntime) { continue }
            $timedOut = $true
            if ([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT) {
                & (Join-Path $env:SystemRoot 'System32/taskkill.exe') /PID $process.Id /T /F *> $null
            }
            else { $process.Kill($true) }
            if (-not $process.WaitForExit(10000)) { throw 'Timed-out process did not terminate.' }
            break
        }
        $null = $stdoutTask.GetAwaiter().GetResult()
        $null = $stderrTask.GetAwaiter().GetResult()
        $code = if ($timedOut) { 124 } else { $process.ExitCode }
        $run = ConvertTo-JobSqlLiteral $job.RunId
        $items = @(Invoke-JobSql -Store $Store -Sql "SELECT status FROM items WHERE source=$source AND epoch=$epoch AND run_id=$run;")
        if ($code -eq 0 -and @($items | Where-Object status -eq 'failed').Count) { $code = 1 }
        $status = if ($code -eq 0) { 'success' } else { 'failed' }
        if ($code -eq 0 -and @($items | Where-Object status -eq 'warning').Count) { $status = 'warning' }
        if ($code -eq 0 -and $items.Count -and @($items | Where-Object status -ne 'skipped').Count -eq 0) { $status = 'skipped' }
        $summary = if ($code -eq 0) { 'Completed' } else { 'Job failed; inspect private local log' }
        Complete-ScriptJob -Job $job -Status $status -ExitCode $code -Summary $summary
        $job = $null
        return [int]$code
    }
    catch {
        if ($started -and -not $process.HasExited) {
            if ([Environment]::OSVersion.Platform -eq [PlatformID]::Win32NT) {
                & (Join-Path $env:SystemRoot 'System32/taskkill.exe') /PID $process.Id /T /F *> $null
            }
            else { $process.Kill($true) }
            $null = $process.WaitForExit(10000)
        }
        if ($job) { Complete-ScriptJob -Job $job -Status failed -ExitCode 255 -Summary 'Runner interrupted or failed' }
        throw 'Job runner failed; inspect private local state.'
    }
    finally {
        if ($process) { $process.Dispose() }
        if ($output) { $output.Dispose() }
        if ($errors) { $errors.Dispose() }
        $lock.Dispose()
    }
}
