# Docker-Container aktualisieren

Für einen ausführenden Lauf begrenzt `--limit` die Hosts. Tagfilter und ein Einstieg mitten im Playbook würden Pflichtprüfungen auslassen und werden abgewiesen. Syntax-, Listen- und Checkmodus dienen der Vorschau.

Vorhandene Kurzformen: `docker-update-run`, `docker-update`.

Der Befehl gehört zum Feature `docker`.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/run_docker_update.sh`

## Container und Portainer prüfen

`bin/control docker-update --limit ZIELHOST` wartet bei jedem aktualisierten Compose-Stack auf laufende Dienste oder deren erfolgreichen Healthcheck (bis zu 180 Sekunden je Stack). Danach prüft es die Compose-Quellen und Docker-Netze. Ein Fehler lässt den Lauf fehlschlagen.

Nur der zusätzliche TCP-Test für Portainer ist schaltbar. In den **lokalen Hostvariablen** des betreffenden Docker-Hosts `portainer_check_enabled: true` setzen. Mit `false` oder ohne Eintrag entfällt der Verbindungsversuch. Standardmäßig prüft der Controller die Ansible-Adresse des Hosts auf Port 9443 mit fünf Sekunden Wartezeit. Ein abweichendes Ziel ist über `portainer_check_host`, `portainer_check_port` und `portainer_check_timeout` konfigurierbar. Der Einzelaufruf lautet `.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit ZIELHOST`.

## Parameter für die TUI

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
