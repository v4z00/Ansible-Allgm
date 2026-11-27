function Read-GpoRegistryPolicy {
    # Read registry.pol for comparison only. Updates use GroupPolicy cmdlets.
    param([Parameter(Mandatory)][byte[]]$Bytes)
    if ($Bytes.Length -gt 8MB) { throw 'Registry policy exceeds the supported size.' }
    $stream = New-Object IO.MemoryStream(,$Bytes)
    $reader = New-Object IO.BinaryReader($stream)
    $values = @{}
    try {
        if ($reader.ReadUInt32() -ne 0x67655250 -or $reader.ReadUInt32() -ne 1) { throw 'Invalid registry policy header.' }
        while ($stream.Position -lt $stream.Length) {
            if ($reader.ReadUInt16() -ne 91) { throw 'Invalid registry policy entry.' }
            $key = Read-GpoPolicyString -Reader $reader
            if ($reader.ReadUInt16() -ne 59) { throw 'Invalid registry policy separator.' }
            $name = Read-GpoPolicyString -Reader $reader
            if ($reader.ReadUInt16() -ne 59) { throw 'Invalid registry policy separator.' }
            $type = $reader.ReadUInt32()
            if ($reader.ReadUInt16() -ne 59) { throw 'Invalid registry policy separator.' }
            $size = $reader.ReadUInt32()
            if ($reader.ReadUInt16() -ne 59 -or $size -gt $stream.Length - $stream.Position - 2) { throw 'Invalid registry policy value size.' }
            $data = $reader.ReadBytes($size)
            if ($reader.ReadUInt16() -ne 93) { throw 'Invalid registry policy terminator.' }
            # No string/password values are decoded, logged or returned.
            if ($type -eq 4 -and $size -eq 4 -and -not $name.StartsWith('**')) {
                $values[('HKLM\' + $key + '\' + $name).ToLowerInvariant()] = [BitConverter]::ToUInt32($data,0)
            }
        }
    }
    finally { $reader.Dispose(); $stream.Dispose() }
    return $values
}
