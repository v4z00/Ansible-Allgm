param([string]$Root,[string]$Directory,[string]$Manager)
$ErrorActionPreference='Stop'
. (Join-Path $Root 'roles/windows_gpo/files/Read-GpoPolicyString.ps1')
. (Join-Path $Root 'roles/windows_gpo/files/Read-GpoRegistryPolicy.ps1')
$stream=New-Object IO.MemoryStream
$writer=New-Object IO.BinaryWriter($stream)
$writer.Write([uint32]0x67655250);$writer.Write([uint32]1)
function Add-Value([string]$Name,[uint32]$Type,[byte[]]$Data) {
    $writer.Write([uint16]91)
    $writer.Write([Text.Encoding]::Unicode.GetBytes('Software\Example'+[char]0));$writer.Write([uint16]59)
    $writer.Write([Text.Encoding]::Unicode.GetBytes($Name+[char]0));$writer.Write([uint16]59)
    $writer.Write($Type);$writer.Write([uint16]59);$writer.Write([uint32]$Data.Length);$writer.Write([uint16]59)
    $writer.Write($Data);$writer.Write([uint16]93)
}
Add-Value 'Enabled' 4 ([BitConverter]::GetBytes([uint32]1))
Add-Value 'String' 1 ([Text.Encoding]::Unicode.GetBytes('private fixture'+[char]0))
$writer.Flush();$bytes=$stream.ToArray()
$parsed=Read-GpoRegistryPolicy $bytes
if ($parsed.Count -ne 1 -or $parsed['hklm\software\example\enabled'] -ne 1) {throw 'Registry comparison failed'}
$bad=$bytes.Clone();$bad[0]=0
try { $null=Read-GpoRegistryPolicy $bad;throw 'Invalid header accepted' } catch {if ($_.Exception.Message -eq 'Invalid header accepted'){throw}}
try { $null=Read-GpoRegistryPolicy $bytes[0..($bytes.Length-2)];throw 'Truncated policy accepted' } catch {if ($_.Exception.Message -eq 'Truncated policy accepted'){throw}}
# Mock AD/GroupPolicy APIs only. No domain, credentials or network is used.
function Import-Module {param($Name,$ErrorAction)}
function Get-ADDomain {param($Identity);[pscustomobject]@{DNSRoot='example.invalid';PDCEmulator='dc.example.invalid'}}
$global:Objects=@();$global:Writes=0;$global:BackupCount=0;$global:Values=@{'hklm\manual\keep'=19}
function Get-GPO {param([switch]$All,$Domain,$Server,$ErrorAction);$global:Objects}
function New-GPO {param($Name,$Comment,$Domain,$Server,$ErrorAction)
    $object=[pscustomobject]@{Id=[guid]::NewGuid();DisplayName=$Name;Description=$Comment}
    $global:Objects+=@($object);return $object
}
function Backup-GPO {param($Guid,$Path,$Domain,$Server,$ErrorAction);$global:BackupCount++;[pscustomobject]@{Id=[guid]::NewGuid()}}
function Set-GPRegistryValue {param($Guid,$Key,$ValueName,$Type,$Value,$Domain,$Server,$ErrorAction);$global:Writes++;$global:Values[($Key+'\'+$ValueName).ToLowerInvariant()]=$Value}
function Get-GpoRegistrySnapshot {param($Root);return $global:Values}
$plan=@{schema=1;profiles=@(@{id='security';name='Ansible: Security';values=@(@{feature='test';key='HKLM\Software\Example';name='Enabled';value=1})})}|ConvertTo-Json -Depth 10
$global:Ansible=@{CheckMode=$true}
& $Manager -Plan $plan -Domain '' -Server '' -BackupRoot $Directory -AdoptExisting $false
if (-not $Ansible.Changed -or $Objects.Count -or $Writes) {throw 'Check mode mutated state'}
$Ansible.CheckMode=$false
& $Manager -Plan $plan -Domain '' -Server '' -BackupRoot $Directory -AdoptExisting $false
if ($Objects.Count -ne 1 -or $Writes -ne 1) {throw 'Creation failed'}
& $Manager -Plan $plan -Domain '' -Server '' -BackupRoot $Directory -AdoptExisting $false
if ($Ansible.Changed -or $Writes -ne 1 -or $BackupCount) {throw 'Second deployment was not idempotent'}
$plan=$plan -replace '"value": 1','"value": 0'
& $Manager -Plan $plan -Domain '' -Server '' -BackupRoot $Directory -AdoptExisting $false
if ($BackupCount -ne 1 -or $Writes -ne 2 -or $Values['hklm\manual\keep'] -ne 19) {throw 'Update lost a manual value or skipped its backup'}
$Objects[0].Description='Manual policy'
try { & $Manager -Plan $plan -Domain '' -Server '' -BackupRoot $Directory -AdoptExisting $false;throw 'Foreign object accepted' } catch {if ($_.Exception.Message -eq 'Foreign object accepted'){throw}}
'GPO parser/check/update fixture OK'
