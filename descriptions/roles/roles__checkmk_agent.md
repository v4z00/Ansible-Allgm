# Role checkmk_agent

Role: `roles/checkmk_agent`.

Task names as written in the role:

- Validate Checkmk settings and credentials
- Check the local Checkmk agent package
- Report a missing Checkmk agent package
- Set the Checkmk hostname
- Create or move the host in Checkmk
- Activate Checkmk changes before registration
- Copy the Checkmk agent package
- Install the Checkmk agent
- Determine the Checkmk plugin list
- Create Checkmk plugin directories
- Deploy available Checkmk plugins
- Read the Checkmk TLS status
- Register the Checkmk agent over TLS
- Enable the Checkmk agent socket
- Remove the temporary agent package

The parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `roles/checkmk_agent/tasks/main.yml`
- `roles/checkmk_agent/defaults/main.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Per-task TLS certificate validation (1.1.0)

In `group_vars/all/settings.yml`, `tls_validate_certs.checkmk_managed_host` covers creating or moving the centrally managed Checkmk host. `tls_validate_certs.checkmk_agent_activation` covers activating changes before registration. Each inherits `tls_validate_certs_default` (default true). An explicit false disables only that check.

The site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.

<details>
<summary>Deutsch</summary>

# Rolle checkmk_agent

Rolle: `roles/checkmk_agent`.

Im Bestand definierte Aufgaben:

- Validate Checkmk settings and credentials
- Check the local Checkmk agent package
- Report a missing Checkmk agent package
- Set the Checkmk hostname
- Create or move the host in Checkmk
- Activate Checkmk changes before registration
- Copy the Checkmk agent package
- Install the Checkmk agent
- Determine the Checkmk plugin list
- Create Checkmk plugin directories
- Deploy available Checkmk plugins
- Read the Checkmk TLS status
- Register the Checkmk agent over TLS
- Enable the Checkmk agent socket
- Remove the temporary agent package

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `roles/checkmk_agent/tasks/main.yml`
- `roles/checkmk_agent/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.checkmk_managed_host`: CheckMK-Host zentral anlegen oder verschieben (Standard true).
- `tls_validate_certs.checkmk_agent_activation`: CheckMK-Aenderungen vor Registrierung aktivieren (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/checkmk_agent",
  "title": "Rolle checkmk_agent",
  "documented": false,
  "fields": [
    {
      "id": "checkmk_agent_package_tmp",
      "label": "checkmk_agent_package_tmp",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/tmp/check-mk-agent.deb"
    },
    {
      "id": "checkmk_plugin_base_dir",
      "label": "checkmk_plugin_base_dir",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/usr/lib/check_mk_agent/plugins"
    },
    {
      "id": "checkmk_local_base_dir",
      "label": "checkmk_local_base_dir",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/usr/lib/check_mk_agent/local"
    },
    {
      "id": "checkmk_linux_base_plugins",
      "label": "checkmk_linux_base_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_docker_plugins",
      "label": "checkmk_docker_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_smart_plugins",
      "label": "checkmk_smart_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_cups_plugins",
      "label": "checkmk_cups_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_webserver_plugins",
      "label": "checkmk_webserver_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_database_plugins",
      "label": "checkmk_database_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    }
  ],
  "constraints": [],
  "sources": [
    "roles/checkmk_agent/tasks/main.yml",
    "roles/checkmk_agent/defaults/main.yml"
  ],
  "source_hashes": {
    "roles/checkmk_agent/defaults/main.yml": "3ac93cd4a2232d3e47a3e797cd5a0ca3db1b7343af439291fb90d5935adbdfaf",
    "roles/checkmk_agent/tasks/main.yml": "2d0e3ec06ab7581d66810710deca8c77ec835322d9e38278801fab785f33ea0f"
  },
  "i18n": {
    "de": {
      "title": "Rolle checkmk_agent",
      "description": "# Rolle checkmk_agent\n\nRolle: `roles/checkmk_agent`.\n\nIm Bestand definierte Aufgaben:\n\n- Validate Checkmk settings and credentials\n- Check the local Checkmk agent package\n- Report a missing Checkmk agent package\n- Set the Checkmk hostname\n- Create or move the host in Checkmk\n- Activate Checkmk changes before registration\n- Copy the Checkmk agent package\n- Install the Checkmk agent\n- Determine the Checkmk plugin list\n- Create Checkmk plugin directories\n- Deploy available Checkmk plugins\n- Read the Checkmk TLS status\n- Register the Checkmk agent over TLS\n- Enable the Checkmk agent socket\n- Remove the temporary agent package\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/checkmk_agent/tasks/main.yml`\n- `roles/checkmk_agent/defaults/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n\n## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)\n\nOptionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.\nFehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.\n- `tls_validate_certs.checkmk_managed_host`: CheckMK-Host zentral anlegen oder verschieben (Standard true).\n- `tls_validate_certs.checkmk_agent_activation`: CheckMK-Aenderungen vor Registrierung aktivieren (Standard true).\n\nStandortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben\nverwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.",
      "fields": {
        "checkmk_agent_package_tmp": {
          "label": "checkmk_agent_package_tmp",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_plugin_base_dir": {
          "label": "checkmk_plugin_base_dir",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_local_base_dir": {
          "label": "checkmk_local_base_dir",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_linux_base_plugins": {
          "label": "checkmk_linux_base_plugins",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_docker_plugins": {
          "label": "checkmk_docker_plugins",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_smart_plugins": {
          "label": "checkmk_smart_plugins",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_cups_plugins": {
          "label": "checkmk_cups_plugins",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_webserver_plugins": {
          "label": "checkmk_webserver_plugins",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "checkmk_database_plugins": {
          "label": "checkmk_database_plugins",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        }
      }
    },
    "en": {
      "title": "Role checkmk_agent",
      "description": "# Role checkmk_agent\n\nRole: `roles/checkmk_agent`.\n\nTask names as written in the role:\n\n- Validate Checkmk settings and credentials\n- Check the local Checkmk agent package\n- Report a missing Checkmk agent package\n- Set the Checkmk hostname\n- Create or move the host in Checkmk\n- Activate Checkmk changes before registration\n- Copy the Checkmk agent package\n- Install the Checkmk agent\n- Determine the Checkmk plugin list\n- Create Checkmk plugin directories\n- Deploy available Checkmk plugins\n- Read the Checkmk TLS status\n- Register the Checkmk agent over TLS\n- Enable the Checkmk agent socket\n- Remove the temporary agent package\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/checkmk_agent/tasks/main.yml`\n- `roles/checkmk_agent/defaults/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Per-task TLS certificate validation (1.1.0)\n\nIn `group_vars/all/settings.yml`, `tls_validate_certs.checkmk_managed_host` covers creating or moving the centrally managed Checkmk host. `tls_validate_certs.checkmk_agent_activation` covers activating changes before registration. Each inherits `tls_validate_certs_default` (default true). An explicit false disables only that check.\n\nThe site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.",
      "fields": {
        "checkmk_agent_package_tmp": {
          "label": "checkmk_agent_package_tmp",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_plugin_base_dir": {
          "label": "checkmk_plugin_base_dir",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_local_base_dir": {
          "label": "checkmk_local_base_dir",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_linux_base_plugins": {
          "label": "checkmk_linux_base_plugins",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_docker_plugins": {
          "label": "checkmk_docker_plugins",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_smart_plugins": {
          "label": "checkmk_smart_plugins",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_cups_plugins": {
          "label": "checkmk_cups_plugins",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_webserver_plugins": {
          "label": "checkmk_webserver_plugins",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "checkmk_database_plugins": {
          "label": "checkmk_database_plugins",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        }
      }
    }
  }
}
```

</details>
