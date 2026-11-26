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
  },
  "i18n": {
    "de": {
      "title": "Controller, Variablenpfade, Inventory und Syntax pruefen",
      "description": "# Controller, Variablenpfade, Inventory und Syntax pruefen\n\nController, Variablenpfade, Inventory und Syntax pruefen\n\nAufruf: `bin/control doctor [Optionen]`.\n\nVorhandene Kurzformen: `doctor`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/doctor.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/doctor.json`\n- `bin/control.d/doctor.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Check the controller, variable paths, inventory and playbook syntax",
      "description": "# Check the controller, variable paths, inventory and playbook syntax\n\nCheck the controller, variable paths, inventory and playbook syntax\n\nRun: `bin/control doctor [options]`.\n\nAliases: `doctor`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/doctor.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/doctor.json`\n- `bin/control.d/doctor.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/doctor.json`
- `bin/control.d/doctor.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
