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
  }
}
```

## Quellen und Pflege

- `bin/control.d/last-log.json`
- `bin/control.d/last-log.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
