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
    "playbooks/scripts/deploy_jobs.yml": "63bf749c89e095234580eb665d29d690b6a4a46da4d64316670ef0c4d640864c"
  },
  "i18n": {
    "de": {
      "title": "Lokale Skripte und Cron bereitstellen",
      "description": "# Lokale Skripte und Cron bereitstellen\n\nAufruf: `ansible-playbook playbooks/scripts/deploy_jobs.yml`. Voraussetzungen und Variablen stehen in den zugeordneten Rollenbeschreibungen unter `descriptions/roles/script_jobs*.md`. Bereitstellung erfolgt nur nach ausdruecklichem Aufruf mit lokaler Konfiguration; diese Datei allein startet keine Aktion.",
      "fields": {}
    },
    "en": {
      "title": "Deploy local scripts and cron jobs",
      "description": "# Deploy local scripts and cron jobs\n\nRun: `ansible-playbook playbooks/scripts/deploy_jobs.yml`. See the role descriptions under `descriptions/roles/script_jobs*.md` for prerequisites and variables. Run the playbook explicitly with a local configuration.",
      "fields": {}
    }
  }
}
```
