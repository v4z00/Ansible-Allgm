# Letzte Zustände direkt auf den Hosts abfragen

```sh
bin/control jobs-last --limit example-host
ansible-playbook playbooks/scripts/show_status.yml --limit example-host
```

Eine ausdrückliche Zielauswahl ist Pflicht. Das Playbook liest über die vorhandenen
Ansible-Verbindungen `bin/job-status` auf jedem Host. Der Helfer gehört zur
vollständigen Library und liest die lokale SQLite, ohne Jobs zu starten, Cron zu
ändern oder Nachrichten zu senden. Der Pfad folgt `script_jobs_target_root`, dann
`script_path`, sonst `/scripte`; die Datenbank `script_jobs_database_path`.

Pro Job erscheint nur der neueste Zustand mit Zeitstempel, Symbol und Exitcode.
Ein laufender Job ersetzt in dieser Ansicht den älteren Erfolg. Fehlende Helfer,
Datenbanken oder nicht erreichbare Hosts werden ausdrücklich als Fehler angezeigt.
Eine leere Liste beweist nicht, dass geplante Jobs bereits gelaufen sind.

Auf einem Host funktioniert derselbe Aufruf lokal: `PFAD/bin/job-status`;
`--job NAME` filtert, `--json` liefert strukturierte Daten. Diese Ansicht benötigt
keinen Controller. `bin/control jobs latest` zeigt dagegen den letzten gespeicherten
Abholstand des Controllers; `runs` und `details` bieten die Historie.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "jobs-last",
  "title": "Letzte Zustände direkt auf den Hosts abfragen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/jobs-last.json",
    "bin/control.d/jobs-last.sh",
    "playbooks/scripts/show_status.yml"
  ],
  "source_hashes": {
    "bin/control.d/jobs-last.json": "23289315b66e43d636fa55911b55ecd2fdde7c2117d340b9a6ef32aae8111960",
    "bin/control.d/jobs-last.sh": "7e9f939cf794e78873b987de31cb193f6572ba5c8f0ea5bc923ab5c10e09a644",
    "playbooks/scripts/show_status.yml": "095511f8fbdfa648be533dd9541079d839ca6972cc0cf4fdb2f16597ab1e777f"
  },
  "i18n": {
    "de": {
      "title": "Letzte Zustände direkt auf den Hosts abfragen",
      "description": "# Letzte Zustände direkt auf den Hosts abfragen\n\n\u0060\u0060\u0060sh\nbin/control jobs-last --limit example-host\nansible-playbook playbooks/scripts/show_status.yml --limit example-host\n\u0060\u0060\u0060\n\nEine ausdrückliche Zielauswahl ist Pflicht. Das Playbook liest über die vorhandenen\nAnsible-Verbindungen `bin/job-status` auf jedem Host. Der Helfer gehört zur\nvollständigen Library und liest die lokale SQLite, ohne Jobs zu starten, Cron zu\nändern oder Nachrichten zu senden. Der Pfad folgt `script_jobs_target_root`, dann\n`script_path`, sonst `/scripte`; die Datenbank `script_jobs_database_path`.\n\nPro Job erscheint nur der neueste Zustand mit Zeitstempel, Symbol und Exitcode.\nEin laufender Job ersetzt in dieser Ansicht den älteren Erfolg. Fehlende Helfer,\nDatenbanken oder nicht erreichbare Hosts werden ausdrücklich als Fehler angezeigt.\nEine leere Liste beweist nicht, dass geplante Jobs bereits gelaufen sind.\n\nAuf einem Host funktioniert derselbe Aufruf lokal: `PFAD/bin/job-status`;\n`--job NAME` filtert, `--json` liefert strukturierte Daten. Diese Ansicht benötigt\nkeinen Controller. `bin/control jobs latest` zeigt dagegen den letzten gespeicherten\nAbholstand des Controllers; `runs` und `details` bieten die Historie.",
      "fields": {}
    },
    "en": {
      "title": "Read the latest job results directly from the hosts",
      "description": "# Read the latest job results directly from the hosts\n\n\u0060\u0060\u0060sh\nbin/control jobs-last --limit example-host\nansible-playbook playbooks/scripts/show_status.yml --limit example-host\n\u0060\u0060\u0060\n\nSelect targets explicitly. Through existing Ansible connections, the playbook calls each host’s `bin/job-status` helper from the complete library. It reads local SQLite results without starting jobs, editing cron or sending messages. The root is `script_jobs_target_root`, then `script_path`, then `/scripte`. Set the database with `script_jobs_database_path`.\n\nEach job shows its latest status, timestamp, symbol and exit code. A running job takes precedence over an earlier success. Missing helpers or databases and unreachable hosts appear as errors. An empty list does not establish that scheduled jobs have run.\n\nOn a host, run `PATH/bin/job-status`. Filter with `--job NAME` or request structured output with `--json`. This works independently of the controller. `bin/control jobs latest` shows the controller’s last collected results. Use `runs` and `details` for history.",
      "fields": {}
    }
  }
}
```
