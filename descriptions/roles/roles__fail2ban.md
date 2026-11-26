# Rolle fail2ban

Rolle: `roles/fail2ban`.

Im Bestand definierte Aufgaben:

- Install Fail2ban
- Validate mail recipients for enabled notifications
- Install the silent mail action for ticket systems
- Remove the silent mail action when ticket notifications are disabled
- Install the Proxmox VE filter
- Install the Proxmox Backup filter
- Deploy the Fail2ban configuration
- Enable Fail2ban

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/fail2ban",
  "title": "Rolle fail2ban",
  "documented": false,
  "fields": [
    {
      "id": "fail2ban_enable_notifications",
      "label": "fail2ban_enable_notifications",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "fail2ban_enable_ticket_notifications",
      "label": "fail2ban_enable_ticket_notifications",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "fail2ban_enable_postfix_jail",
      "label": "fail2ban_enable_postfix_jail",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    }
  ],
  "constraints": [],
  "sources": [
    "roles/fail2ban/tasks/main.yml",
    "roles/fail2ban/defaults/main.yml"
  ],
  "source_hashes": {
    "roles/fail2ban/defaults/main.yml": "5bb52f807b33493ab59615b1f8dbae46f3b7c3dce54c959e213a5fc58c098f86",
    "roles/fail2ban/tasks/main.yml": "ff45239963d759b07c1870a9a4e1188093cb96e7ef2f8d6fcd191dcc8e82e137"
  },
  "i18n": {
    "de": {
      "title": "Rolle fail2ban",
      "description": "# Rolle fail2ban\n\nRolle: `roles/fail2ban`.\n\nIm Bestand definierte Aufgaben:\n\n- Install Fail2ban\n- Validate mail recipients for enabled notifications\n- Install the silent mail action for ticket systems\n- Remove the silent mail action when ticket notifications are disabled\n- Install the Proxmox VE filter\n- Install the Proxmox Backup filter\n- Deploy the Fail2ban configuration\n- Enable Fail2ban\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/fail2ban/tasks/main.yml`\n- `roles/fail2ban/defaults/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "fail2ban_enable_notifications": {
          "label": "fail2ban_enable_notifications",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "fail2ban_enable_ticket_notifications": {
          "label": "fail2ban_enable_ticket_notifications",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "fail2ban_enable_postfix_jail": {
          "label": "fail2ban_enable_postfix_jail",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        }
      }
    },
    "en": {
      "title": "Role fail2ban",
      "description": "# Role fail2ban\n\nRole: `roles/fail2ban`.\n\nTask names as written in the role:\n\n- Install Fail2ban\n- Validate mail recipients for enabled notifications\n- Install the silent mail action for ticket systems\n- Remove the silent mail action when ticket notifications are disabled\n- Install the Proxmox VE filter\n- Install the Proxmox Backup filter\n- Deploy the Fail2ban configuration\n- Enable Fail2ban\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/fail2ban/tasks/main.yml`\n- `roles/fail2ban/defaults/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "fail2ban_enable_notifications": {
          "label": "fail2ban_enable_notifications",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "fail2ban_enable_ticket_notifications": {
          "label": "fail2ban_enable_ticket_notifications",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "fail2ban_enable_postfix_jail": {
          "label": "fail2ban_enable_postfix_jail",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        }
      }
    }
  }
}
```

## Quellen und Pflege

- `roles/fail2ban/tasks/main.yml`
- `roles/fail2ban/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
