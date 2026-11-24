# Alle verwalteten Docker-Stacks stoppen

Alle verwalteten Docker-Stacks stoppen

Aufruf: `bin/control docker-stop [Optionen]`.

Vorhandene Kurzformen: `docker-stop`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/docker/stop_all_docker.yaml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-stop",
  "title": "Alle verwalteten Docker-Stacks stoppen",
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
    "bin/control.d/docker-stop.json",
    "bin/control.d/docker-stop.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-stop.json": "794c4121f59a0732ecd08efcb027a398777d28472e71c4130bc30628ee51d1a2",
    "bin/control.d/docker-stop.sh": "6356c6a4980d4a2251d7a14184869b4a4616ffca01349ff81b2755f571741737",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-stop.json`
- `bin/control.d/docker-stop.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
