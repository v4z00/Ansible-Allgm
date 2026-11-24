# CheckMK-Altbestand interaktiv dem Inventory zuordnen

CheckMK-Altbestand interaktiv dem Inventory zuordnen

Aufruf: `bin/control checkmk-migration-plan [Optionen]`.

Vorhandene Kurzformen: `checkmk-migration-plan`.

Feature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/plan_checkmk_migration.py`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "checkmk-migration-plan",
  "title": "CheckMK-Altbestand interaktiv dem Inventory zuordnen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/checkmk-migration-plan.json",
    "bin/control.d/checkmk-migration-plan.sh"
  ],
  "source_hashes": {
    "bin/control.d/checkmk-migration-plan.json": "d09a93daf07ecb741cefc23288f69fdd5f7422607a9079a0ec91e63370bd4515",
    "bin/control.d/checkmk-migration-plan.sh": "69b8b1e8d9cbd6638cea58d60229d5470024d2234371c0182dfdfbd5f0e5531f"
  }
}
```

## Quellen und Pflege

- `bin/control.d/checkmk-migration-plan.json`
- `bin/control.d/checkmk-migration-plan.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
