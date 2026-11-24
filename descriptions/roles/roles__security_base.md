# Rolle security_base

Rolle: `roles/security_base`.

Im Bestand definierte Aufgaben:

- Rechtlichen Login-Banner setzen
- login.defs haerten
- Verwaiste Pakete optional entfernen

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/security_base",
  "title": "Rolle security_base",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/security_base/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/security_base/tasks/main.yml": "0a5a737f5a3fc60f8474dc88cf2107dde6f70f4887b9da51c2d141d39134b691"
  }
}
```

## Quellen und Pflege

- `roles/security_base/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
