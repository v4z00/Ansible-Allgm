# Rolle security_ssh

Rolle: `roles/security_ssh`.

Im Bestand definierte Aufgaben:

- Liste zusaetzlicher SSH-Listenadressen validieren
- Zusaetzliche SSH-Listenadressen auf lokale Zuordnung pruefen
- SSH-Authentifizierungsmodus validieren
- Break-Glass-Kennwort pruefen
- Break-Glass-Benutzer anlegen
- {{ ssh_breakglass_user }}
- Eingeschraenktes Break-Glass-Bin-Verzeichnis anlegen
- Ausschliesslich su fuer Break-Glass bereitstellen
- Eingeschraenktes Break-Glass-Profil installieren
- SSH-Drop-in-Verzeichnis sicherstellen
- Einbindung der SSH-Drop-ins sicherstellen
- Direkte Root-Login-Freigaben in sshd_config deaktivieren
- Gehärtete SSH-Konfiguration verteilen
- Gesamte SSH-Konfiguration validieren
- SSH-Handler jetzt ausfuehren
- Nach SSH-Neustart auf Verbindung warten

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
    "roles/security_ssh/tasks/main.yml": "6ba94983454841184a5090e36e822e68f25d73df6388200a0df22c4f8baa7c0a"
  }
}
```

## Quellen und Pflege

- `roles/security_ssh/tasks/main.yml`
- `roles/security_ssh/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
