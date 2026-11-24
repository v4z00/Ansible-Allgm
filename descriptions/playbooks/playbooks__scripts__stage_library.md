# Öffentliche Bash-Bibliothek verteilen

Auf dem Controller `.venv/bin/ansible-playbook playbooks/scripts/stage_library.yml --limit ZIELHOST` ausführen. Die Rolle kopiert Loader, gemeinsame Funktionen und Mailtabelle nach `/root/script-config/lib/`. Sie führt die Funktionen auf den Zielhosts nicht aus.

Eine explizite Hostauswahl mit `--limit` ist erforderlich.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/scripts/stage_library.yml",
  "title": "Öffentliche Bash-Bibliothek verteilen",
  "documented": true,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/scripts/stage_library.yml",
    "roles/script_library/tasks/main.yml"
  ],
  "source_hashes": {
    "playbooks/scripts/stage_library.yml": "f981967c97e6c2d4f19154d7693b21b02ac2700779876605dea82f7038700db8",
    "roles/script_library/tasks/main.yml": "7130acfaabe9871417b3ddd69a0595c09546d1910b89cbb7eddebde03a238728"
  }
}
```
