# Controller, Variablenpfade, Inventory und Syntax pruefen

Controller, Variablenpfade, Inventory und Syntax pruefen

Aufruf: `bin/control doctor [Optionen]`.

Vorhandene Kurzformen: `doctor`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/doctor.sh`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "doctor",
  "title": "Controller, Variablenpfade, Inventory und Syntax pruefen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/doctor.json",
    "bin/control.d/doctor.sh"
  ],
  "source_hashes": {
    "bin/control.d/doctor.json": "244539a84f6d619b574081c6f77fe2f0070a9db2122df5c245ac5b23fb55c030",
    "bin/control.d/doctor.sh": "117e979b757f626f1977877587ac3d44fb63dc5bba1cbc5d6ab8e7208908e761"
  }
}
```

## Quellen und Pflege

- `bin/control.d/doctor.json`
- `bin/control.d/doctor.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
