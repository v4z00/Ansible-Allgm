# Rolle security_ssh

Rolle: `roles/security_ssh`.

Im Bestand definierte Aufgaben:

- Validate additional SSH listen addresses
- Check that additional SSH listen addresses are assigned locally
- Validate the SSH authentication mode
- Validate the break-glass password
- Create the break-glass user
- Create the restricted break-glass bin directory
- Provide only su for break-glass access
- Install the restricted break-glass profile
- Create the SSH drop-in directory
- Ensure sshd includes the drop-in directory
- Disable direct root login overrides in sshd_config
- Deploy the hardened SSH configuration
- Validate the complete SSH configuration
- Run SSH handlers now
- Wait for connectivity after the SSH restart

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/security_ssh",
  "title": "Rolle security_ssh",
  "documented": false,
  "fields": [
    {
      "id": "ssh_breakglass_enabled",
      "label": "ssh_breakglass_enabled",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "ssh_breakglass_user",
      "label": "ssh_breakglass_user",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "ansible-rescue"
    },
    {
      "id": "ssh_breakglass_uid",
      "label": "ssh_breakglass_uid",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "default": 3030
    },
    {
      "id": "ssh_breakglass_home",
      "label": "ssh_breakglass_home",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/home/ansible-rescue"
    },
    {
      "id": "ssh_breakglass_password",
      "label": "ssh_breakglass_password",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": true
    },
    {
      "id": "ssh_breakglass_password_salt",
      "label": "ssh_breakglass_password_salt",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": true
    }
  ],
  "constraints": [],
  "sources": [
    "roles/security_ssh/tasks/main.yml",
    "roles/security_ssh/defaults/main.yml"
  ],
  "source_hashes": {
    "roles/security_ssh/defaults/main.yml": "dbff17c98ddc68e47ce52ad0ad813ad063f484d1bfbcd7b85d59946de0f467e6",
    "roles/security_ssh/tasks/main.yml": "67f933c96bf495917007e45de03628af5a81bb0b0aeea294e7cb9eee1d4c11c5"
  },
  "i18n": {
    "de": {
      "title": "Rolle security_ssh",
      "description": "# Rolle security_ssh\n\nRolle: `roles/security_ssh`.\n\nIm Bestand definierte Aufgaben:\n\n- Validate additional SSH listen addresses\n- Check that additional SSH listen addresses are assigned locally\n- Validate the SSH authentication mode\n- Validate the break-glass password\n- Create the break-glass user\n- Create the restricted break-glass bin directory\n- Provide only su for break-glass access\n- Install the restricted break-glass profile\n- Create the SSH drop-in directory\n- Ensure sshd includes the drop-in directory\n- Disable direct root login overrides in sshd_config\n- Deploy the hardened SSH configuration\n- Validate the complete SSH configuration\n- Run SSH handlers now\n- Wait for connectivity after the SSH restart\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/security_ssh/tasks/main.yml`\n- `roles/security_ssh/defaults/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "ssh_breakglass_enabled": {
          "label": "ssh_breakglass_enabled",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "ssh_breakglass_user": {
          "label": "ssh_breakglass_user",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "ssh_breakglass_uid": {
          "label": "ssh_breakglass_uid",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "ssh_breakglass_home": {
          "label": "ssh_breakglass_home",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "ssh_breakglass_password": {
          "label": "ssh_breakglass_password",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "ssh_breakglass_password_salt": {
          "label": "ssh_breakglass_password_salt",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        }
      }
    },
    "en": {
      "title": "Role security_ssh",
      "description": "# Role security_ssh\n\nRole: `roles/security_ssh`.\n\nTask names as written in the role:\n\n- Validate additional SSH listen addresses\n- Check that additional SSH listen addresses are assigned locally\n- Validate the SSH authentication mode\n- Validate the break-glass password\n- Create the break-glass user\n- Create the restricted break-glass bin directory\n- Provide only su for break-glass access\n- Install the restricted break-glass profile\n- Create the SSH drop-in directory\n- Ensure sshd includes the drop-in directory\n- Disable direct root login overrides in sshd_config\n- Deploy the hardened SSH configuration\n- Validate the complete SSH configuration\n- Run SSH handlers now\n- Wait for connectivity after the SSH restart\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/security_ssh/tasks/main.yml`\n- `roles/security_ssh/defaults/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "ssh_breakglass_enabled": {
          "label": "ssh_breakglass_enabled",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "ssh_breakglass_user": {
          "label": "ssh_breakglass_user",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "ssh_breakglass_uid": {
          "label": "ssh_breakglass_uid",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "ssh_breakglass_home": {
          "label": "ssh_breakglass_home",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "ssh_breakglass_password": {
          "label": "ssh_breakglass_password",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "ssh_breakglass_password_salt": {
          "label": "ssh_breakglass_password_salt",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        }
      }
    }
  }
}
```

## Quellen und Pflege

- `roles/security_ssh/tasks/main.yml`
- `roles/security_ssh/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
