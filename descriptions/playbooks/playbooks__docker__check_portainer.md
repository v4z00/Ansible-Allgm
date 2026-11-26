# Portainer-Erreichbarkeit prüfen

Das Playbook wird nach dem regulären Container-Check für dieselben Docker-Hosts aufgerufen. Mit `portainer_check_enabled: true` prüft der Controller den konfigurierten TCP-Port. Ohne Eintrag oder bei `false` entfällt die Verbindung. Ein aktiviertes, unerreichbares Ziel führt zum Fehler. `portainer_check_host`, `portainer_check_port` und `portainer_check_timeout` überschreiben Ansible-Zieladresse, Port 9443 und fünf Sekunden Timeout.

Einzeln aus dem Controllerverzeichnis ausführen:

```bash
.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit ZIELHOST
```

## Parameter

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/check_portainer.yml",
  "title": "Portainer-Erreichbarkeit prüfen",
  "documented": true,
  "fields": [
    {
      "id": "portainer_check_enabled",
      "label": "portainer_check_enabled",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "description": "Zusätzlichen TCP-Test für Portainer nach dem Pflichtcheck aktivieren."
    },
    {
      "id": "portainer_check_host",
      "label": "portainer_check_host",
      "type": "string",
      "required": false,
      "sensitive": false,
      "description": "Optionales TCP-Ziel. Ohne Eintrag gilt die Ansible-Adresse des Docker-Hosts."
    },
    {
      "id": "portainer_check_port",
      "label": "portainer_check_port",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "description": "TCP-Port für den optionalen Portainer-Test."
    },
    {
      "id": "portainer_check_timeout",
      "label": "portainer_check_timeout",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "description": "Wartezeit für den Portainer-TCP-Test in Sekunden."
    }
  ],
  "constraints": [],
  "sources": [
    "playbooks/docker/check_portainer.yml"
  ],
  "source_hashes": {
    "playbooks/docker/check_portainer.yml": "b1476bf04dd3f367adaf3bc73d7bbef5b60615766e944ad003780f69a649b5ee"
  },
  "i18n": {
    "de": {
      "title": "Portainer-Erreichbarkeit prüfen",
      "description": "# Portainer-Erreichbarkeit prüfen\n\nDas Playbook wird nach dem regulären Container-Check für dieselben Docker-Hosts aufgerufen. Mit `portainer_check_enabled: true` prüft der Controller den konfigurierten TCP-Port. Ohne Eintrag oder bei `false` entfällt die Verbindung. Ein aktiviertes, unerreichbares Ziel führt zum Fehler. `portainer_check_host`, `portainer_check_port` und `portainer_check_timeout` überschreiben Ansible-Zieladresse, Port 9443 und fünf Sekunden Timeout.\n\nEinzeln aus dem Controllerverzeichnis ausführen:\n\n\u0060\u0060\u0060bash\n.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit ZIELHOST\n\u0060\u0060\u0060\n\n## Parameter",
      "fields": {
        "portainer_check_enabled": {
          "label": "portainer_check_enabled",
          "description": "Zusätzlichen TCP-Test für Portainer nach dem Pflichtcheck aktivieren."
        },
        "portainer_check_host": {
          "label": "portainer_check_host",
          "description": "Optionales TCP-Ziel. Ohne Eintrag gilt die Ansible-Adresse des Docker-Hosts."
        },
        "portainer_check_port": {
          "label": "portainer_check_port",
          "description": "TCP-Port für den optionalen Portainer-Test."
        },
        "portainer_check_timeout": {
          "label": "portainer_check_timeout",
          "description": "Wartezeit für den Portainer-TCP-Test in Sekunden."
        }
      }
    },
    "en": {
      "title": "Check Portainer connectivity",
      "description": "# Check Portainer connectivity\n\nThis playbook runs for the same Docker hosts after their regular container check. With `portainer_check_enabled: true` the controller probes the TCP port and fails if unreachable. Without the setting, or when false, it skips the probe. Override the default Ansible address, port 9443 and five-second timeout with `portainer_check_host`, `portainer_check_port` and `portainer_check_timeout`.\n\nTo run it separately from the controller directory:\n\n\u0060\u0060\u0060bash\n.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit ZIELHOST\n\u0060\u0060\u0060\n\n## Parameters",
      "fields": {
        "portainer_check_enabled": {
          "label": "portainer_check_enabled",
          "description": "Enable an additional TCP check for Portainer after the mandatory container checks."
        },
        "portainer_check_host": {
          "label": "portainer_check_host",
          "description": "Optional TCP target. Defaults to the Docker host’s Ansible address."
        },
        "portainer_check_port": {
          "label": "portainer_check_port",
          "description": "TCP port for the optional Portainer check."
        },
        "portainer_check_timeout": {
          "label": "portainer_check_timeout",
          "description": "Timeout for the Portainer TCP check, in seconds."
        }
      }
    }
  }
}
```
