# Service-User aus Docker-Konfigurationen nach host_vars exportieren

Service-User aus Docker-Konfigurationen nach host_vars exportieren

Aufruf: `bin/control docker-users-export [Optionen]`.

Vorhandene Kurzformen: `docker-users-export`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Gib das Compose-Verzeichnis mit `--source PFAD` oder `ANSIBLE_DOCKER_CONFIG_ROOT` an. Ohne Vorgabe sucht der Export im Ordner `docker-configs` neben dem Projekt. Das Projekt bestimmt `--root PFAD`, danach `ANSIBLE_PROJECT_ROOT`, sonst der Speicherort des Skripts. `--check` zeigt Änderungen an, bevor die Übersicht geschrieben wird.

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
  },
  "i18n": {
    "de": {
      "title": "Service-User aus Docker-Konfigurationen nach host_vars exportieren",
      "description": "# Service-User aus Docker-Konfigurationen nach host_vars exportieren\n\nService-User aus Docker-Konfigurationen nach host_vars exportieren\n\nAufruf: `bin/control docker-users-export [Optionen]`.\n\nVorhandene Kurzformen: `docker-users-export`.\n\nFeature: docker. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nGib das Compose-Verzeichnis mit `--source PFAD` oder `ANSIBLE_DOCKER_CONFIG_ROOT` an. Ohne Vorgabe sucht der Export im Ordner `docker-configs` neben dem Projekt. Das Projekt bestimmt `--root PFAD`, danach `ANSIBLE_PROJECT_ROOT`, sonst der Speicherort des Skripts. `--check` zeigt Änderungen an, bevor die Übersicht geschrieben wird.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/export_docker_users.py`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/docker-users-export.json`\n- `bin/control.d/docker-users-export.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Export service users from Docker configuration to host_vars",
      "description": "# Export service users from Docker configuration to host_vars\n\nExport service users from Docker configuration to host_vars\n\nRun: `bin/control docker-users-export [options]`.\n\nAliases: `docker-users-export`.\n\nFeature: docker. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nSet the Compose directory with `--source PATH` or `ANSIBLE_DOCKER_CONFIG_ROOT`. By default the export reads `docker-configs` next to the project. The project is chosen by `--root PATH`, then `ANSIBLE_PROJECT_ROOT`, then the checkout containing the script. Use `--check` to preview changes.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/export_docker_users.py`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/docker-users-export.json`\n- `bin/control.d/docker-users-export.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-users-export.json`
- `bin/control.d/docker-users-export.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
