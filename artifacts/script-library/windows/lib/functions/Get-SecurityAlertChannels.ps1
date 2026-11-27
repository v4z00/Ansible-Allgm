function Get-SecurityAlertChannels {
    param([Parameter(Mandatory)][hashtable]$Config)
    $channels = @($Config['SECURITY_CHANNELS'])
    if (-not $Config.ContainsKey('SECURITY_CHANNELS')) {
        $channels = @()
        if ($Config['EMAIL'] -or $Config['MAIL_TO']) { $channels += 'mail' }
        if (($Config['BOT_TOKEN'] -or $Config['TELEGRAM_BOT_TOKEN']) -and ($Config['CHAT_ID'] -or $Config['TELEGRAM_CHAT_ID'])) { $channels += 'telegram' }
    }
    if ($channels.Count -eq 0 -or @($channels | Select-Object -Unique).Count -ne $channels.Count) {
        throw 'Explicit security notification channels required.'
    }
    foreach ($channel in $channels) {
        if ($channel -notin @('mail','telegram')) { throw 'Invalid security channel.' }
    }
    return $channels
}
