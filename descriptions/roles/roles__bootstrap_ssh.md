# Role bootstrap_ssh

Role: `roles/bootstrap_ssh`.

Task names as written in the role:

- Read the configured controller key locally
- Install the controller key for the Ansible user
- Install existing site admin keys for root
- List local users with UID 1000 or higher
- Remove site admin keys from non-root accounts
- Check key authentication before disabling passwords
- Disable password authentication when explicitly approved
- Validate the SSH configuration before reload

The parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `roles/bootstrap_ssh/tasks/main.yml`
- `roles/bootstrap_ssh/defaults/main.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Rolle bootstrap_ssh

Rolle: `roles/bootstrap_ssh`.

Im Bestand definierte Aufgaben:

- Read the configured controller key locally
- Install the controller key for the Ansible user
- Install existing site admin keys for root
- List local users with UID 1000 or higher
- Remove site admin keys from non-root accounts
- Check key authentication before disabling passwords
- Disable password authentication when explicitly approved
- Validate the SSH configuration before reload

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `roles/bootstrap_ssh/tasks/main.yml`
- `roles/bootstrap_ssh/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/bootstrap_ssh",
  "title": "Rolle bootstrap_ssh",
  "documented": false,
  "fields": [
    {
      "id": "root_allowed_keys",
      "label": "root_allowed_keys",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    }
  ],
  "constraints": [],
  "sources": [
    "roles/bootstrap_ssh/tasks/main.yml",
    "roles/bootstrap_ssh/defaults/main.yml"
  ],
  "source_hashes": {
    "roles/bootstrap_ssh/defaults/main.yml": "ea2e0ef76b455a623e9609948662247fb3dc0e7bda7c8dbe34bfb888a2ec4915",
    "roles/bootstrap_ssh/tasks/main.yml": "d168265533ba97af5f81e007f50a154e4a788f74ba9543ade1cf100e19df228d"
  },
  "i18n": {
    "de": {
      "title": "Rolle bootstrap_ssh",
      "description": "# Rolle bootstrap_ssh\n\nRolle: `roles/bootstrap_ssh`.\n\nIm Bestand definierte Aufgaben:\n\n- Read the configured controller key locally\n- Install the controller key for the Ansible user\n- Install existing site admin keys for root\n- List local users with UID 1000 or higher\n- Remove site admin keys from non-root accounts\n- Check key authentication before disabling passwords\n- Disable password authentication when explicitly approved\n- Validate the SSH configuration before reload\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/bootstrap_ssh/tasks/main.yml`\n- `roles/bootstrap_ssh/defaults/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "root_allowed_keys": {
          "label": "root_allowed_keys",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        }
      }
    },
    "en": {
      "title": "Role bootstrap_ssh",
      "description": "# Role bootstrap_ssh\n\nRole: `roles/bootstrap_ssh`.\n\nTask names as written in the role:\n\n- Read the configured controller key locally\n- Install the controller key for the Ansible user\n- Install existing site admin keys for root\n- List local users with UID 1000 or higher\n- Remove site admin keys from non-root accounts\n- Check key authentication before disabling passwords\n- Disable password authentication when explicitly approved\n- Validate the SSH configuration before reload\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/bootstrap_ssh/tasks/main.yml`\n- `roles/bootstrap_ssh/defaults/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "root_allowed_keys": {
          "label": "root_allowed_keys",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        }
      }
    }
  }
}
```

</details>
