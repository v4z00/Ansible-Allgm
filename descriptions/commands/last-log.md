# [EXAMPLE] Show the latest execution log

[EXAMPLE] Show the latest execution log

Run: `bin/control last-log [options]`.

Aliases: `docker-last-log docker`, `last-log`.

Available without a separate feature switch. Control checks availability at runtime.

No structured parameter list is available. Use the existing terminal workflow and its help.

Registry prerequisites:
- `lib/control/helpers.sh`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/last-log.json`
- `bin/control.d/last-log.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# [MUSTER] Letztes Ausfuehrungslog anzeigen

[MUSTER] Letztes Ausfuehrungslog anzeigen

Aufruf: `bin/control last-log [Optionen]`.

Vorhandene Kurzformen: `docker-last-log docker`, `last-log`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `bin/control.d/last-log.json`
- `bin/control.d/last-log.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "last-log",
  "title": "[MUSTER] Letztes Ausfuehrungslog anzeigen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/last-log.json",
    "bin/control.d/last-log.sh"
  ],
  "source_hashes": {
    "bin/control.d/last-log.json": "9a7baff5d34773b962aaad238d1c7065f21455d1a01481b6041d83cee92184ff",
    "bin/control.d/last-log.sh": "84f8dcd8d04a849586485882f30923e0e95054fb7d842e95a08e6af83a0bd5a4"
  },
  "i18n": {
    "de": {
      "title": "[MUSTER] Letztes Ausfuehrungslog anzeigen",
      "description": "# [MUSTER] Letztes Ausfuehrungslog anzeigen\n\n[MUSTER] Letztes Ausfuehrungslog anzeigen\n\nAufruf: `bin/control last-log [Optionen]`.\n\nVorhandene Kurzformen: `docker-last-log docker`, `last-log`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/last-log.json`\n- `bin/control.d/last-log.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "[EXAMPLE] Show the latest execution log",
      "description": "# [EXAMPLE] Show the latest execution log\n\n[EXAMPLE] Show the latest execution log\n\nRun: `bin/control last-log [options]`.\n\nAliases: `docker-last-log docker`, `last-log`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/last-log.json`\n- `bin/control.d/last-log.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
