# Rolle kerberos

Rolle: `roles/kerberos`.

Im Bestand definierte Aufgaben:

- Kerberos-Konfiguration pruefen
- Kerberos-Client installieren
- {{ 'krb5-user' if ansible_os_family == 'Debian' else 'krb5-workstation' }}
- Kerberos-Konfiguration ausrollen
- Debian-/Proxmox-CIFS-Upcall korrigieren

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

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
    "roles/kerberos/tasks/main.yml": "99359d4ce364030c1eb27dccb193f3a708abcdf5bd110d71a556ff625f9bd487"
  }
}
```

## Quellen und Pflege

- `roles/kerberos/tasks/main.yml`
- `roles/kerberos/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
