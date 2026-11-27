# Check connectivity to Linux hosts

Check connectivity to Linux hosts

Run: `bin/control ping [options]`.

Aliases: `ansible-ping`.

Available without a separate feature switch. Control checks availability at runtime.

No structured parameter list is available. Use the existing terminal workflow and its help.

Registry prerequisites:
- `lib/control/helpers.sh`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/ping.json`
- `bin/control.d/ping.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Verbindung zu Linux-Hosts pruefen

Verbindung zu Linux-Hosts pruefen

Aufruf: `bin/control ping [Optionen]`.

Vorhandene Kurzformen: `ansible-ping`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `bin/control.d/ping.json`
- `bin/control.d/ping.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "ping",
  "title": "Verbindung zu Linux-Hosts pruefen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/ping.json",
    "bin/control.d/ping.sh"
  ],
  "source_hashes": {
    "bin/control.d/ping.json": "eda87fbbd42632833792074bf2ebc3b832ef2a9b31b6f57ea31f4c568a02211b",
    "bin/control.d/ping.sh": "107426d1a1d0b6afc412350f3a519b1f31667bc370d746e0c8e418bc4ad977d9"
  },
  "i18n": {
    "de": {
      "title": "Verbindung zu Linux-Hosts pruefen",
      "description": "# Verbindung zu Linux-Hosts pruefen\n\nVerbindung zu Linux-Hosts pruefen\n\nAufruf: `bin/control ping [Optionen]`.\n\nVorhandene Kurzformen: `ansible-ping`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/ping.json`\n- `bin/control.d/ping.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Check connectivity to Linux hosts",
      "description": "# Check connectivity to Linux hosts\n\nCheck connectivity to Linux hosts\n\nRun: `bin/control ping [options]`.\n\nAliases: `ansible-ping`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/ping.json`\n- `bin/control.d/ping.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
