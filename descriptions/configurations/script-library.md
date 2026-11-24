# Bash-Bibliothek verwenden

Die Funktionen liegen unter [artifacts/script-library/lib](../../artifacts/script-library/lib/). Der Loader lädt die Dateien aus `common/`. Die Mailfunktionen brauchen außerdem `data/mail-translations.json`.

Auf dem Controller verteilst du die Bibliothek mit dem [Playbook für die Bash-Bibliothek](../playbooks/playbooks__scripts__stage_library.md). Auf dem Zielhost bindest du sie so in dein Skript ein:

```bash
source /root/script-config/lib/load.sh
```

Eine einzelne Funktion wie `hm_log` kannst du auch direkt herunterladen:

```sh
curl -fsSLo hm_log.sh https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/artifacts/script-library/lib/common/hm_log.sh
```

Die SHA-256-Prüfsummen stehen im [Manifest](../../SHA256SUMS.json).

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "script-library",
  "title": "Bash-Bibliothek verwenden",
  "documented": true,
  "fields": [],
  "sources": [],
  "source_hashes": {}
}
```
