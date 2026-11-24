# Windows 10/11 mit WSL-Unterstuetzung. Als normaler Windows-Benutzer starten.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$distribution = 'Ubuntu'
$wsl = Join-Path $env:WINDIR 'System32\wsl.exe'
if (-not (Test-Path -LiteralPath $wsl)) {
    throw 'wsl.exe fehlt. Dieses Windows benoetigt zuerst eine von Microsoft unterstuetzte WSL-Version. Siehe START-HIER.md.'
}

$ready = $false
try {
    $listed = @(& $wsl --list --quiet 2>$null)
    $ready = ($LASTEXITCODE -eq 0)
} catch { $listed = @() }
if (-not $ready) {
    Write-Host 'WSL ist noch nicht betriebsbereit. Windows fragt jetzt nach Admin-Rechten (UAC).'
    Write-Host 'Es werden nur WSL-Komponenten eingerichtet; kein automatischer Neustart.'
    $process = Start-Process -FilePath $wsl -ArgumentList @('--install', '--no-distribution') -Verb RunAs -Wait -PassThru
    if ($process.ExitCode -notin @(0, 3010)) {
        throw "WSL-Einrichtung fehlgeschlagen (Code $($process.ExitCode)). Keine Sicherheitsrichtlinien umgehen; technische Hilfe kontaktieren."
    }
    throw 'WSL-Vorbereitung ausgefuehrt. Falls von Windows verlangt, neu starten. Danach start-html.bat erneut starten.'
}
$names = @($listed | ForEach-Object { ($_ -replace "`0", '').Trim() })
if ($names -notcontains $distribution) {
    Write-Host 'Die WSL-Distribution Ubuntu wird fuer dieses Windows-Benutzerkonto installiert.'
    & $wsl --install --distribution $distribution --no-launch
    if ($LASTEXITCODE -ne 0) {
        throw 'Ubuntu-Installation fehlgeschlagen oder Neustart erforderlich. Hinweise von WSL beachten und danach erneut starten.'
    }
    Write-Host 'Ubuntu wird erstmals geoeffnet. Falls verlangt, Linux-Benutzername und Passwort festlegen.'
    Write-Host 'Wenn die Ubuntu-Shell bereit ist, exit eingeben, um die Vorbereitung fortzusetzen.'
    & $wsl --distribution $distribution
    if ($LASTEXITCODE -ne 0) { throw 'Ubuntu-Ersteinrichtung nicht abgeschlossen.' }
}

# Pfade als einzelne Argumente an wslpath uebergeben, nicht in Shell-Code einsetzen.
$installer = Join-Path $PSScriptRoot 'install-voraussetzungen.sh'
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) { throw 'install-voraussetzungen.sh fehlt im Werkzeugordner.' }
$converted = @(& $wsl --distribution $distribution --exec wslpath -a $installer)
if ($LASTEXITCODE -ne 0 -or $converted.Count -ne 1) { throw 'Der Werkzeugpfad ist in WSL nicht erreichbar. ZIP auf ein lokales Windows-Laufwerk entpacken.' }
Write-Host 'Linux-Voraussetzungen pruefen. Bei Bedarf fragt Ubuntu nach dem Linux-sudo-Passwort.'
& $wsl --distribution $distribution --exec bash $converted[0]
if ($LASTEXITCODE -ne 0) { throw 'Installation der Linux-Voraussetzungen fehlgeschlagen.' }
