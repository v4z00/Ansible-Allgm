# Macvlan-Parent-Interfaces vorbereiten

Macvlan-Parent-Interfaces vorbereiten

Aufruf: `bin/control docker-macvlan-prepare [Optionen]`.

Vorhandene Kurzformen: `docker-macvlan-prepare`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/docker/prepare_macvlan_parents.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-macvlan-prepare",
  "title": "Macvlan-Parent-Interfaces vorbereiten",
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
    "bin/control.d/docker-macvlan-prepare.json",
    "bin/control.d/docker-macvlan-prepare.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-macvlan-prepare.json": "80e8bf3a8efa8dded36440a863c821c6551a79694875c0770f3f421e6bce264c",
    "bin/control.d/docker-macvlan-prepare.sh": "c53f7870a201d3ef0d9da4bf5dbfe44d1bb40b6d188b732b0d96b4f0fdb98453",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-macvlan-prepare.json`
- `bin/control.d/docker-macvlan-prepare.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
