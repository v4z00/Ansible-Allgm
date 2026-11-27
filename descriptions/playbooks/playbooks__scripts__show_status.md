# Show the latest local job states

See [jobs-last](../commands/jobs-last.md) for invocation and path resolution. An explicit host selection is required. The playbook only calls the local SQLite status helper.

<details>
<summary>Deutsch</summary>

# Letzte lokale Jobzustände anzeigen

Aufruf und Pfadauflösung stehen unter [jobs-last](../commands/jobs-last.md).
Die explizite Hostauswahl ist Pflicht. Das Playbook führt ausschließlich den
lokalen SQLite-Statushelfer aus.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
    "playbooks/scripts/show_status.yml": "095511f8fbdfa648be533dd9541079d839ca6972cc0cf4fdb2f16597ab1e777f"
  },
  "i18n": {
    "de": {
      "title": "Letzte Zustände direkt auf den Hosts abfragen",
      "description": "# Letzte lokale Jobzustände anzeigen\n\nAufruf und Pfadauflösung stehen unter [jobs-last](../commands/jobs-last.md).\nDie explizite Hostauswahl ist Pflicht. Das Playbook führt ausschließlich den\nlokalen SQLite-Statushelfer aus.",
      "fields": {}
    },
    "en": {
      "title": "Read the latest job results directly from the hosts",
      "description": "# Show the latest local job states\n\nSee [jobs-last](../commands/jobs-last.md) for invocation and path resolution. An explicit host selection is required. The playbook only calls the local SQLite status helper.",
      "fields": {}
    }
  }
}
```

</details>
