# Feature-Schalter und lokale Umgebung pruefen; keine Settings aendern

Feature-Schalter und lokale Umgebung pruefen; keine Settings aendern

Aufruf: `bin/control features-check [Optionen]`.

Vorhandene Kurzformen: `features-check`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `scripts/feature_audit.py`
- `scripts/feature_catalog.json`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "features-check",
  "title": "Feature-Schalter und lokale Umgebung pruefen; keine Settings aendern",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/features-check.json",
    "bin/control.d/features-check.sh"
  ],
  "source_hashes": {
    "bin/control.d/features-check.json": "808e3ae28705465fe9b39727fadae9fc870ba8d366ebf1857d3a65a15aceafd1",
    "bin/control.d/features-check.sh": "65f1158880bcb59e81df96beb0ffbdd77be92332244be63efcdeba6abf1b5fe9"
  }
}
```

## Quellen und Pflege

- `bin/control.d/features-check.json`
- `bin/control.d/features-check.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
