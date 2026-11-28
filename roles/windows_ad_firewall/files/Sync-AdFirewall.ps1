[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory)][string]$Plan,
    [bool]$Apply
)
$ErrorActionPreference = 'Stop'
$Ansible.Changed = $false
$ownerGroup = 'Ansible: Active Directory'
$description = 'Managed by Ansible windows_ad_firewall'
$desired = @($Plan | ConvertFrom-Json)

function Convert-ToFirewallCidr {
    param([string]$Address)
    $parts = $Address.Split('/')
    $ip = [Net.IPAddress]::Parse($parts[0])
    $length = $ip.GetAddressBytes().Length * 8
    if ($parts.Count -eq 2) {
        $length = if ($parts[1] -match '^\d+$') { [int]$parts[1] } else {
            $bits = @([Net.IPAddress]::Parse($parts[1]).GetAddressBytes() | ForEach-Object {
                [Convert]::ToString($_, 2).PadLeft(8, '0')
            }) -join ''
            if ($bits -notmatch '^1+0*$') { throw 'Invalid firewall netmask.' }
            $bits.TrimEnd('0').Length
        }
    }
    "$($ip.ToString())/$length"
}

function Test-DesiredFirewallRule {
    param($Rule, $Expected)
    $port = $Rule | Get-NetFirewallPortFilter
    $address = $Rule | Get-NetFirewallAddressFilter
    if ($Rule.DisplayName -cne $Expected.display_name -or $Rule.Enabled -ne 'True' -or
        $Rule.Profile -ne 'Domain' -or $Rule.Direction -ne 'Inbound' -or $Rule.Action -ne 'Allow' -or
        $port.Protocol -ne $Expected.protocol -or ($port.LocalPort -join ',') -ne $Expected.port -or
        ($port.RemotePort -join ',') -ne 'Any' -or ($address.LocalAddress -join ',') -ne 'Any') {
        return $false
    }
    try {
        $current = @($address.RemoteAddress | ForEach-Object { Convert-ToFirewallCidr $_ } | Sort-Object -Unique)
        $required = @($Expected.addresses | ForEach-Object { Convert-ToFirewallCidr $_ } | Sort-Object -Unique)
        return ($current -join ',') -ceq ($required -join ',')
    }
    catch { return $false }
}

$local = @(Get-NetFirewallRule -PolicyStore PersistentStore)
$operations = foreach ($rule in $desired) {
    $current = @($local | Where-Object Name -eq $rule.name)
    if ($current.Count -gt 1 -or ($current.Count -and
        ($current[0].Group -cne $ownerGroup -or $current[0].Description -cne $description))) {
        throw "Firewall rule ownership conflict: $($rule.name)"
    }
    $operation = if (!$current.Count) { 'create' }
                 elseif (Test-DesiredFirewallRule $current[0] $rule) { 'unchanged' }
                 else { 'update' }
    [pscustomobject]@{ rule = $rule; operation = $operation }
}

if ($Apply -and !$Ansible.CheckMode) {
    foreach ($entry in $operations) {
        if ($entry.operation -eq 'unchanged') { continue }
        $rule = $entry.rule
        if (!$PSCmdlet.ShouldProcess($rule.name, $entry.operation)) { continue }
        $settings = @{
            PolicyStore = 'PersistentStore'; Name = $rule.name
            Direction = 'Inbound'; Action = 'Allow'; Enabled = 'True'; Profile = 'Domain'
            Protocol = $rule.protocol; LocalPort = $rule.port; RemotePort = 'Any'
            LocalAddress = 'Any'; RemoteAddress = [string[]]$rule.addresses
        }
        if ($entry.operation -eq 'create') {
            $null = New-NetFirewallRule @settings -DisplayName $rule.display_name -Group $ownerGroup -Description $description
        }
        else {
            $null = Set-NetFirewallRule @settings -NewDisplayName $rule.display_name
        }
        $Ansible.Changed = $true
    }
}

$effective = @(Get-NetFirewallRule -PolicyStore ActiveStore)
$Ansible.Result = @(
    foreach ($entry in $operations) {
        $rule = $entry.rule
        $active = @($effective | Where-Object { $_.Name -eq $rule.name -and $_.Group -ceq $ownerGroup -and $_.Description -ceq $description })
        [pscustomobject]@{
            name = $rule.name; stage = $rule.stage; operation = $entry.operation
            active = $active.Count -eq 1 -and (Test-DesiredFirewallRule $active[0] $rule)
        }
    }
)
if ($Apply -and !$Ansible.CheckMode -and @($Ansible.Result | Where-Object { !$_.active }).Count) {
    $Ansible.Failed = $true
}
