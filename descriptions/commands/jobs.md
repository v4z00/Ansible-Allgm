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
    "scripts/job_console.py": "e4f31a820b92cc918e5c2b0d5bd91a3c4da97bcfbaa58169a48b628bb1becdfe"
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
