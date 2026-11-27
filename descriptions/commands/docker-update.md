# Update Docker containers

Use `--limit` to select hosts for execution. The command rejects tag filters and starting mid-play because these could skip mandatory checks. Use syntax, list and check modes for previews.

Aliases: `docker-update-run`, `docker-update`.

Feature: `docker`.

Registry prerequisites:
- `playbooks/docker/vars/paths.yml`
- `lib/control/helpers.sh`
- `scripts/run_docker_update.sh`

## Check containers and Portainer

For each updated Compose stack, `bin/control docker-update --limit TARGET_HOST` waits up to 180 seconds for services to be running or healthy. It then checks Compose sources and Docker networks. A failed check fails the run.

Enable the additional TCP check with `portainer_check_enabled: true` in the Docker host’s **local host variables**. If absent or false, the controller skips the connection. The default is the host’s Ansible address, port 9443, with a five-second timeout. Override it with `portainer_check_host`, `portainer_check_port` and `portainer_check_timeout`. Run it separately with `.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit TARGET_HOST`.

## Parameters

## Sources and maintenance

- `bin/control.d/docker-update.json`
- `bin/control.d/docker-update.sh`

<details>
<summary>Deutsch</summary>

# Docker-Container aktualisieren

Für einen ausführenden Lauf begrenzt `--limit` die Hosts. Tagfilter und ein Einstieg mitten im Playbook würden Pflichtprüfungen auslassen und werden abgewiesen. Syntax-, Listen- und Checkmodus dienen der Vorschau.

Vorhandene Kurzformen: `docker-update-run`, `docker-update`.

Der Befehl gehört zum Feature `docker`.

Voraussetzungen laut Registry:
- `playbooks/docker/vars/paths.yml`
- `lib/control/helpers.sh`
- `scripts/run_docker_update.sh`

## Container und Portainer prüfen

`bin/control docker-update --limit ZIELHOST` wartet bei jedem aktualisierten Compose-Stack auf laufende Dienste oder deren erfolgreichen Healthcheck (bis zu 180 Sekunden je Stack). Danach prüft es die Compose-Quellen und Docker-Netze. Ein Fehler lässt den Lauf fehlschlagen.

Nur der zusätzliche TCP-Test für Portainer ist schaltbar. In den **lokalen Hostvariablen** des betreffenden Docker-Hosts `portainer_check_enabled: true` setzen. Mit `false` oder ohne Eintrag entfällt der Verbindungsversuch. Standardmäßig prüft der Controller die Ansible-Adresse des Hosts auf Port 9443 mit fünf Sekunden Wartezeit. Ein abweichendes Ziel ist über `portainer_check_host`, `portainer_check_port` und `portainer_check_timeout` konfigurierbar. Der Einzelaufruf lautet `.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit ZIELHOST`.

## Parameter für die TUI

## Quellen und Pflege

- `bin/control.d/docker-update.json`
- `bin/control.d/docker-update.sh`

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
    "bin/control.d/docker-update.json": "61ea18d3fe1bd313555865b6c0eef25b63b610db157a92e7e6ba392389986970",
    "bin/control.d/docker-update.sh": "473e7c7fcf7bc2bb8402d6ac602d0e4c47fba2acd42387a4716cd283553b2cdf"
  },
  "i18n": {
    "de": {
      "title": "Docker-Container aktualisieren",
      "description": "# Docker-Container aktualisieren\n\nFür einen ausführenden Lauf begrenzt `--limit` die Hosts. Tagfilter und ein Einstieg mitten im Playbook würden Pflichtprüfungen auslassen und werden abgewiesen. Syntax-, Listen- und Checkmodus dienen der Vorschau.\n\nVorhandene Kurzformen: `docker-update-run`, `docker-update`.\n\nDer Befehl gehört zum Feature `docker`.\n\nVoraussetzungen laut Registry:\n- `playbooks/docker/vars/paths.yml`\n- `lib/control/helpers.sh`\n- `scripts/run_docker_update.sh`\n\n## Container und Portainer prüfen\n\n`bin/control docker-update --limit ZIELHOST` wartet bei jedem aktualisierten Compose-Stack auf laufende Dienste oder deren erfolgreichen Healthcheck (bis zu 180 Sekunden je Stack). Danach prüft es die Compose-Quellen und Docker-Netze. Ein Fehler lässt den Lauf fehlschlagen.\n\nNur der zusätzliche TCP-Test für Portainer ist schaltbar. In den **lokalen Hostvariablen** des betreffenden Docker-Hosts `portainer_check_enabled: true` setzen. Mit `false` oder ohne Eintrag entfällt der Verbindungsversuch. Standardmäßig prüft der Controller die Ansible-Adresse des Hosts auf Port 9443 mit fünf Sekunden Wartezeit. Ein abweichendes Ziel ist über `portainer_check_host`, `portainer_check_port` und `portainer_check_timeout` konfigurierbar. Der Einzelaufruf lautet `.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit ZIELHOST`.\n\n## Parameter für die TUI\n\n## Quellen und Pflege\n\n- `bin/control.d/docker-update.json`\n- `bin/control.d/docker-update.sh`",
      "fields": {}
    },
    "en": {
      "title": "Update Docker containers",
      "description": "# Update Docker containers\n\nUse `--limit` to select hosts for execution. The command rejects tag filters and starting mid-play because these could skip mandatory checks. Use syntax, list and check modes for previews.\n\nAliases: `docker-update-run`, `docker-update`.\n\nFeature: `docker`.\n\nRegistry prerequisites:\n- `playbooks/docker/vars/paths.yml`\n- `lib/control/helpers.sh`\n- `scripts/run_docker_update.sh`\n\n## Check containers and Portainer\n\nFor each updated Compose stack, `bin/control docker-update --limit TARGET_HOST` waits up to 180 seconds for services to be running or healthy. It then checks Compose sources and Docker networks. A failed check fails the run.\n\nEnable the additional TCP check with `portainer_check_enabled: true` in the Docker host’s **local host variables**. If absent or false, the controller skips the connection. The default is the host’s Ansible address, port 9443, with a five-second timeout. Override it with `portainer_check_host`, `portainer_check_port` and `portainer_check_timeout`. Run it separately with `.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit TARGET_HOST`.\n\n## Parameters\n\n## Sources and maintenance\n\n- `bin/control.d/docker-update.json`\n- `bin/control.d/docker-update.sh`",
      "fields": {}
    }
  }
}
```

</details>
