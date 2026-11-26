# Alle Playbooks syntaktisch pruefen

Alle Playbooks syntaktisch pruefen

Aufruf: `bin/control syntax [Optionen]`.

Vorhandene Kurzformen: `syntax`.

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
  "ref": "syntax",
  "title": "Alle Playbooks syntaktisch pruefen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/syntax.json",
    "bin/control.d/syntax.sh"
  ],
  "source_hashes": {
    "bin/control.d/syntax.json": "fad14089e53a52fc1a8a9f608d997617bf1fcf6bdc24ad5c81f4625f0eae2c9f",
    "bin/control.d/syntax.sh": "fe03c63c28c404a8e00dc85442b958b0971adbe07c4d7ee864c328e43afdccd4"
  },
  "i18n": {
    "de": {
      "title": "Alle Playbooks syntaktisch pruefen",
      "description": "# Alle Playbooks syntaktisch pruefen\n\nAlle Playbooks syntaktisch pruefen\n\nAufruf: `bin/control syntax [Optionen]`.\n\nVorhandene Kurzformen: `syntax`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/syntax.json`\n- `bin/control.d/syntax.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Check the syntax of all playbooks",
      "description": "# Check the syntax of all playbooks\n\nCheck the syntax of all playbooks\n\nRun: `bin/control syntax [options]`.\n\nAliases: `syntax`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/syntax.json`\n- `bin/control.d/syntax.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/syntax.json`
- `bin/control.d/syntax.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
