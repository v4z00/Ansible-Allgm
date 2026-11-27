# Complete shared script library

Every selected Linux host receives the complete shared library from `artifacts/script-library/`: mail/Telegram, logging, fixed ASCII mail transliteration, SQLite job runner and query helper. Operational programs and custom functions stay in private controller sources managed by `script_jobs`.

`script_library_root` sets the installation directory (default `/root/script-config`). `script_library_owner` and `script_library_group` both default to root. When called by `script_jobs`, the library is installed relative to the existing target script directory.

The role requires explicit targets, guards existing symlinks and never starts scripts. Library files use 0600, directories and the job helper 0700. Job execution needs Python 3 with SQLite. No network service is installed.

Run the helpers directly:

```sh
/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 runs
/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 watch --seconds 30
/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 details --run LAUF-ID
```

When querying a missing database, the helper reports it as not yet connected. Initialization and job execution are separate explicit operations. Sourcing shell functions starts no jobs.

<details>
<summary>Deutsch</summary>

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

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/script_library",
  "title": "Vollständige neutrale Skriptbibliothek",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/script_library/defaults/main.yml",
    "roles/script_library/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/script_library/defaults/main.yml": "528e1bc8cdc3355cdc681063581a63f9ac4d2c6643bf7773792dbe416e71b709",
    "roles/script_library/tasks/main.yml": "3bf8e5b0ab4f2a4b63e3ece3dec8945866970fb78ccb25d1e54525ad38a04839"
  },
  "i18n": {
    "de": {
      "title": "Vollständige neutrale Skriptbibliothek",
      "description": "# Vollständige neutrale Skriptbibliothek\n\nJeder ausgewählte Linux-Host erhält die ganze Grundbibliothek aus\n`artifacts/script-library/`. Darin liegen Mail/Telegram, Logging, feste\nASCII-Mailübersetzung sowie der neutrale SQLite-Jobrunner und Abfragehelfer.\nProduktive Programme und Spezialfunktionen gehören ausdrücklich nicht in dieses\nArtefakt; die Rolle `script_jobs` verwendet dafür private Controllerquellen.\n\n`script_library_root` bestimmt den Installationspfad (Standard\n`/root/script-config`), `script_library_owner`/`script_library_group` den Besitzer\n(Standard root). Beim Aufruf durch `script_jobs` wird die Library relativ zu den\nSkripten unter deren bestehendem Zielpfad installiert.\n\nDie Rolle verlangt eine explizite Zielauswahl, schützt vorhandene Verknüpfungen\nund startet keine Skripte. Librarydateien sind 0600, Verzeichnisse 0700 und der\nJobhelfer 0700. Python3 mit SQLite gehört zur Job-Laufzeit; es wird kein\nNetzwerkdienst angelegt.\n\nDirekte Helferbeispiele:\n\n```sh\n/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 runs\n/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 watch --seconds 30\n/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 details --run LAUF-ID\n```\n\nEine fehlende Datenbank wird bei einer Abfrage als noch nicht angebunden gemeldet.\nDas Initialisieren und das Ausführen eines Jobs sind eigene ausdrückliche\nOperationen. Das Laden der Shell-Funktionen führt keinen Job aus.",
      "fields": {}
    },
    "en": {
      "title": "Complete shared script library",
      "description": "# Complete shared script library\n\nEvery selected Linux host receives the complete shared library from `artifacts/script-library/`: mail/Telegram, logging, fixed ASCII mail transliteration, SQLite job runner and query helper. Operational programs and custom functions stay in private controller sources managed by `script_jobs`.\n\n`script_library_root` sets the installation directory (default `/root/script-config`). `script_library_owner` and `script_library_group` both default to root. When called by `script_jobs`, the library is installed relative to the existing target script directory.\n\nThe role requires explicit targets, guards existing symlinks and never starts scripts. Library files use 0600, directories and the job helper 0700. Job execution needs Python 3 with SQLite. No network service is installed.\n\nRun the helpers directly:\n\n```sh\n/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 runs\n/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 watch --seconds 30\n/root/script-config/bin/script-jobs --db /var/lib/script-jobs/jobs.sqlite3 details --run LAUF-ID\n```\n\nWhen querying a missing database, the helper reports it as not yet connected. Initialization and job execution are separate explicit operations. Sourcing shell functions starts no jobs.",
      "fields": {}
    }
  }
}
```

</details>
