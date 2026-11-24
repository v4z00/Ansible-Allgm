# Rolle security_tools

Rolle: `roles/security_tools`.

Im Bestand definierte Aufgaben:

- PAM- und Security-Werkzeuge installieren
- Needrestart non-interaktiv konfigurieren

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/security_tools",
  "title": "Rolle security_tools",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/security_tools/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/security_tools/tasks/main.yml": "1e85044f692d043623e2d4559636c56fd86dcc5886d5ececd897cabdd510aafc"
  }
}
```

## Quellen und Pflege

- `roles/security_tools/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
