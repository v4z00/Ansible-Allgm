# Lokale Skripte und Cron bereitstellen

Aufruf: `ansible-playbook playbooks/scripts/deploy_jobs.yml`. Voraussetzungen und Variablen stehen in den zugeordneten Rollenbeschreibungen unter `descriptions/roles/script_jobs*.md`. Bereitstellung erfolgt nur nach ausdruecklichem Aufruf mit lokaler Konfiguration; diese Datei allein startet keine Aktion.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/scripts/deploy_jobs.yml",
  "title": "Lokale Skripte und Cron bereitstellen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/scripts/deploy_jobs.yml"
  ],
  "source_hashes": {
    "playbooks/scripts/deploy_jobs.yml": "b6aac9b54600df070051e9f904867f01aad28425d57027922759b517585794cc"
  }
}
```
