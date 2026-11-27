function Get-JobConfig {
    param([Parameter(Mandatory)][string[]]$Path)
    $result = @{}
    $script:PrivateValues = @()
    foreach ($file in $Path) {
        Assert-JobPrivatePath -Path $file
        $data = [IO.File]::ReadAllText($file, [Text.Encoding]::UTF8) | ConvertFrom-Json
        if ($data -isnot [PSCustomObject]) { throw 'A configuration object is required.' }
        foreach ($property in $data.PSObject.Properties) {
            $result[$property.Name] = $property.Value
            if ($property.Name -match 'PASSWORD|PASSPHRASE|SECRET|TOKEN|API_KEY' -and
                $property.Value -is [string] -and $property.Value.Length -gt 3) {
                $script:PrivateValues += $property.Value
            }
        }
    }
    return $result
}
