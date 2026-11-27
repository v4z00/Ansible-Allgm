# Map the existing Checkmk hosts to the inventory interactively

Map the existing Checkmk hosts to the inventory interactively

Run: `bin/control checkmk-migration-plan [options]`.

Aliases: `checkmk-migration-plan`.

Feature: checkmk. Control checks availability at runtime.

No structured parameter list is available. Use the existing terminal workflow and its help.

Registry prerequisites:
- `lib/control/helpers.sh`
- `scripts/plan_checkmk_migration.py`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/checkmk-migration-plan.json`
- `bin/control.d/checkmk-migration-plan.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

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

## Quellen und Pflege

- `bin/control.d/checkmk-migration-plan.json`
- `bin/control.d/checkmk-migration-plan.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
  },
  "i18n": {
    "de": {
      "title": "CheckMK-Altbestand interaktiv dem Inventory zuordnen",
      "description": "# CheckMK-Altbestand interaktiv dem Inventory zuordnen\n\nCheckMK-Altbestand interaktiv dem Inventory zuordnen\n\nAufruf: `bin/control checkmk-migration-plan [Optionen]`.\n\nVorhandene Kurzformen: `checkmk-migration-plan`.\n\nFeature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/plan_checkmk_migration.py`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/checkmk-migration-plan.json`\n- `bin/control.d/checkmk-migration-plan.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Map the existing Checkmk hosts to the inventory interactively",
      "description": "# Map the existing Checkmk hosts to the inventory interactively\n\nMap the existing Checkmk hosts to the inventory interactively\n\nRun: `bin/control checkmk-migration-plan [options]`.\n\nAliases: `checkmk-migration-plan`.\n\nFeature: checkmk. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/plan_checkmk_migration.py`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/checkmk-migration-plan.json`\n- `bin/control.d/checkmk-migration-plan.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
