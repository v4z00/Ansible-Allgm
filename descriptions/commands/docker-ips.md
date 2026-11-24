# Docker-Netze und statische IPs auswerten

Docker-Netze und statische IPs auswerten

Aufruf: `bin/control docker-ips [Optionen]`.

Vorhandene Kurzformen: `docker-ips`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/docker/get_docker_ips.yaml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-ips",
  "title": "Docker-Netze und statische IPs auswerten",
  "documented": true,
  "fields": [
    {
      "id": "targets",
      "label": "targets",
      "description": "Inventory-Hosts/-Gruppen als Ansible --limit. Fachliche Pruefungen bleiben aktiv.",
      "type": "array",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--limit",
        "separator": ","
      },
      "completion": {
        "source": "inventory.targets"
      }
    },
    {
      "id": "check",
      "label": "check",
      "description": "Ansible-Check-Mode anfordern. Ob Aktionen diesen vollstaendig unterstuetzen, bestimmt das Playbook.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--check"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/docker-ips.json",
    "bin/control.d/docker-ips.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-ips.json": "99904af0da7f767356b6edc4157aae43b2238bead74b17a806e07a914c0a9f86",
    "bin/control.d/docker-ips.sh": "350dede679ee4f4fa3ce0d61a7c4d3647b88ed51ecda2bfbdc5dd9f97bdab387",
    "lib/control/helpers.sh": "2b74a20d4cca10749451010fe2b9239be3018926fcc5f3e56135b17b7e68d97f"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-ips.json`
- `bin/control.d/docker-ips.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
