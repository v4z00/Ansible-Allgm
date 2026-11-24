# Vollständige neutrale Skriptbibliothek

Jeder ausgewählte Linux-Host erhält die ganze Grundbibliothek aus
`artifacts/script-library/`. Darin liegen Mail/Telegram, Logging, feste
ASCII-Mailübersetzung sowie der neutrale SQLite-Jobrunner und Abfragehelfer.
Produktive Programme und Spezialfunktionen gehören ausdrücklich nicht in dieses
Artefakt; die Rolle `script_jobs` verwendet dafür private Controllerquellen.

`script_library_root` bestimmt den Installationspfad (Standard
`/root/script-config`), `script_library_owner`/`script_library_group` den Besitzer
(Standard root). Beim Aufruf durch `script_jobs` wird die Library relativ zu den
Skripten unter deren bestehendem Zielpfad installiert.

Die Rolle verlangt eine explizite Zielauswahl, schützt vorhandene Verknüpfungen
und startet keine Skripte. Librarydateien sind 0600, Verzeichnisse 0700 und der
Jobhelfer 0700. Python3 mit SQLite gehört zur Job-Laufzeit; es wird kein
Netzwerkdienst angelegt.

Direkte Helferbeispiele:

```sh
/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 runs
/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 watch --seconds 30
/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 details --run LAUF-ID
```

Eine fehlende Datenbank wird bei einer Abfrage als noch nicht angebunden gemeldet.
Das Initialisieren und das Ausführen eines Jobs sind eigene ausdrückliche
Operationen. Das Laden der Shell-Funktionen führt keinen Job aus.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/script_library",
  "title": "Vollst\u00e4ndige neutrale Skriptbibliothek",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/script_library/defaults/main.yml",
    "roles/script_library/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/script_library/defaults/main.yml": "528e1bc8cdc3355cdc681063581a63f9ac4d2c6643bf7773792dbe416e71b709",
    "roles/script_library/tasks/main.yml": "7130acfaabe9871417b3ddd69a0595c09546d1910b89cbb7eddebde03a238728"
  }
}
```
