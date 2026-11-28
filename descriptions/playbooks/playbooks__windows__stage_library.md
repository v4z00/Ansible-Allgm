# Stage the shared Windows job library

Prepare the verified x64 SQLite artifact with `python3 scripts/download_windows_sqlite.py --apply`.
The downloader pins the official archive version and SHA3-256, extracts only sqlite3.exe,
and retains a different existing executable. Binaries/private settings stay outside Git.
Then run `ansible-playbook playbooks/windows/stage_library.yml --limit example-windows-host`.
Use a separate pilot code/state path for the first test.

`windows_script_root` defaults to C:\Scripte, `windows_state_root` to C:\ProgramData\ScriptJobs.
The role deploys the complete common PowerShell library, the shared SQL schema and mail
table, query helpers and declared SQLite runtime. Code/state directories grant SYSTEM
and built-in Administrators access by SID. Reparse points are refused. AllSigned requires the configured central signing pipeline; disabled signing cannot bypass it. Real Windows ACL/signing/MSI behavior still needs
an authenticated Windows pilot; portable PowerShell tests do not establish that behavior.

Local APIs record start/items/completion, export schema-1 cursor batches, prune completed
history after 90 days and provide read-only latest/Checkmk views. Process execution is
an explicit API for server jobs; it is not a replacement for an existing GPO background
wrapper. This playbook schedules no business task and deploys no private host scripts.
SYSVOL, GPO links/settings and ADMX deployment remain separate work.

<details>
<summary>Deutsch</summary>

# Gemeinsame Windows-Joblibrary bereitstellen

`python3 scripts/download_windows_sqlite.py --apply` bereitet die fest versionierte,
gegen die offizielle SHA3-Summe geprüfte x64-SQLite-Laufzeit vor. Nur sqlite3.exe wird
entnommen; eine abweichende vorhandene EXE bleibt erhalten. Die Binärdatei bleibt lokal.
Danach `ansible-playbook playbooks/windows/stage_library.yml --limit example-windows-host`
verwenden. Beim ersten Pilot getrennte Code-/Datenpfade wählen.

Die komplette Grundlibrary, ein gemeinsames SQL-Schema, die feste Mailtabelle und lokale
Abfragehelfer werden verteilt. Standardpfade sind C:\Scripte und C:\ProgramData\ScriptJobs;
`windows_script_root`, `windows_state_root`, `windows_job_database` und `windows_sqlite_exe`
bilden die feste Zuordnung. Private ACLs verwenden SYSTEM-/Administratoren-SIDs.
Reparsepunkte werden abgewiesen. AllSigned verlangt eine konfigurierte Signierstrecke.
Windows-ACLs, Signierung und MSI brauchen noch einen echten Windows-Pilot.

Die APIs erfassen Start, Einzelobjekte und Ende in SQLite, exportieren Cursorpakete und
halten abgeschlossene Läufe 90 Tage. Status- und Checkmk-Abfragen sind lesend. Ein
Prozessrunner ist ausdrücklich für Serverjobs vorgesehen und ersetzt keinen GPO-
Background-Wrapper. Dieses Playbook verteilt keine privaten Fachskripte und aktiviert
keine Fachaufgabe. SYSVOL, GPOs und ADMX bleiben getrennt.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/windows/stage_library.yml",
  "title": "Gemeinsame Windows-Joblibrary bereitstellen",
  "documented": true,
  "fields": [],
  "constraints": [],
  "sources": [
    "artifacts/script-library/windows/bin/job-status.ps1",
    "artifacts/script-library/windows/bin/script-jobs.ps1",
    "artifacts/script-library/windows/lib/ScriptLibrary.psm1",
    "artifacts/script-library/windows/lib/functions/Assert-JobPrivatePath.ps1",
    "artifacts/script-library/windows/lib/functions/Complete-ScriptJob.ps1",
    "artifacts/script-library/windows/lib/functions/ConvertTo-JobAsciiMail.ps1",
    "artifacts/script-library/windows/lib/functions/ConvertTo-JobSafeText.ps1",
    "artifacts/script-library/windows/lib/functions/ConvertTo-JobSqlLiteral.ps1",
    "artifacts/script-library/windows/lib/functions/Export-JobEvents.ps1",
    "artifacts/script-library/windows/lib/functions/Get-JobConfig.ps1",
    "artifacts/script-library/windows/lib/functions/Get-JobEventSql.ps1",
    "artifacts/script-library/windows/lib/functions/Get-JobLocalCheck.ps1",
    "artifacts/script-library/windows/lib/functions/Get-JobState.ps1",
    "artifacts/script-library/windows/lib/functions/Get-JobTimestamp.ps1",
    "artifacts/script-library/windows/lib/functions/Get-SecurityAlertChannels.ps1",
    "artifacts/script-library/windows/lib/functions/Invoke-JobSql.ps1",
    "artifacts/script-library/windows/lib/functions/Invoke-ScriptJob.ps1",
    "artifacts/script-library/windows/lib/functions/New-JobStore.ps1",
    "artifacts/script-library/windows/lib/functions/Open-JobStore.ps1",
    "artifacts/script-library/windows/lib/functions/Remove-JobHistory.ps1",
    "artifacts/script-library/windows/lib/functions/Save-SecurityAlert.ps1",
    "artifacts/script-library/windows/lib/functions/Send-JobNotification.ps1",
    "artifacts/script-library/windows/lib/functions/Send-SecurityAlert.ps1",
    "artifacts/script-library/windows/lib/functions/Send-SecurityAlertQueue.ps1",
    "artifacts/script-library/windows/lib/functions/Set-JobItem.ps1",
    "artifacts/script-library/windows/lib/functions/Start-ScriptJob.ps1",
    "playbooks/windows/stage_library.yml",
    "roles/windows_private_paths/defaults/main.yml",
    "roles/windows_private_paths/tasks/main.yml",
    "roles/windows_script_library/defaults/main.yml",
    "roles/windows_script_library/tasks/main.yml",
    "scripts/download_windows_sqlite.py"
  ],
  "source_hashes": {
    "artifacts/script-library/windows/bin/job-status.ps1": "079b16b49a9465be181c91d9d7dccf104dbffc06435420815297e31fdcf78203",
    "artifacts/script-library/windows/bin/script-jobs.ps1": "8e974b7c6db7d6bf50678816ddd3a9fc4ed3e9be4b22ebfcc9ff0d8813d4ecb1",
    "artifacts/script-library/windows/lib/ScriptLibrary.psm1": "7a0686547fdbeff443c849792b439b4f49314ab4e0b923653d244530983ec2a9",
    "artifacts/script-library/windows/lib/functions/Assert-JobPrivatePath.ps1": "d7e169bf3c1f3920259dbbcf28985e1e3b15bbe3b662653a0bf98a1d397670ba",
    "artifacts/script-library/windows/lib/functions/Complete-ScriptJob.ps1": "bc57772e978fd3e5087458a42ecb52e198b301a1be972e6186c1b43b7ee47061",
    "artifacts/script-library/windows/lib/functions/ConvertTo-JobAsciiMail.ps1": "bc02f170c1380984dd85abd57cd508bfbdf061f7c3a9d62d95de4082b292ebe8",
    "artifacts/script-library/windows/lib/functions/ConvertTo-JobSafeText.ps1": "77472536a6cd062113e14aa3cf63f7dbf8f9f383b30c386f974d885fb4ec0492",
    "artifacts/script-library/windows/lib/functions/ConvertTo-JobSqlLiteral.ps1": "e5af539dbf6faec3564f60b9dad418bf96f6287b09caa6aaf8bc2d576a863865",
    "artifacts/script-library/windows/lib/functions/Export-JobEvents.ps1": "e9755c57a7e2c3777dc148f06999e0d80c72d75f5623c5d12712d4b786263bf5",
    "artifacts/script-library/windows/lib/functions/Get-JobConfig.ps1": "56185172007601302e15c6b041e72e7f26da77533b0f93ce88957a4eee3b54ed",
    "artifacts/script-library/windows/lib/functions/Get-JobEventSql.ps1": "6d9216447874dfc9017ee9439bd615eed6118275acaa02485701f26fb042a49e",
    "artifacts/script-library/windows/lib/functions/Get-JobLocalCheck.ps1": "57596b81a186589c17a85e517bd12bb4cb4052e01eb3a5fe7e89ca5853e64af1",
    "artifacts/script-library/windows/lib/functions/Get-JobState.ps1": "3571b2af49e1189d5635e835da9ab286ae70274c63abeb95990f47dd52ca4e52",
    "artifacts/script-library/windows/lib/functions/Get-JobTimestamp.ps1": "91eb07d1ef9a5158235856a499cf7b8aca9cba8200101e3d1728104aa8493aea",
    "artifacts/script-library/windows/lib/functions/Get-SecurityAlertChannels.ps1": "dd8d156c56d8b797a49523b4ec8cc8af81b6e19a549e7eb6b35045e3f5a49b33",
    "artifacts/script-library/windows/lib/functions/Invoke-JobSql.ps1": "f816f97ad5ea31bd44b50fddbad8638b8bbee3b168e37a5808b554d8677c4d5d",
    "artifacts/script-library/windows/lib/functions/Invoke-ScriptJob.ps1": "8d617feff1e61e82201d3b4cb17073057372b1bf4c814ef527fde622042cc3e3",
    "artifacts/script-library/windows/lib/functions/New-JobStore.ps1": "b1e503dca715fb152767174442d9fbce0393715df62b3d5b206ff27a9a758fb3",
    "artifacts/script-library/windows/lib/functions/Open-JobStore.ps1": "59169a5aeffe8b1191e0f92b28744c6f6577153af0700962a38ae206bbe74afe",
    "artifacts/script-library/windows/lib/functions/Remove-JobHistory.ps1": "dd8ae68986e4abe61f6ea29a9d2b695e568903b93341d6dca1d9306d564a4009",
    "artifacts/script-library/windows/lib/functions/Save-SecurityAlert.ps1": "a91e7523373313b32a2074447b113a69c948acab8516e6d9d938dbb8ae2674cc",
    "artifacts/script-library/windows/lib/functions/Send-JobNotification.ps1": "ff68e6ccd0873fcf0505f25599a86688ba27e88bc40d38dbf1b5f1565bf14a45",
    "artifacts/script-library/windows/lib/functions/Send-SecurityAlert.ps1": "eab2b302ec1e18d8e815680693e3a5763f3217d8e851ec414543f2528fe58814",
    "artifacts/script-library/windows/lib/functions/Send-SecurityAlertQueue.ps1": "5a4bb765ca975c5fb3f4137de7e07d65fa4a4aadaf0841bd6d755929dbc9d81f",
    "artifacts/script-library/windows/lib/functions/Set-JobItem.ps1": "c30018cf1a93cdbb21a8d9bad9ecb13a79c426b0fb346d03a4d40649590d42a5",
    "artifacts/script-library/windows/lib/functions/Start-ScriptJob.ps1": "fbedfb018f998f38f4453232f5b926d17fcb3752cb6452d571291b4f5cc644ab",
    "playbooks/windows/stage_library.yml": "1c95dca690bc7a5203140ba695c6c041301baa83764246f2b27bbf4e058238c3",
    "roles/windows_private_paths/defaults/main.yml": "837dd13bfcadd8e9aa90d307c16f693d50f98c30665bdf007cf28d653713a2a0",
    "roles/windows_private_paths/tasks/main.yml": "339efbc5858ac5acb1fbd2a53a988be36e60d03aa6f47bc19a80f3b0a9fdb38e",
    "roles/windows_script_library/defaults/main.yml": "498c646175a7f392295d6cb65a15b36c9326837c1cc5b837d360a90238d933f5",
    "roles/windows_script_library/tasks/main.yml": "fa716834bc1593354a822ca6a378261b0d939c5e842631db2289082e986bd667",
    "scripts/download_windows_sqlite.py": "9e54ffc684d76230e1b79af158fb98cea1eee7f19bd0c812ec391c3390598a62"
  },
  "i18n": {
    "en": {
      "title": "Stage the shared Windows job library",
      "description": "# Stage the shared Windows job library\n\nPrepare the verified x64 SQLite artifact with `python3 scripts/download_windows_sqlite.py --apply`.\nThe downloader pins the official archive version and SHA3-256, extracts only sqlite3.exe,\nand retains a different existing executable. Binaries/private settings stay outside Git.\nThen run `ansible-playbook playbooks/windows/stage_library.yml --limit example-windows-host`.\nUse a separate pilot code/state path for the first test.\n\n`windows_script_root` defaults to C:\\Scripte, `windows_state_root` to C:\\ProgramData\\ScriptJobs.\nThe role deploys the complete common PowerShell library, the shared SQL schema and mail\ntable, query helpers and declared SQLite runtime. Code/state directories grant SYSTEM\nand built-in Administrators access by SID. Reparse points are refused. AllSigned requires the configured central signing pipeline; disabled signing cannot bypass it. Real Windows ACL/signing/MSI behavior still needs\nan authenticated Windows pilot; portable PowerShell tests do not establish that behavior.\n\nLocal APIs record start/items/completion, export schema-1 cursor batches, prune completed\nhistory after 90 days and provide read-only latest/Checkmk views. Process execution is\nan explicit API for server jobs; it is not a replacement for an existing GPO background\nwrapper. This playbook schedules no business task and deploys no private host scripts.\nSYSVOL, GPO links/settings and ADMX deployment remain separate work.",
      "fields": {}
    },
    "de": {
      "title": "Gemeinsame Windows-Joblibrary bereitstellen",
      "description": "# Gemeinsame Windows-Joblibrary bereitstellen\n\n`python3 scripts/download_windows_sqlite.py --apply` bereitet die fest versionierte,\ngegen die offizielle SHA3-Summe geprüfte x64-SQLite-Laufzeit vor. Nur sqlite3.exe wird\nentnommen; eine abweichende vorhandene EXE bleibt erhalten. Die Binärdatei bleibt lokal.\nDanach `ansible-playbook playbooks/windows/stage_library.yml --limit example-windows-host`\nverwenden. Beim ersten Pilot getrennte Code-/Datenpfade wählen.\n\nDie komplette Grundlibrary, ein gemeinsames SQL-Schema, die feste Mailtabelle und lokale\nAbfragehelfer werden verteilt. Standardpfade sind C:\\Scripte und C:\\ProgramData\\ScriptJobs;\n`windows_script_root`, `windows_state_root`, `windows_job_database` und `windows_sqlite_exe`\nbilden die feste Zuordnung. Private ACLs verwenden SYSTEM-/Administratoren-SIDs.\nReparsepunkte werden abgewiesen. AllSigned verlangt eine konfigurierte Signierstrecke.\nWindows-ACLs, Signierung und MSI brauchen noch einen echten Windows-Pilot.\n\nDie APIs erfassen Start, Einzelobjekte und Ende in SQLite, exportieren Cursorpakete und\nhalten abgeschlossene Läufe 90 Tage. Status- und Checkmk-Abfragen sind lesend. Ein\nProzessrunner ist ausdrücklich für Serverjobs vorgesehen und ersetzt keinen GPO-\nBackground-Wrapper. Dieses Playbook verteilt keine privaten Fachskripte und aktiviert\nkeine Fachaufgabe. SYSVOL, GPOs und ADMX bleiben getrennt.",
      "fields": {}
    }
  }
}
```

</details>
