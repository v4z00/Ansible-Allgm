# Role kerberos

Role: `roles/kerberos`.

Task names as written in the role:

- Validate Kerberos configuration
- Install the Kerberos client
- Deploy the Kerberos configuration
- Fix the Debian and Proxmox CIFS upcall

The parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `roles/kerberos/tasks/main.yml`
- `roles/kerberos/defaults/main.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Rolle kerberos

Rolle: `roles/kerberos`.

Im Bestand definierte Aufgaben:

- Validate Kerberos configuration
- Install the Kerberos client
- Deploy the Kerberos configuration
- Fix the Debian and Proxmox CIFS upcall

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `roles/kerberos/tasks/main.yml`
- `roles/kerberos/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/kerberos",
  "title": "Rolle kerberos",
  "documented": false,
  "fields": [
    {
      "id": "kerberos_realm",
      "label": "kerberos_realm",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": ""
    },
    {
      "id": "kerberos_kdcs",
      "label": "kerberos_kdcs",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "kerberos_admin_server",
      "label": "kerberos_admin_server",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "kerberos_dns_lookup_realm",
      "label": "kerberos_dns_lookup_realm",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "kerberos_dns_lookup_kdc",
      "label": "kerberos_dns_lookup_kdc",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    },
    {
      "id": "kerberos_force_tcp",
      "label": "kerberos_force_tcp",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    },
    {
      "id": "kerberos_fix_cifs_upcall",
      "label": "kerberos_fix_cifs_upcall",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": true
    }
  ],
  "constraints": [],
  "sources": [
    "roles/kerberos/tasks/main.yml",
    "roles/kerberos/defaults/main.yml"
  ],
  "source_hashes": {
    "roles/kerberos/defaults/main.yml": "6f54f15bcd6f8333a08e51f07c10d3c4c1decb907c335e240ddeea31e5659cee",
    "roles/kerberos/tasks/main.yml": "e9a255d89d5acfdd0f0518d9012d4bce91713593c3076f1048a43e4f2158b79c"
  },
  "i18n": {
    "de": {
      "title": "Rolle kerberos",
      "description": "# Rolle kerberos\n\nRolle: `roles/kerberos`.\n\nIm Bestand definierte Aufgaben:\n\n- Validate Kerberos configuration\n- Install the Kerberos client\n- Deploy the Kerberos configuration\n- Fix the Debian and Proxmox CIFS upcall\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/kerberos/tasks/main.yml`\n- `roles/kerberos/defaults/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "kerberos_realm": {
          "label": "kerberos_realm",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "kerberos_kdcs": {
          "label": "kerberos_kdcs",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "kerberos_admin_server": {
          "label": "kerberos_admin_server",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "kerberos_dns_lookup_realm": {
          "label": "kerberos_dns_lookup_realm",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "kerberos_dns_lookup_kdc": {
          "label": "kerberos_dns_lookup_kdc",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "kerberos_force_tcp": {
          "label": "kerberos_force_tcp",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        },
        "kerberos_fix_cifs_upcall": {
          "label": "kerberos_fix_cifs_upcall",
          "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand."
        }
      }
    },
    "en": {
      "title": "Role kerberos",
      "description": "# Role kerberos\n\nRole: `roles/kerberos`.\n\nTask names as written in the role:\n\n- Validate Kerberos configuration\n- Install the Kerberos client\n- Deploy the Kerberos configuration\n- Fix the Debian and Proxmox CIFS upcall\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/kerberos/tasks/main.yml`\n- `roles/kerberos/defaults/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "kerberos_realm": {
          "label": "kerberos_realm",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "kerberos_kdcs": {
          "label": "kerberos_kdcs",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "kerberos_admin_server": {
          "label": "kerberos_admin_server",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "kerberos_dns_lookup_realm": {
          "label": "kerberos_dns_lookup_realm",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "kerberos_dns_lookup_kdc": {
          "label": "kerberos_dns_lookup_kdc",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "kerberos_force_tcp": {
          "label": "kerberos_force_tcp",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        },
        "kerberos_fix_cifs_upcall": {
          "label": "kerberos_fix_cifs_upcall",
          "description": "Role default. Consult the listed tasks for its purpose. The original role has no separate field description."
        }
      }
    }
  }
}
```

</details>
