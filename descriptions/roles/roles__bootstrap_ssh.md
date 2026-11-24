# Rolle bootstrap_ssh

Rolle: `roles/bootstrap_ssh`.

Im Bestand definierte Aufgaben:

- Konfigurierten Controller-Key lokal lesen
- Controller-Key fuer den Ansible-Benutzer hinterlegen
- Bestehende Standort-Admin-Keys fuer root hinterlegen
- Lokale Benutzer ab UID 1000 ermitteln
- Standort-Admin-Keys aus Nicht-root-Konten entfernen
- Key-Anmeldung vor einer Passwortabschaltung pruefen
- Passwortanmeldung nach expliziter Freigabe abschalten
- SSH-Konfiguration vor dem Reload pruefen

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

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
    "roles/bootstrap_ssh/tasks/main.yml": "3641ade83ffefabdf568f3a4a2b2e67183fc7a6c17cee0c44e9dea8361dfbc4c"
  }
}
```

## Quellen und Pflege

- `roles/bootstrap_ssh/tasks/main.yml`
- `roles/bootstrap_ssh/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
