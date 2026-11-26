# Jobs und lokale Ergebnisse

`bin/control jobs` öffnet das Shell-Menü. Die Daten bleiben lokal auf den Hosts;
Abfragen verwenden das vorhandene Inventory und dessen SSH-/Become-Einstellungen.

```sh
bin/control jobs --limit example-host collect
bin/control jobs --source example-host runs
bin/control jobs --source example-host latest
bin/control jobs --source example-host --job backup errors
bin/control jobs --run LAUF-ID details
bin/control jobs --limit example-host live --seconds 60
bin/control jobs --limit example-host --json live --seconds 60
bin/control jobs --item 101 --since 1795392000 runs
bin/control jobs reports
```

`--project` bezeichnet den bestehenden Controllerroot, `--inventory` überschreibt
nur auf ausdrücklichen Wunsch das Inventory. `--db` überschreibt die lokale
Controllerdatenbank; sonst gilt `config/script_jobs_controller.json` oder der
Standard `/var/lib/script-jobs/controller.sqlite3`. `--since`/`--until` sind
UTC-Unixzeitstempel. Anzeigen starten keine Backupjobs.

`collect` liefert JSON. `live --json` liefert NDJSON mit einzelnen Ereignissen und
Heartbeats. Die Abfrage erfolgt in kurzen Ansible-Aufrufen über SSH; es ist kein
separater Netzwerkdienst installiert. Ohne `--json` zeigt die Liveansicht Symbole
und Text. Frühere Daten bleiben nach Verbindungsabbruch abrufbar.

Eine neue Datenbankgeneration oder Lücke durch die 90-Tage-Aufbewahrung wird nicht
stillschweigend akzeptiert. Nach Prüfung bestätigt
`bin/control jobs --source example-host reset-cursor` den erneuten Import der noch
vorhandenen Daten. Bereits gesendete Inhalte können nach einer solchen bewussten
Neuanbindung erneut erscheinen; Verlauf und Bericht-IDs bleiben sichtbar.

Das Menü zeigt laufende Jobs, letzte Ergebnisse, Fehler/Warnungen, Details,
Liveereignisse und Versandzustände. Root bzw. der konfigurierte Datenbankbesitzer
benötigt Zugriff auf die privaten lokalen Dateien. Controller: Python ab 3.11 und
die vorhandene Ansible-Umgebung. Keine freien SQL- oder Remote-Shell-Eingaben.

## Lokale Jobs und Ergebnisansicht

Die neutrale Grundbibliothek liegt unter [artifacts/script-library](../../artifacts/script-library/).
Betriebsskripte, Spezialfunktionen, Hostkonfiguration und Secrets bleiben lokal
unter `/root/skripte-config/<Hostname>/`. Die Playbooks verteilen aus diesen
privaten Quellen in den vorhandenen `script_path`; Git verteilt die Library und
die generischen Playbooks, nicht die produktiven Skripte.

`bin/control jobs` öffnet die kleine Shell-Oberfläche. Die Hosts führen ihre Jobs
weiterhin selbst per Cron aus. Ergebnisse liegen lokal in SQLite, werden 90 Tage
aufbewahrt und über die vorhandenen Ansible-/SSH-Verbindungen abgefragt. Die
Liveansicht kann einzelne JSON-Ereignisse ausgeben, ohne die Datenbank über das
Netzwerk zu öffnen. `bin/control jobs-summary` konsolidiert die allgemeinen
Ergebnisse. Der Controller sendet für Vzdump einen getrennten Abschlussbericht.

Die Einrichtung ist unter [Skripte verteilen](../roles/script_jobs.md), [Ergebnis-Controller einrichten](../roles/script_jobs_controller.md) und in den [Beispielen](../../examples/script_jobs/) beschrieben. Ohne eine konkrete lokale Auswahl und
Zeitpläne wird kein Cronjob erfunden oder gestartet.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "jobs",
  "title": "Jobs und lokale Ergebnisse",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/jobs.json",
    "bin/control.d/jobs.sh",
    "scripts/job_console.py"
  ],
  "source_hashes": {
    "bin/control.d/jobs.json": "24dcd5c94d8d2bb818f3b3100d74f2b294d8ff07479395dc4273307a61384c68",
    "bin/control.d/jobs.sh": "7247b8df4c0662e5a92338d005fac347d9632ce52f3f2bfc84217b363702293e",
    "scripts/job_console.py": "03c27d3957d2f9df811175ca3bf5fc22434554585471379d9ae249cef46e513d"
  },
  "i18n": {
    "de": {
      "title": "Jobs und lokale Ergebnisse",
      "description": "# Jobs und lokale Ergebnisse\n\n`bin/control jobs` öffnet das Shell-Menü. Die Daten bleiben lokal auf den Hosts;\nAbfragen verwenden das vorhandene Inventory und dessen SSH-/Become-Einstellungen.\n\n```sh\nbin/control jobs --limit example-host collect\nbin/control jobs --source example-host runs\nbin/control jobs --source example-host latest\nbin/control jobs --source example-host --job backup errors\nbin/control jobs --run LAUF-ID details\nbin/control jobs --limit example-host live --seconds 60\nbin/control jobs --limit example-host --json live --seconds 60\nbin/control jobs --item 101 --since 1795392000 runs\nbin/control jobs reports\n```\n\n`--project` bezeichnet den bestehenden Controllerroot, `--inventory` überschreibt\nnur auf ausdrücklichen Wunsch das Inventory. `--db` überschreibt die lokale\nControllerdatenbank; sonst gilt `config/script_jobs_controller.json` oder der\nStandard `/var/lib/script-jobs/controller.sqlite3`. `--since`/`--until` sind\nUTC-Unixzeitstempel. Anzeigen starten keine Backupjobs.\n\n`collect` liefert JSON. `live --json` liefert NDJSON mit einzelnen Ereignissen und\nHeartbeats. Die Abfrage erfolgt in kurzen Ansible-Aufrufen über SSH; es ist kein\nseparater Netzwerkdienst installiert. Ohne `--json` zeigt die Liveansicht Symbole\nund Text. Frühere Daten bleiben nach Verbindungsabbruch abrufbar.\n\nEine neue Datenbankgeneration oder Lücke durch die 90-Tage-Aufbewahrung wird nicht\nstillschweigend akzeptiert. Nach Prüfung bestätigt\n`bin/control jobs --source example-host reset-cursor` den erneuten Import der noch\nvorhandenen Daten. Bereits gesendete Inhalte können nach einer solchen bewussten\nNeuanbindung erneut erscheinen; Verlauf und Bericht-IDs bleiben sichtbar.\n\nDas Menü zeigt laufende Jobs, letzte Ergebnisse, Fehler/Warnungen, Details,\nLiveereignisse und Versandzustände. Root bzw. der konfigurierte Datenbankbesitzer\nbenötigt Zugriff auf die privaten lokalen Dateien. Controller: Python ab 3.11 und\ndie vorhandene Ansible-Umgebung. Keine freien SQL- oder Remote-Shell-Eingaben.\n\n## Lokale Jobs und Ergebnisansicht\n\nDie neutrale Grundbibliothek liegt unter [artifacts/script-library](../../artifacts/script-library/).\nBetriebsskripte, Spezialfunktionen, Hostkonfiguration und Secrets bleiben lokal\nunter `/root/skripte-config/<Hostname>/`. Die Playbooks verteilen aus diesen\nprivaten Quellen in den vorhandenen `script_path`; Git verteilt die Library und\ndie generischen Playbooks, nicht die produktiven Skripte.\n\n`bin/control jobs` öffnet die kleine Shell-Oberfläche. Die Hosts führen ihre Jobs\nweiterhin selbst per Cron aus. Ergebnisse liegen lokal in SQLite, werden 90 Tage\naufbewahrt und über die vorhandenen Ansible-/SSH-Verbindungen abgefragt. Die\nLiveansicht kann einzelne JSON-Ereignisse ausgeben, ohne die Datenbank über das\nNetzwerk zu öffnen. `bin/control jobs-summary` konsolidiert die allgemeinen\nErgebnisse. Der Controller sendet für Vzdump einen getrennten Abschlussbericht.\n\nDie Einrichtung ist unter [Skripte verteilen](../roles/script_jobs.md), [Ergebnis-Controller einrichten](../roles/script_jobs_controller.md) und in den [Beispielen](../../examples/script_jobs/) beschrieben. Ohne eine konkrete lokale Auswahl und\nZeitpläne wird kein Cronjob erfunden oder gestartet.\n\nDer Abfragepfad folgt wie das Job-Deployment `script_jobs_target_root`, dann\n`script_path`, sonst `/scripte`. Eine separat gestagte Library legt keinen\nabweichenden Pfad für produktive Jobs fest.\n\n`latest` zeigt den letzten gespeicherten Zustand je Quelle/Job, einschließlich\nlaufender Jobs. Diese Ansicht verwendet den letzten Abholstand und unterstützt\n`--source`/`--job`. Für Zeit- und Einzelobjektfilter bleibt `runs` zuständig.\n`--config` wählt eine eigene private Controllerkonfiguration.\n\n[jobs-last](jobs-last.md) fragt die letzten Zustände unmittelbar auf den Hosts ab.\nBeide Ansichten starten keine Jobs und senden keine Nachrichten.",
      "fields": {}
    },
    "en": {
      "title": "Browse jobs and local results",
      "description": "# Browse jobs and local results\n\n`bin/control jobs` opens the shell menu. Hosts keep their local data. Queries use the existing inventory and SSH/become settings.\n\n```sh\nbin/control jobs --limit example-host collect\nbin/control jobs --source example-host runs\nbin/control jobs --source example-host latest\nbin/control jobs --source example-host --job backup errors\nbin/control jobs --run LAUF-ID details\nbin/control jobs --limit example-host live --seconds 60\nbin/control jobs --limit example-host --json live --seconds 60\nbin/control jobs --item 101 --since 1795392000 runs\nbin/control jobs reports\n```\n\n`--project` identifies the controller root. Override inventory explicitly with `--inventory` or the local database with `--db`. By default the database comes from `config/script_jobs_controller.json` or `/var/lib/script-jobs/controller.sqlite3`. `--since` and `--until` use UTC Unix timestamps. Viewing results starts no backups.\n\n`collect` returns JSON. `live --json` streams NDJSON events and heartbeats through short Ansible SSH calls. There is no additional network service. The regular live view shows symbols and text. Earlier data remains available after disconnection.\n\nA new database generation or gap caused by 90-day retention requires review. After checking it, run `bin/control jobs --source example-host reset-cursor` to reimport remaining data. Previously delivered content can reappear after this explicit reset. History and report IDs stay visible.\n\nThe menu shows running jobs, recent outcomes, warnings/errors, details, live events and delivery states. Root or the configured database owner needs access to the private files. The controller requires Python 3.11+ and its Ansible environment. There is no arbitrary SQL or remote-shell input.\n\n## Local jobs and results\n\nThe shared library is under [artifacts/script-library](../../artifacts/script-library/). Operational scripts, custom functions, host settings and secrets stay under `/root/skripte-config/<Hostname>/`. Playbooks deploy from these private sources to the existing `script_path`. Git supplies the library and generic playbooks.\n\n`bin/control jobs` opens the shell UI. Each host’s cron continues running jobs locally. SQLite retains results for 90 days. Queries use existing Ansible/SSH connections. Live mode can return individual JSON events while keeping SQLite off the network. `bin/control jobs-summary` aggregates ordinary results. Vzdump gets its own completion report.\n\nSee [Deploy scripts](../roles/script_jobs.md), [Set up the results controller](../roles/script_jobs_controller.md) and the [examples](../../examples/script_jobs/). Select local jobs and schedules explicitly before enabling cron.\n\nThe query root follows job deployment: `script_jobs_target_root`, then `script_path`, otherwise `/scripte`. Staging a library separately does not change the live job paths.\n\n`latest` shows the latest collected state per source and job, including running jobs. Filter using `--source` or `--job`. Use `runs` for time or individual-item filters. Select a private controller configuration with `--config`.\n\n[jobs-last](jobs-last.md) queries the hosts directly for current states. Both views are read-only and send no notifications.",
      "fields": {}
    }
  }
}
```

Der Abfragepfad folgt wie das Job-Deployment `script_jobs_target_root`, dann
`script_path`, sonst `/scripte`. Eine separat gestagte Library legt keinen
abweichenden Pfad für produktive Jobs fest.

`latest` zeigt den letzten gespeicherten Zustand je Quelle/Job, einschließlich
laufender Jobs. Diese Ansicht verwendet den letzten Abholstand und unterstützt
`--source`/`--job`. Für Zeit- und Einzelobjektfilter bleibt `runs` zuständig.
`--config` wählt eine eigene private Controllerkonfiguration.

[jobs-last](jobs-last.md) fragt die letzten Zustände unmittelbar auf den Hosts ab.
Beide Ansichten starten keine Jobs und senden keine Nachrichten.
