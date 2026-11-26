# Docker-Konfiguration und Quellen pruefen

Docker-Konfiguration und Quellen pruefen

Aufruf: `bin/control docker-check [Optionen]`.

Vorhandene Kurzformen: `docker-check`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `playbooks/docker/vars/paths.yml`
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
    "bin/control.d/docker-check.json": "9e5d709f4fe4525d3894c6477ac8512e3ff8300e95a6017551cedac2ed7ed65a",
    "bin/control.d/docker-check.sh": "a52d40c0657c5e791af695788bbe2cbfece6b5286b8ac707a44d80272722b433"
  },
  "i18n": {
    "de": {
      "title": "Docker-Konfiguration und Quellen pruefen",
      "description": "# Docker-Konfiguration und Quellen pruefen\n\nDocker-Konfiguration und Quellen pruefen\n\nAufruf: `bin/control docker-check [Optionen]`.\n\nVorhandene Kurzformen: `docker-check`.\n\nFeature: docker. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `playbooks/docker/vars/paths.yml`\n- `lib/control/helpers.sh`\n- `scripts/check_docker.sh`\n- `scripts/check_docker_sources.py`\n- `playbooks/docker/check_docker.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/docker-check.json`\n- `bin/control.d/docker-check.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Check Docker configuration and Compose sources",
      "description": "# Check Docker configuration and Compose sources\n\nCheck Docker configuration and Compose sources\n\nRun: `bin/control docker-check [options]`.\n\nAliases: `docker-check`.\n\nFeature: docker. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `playbooks/docker/vars/paths.yml`\n- `lib/control/helpers.sh`\n- `scripts/check_docker.sh`\n- `scripts/check_docker_sources.py`\n- `playbooks/docker/check_docker.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/docker-check.json`\n- `bin/control.d/docker-check.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-check.json`
- `bin/control.d/docker-check.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
