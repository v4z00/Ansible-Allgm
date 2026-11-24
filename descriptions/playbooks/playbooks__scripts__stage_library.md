# Öffentliche Bash-Bibliothek verteilen

Auf dem Controller `.venv/bin/ansible-playbook playbooks/scripts/stage_library.yml --limit ZIELHOST` ausführen. Die Rolle kopiert Loader, gemeinsame Funktionen und Mailtabelle nach `/root/script-config/lib/`. Sie führt die Funktionen auf den Zielhosts nicht aus.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/scripts/stage_library.yml",
  "title": "Öffentliche Bash-Bibliothek verteilen",
  "documented": true,
  "fields": [],
  "constraints": [
    "Eine explizite Hostauswahl mit --limit ist erforderlich."
  ],
  "sources": [
    "playbooks/scripts/stage_library.yml",
    "roles/script_library/tasks/main.yml"
  ],
  "source_hashes": {
    "playbooks/scripts/stage_library.yml": "f981967c97e6c2d4f19154d7693b21b02ac2700779876605dea82f7038700db8",
    "roles/script_library/tasks/main.yml": "6f50ce15ad462998f74e280d18d0cbec114abc5c10bbb601ad33ae5250295558"
  }
}
```
