#Requires -Version 5.1
#Requires -RunAsAdministrator

[CmdletBinding(SupportsShouldProcess)]
param([ValidateRange(1, 65535)][int]$Port = 5986)

$ErrorActionPreference = 'Stop'

$computer = Get-CimInstance -ClassName Win32_ComputerSystem
if (-not $computer.PartOfDomain -or -not $computer.DNSHostName -or -not $computer.Domain) {
    throw 'A domain-joined Windows computer with a DNS name is required.'
}
$fqdn = ('{0}.{1}' -f $computer.DNSHostName, $computer.Domain).ToLowerInvariant()

$service = 'WSMan:\localhost\Service'
if ((Get-Item "$service\Auth\Kerberos").Value -ne 'true' -or
    (Get-Item "$service\Auth\Basic").Value -ne 'false' -or
    (Get-Item "$service\AllowUnencrypted").Value -ne 'false') {
    throw 'WinRM must allow Kerberos and disable Basic and unencrypted messages.'
}

$existing = @(Get-ChildItem -Path WSMan:\localhost\Listener |
    Where-Object { $_.Keys -contains 'Transport=HTTPS' })
if ($existing.Count) {
    foreach ($listener in $existing) {
        $values = Get-ChildItem -LiteralPath $listener.PSPath
        $boundPort = ($values | Where-Object Name -eq 'Port').Value
        if ($boundPort -eq $Port -and (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue)) {
            [pscustomobject]@{ Computer = $fqdn; Port = $Port; State = 'present' }
            return
        }
    }
    throw 'An HTTPS listener exists with a different port or an inactive binding.'
}

$now = Get-Date
$candidates = Get-ChildItem -Path Cert:\LocalMachine\My -SSLServerAuthentication |
    Where-Object {
        $_.HasPrivateKey -and $_.NotBefore -le $now -and $_.NotAfter -gt $now -and
        $_.Issuer -ne $_.Subject -and $_.DnsNameList.Unicode -contains $fqdn
    } |
    Sort-Object -Property NotAfter, NotBefore, Thumbprint -Descending

$certificate = $null
foreach ($candidate in $candidates) {
    if ($candidate.Verify()) {
        $certificate = $candidate
        break
    }
}
if (-not $certificate) {
    throw "No trusted Server Authentication certificate with the DNS name $fqdn and a private key was found."
}

if ($PSCmdlet.ShouldProcess($fqdn, "Create WinRM HTTPS listener on TCP $Port")) {
    # The exact FQDN was checked against the certificate. Supplying a Hostname here
    # would make WSMan reject some valid certificates with a SAN-only DNS match.
    $null = New-WSManInstance -ResourceURI 'winrm/config/Listener' -SelectorSet @{
        Transport = 'HTTPS'
        Address = '*'
    } -ValueSet @{
        Port = [string]$Port
        CertificateThumbprint = $certificate.Thumbprint
    }
    for ($attempt = 0; $attempt -lt 10; $attempt++) {
        if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) {
            [pscustomobject]@{ Computer = $fqdn; Port = $Port; State = 'created' }
            return
        }
        Start-Sleep -Seconds 1
    }
    throw "WinRM HTTPS was configured but TCP $Port did not start listening."
}
