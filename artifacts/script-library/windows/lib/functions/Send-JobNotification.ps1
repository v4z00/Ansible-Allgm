function Send-JobNotification {
    param(
        [Parameter(Mandatory)][ValidateSet('mail','telegram')][string]$Channel,
        [Parameter(Mandatory)][string]$Body,
        [Parameter(Mandatory)][hashtable]$Config
    )
    if ($Channel -eq 'telegram') {
        $token = if ($Config['BOT_TOKEN']) { $Config['BOT_TOKEN'] } else { $Config['TELEGRAM_BOT_TOKEN'] }
        $chat = if ($Config['CHAT_ID']) { $Config['CHAT_ID'] } else { $Config['TELEGRAM_CHAT_ID'] }
        if ($token -notmatch '^[0-9]+:[A-Za-z0-9_-]+$' -or -not $chat) { throw 'Telegram configuration incomplete.' }
        # Do not allow PS 5.1 to fall back to obsolete TLS versions.
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        try {
            for ($offset = 0; $offset -lt $Body.Length; $offset += 1800) {
                $payload = @{ chat_id = $chat; text = $Body.Substring($offset, [Math]::Min(1800, $Body.Length - $offset)) }
                $bytes = [Text.Encoding]::UTF8.GetBytes(($payload | ConvertTo-Json -Compress))
                $answer = Invoke-RestMethod -Method Post -Uri ('https://api.telegram.org/bot' + $token + '/sendMessage') -Body $bytes -ContentType 'application/json; charset=utf-8' -TimeoutSec 30
                if ($answer.ok -ne $true) { throw 'Rejected.' }
            }
        }
        catch { throw 'Telegram delivery failed.' }
        return
    }
    $recipient = if ($Config['EMAIL']) { $Config['EMAIL'] } else { $Config['MAIL_TO'] }
    $mode = if ($Config['SMTP_TLS']) { $Config['SMTP_TLS'] } else { 'starttls' }
    $auth = if ($Config['SMTP_AUTH']) { $Config['SMTP_AUTH'] } else { 'none' }
    if ($mode -notin @('none','starttls') -or $auth -notin @('none','password')) {
        throw 'Windows SMTP supports explicit none/starttls and none/password authentication.'
    }
    foreach ($value in @($Config['SMTP_HOST'], $Config['SMTP_FROM'], $recipient)) {
        if (-not $value -or [string]$value -match '[\r\n]') { throw 'SMTP configuration incomplete.' }
    }
    $port = if ($Config['SMTP_PORT']) { [int]$Config['SMTP_PORT'] } elseif ($mode -eq 'none') { 25 } else { 587 }
    if ($port -lt 1 -or $port -gt 65535) { throw 'Invalid SMTP port.' }
    $client = New-Object Net.Mail.SmtpClient([string]$Config['SMTP_HOST'], $port)
    $message = New-Object Net.Mail.MailMessage([string]$Config['SMTP_FROM'], [string]$recipient)
    try {
        $client.UseDefaultCredentials = $false
        $client.EnableSsl = $mode -eq 'starttls'
        $client.Timeout = 30000
        if ($auth -eq 'password') {
            if (-not $Config['SMTP_USERNAME'] -or -not $Config['SMTP_PASSWORD']) { throw 'SMTP credentials incomplete.' }
            $client.Credentials = New-Object Net.NetworkCredential([string]$Config['SMTP_USERNAME'], [string]$Config['SMTP_PASSWORD'])
        }
        $message.Subject = ConvertTo-JobAsciiMail (($Body -split '[\r\n]')[0])
        $message.Body = ConvertTo-JobAsciiMail $Body
        $message.SubjectEncoding = [Text.Encoding]::ASCII
        $message.BodyEncoding = [Text.Encoding]::ASCII
        $client.Send($message)
    }
    catch { throw 'SMTP delivery failed.' }
    finally { $message.Dispose(); $client.Dispose() }
}
