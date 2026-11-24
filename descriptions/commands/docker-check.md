# Docker-Konfiguration und Quellen pruefen

Docker-Konfiguration und Quellen pruefen

Aufruf: `bin/control docker-check [Optionen]`.

Vorhandene Kurzformen: `docker-check`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/check_docker.sh`
- `scripts/check_docker_sources.py`
- `playbooks/docker/check_docker.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-check",
  "title": "Docker-Konfiguration und Quellen pruefen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/docker-check.json",
    "bin/control.d/docker-check.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-check.json": "ea15192dbdf801a8bfd9dc1e3c31ae7e2af9edc8031b9a818036e5ef35c01b97",
    "bin/control.d/docker-check.sh": "a52d40c0657c5e791af695788bbe2cbfece6b5286b8ac707a44d80272722b433"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-check.json`
- `bin/control.d/docker-check.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
