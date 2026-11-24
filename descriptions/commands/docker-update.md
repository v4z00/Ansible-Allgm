# Docker-Container aktualisieren

Docker-Container aktualisieren

Aufruf: `bin/control docker-update [Optionen]`.

Vorhandene Kurzformen: `docker-update-run`, `docker-update`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/run_docker_update.sh`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-update",
  "title": "Docker-Container aktualisieren",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/docker-update.json",
    "bin/control.d/docker-update.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-update.json": "64972b09739a1b6cc4c8b0e8a29108ee38d746f5e1d0f0de21608e7ab07276e3",
    "bin/control.d/docker-update.sh": "473e7c7fcf7bc2bb8402d6ac602d0e4c47fba2acd42387a4716cd283553b2cdf"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-update.json`
- `bin/control.d/docker-update.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
