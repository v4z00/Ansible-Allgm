function ConvertTo-JobSqlLiteral {
    param([AllowNull()]$Value)
    if ($null -eq $Value) { return 'NULL' }
    if ($Value -is [bool]) { return [int]$Value }
    if ($Value -is [ValueType] -and $Value -is [IFormattable]) {
        $number = $Value.ToString($null, [Globalization.CultureInfo]::InvariantCulture)
        if ($number -notmatch '^-?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?$') {
            throw 'Invalid SQL number.'
        }
        return $number
    }
    if (([string]$Value).Contains([string][char]0)) { throw 'NUL is not a valid SQL text value.' }
    return "'" + ([string]$Value).Replace("'", "''") + "'"
}
