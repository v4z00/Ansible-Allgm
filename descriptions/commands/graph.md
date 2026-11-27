# Show the inventory

Show the inventory

Run: `bin/control graph [options]`.

Aliases: `inv-graph`, `graph`.

Available without a separate feature switch. Control checks availability at runtime.

No structured parameter list is available. Use the existing terminal workflow and its help.

Registry prerequisites:
- `lib/control/helpers.sh`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/graph.json`
- `bin/control.d/graph.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

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

## Quellen und Pflege

- `bin/control.d/graph.json`
- `bin/control.d/graph.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
  },
  "i18n": {
    "de": {
      "title": "Inventory anzeigen",
      "description": "# Inventory anzeigen\n\nInventory anzeigen\n\nAufruf: `bin/control graph [Optionen]`.\n\nVorhandene Kurzformen: `inv-graph`, `graph`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/graph.json`\n- `bin/control.d/graph.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Show the inventory",
      "description": "# Show the inventory\n\nShow the inventory\n\nRun: `bin/control graph [options]`.\n\nAliases: `inv-graph`, `graph`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/graph.json`\n- `bin/control.d/graph.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
