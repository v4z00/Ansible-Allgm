# Letzte lokale Jobzustände anzeigen

Aufruf und Pfadauflösung stehen unter [jobs-last](../commands/jobs-last.md).
Die explizite Hostauswahl ist Pflicht. Das Playbook führt ausschließlich den
lokalen SQLite-Statushelfer aus.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/scripts/show_status.yml",
  "title": "Letzte Zustände direkt auf den Hosts abfragen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/scripts/show_status.yml"
  ],
  "source_hashes": {
    "playbooks/scripts/show_status.yml": "9802fcab327927b0459a04a49b3463b63ecceea9fc5853f7a4136bc7ded5f1dd"
  }
}
```
