function ConvertTo-JobSafeText {
    param([AllowNull()][string]$Text, [int]$Limit = 1000)
    if ($null -eq $Text) { return '' }
    $value = $Text
    foreach ($secret in $script:PrivateValues) { $value = $value.Replace($secret, '[redacted]') }
    $value = [regex]::Replace($value, '(?i)(?:https?://)?api\.telegram\.org/bot[^/\s]+', '[telegram]')
    $value = [regex]::Replace($value, '(?i)(password|passwd|secret|token|authorization|api[_-]?key)\s*[:=]\s*[^\s,;]+', '$1=[redacted]')
    $value = [regex]::Replace($value, '([a-z][a-z0-9+.-]*://)[^\s/@]+:[^\s/@]+@', '$1[redacted]@')
    $value = [regex]::Replace($value, '[\x00-\x08\x0B\x0C\x0E-\x1F]', '')
    return $value.Substring(0, [Math]::Min($value.Length, $Limit))
}
