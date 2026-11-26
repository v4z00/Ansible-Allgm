# Job-Zusammenfassung bilden

Aufruf: `ansible-playbook playbooks/scripts/summary_jobs.yml`. Voraussetzungen und Variablen stehen in den zugeordneten Rollenbeschreibungen unter `descriptions/roles/script_jobs*.md`. Bereitstellung erfolgt nur nach ausdruecklichem Aufruf mit lokaler Konfiguration; diese Datei allein startet keine Aktion.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/scripts/summary_jobs.yml",
  "title": "Job-Zusammenfassung bilden",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/scripts/summary_jobs.yml"
  ],
  "source_hashes": {
    "playbooks/scripts/summary_jobs.yml": "ac6fbab4e7add7ba5625df407c92492db49d0e068359539fb34ba8f7eba4ab7f"
  },
  "i18n": {
    "de": {
      "title": "Job-Zusammenfassung bilden",
      "description": "# Job-Zusammenfassung bilden\n\nAufruf: `ansible-playbook playbooks/scripts/summary_jobs.yml`. Voraussetzungen und Variablen stehen in den zugeordneten Rollenbeschreibungen unter `descriptions/roles/script_jobs*.md`. Bereitstellung erfolgt nur nach ausdruecklichem Aufruf mit lokaler Konfiguration; diese Datei allein startet keine Aktion.",
      "fields": {}
    },
    "en": {
      "title": "Build a job summary",
      "description": "# Build a job summary\n\nRun: `ansible-playbook playbooks/scripts/summary_jobs.yml`. See the role descriptions under `descriptions/roles/script_jobs*.md` for prerequisites and variables. Run the playbook explicitly with a local configuration.",
      "fields": {}
    }
  }
}
```
