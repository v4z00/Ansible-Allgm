# Docker-Container aktualisieren

Docker-Container aktualisieren

Aufruf: `bin/control docker-update [Optionen]`.

Der Update-Lauf prüft den Laufzustand jedes aktualisierten Stacks sowie Quellen und Netze. Eine nicht bestandene Prüfung führt zu einem Fehler. Nur der zusätzliche TCP-Test für Portainer wird mit `portainer_check_enabled: true` in den lokalen Hostvariablen aktiviert.

Für einen ausführenden Lauf begrenzt `--limit` die Hosts. Tagfilter und ein Einstieg mitten im Playbook würden Pflichtprüfungen auslassen und werden abgewiesen. Syntax-, Listen- und Checkmodus dienen der Vorschau.

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
    "bin/control.d/docker-update.json": "f43ab973642b6db693086ac2a13d82ede8b94185fe50007c22ccd5e0c7fca098",
    "bin/control.d/docker-update.sh": "473e7c7fcf7bc2bb8402d6ac602d0e4c47fba2acd42387a4716cd283553b2cdf"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-update.json`
- `bin/control.d/docker-update.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
