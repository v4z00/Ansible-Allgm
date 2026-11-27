#requires -Version 5.1
Set-StrictMode -Version Latest
$script:LibraryRoot = $PSScriptRoot
$script:PrivateValues = @()
foreach ($functionFile in Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'functions') -Filter '*.ps1' -File | Sort-Object Name) {
    . $functionFile.FullName
}
Export-ModuleMember -Function *-Job*, *-ScriptJob*, *-SecurityAlert*
