# Role accounting

Role: `roles/accounting`.

Task names as written in the role:

- Detect LXC for process accounting
- Install applicable accounting packages
- Enable sysstat data collection
- Enable sysstat
- Enable process accounting outside LXC
- Enable auditd outside LXC
- Report the accounting limitation on LXC

The parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `roles/accounting/tasks/main.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Rolle accounting

Rolle: `roles/accounting`.

Im Bestand definierte Aufgaben:

- Detect LXC for process accounting
- Install applicable accounting packages
- Enable sysstat data collection
- Enable sysstat
- Enable process accounting outside LXC
- Enable auditd outside LXC
- Report the accounting limitation on LXC

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `roles/accounting/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/accounting",
  "title": "Rolle accounting",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/accounting/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/accounting/tasks/main.yml": "f1d2532253fd7f44363734bd14316605371e8458c0a1a21dba82a6aefe026a3c"
  },
  "i18n": {
    "de": {
      "title": "Rolle accounting",
      "description": "# Rolle accounting\n\nRolle: `roles/accounting`.\n\nIm Bestand definierte Aufgaben:\n\n- Detect LXC for process accounting\n- Install applicable accounting packages\n- Enable sysstat data collection\n- Enable sysstat\n- Enable process accounting outside LXC\n- Enable auditd outside LXC\n- Report the accounting limitation on LXC\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/accounting/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role accounting",
      "description": "# Role accounting\n\nRole: `roles/accounting`.\n\nTask names as written in the role:\n\n- Detect LXC for process accounting\n- Install applicable accounting packages\n- Enable sysstat data collection\n- Enable sysstat\n- Enable process accounting outside LXC\n- Enable auditd outside LXC\n- Report the accounting limitation on LXC\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/accounting/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
