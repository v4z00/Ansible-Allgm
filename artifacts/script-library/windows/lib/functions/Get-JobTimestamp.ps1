function Get-JobTimestamp {
    return [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() / 1000.0
}
