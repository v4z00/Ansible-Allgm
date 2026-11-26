# Bash-Bibliothek verwenden

Die Funktionen liegen unter [artifacts/script-library/lib](../../artifacts/script-library/lib/). Der Loader lädt die Dateien aus `common/`. Die Mailfunktionen brauchen außerdem `data/mail-translations.json`.

Auf dem Controller verteilst du die Bibliothek mit dem [Playbook für die Bash-Bibliothek](../playbooks/playbooks__scripts__stage_library.md). Auf dem Zielhost bindest du sie so in dein Skript ein:

```bash
source /root/script-config/lib/load.sh
```

Eine einzelne Funktion wie `hm_log` kannst du auch direkt herunterladen:

```sh
curl -fsSLo hm_log.sh https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/artifacts/script-library/lib/common/hm_log.sh
```

Die SHA-256-Prüfsummen stehen im [Manifest](../../SHA256SUMS.json).

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "script-library",
  "title": "Bash-Bibliothek verwenden",
  "documented": true,
  "fields": [],
  "sources": [],
  "source_hashes": {},
  "i18n": {
    "de": {
      "title": "Bash-Bibliothek verwenden",
      "description": "# Bash-Bibliothek verwenden\n\nDie Funktionen liegen unter [artifacts/script-library/lib](../../artifacts/script-library/lib/). Der Loader lädt die Dateien aus `common/`. Die Mailfunktionen brauchen außerdem `data/mail-translations.json`.\n\nAuf dem Controller verteilst du die Bibliothek mit dem [Playbook für die Bash-Bibliothek](../playbooks/playbooks__scripts__stage_library.md). Auf dem Zielhost bindest du sie so in dein Skript ein:\n\n\u0060\u0060\u0060bash\nsource /root/script-config/lib/load.sh\n\u0060\u0060\u0060\n\nEine einzelne Funktion wie `hm_log` kannst du auch direkt herunterladen:\n\n\u0060\u0060\u0060sh\ncurl -fsSLo hm_log.sh https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/artifacts/script-library/lib/common/hm_log.sh\n\u0060\u0060\u0060\n\nDie SHA-256-Prüfsummen stehen im [Manifest](../../SHA256SUMS.json).\n\n## Lokalen Jobzustand abfragen\n\nDie vollständige Library enthält `bin/job-status` und `bin/script-jobs`.\nBeispiel auf einem Host mit dem Skriptpfad `/scripte`:\n\n\u0060\u0060\u0060sh\n/scripte/bin/job-status\n/scripte/bin/job-status --job backup\n/scripte/bin/job-status --db /var/lib/script-jobs/jobs.sqlite3 --json\n\u0060\u0060\u0060\n\n`job-status` ermittelt die Datenbank aus der lokalen `config/common.json`;\n`--db` überschreibt diese Zuordnung. Es erscheint pro Job nur der neueste Lauf,\nauch ein gerade laufender. Zeitstempel und Exitcode sind sichtbar, interne IDs\nnur in JSON. Eine fehlende Datenbank wird als nicht angebunden gemeldet (Exit 3)\nund nicht neu angelegt. Keine Statusabfrage startet einen Job oder Versand.\nDie Hosts benötigen für ihre Cronjobs keinen erreichbaren Controller.",
      "fields": {}
    },
    "en": {
      "title": "Use the Bash library",
      "description": "# Use the Bash library\n\nFunctions are under [artifacts/script-library/lib](../../artifacts/script-library/lib/). The loader reads files from `common/`. Email functions also require `data/mail-translations.json`.\n\nDeploy the library from the controller with the [Bash library playbook](../playbooks/playbooks__scripts__stage_library.md). On the target, source it from your script:\n\n\u0060\u0060\u0060bash\nsource /root/script-config/lib/load.sh\n\u0060\u0060\u0060\n\nTo download one function such as `hm_log` directly:\n\n\u0060\u0060\u0060sh\ncurl -fsSLo hm_log.sh https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/artifacts/script-library/lib/common/hm_log.sh\n\u0060\u0060\u0060\n\nThe [manifest](../../SHA256SUMS.json) lists the SHA-256 values.\n\n## Query local job status\n\nThe full library includes `bin/job-status` and `bin/script-jobs`. Example on a host using `/scripte`:\n\n\u0060\u0060\u0060sh\n/scripte/bin/job-status\n/scripte/bin/job-status --job backup\n/scripte/bin/job-status --db /var/lib/script-jobs/jobs.sqlite3 --json\n\u0060\u0060\u0060\n\n`job-status` locates the database through local `config/common.json` or `--db`. It shows each job’s latest run, including running jobs, with timestamp and exit code. Internal IDs are shown only in JSON. A missing database returns “not connected” (exit 3) without creating it. Queries start no jobs or deliveries. Host cron jobs can run while the controller is unreachable.",
      "fields": {}
    }
  }
}
```

## Lokalen Jobzustand abfragen

Die vollständige Library enthält `bin/job-status` und `bin/script-jobs`.
Beispiel auf einem Host mit dem Skriptpfad `/scripte`:

```sh
/scripte/bin/job-status
/scripte/bin/job-status --job backup
/scripte/bin/job-status --db /var/lib/script-jobs/jobs.sqlite3 --json
```

`job-status` ermittelt die Datenbank aus der lokalen `config/common.json`;
`--db` überschreibt diese Zuordnung. Es erscheint pro Job nur der neueste Lauf,
auch ein gerade laufender. Zeitstempel und Exitcode sind sichtbar, interne IDs
nur in JSON. Eine fehlende Datenbank wird als nicht angebunden gemeldet (Exit 3)
und nicht neu angelegt. Keine Statusabfrage startet einen Job oder Versand.
Die Hosts benötigen für ihre Cronjobs keinen erreichbaren Controller.
