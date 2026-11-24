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
    "playbooks/docker/check_portainer.yml": "83d9f3270f694e70adf9982c2ce92988aa7f389224026d5fc6de666d6f4247d1"
  }
}
```
