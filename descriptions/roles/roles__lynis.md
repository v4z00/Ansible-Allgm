# Rolle lynis

Rolle: `roles/lynis`.

Im Bestand definierte Aufgaben:

- Lynis installieren
- lynis
- Lynis-Audit ausfuehren
- Lokalen Reportordner sicherstellen
- Lynis-Ergebnisse abholen

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/lynis",
  "title": "Rolle lynis",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/lynis/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/lynis/tasks/main.yml": "9333ec3ddfaf508a9235a5f34f551a3ea251673925e3d77d070bfa3f8144da9d"
  }
}
```

## Quellen und Pflege

- `roles/lynis/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
