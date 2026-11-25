# Lokale Skripte mit neutraler Library bereitstellen

Die ausführbaren Betriebsskripte liegen ausschließlich unter
`/root/skripte-config/<inventory_hostname>/` auf dem Controller. Diese privaten
Quellen, Spezialfunktionen, Hostwerte und Secrets gehören nicht in ein Git-Repo.
In `artifacts/script-library/` liegt nur die neutrale Grundbibliothek.

```sh
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --syntax-check
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --check
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host
```

Die Rolle verlangt ein geprüftes lokales `deployment.json` mit `files`-Einträgen
(`path`, `sha256`, `kind`). Erlaubt sind Einstiegsskripte, `programs/*.sh`,
`config/*.json` und `lib/special/**/*.sh`. Lokale Quellen dürfen die Git-Library
nicht überschreiben. Eingangs-SHA werden vor dem Übertragen geprüft; gerenderte
Zielkonfigurationen sind bewusst eigenständige lokale Dateien.

| Variable | Bedeutung / Standard |
|---|---|
| `script_jobs_source_root` | Lokale Controllerquelle, `/root/skripte-config` |
| `script_jobs_target_root` | Bestehendes `script_path`, sonst `/scripte` |
| `script_jobs_database_path` | Laufzeitdaten außerhalb der Skripte, `/var/lib/script-jobs/jobs.sqlite3` |
| `script_jobs_owner`, `script_jobs_group` | Ausführungs-/Dateibesitzer, jeweils `root` |
| `script_jobs_common_config` | Ausdrückliche gemeinsame JSON-Werte, sonst bestehendes `script_library_common_config` oder `{}` |
| `script_jobs_job_config` | Ausdrückliche Werte pro Skriptinstanz, sonst `script_library_job_config` oder `{}` |
| `script_jobs` | Ausdrückliche Liste zu verwaltender Cronjobs, `[]` |
| `script_jobs_sets` | Lokal definierte wiederverwendbare Joblisten, `{}` |
| `script_jobs_selected_sets` | Ausgewählte lokale Sets, `[]` |
| `script_jobs_timezone` | Explizite IANA-Zeitzone für Erwartungsprüfung |

Ein Job hat `name`, `script`, optional `args` als Liste und `user`, `category`
(`general`/`vzdump`), einen `cron`-Block und gegebenenfalls `expected`.
Cron kann Kalenderfelder oder `special_time` verwenden. Vzdump benötigt explizit
Montag (`1`/`mon`). `expected.deadline_minutes` und
`expected.max_runtime_minutes` bestimmen fehlende/überfällige Läufe. Komplexe
Zeitpläne benötigen explizite `expected.start`/`expected.weekdays` (Montag=0).
Ein nicht vollständig beschriebener Erwartungsplan wird als unkonfiguriert
angezeigt, niemals als bewiesener Erfolg. Kalenderüberwachung und tatsächliche
Ausführung sind getrennte Dinge.

Konfiguration: private Quelldaten, dann ausdrücklich gesetzte Hostvariablen.
Beim Lauf gilt `common.json`, danach die Skriptdatei. Explizit leere Skriptwerte
überschreiben gemeinsame Werte. `JOB_DATABASE_PATH` muss mit der
Ansible-Datenbankzuordnung übereinstimmen; Konflikte werden vor dem Schreiben
abgewiesen. `JOB_MAX_RUNTIME_SECONDS` kann das Laufzeitlimit des Runners setzen.

Alle Jobs einer lokalen Datenbank verwenden denselben konfigurierten Besitzer.
Die Dateien und Datenbank sind `0600`, Verzeichnisse `0700`, Programme `0700`.
Die Rolle wird unter den vorhandenen Become-Einstellungen ausgeführt.

Cron wird ausschließlich für die expliziten Einträge verwaltet. Ein unbekannter
Altaufruf, ein noch laufendes Skript oder ein systemweiter Cron-Konflikt blockiert
die Umstellung. Eine genaue alte Befehlszeile kann nach Prüfung als
`legacy_command` zugeordnet werden. Fremde Jobs werden nicht gelöscht. Unbekannte
Dateien oder aus der Auswahl entfernte frühere Jobs werden nicht still bereinigt.

Die Rolle startet keine Backupskripte. Ohne Cronliste werden Dateien und SQLite
bereitgestellt, aber kein Zeitplan erfunden. Es gibt keine künstlichen
Deaktivierungsschalter. Für die tatsächliche Cron-Übernahme ist ein Pilot mit der
konkreten lokalen Konfiguration erforderlich.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/script_jobs",
  "title": "Lokale Skripte mit neutraler Library bereitstellen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/script_jobs/defaults/main.yml",
    "roles/script_jobs/tasks/main.yml",
    "roles/script_jobs/templates/expectations.json.j2",
    "scripts/job_cron_guard.py",
    "roles/script_jobs/filter_plugins/local_config.py"
  ],
  "source_hashes": {
    "roles/script_jobs/defaults/main.yml": "617986cf4e0b7202baeda6c21654b606cade532987440a04c5a17ee66a04fc4f",
    "roles/script_jobs/tasks/main.yml": "9877c12026e2a4f4920e8c176b3717163678e50c8d8296aa34da36b59826dbdd",
    "roles/script_jobs/templates/expectations.json.j2": "8784701f26e6f5e251f580e6b5dc6415775f0470526a7b17c67bd8919ab5d5bd",
    "scripts/job_cron_guard.py": "c34ea1082b716021447fcff3869c73d9dfac808775118d3d38cde965543457d2",
    "roles/script_jobs/filter_plugins/local_config.py": "7932352e3605e2826910081c8f2cbf513d9b8dcedbad205b08fcb9e27e115adc"
  }
}
```

Nach dem Zusammenführen der Konfiguration entfernt die Rolle die Mail-/Telegramwerte
und setzt alte Versandflags auf `false`. Leere Kompatibilitätsfelder halten ältere
Shellprogramme lauffähig. Fachliche Zugangsdaten, etwa zum Backupziel, bleiben
bestehen. Alle Jobs einschließlich Vzdump erfassen ausschließlich lokale Ergebnisse.
Die zu verwaltenden Cron-Skripte müssen im geprüften Quellmanifest enthalten sein.

Die Library verteilt `bin/job-status` auf jeden Host. Es liest den letzten lokalen
Zustand je Job, ohne Controller, Netzwerk oder Jobstart. Der Controller verwendet
denselben Helfer über `bin/control jobs-last --limit ZIEL`.
