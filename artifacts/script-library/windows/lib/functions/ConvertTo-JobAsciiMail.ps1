function ConvertTo-JobAsciiMail {
    param([Parameter(Mandatory)][string]$Text)
    $tablePath = Join-Path $script:LibraryRoot 'data/mail-translations.json'
    if (-not (Test-Path -LiteralPath $tablePath)) {
        $root = Split-Path -Parent (Split-Path -Parent $script:LibraryRoot)
        $tablePath = Join-Path $root 'lib/data/mail-translations.json'
    }
    # PS 5.1 PSCustomObject keys are case-insensitive (for example a/A umlauts).
    # A typed .NET dictionary preserves the shared table exactly.
    Add-Type -AssemblyName System.Runtime.Serialization
    $settings = New-Object Runtime.Serialization.Json.DataContractJsonSerializerSettings
    $settings.UseSimpleDictionaryFormat = $true
    $serializer = New-Object Runtime.Serialization.Json.DataContractJsonSerializer([Collections.Generic.Dictionary[string,string]], $settings)
    $stream = [IO.File]::OpenRead($tablePath)
    try { $table = $serializer.ReadObject($stream) }
    finally { $stream.Dispose() }
    $value = $Text.Normalize([Text.NormalizationForm]::FormC)
    foreach ($entry in $table.GetEnumerator()) { $value = $value.Replace($entry.Key, $entry.Value) }
    $result = New-Object Text.StringBuilder
    foreach ($letter in $value.Normalize([Text.NormalizationForm]::FormKD).ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($letter) -eq 'NonSpacingMark') { continue }
        if ([int]$letter -le 127) { $null = $result.Append($letter) }
        else { $null = $result.Append('?') }
    }
    return $result.ToString()
}
