# Role postfix

Role: `roles/postfix`.

Task names as written in the role:

- Validate the Postfix configuration
- Install Postfix packages
- Deploy Postfix main.cf
- Determine the sender address for this host
- Deploy the sender canonical map
- Write SASL credentials
- Enable Postfix

The parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `roles/postfix/tasks/main.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Rolle postfix

Rolle: `roles/postfix`.

Im Bestand definierte Aufgaben:

- Validate the Postfix configuration
- Install Postfix packages
- Deploy Postfix main.cf
- Determine the sender address for this host
- Deploy the sender canonical map
- Write SASL credentials
- Enable Postfix

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `roles/postfix/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/postfix",
  "title": "Rolle postfix",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/postfix/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/postfix/tasks/main.yml": "bb1c1de37bdda95c5fe7a89bc437f5d7beb2253e4741bdb09b9094515d47d06e"
  },
  "i18n": {
    "de": {
      "title": "Rolle postfix",
      "description": "# Rolle postfix\n\nRolle: `roles/postfix`.\n\nIm Bestand definierte Aufgaben:\n\n- Validate the Postfix configuration\n- Install Postfix packages\n- Deploy Postfix main.cf\n- Determine the sender address for this host\n- Deploy the sender canonical map\n- Write SASL credentials\n- Enable Postfix\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/postfix/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role postfix",
      "description": "# Role postfix\n\nRole: `roles/postfix`.\n\nTask names as written in the role:\n\n- Validate the Postfix configuration\n- Install Postfix packages\n- Deploy Postfix main.cf\n- Determine the sender address for this host\n- Deploy the sender canonical map\n- Write SASL credentials\n- Enable Postfix\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/postfix/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
