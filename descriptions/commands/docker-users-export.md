# Service-User aus Docker-Konfigurationen nach host_vars exportieren

Service-User aus Docker-Konfigurationen nach host_vars exportieren

Aufruf: `bin/control docker-users-export [Optionen]`.

Vorhandene Kurzformen: `docker-users-export`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/export_docker_users.py`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-users-export",
  "title": "Service-User aus Docker-Konfigurationen nach host_vars exportieren",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/docker-users-export.json",
    "bin/control.d/docker-users-export.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-users-export.json": "9efe561a10d07c3a8a0a26b1536eba3ae0cda5bc4dc3731a3dbd85e095822c14",
    "bin/control.d/docker-users-export.sh": "f90580ede7d8c608dd1b8420c6e0ec1062ac995afd2c3990b0757212ac7c0a4c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-users-export.json`
- `bin/control.d/docker-users-export.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
