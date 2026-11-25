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
    "playbooks/scripts/show_status.yml": "9802fcab327927b0459a04a49b3463b63ecceea9fc5853f7a4136bc7ded5f1dd"
  }
}
```
