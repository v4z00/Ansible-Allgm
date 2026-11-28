# Read local job health with Checkmk

Run `ansible-playbook playbooks/scripts/checkmk_jobs.yml --limit example-host` after
choosing `script_jobs_checkmk_jobs`. Each entry explicitly names job, max_age_seconds
and max_runtime_seconds. Only selected jobs are monitored; no task is started or repaired.
Missing data is UNKNOWN, failed/overdue jobs are CRIT, warnings WARN. Raw summaries and
notification credentials are never included in the local-check output.

`script_jobs_checkmk_security_outbox: true` adds a pending-delivery service. Linux uses
a read-only Python SQLite connection; Windows uses the PowerShell library and SQLite
CLI. The Windows agent calls `script_jobs.cmd`, which invokes the managed
PowerShell entry point in the shared library. In a signing environment that entry
point is covered by the library's Authenticode receipt and keeps the host policy.
Verify live output in the agent's `dump` command in addition to testing the query.
The playbook preserves other local checks.

Windows agent rollout is separate: `checkmk-download --platform windows` downloads the
site MSI and selected Windows plugins; `checkmk_manage_windows_agents: true` in the
inventory generator config enrolls discovered Windows guests as managed agent hosts.
Keep that opt-in off until WinRM/credentials and an MSI pilot have been checked. The
agent role routes Windows to MSI/service tasks and Linux to the existing apt/systemd tasks.

<details>
<summary>Deutsch</summary>

# Lokale Jobzustände mit Checkmk prüfen

`playbooks/scripts/checkmk_jobs.yml --limit example-host` installiert lesende Checks.
`script_jobs_checkmk_jobs` enthält je Eintrag job, max_age_seconds und max_runtime_seconds.
Nur ausdrücklich ausgewählte Jobs werden überwacht. Fehlende Daten sind UNKNOWN,
fehlgeschlagene oder überfällige Läufe CRIT, Warnungen WARN. Keine Reparaturen oder
Fachjobs werden gestartet; Rohmeldungen und Zugangsdaten erscheinen nicht im Output.

`script_jobs_checkmk_security_outbox: true` überwacht offene Alarmzustellungen. Linux
liest SQLite über Python, Windows über die PowerShell-Library. Deren Signatur- und
Laufzeitvoraussetzungen gelten auch hier. Andere lokale Checks bleiben erhalten.

Der Agentrollout ist getrennt: `checkmk-download --platform windows` lädt Site-MSI und
ausgewählte Windows-Plugins. `checkmk_manage_windows_agents: true` im Inventorygenerator
nimmt Windows in die verwaltete Agentgruppe auf. Erst nach geprüftem WinRM-/MSI-Pilot
aktivieren. Die Agentrolle trennt Windows-MSI/Service von Linux-apt/systemd.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "playbooks/scripts/checkmk_jobs.yml",
  "title": "Lokale Jobzustände mit Checkmk prüfen",
  "documented": true,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/checkmk.yml",
    "playbooks/scripts/checkmk_jobs.yml",
    "roles/checkmk_agent/defaults/main.yml",
    "roles/checkmk_agent/tasks/linux.yml",
    "roles/checkmk_agent/tasks/main.yml",
    "roles/checkmk_agent/tasks/windows.yml",
    "roles/script_jobs_checkmk/defaults/main.yml",
    "roles/script_jobs_checkmk/filter_plugins/checks.py",
    "roles/script_jobs_checkmk/tasks/linux.yml",
    "roles/script_jobs_checkmk/tasks/main.yml",
    "roles/script_jobs_checkmk/tasks/windows.yml",
    "roles/script_jobs_checkmk/templates/script_jobs.ps1.j2",
    "scripts/download_checkmk_artifacts.sh",
    "scripts/generate_inventory.py",
    "scripts/job_local_check.py"
  ],
  "source_hashes": {
    "playbooks/checkmk.yml": "de3ba3fbc4b5062e096841d927f18c9e7aba041582d249c43b5c8e81d8d9436e",
    "playbooks/scripts/checkmk_jobs.yml": "d90bc0f376cca1bf9131dbe09299007805f337bdcaae5c2784d2fe03eb8b562c",
    "roles/checkmk_agent/defaults/main.yml": "422897957fc27c7ba1ed404f0cf20ea170bd2780150e0f1c68f80a704c32f910",
    "roles/checkmk_agent/tasks/linux.yml": "8aa1d752862aa41512a2024dbe7ee15c90a6d0360708f5f97c839cc40353d4e8",
    "roles/checkmk_agent/tasks/main.yml": "de2fe6270bda944bea360070650949668ace1dc1aa4e5b67b58909d165ea1319",
    "roles/checkmk_agent/tasks/windows.yml": "699e248aca276dd5f3e0f270f86839db8e8f9542f63cbd1d1ca9e7ad76c63510",
    "roles/script_jobs_checkmk/defaults/main.yml": "09a50c65d8d4b08745fe2df006c1625d3669b81db0bd5e8de0d5d5c48a3f555c",
    "roles/script_jobs_checkmk/filter_plugins/checks.py": "cf7777c13774bbbe3a3213c7eeeb895916095003f47f933b6597d7312b98cde8",
    "roles/script_jobs_checkmk/tasks/linux.yml": "1da9580d2d105a26bc8eacf7724794084f0a16dddf843f0fe9dcc7317aeb9d8d",
    "roles/script_jobs_checkmk/tasks/main.yml": "261b4e9fb6a40586b75d6e19cef3a26a7a2773b945cde5bff946b611a214b29a",
    "roles/script_jobs_checkmk/tasks/windows.yml": "656b4354da46bac1adeac2133792b6ce15ded20b94a9a79870c488c785689ed1",
    "roles/script_jobs_checkmk/templates/script_jobs.ps1.j2": "607417cde68fc33d578bb5fbd929d5c95efb20b78cae4b918a669c75464adaad",
    "scripts/download_checkmk_artifacts.sh": "d8e84ccf2ca1f4a235e9081de370884d8e4bb624aa18914ac88014a3585da1c7",
    "scripts/generate_inventory.py": "59884a06584dd700b3235e07a0e804005edae6ffbcd88e51ce7d0e2cba0bc6a9",
    "scripts/job_local_check.py": "1e9f40f91816d17442ec2f1e6f261ddb820e46b9deeea65472dd69f2ab38fede"
  },
  "i18n": {
    "en": {
      "title": "Read local job health with Checkmk",
      "description": "# Read local job health with Checkmk\n\nRun `ansible-playbook playbooks/scripts/checkmk_jobs.yml --limit example-host` after\nchoosing `script_jobs_checkmk_jobs`. Each entry explicitly names job, max_age_seconds\nand max_runtime_seconds. Only selected jobs are monitored; no task is started or repaired.\nMissing data is UNKNOWN, failed/overdue jobs are CRIT, warnings WARN. Raw summaries and\nnotification credentials are never included in the local-check output.\n\n`script_jobs_checkmk_security_outbox: true` adds a pending-delivery service. Linux uses\na read-only Python SQLite connection; Windows uses the PowerShell library and SQLite\nCLI. The Windows library/signing prerequisites apply. The playbook adds only its own\nentry point and leaves other local checks intact.\n\nWindows agent rollout is separate: `checkmk-download --platform windows` downloads the\nsite MSI and selected Windows plugins; `checkmk_manage_windows_agents: true` in the\ninventory generator config enrolls discovered Windows guests as managed agent hosts.\nKeep that opt-in off until WinRM/credentials and an MSI pilot have been checked. The\nagent role routes Windows to MSI/service tasks and Linux to the existing apt/systemd tasks.",
      "fields": {}
    },
    "de": {
      "title": "Lokale Jobzustände mit Checkmk prüfen",
      "description": "# Lokale Jobzustände mit Checkmk prüfen\n\n`playbooks/scripts/checkmk_jobs.yml --limit example-host` installiert lesende Checks.\n`script_jobs_checkmk_jobs` enthält je Eintrag job, max_age_seconds und max_runtime_seconds.\nNur ausdrücklich ausgewählte Jobs werden überwacht. Fehlende Daten sind UNKNOWN,\nfehlgeschlagene oder überfällige Läufe CRIT, Warnungen WARN. Keine Reparaturen oder\nFachjobs werden gestartet; Rohmeldungen und Zugangsdaten erscheinen nicht im Output.\n\n`script_jobs_checkmk_security_outbox: true` überwacht offene Alarmzustellungen. Linux\nliest SQLite über Python, Windows über die PowerShell-Library. Deren Signatur- und\nLaufzeitvoraussetzungen gelten auch hier. Andere lokale Checks bleiben erhalten.\n\nDer Agentrollout ist getrennt: `checkmk-download --platform windows` lädt Site-MSI und\nausgewählte Windows-Plugins. `checkmk_manage_windows_agents: true` im Inventorygenerator\nnimmt Windows in die verwaltete Agentgruppe auf. Erst nach geprüftem WinRM-/MSI-Pilot\naktivieren. Die Agentrolle trennt Windows-MSI/Service von Linux-apt/systemd.",
      "fields": {}
    }
  }
}
```

</details>
