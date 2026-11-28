# Windows-Skriptprofile

Die Windows-Inventorygruppen enthalten die Ziele. Gruppenvariablen definieren
Profile, Hostvariablen wählen sie aus. `windows_script_profiles_source_root`
bestimmt den privaten Quellordner. Standard ist `/root/skripte-config/windows`.

Jeder Profilordner enthält ein `deployment.json` mit `schema: 1` und einer
expliziten Dateiliste unter `files`. Jeder Eintrag nennt den relativen `path`
und die `sha256` der geprüften PowerShell-Datei. Ansible erhält die relative
Struktur und legt pro Inhalt einen eigenen Release an. Frühere Releases
stehen für den Rückweg zur Verfügung.

```yaml
windows_script_profiles:
  inventory-report:
    scope: local
    task:
      script: bin/Inventory-Report.ps1
      enabled: true
      multiple_instances: 2
      triggers:
        - type: daily
          start_boundary: '2026-01-01T07:00:00'
  windows-logon-tools:
    scope: sysvol
windows_script_profiles_selected:
  - inventory-report
```

`task` ist optional. Lokale Aufgaben verwenden das Skriptverzeichnis als
Arbeitsverzeichnis. Standardkonto ist SYSTEM. Für vorhandene Aufgaben mit
Domänenkonto verweist `task.principal` auf den benannten Eintrag in
`windows_script_profiles_principals` mit `username` und `password` aus der
privaten Secrets-Datei. Das Konto braucht die vorgesehenen Netzwerk- und
Dateirechte sowie das Windows-Recht zur Anmeldung als Stapelauftrag.
`run_level` kann beim Konto `highest` oder `limited` sein. Ein eingeschränktes
Konto braucht getrennt vergebene Zugriffsrechte auf Code, Konfiguration und
SQLite, damit der Jobrunner den Lauf speichern kann.
`update_password` am Konto erfolgt bei unveränderter Aufgabe nur auf
ausdrückliche Konfiguration. Ein bestehender Name unter
`\Ansible\PrivateScripts` muss der eigenen Besitzbeschreibung entsprechen.

Lokale Profilaufgaben verwenden standardmäßig den SQLite-Jobrunner. Die Rolle
prüft den installierten Runner und die lokale Datenbank, schreibt die
Auftragsspezifikation unter `config/profile-jobs` in den privaten Windows-
Statusordner und registriert den Aufruf ohne eine sofortige Ausführung.
Die Windows-Bibliothek mit aktualisiertem `script-jobs.ps1` und geprüftem
SQLite wird vorher über `playbooks/windows/stage_library.yml` bereitgestellt.
Versionierte Spezifikationen und Einstellungen erhalten einen nutzbaren Rückweg für die
Aufgabenplanung. `task.record_job: false` ermöglicht einzelne Aufgaben ohne
Job-Erfassung, beispielsweise reine Installationshilfen.

Für eine feste Reihenfolge enthält `task.additional_profiles` die Namen der
Profile, die der Hauptaufgabe folgen. Die Zusatzprofile stehen früher in
`windows_script_profiles_selected` und setzen `task.on_demand: true` ohne
Trigger. Alle Schritte laufen unter dem Konto der Hauptaufgabe. Der
Jobrunner speichert Ergebnis und Laufzeit jedes Schritts separat.

Private Gruppen- oder Hostvariablen können `windows_script_profiles_settings`
mit je einem Schlüssel pro überwachtem Profil setzen. Ansible rendert dessen
Einstellungen in den geschützten Jobstatusordner. `HM_JOB_CONFIGFILES` enthält
im gestarteten Programm die JSON-Liste der Konfigurationspfade.
`Get-JobConfig` liest die Dateien aus der lokalen Bibliothek. Werte bleiben
außerhalb des Code-Manifests, der Task-Argumente und von SYSVOL.

Der zentrale Sammler übernimmt die Läufe, sobald die zugehörigen Windows-
Inventorygruppen in `script_jobs_targets` stehen. Die vorhandenen Checkmk-
Local-Checks lesen ausgewählte Jobs aus derselben Datenbank.

```sh
ansible-playbook playbooks/windows/deploy_profiles.yml --limit app-example --check
ansible-playbook playbooks/windows/deploy_sysvol_profiles.yml --limit dc-example --check
```

Für SYSVOL bestimmt `windows_script_profiles_sysvol_writer` den schreibenden
DC des Laufs. Die Rolle ermittelt die Domäne auf dem Ziel. Der Code landet
unter `SYSVOL/<Domäne>/scripts/<windows_script_profiles_sysvol_subdir>/<Profil>/<Release>`
mit den geerbten ACLs. Die Verknüpfung in der GPMC bestimmt den GPO-Geltungsbereich.
Vor der Verknüpfung die Replikation auf den DCs prüfen.

Die [Codesignierung](../configurations/windows-code-signing.md) kann auf dem
Signierhost oder vorab in einer interaktiven Benutzersitzung erfolgen.
Für die zweite Variante `windows_script_profiles_use_presigned: true` setzen
und die SHA-256 der signierten Dateien in das Manifest übernehmen. Beide
Varianten prüfen Authenticode und den erwarteten Herausgeber beim Echtlauf.

Der [WinRM-Helfer](../../scripts/windows/Ensure-WinRmHttps.ps1) bestimmt
seinen eigenen Domänen-FQDN und nutzt ein passendes Maschinenzertifikat.
Die GPO-Computeraufgabe ruft `powershell.exe -NoProfile -NonInteractive -File
"<vollständiger UNC-Pfad zur signierten Datei>"` auf. Standard ist TCP
5986. Der Helfer richtet einen fehlenden Listener ein und erhält vorhandene
Bindungen. Die GPO-Verknüpfung bestimmt, welche Computer die Aufgabe erhalten.

## Neue Windows-Installation

Maschinenzertifikat, Firewall, Kerberos und HTTPS-Listener bilden den
Zugang für neue Domänencomputer. Danach zuerst das bestehende Windows-
Check-Playbook aufrufen, dann das [Bootstrap-Playbook](../../playbooks/windows/bootstrap.yml)
für die gewählte Inventorygruppe. Anschließend können die gemeinsame Windows-
Library und die ausgewählten Skriptprofile auf dieselbe Gruppe verteilt werden.
