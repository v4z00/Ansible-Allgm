function Read-GpoPolicyString {
    param([Parameter(Mandatory)]$Reader)
    $text = New-Object Text.StringBuilder
    for ($index=0; $index -lt 32768; $index++) {
        $character = $Reader.ReadUInt16()
        if ($character -eq 0) { return $text.ToString() }
        $null = $text.Append([char]$character)
    }
    throw 'Registry policy string is too long.'
}
