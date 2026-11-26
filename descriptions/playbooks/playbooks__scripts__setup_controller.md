# Ergebnis-Controller einrichten

Aufruf: `ansible-playbook playbooks/scripts/setup_controller.yml`. Voraussetzungen und Variablen stehen in den zugeordneten Rollenbeschreibungen unter `descriptions/roles/script_jobs*.md`. Bereitstellung erfolgt nur nach ausdruecklichem Aufruf mit lokaler Konfiguration; diese Datei allein startet keine Aktion.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/scripts/setup_controller.yml",
  "title": "Ergebnis-Controller einrichten",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/scripts/setup_controller.yml"
  ],
  "source_hashes": {
    "playbooks/scripts/setup_controller.yml": "7d6e336721b80f30686c4eb87e412a7343142edf2ade81182471c68d275d66c8"
  },
  "i18n": {
    "de": {
      "title": "Ergebnis-Controller einrichten",
      "description": "# Ergebnis-Controller einrichten\n\nAufruf: `ansible-playbook playbooks/scripts/setup_controller.yml`. Voraussetzungen und Variablen stehen in den zugeordneten Rollenbeschreibungen unter `descriptions/roles/script_jobs*.md`. Bereitstellung erfolgt nur nach ausdruecklichem Aufruf mit lokaler Konfiguration; diese Datei allein startet keine Aktion.",
      "fields": {}
    },
    "en": {
      "title": "Set up the results controller",
      "description": "# Set up the results controller\n\nRun: `ansible-playbook playbooks/scripts/setup_controller.yml`. See the role descriptions under `descriptions/roles/script_jobs*.md` for prerequisites and variables. Run the playbook explicitly with a local configuration.",
      "fields": {}
    }
  }
}
```
