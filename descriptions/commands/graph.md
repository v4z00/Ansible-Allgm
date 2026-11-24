# Inventory anzeigen

Inventory anzeigen

Aufruf: `bin/control graph [Optionen]`.

Vorhandene Kurzformen: `inv-graph`, `graph`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "graph",
  "title": "Inventory anzeigen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/graph.json",
    "bin/control.d/graph.sh"
  ],
  "source_hashes": {
    "bin/control.d/graph.json": "1c160e39f83f8ff851f600300df11ff09a210df28178895c943ae628f3399fff",
    "bin/control.d/graph.sh": "e96aaf7fd15f6f01d3b4262975f31a55d0210edb5a4119f46eb7d5c04633a5fb"
  }
}
```

## Quellen und Pflege

- `bin/control.d/graph.json`
- `bin/control.d/graph.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
