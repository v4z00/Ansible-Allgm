function Send-SecurityAlert {
    param(
        [Parameter(Mandatory)]$Store,
        [Parameter(Mandatory)][hashtable]$Config,
        [Parameter(Mandatory)][string]$EventKey,
        [Parameter(Mandatory)][string]$Job,
        [Parameter(Mandatory)][string]$Summary,
        [string]$Details = ''
    )
    $channels = @(Get-SecurityAlertChannels -Config $Config)
    $id = Save-SecurityAlert -Store $Store -EventKey $EventKey -Job $Job -Summary $Summary -Details $Details -Channels $channels
    return Send-SecurityAlertQueue -Store $Store -Config $Config -ReportId $id
}
