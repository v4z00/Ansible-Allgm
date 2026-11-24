# Rolle baseline

Rolle: `roles/baseline`.

Im Bestand definierte Aufgaben:

- APT-Cache aktualisieren und Basispakete installieren
- {{ base_packages }}

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/baseline",
  "title": "Rolle baseline",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/baseline/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/baseline/tasks/main.yml": "87a7219760f84883a88c9fc8adfe9ec78bd8fec3601b022a0717dbf812c161b1"
  }
}
```

## Quellen und Pflege

- `roles/baseline/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
