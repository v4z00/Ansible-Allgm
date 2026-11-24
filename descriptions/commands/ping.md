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
  }
}
```

## Quellen und Pflege

- `bin/control.d/ping.json`
- `bin/control.d/ping.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
