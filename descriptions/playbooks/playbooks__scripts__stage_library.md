# Distribute the public Bash library

From the controller, run `.venv/bin/ansible-playbook playbooks/scripts/stage_library.yml --limit TARGET_HOST`. The role copies the loader, shared functions and email mapping to `/root/script-config/lib/`. It does not execute the functions on target hosts.

Select target hosts explicitly with `--limit`.

<details>
<summary>Deutsch</summary>

# Öffentliche Bash-Bibliothek verteilen

Auf dem Controller `.venv/bin/ansible-playbook playbooks/scripts/stage_library.yml --limit ZIELHOST` ausführen. Die Rolle kopiert Loader, gemeinsame Funktionen und Mailtabelle nach `/root/script-config/lib/`. Sie führt die Funktionen auf den Zielhosts nicht aus.

Eine explizite Hostauswahl mit `--limit` ist erforderlich.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
    "playbooks/scripts/stage_library.yml": "cee843513e8779c47c3121a540bb03702cb2a66336d4e75316cb02ffbee25a39",
    "roles/script_library/tasks/main.yml": "3bf8e5b0ab4f2a4b63e3ece3dec8945866970fb78ccb25d1e54525ad38a04839"
  },
  "i18n": {
    "de": {
      "title": "Öffentliche Bash-Bibliothek verteilen",
      "description": "# Öffentliche Bash-Bibliothek verteilen\n\nAuf dem Controller `.venv/bin/ansible-playbook playbooks/scripts/stage_library.yml --limit ZIELHOST` ausführen. Die Rolle kopiert Loader, gemeinsame Funktionen und Mailtabelle nach `/root/script-config/lib/`. Sie führt die Funktionen auf den Zielhosts nicht aus.\n\nEine explizite Hostauswahl mit `--limit` ist erforderlich.",
      "fields": {}
    },
    "en": {
      "title": "Distribute the public Bash library",
      "description": "# Distribute the public Bash library\n\nFrom the controller, run `.venv/bin/ansible-playbook playbooks/scripts/stage_library.yml --limit TARGET_HOST`. The role copies the loader, shared functions and email mapping to `/root/script-config/lib/`. It does not execute the functions on target hosts.\n\nSelect target hosts explicitly with `--limit`.",
      "fields": {}
    }
  }
}
```

</details>
