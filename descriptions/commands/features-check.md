# Check feature switches and the local environment without editing settings

Check feature switches and the local environment without editing settings

Run: `bin/control features-check [options]`.

Aliases: `features-check`.

Available without a separate feature switch. Control checks availability at runtime.

No structured parameter list is available. Use the existing terminal workflow and its help.

Registry prerequisites:
- `scripts/feature_audit.py`
- `scripts/feature_catalog.json`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/features-check.json`
- `bin/control.d/features-check.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

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

## Quellen und Pflege

- `bin/control.d/features-check.json`
- `bin/control.d/features-check.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
  },
  "i18n": {
    "de": {
      "title": "Feature-Schalter und lokale Umgebung pruefen; keine Settings aendern",
      "description": "# Feature-Schalter und lokale Umgebung pruefen; keine Settings aendern\n\nFeature-Schalter und lokale Umgebung pruefen; keine Settings aendern\n\nAufruf: `bin/control features-check [Optionen]`.\n\nVorhandene Kurzformen: `features-check`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `scripts/feature_audit.py`\n- `scripts/feature_catalog.json`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/features-check.json`\n- `bin/control.d/features-check.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Check feature switches and the local environment without editing settings",
      "description": "# Check feature switches and the local environment without editing settings\n\nCheck feature switches and the local environment without editing settings\n\nRun: `bin/control features-check [options]`.\n\nAliases: `features-check`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `scripts/feature_audit.py`\n- `scripts/feature_catalog.json`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/features-check.json`\n- `bin/control.d/features-check.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
