# Postfix-Warteschlange leeren

Postfix-Warteschlange leeren

Aufruf: `bin/control postfix-queue-clear [Optionen]`.

Vorhandene Kurzformen: `postfix-queue-clear`.

Feature: postfix. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/clear_postfix_que.yaml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "postfix-queue-clear",
  "title": "Postfix-Warteschlange leeren",
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
    "bin/control.d/postfix-queue-clear.json",
    "bin/control.d/postfix-queue-clear.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/postfix-queue-clear.json": "dd1ebe567e835e10ef368d4d361d23ce10ff942cc99ff10bd8cd7ca3c00db57c",
    "bin/control.d/postfix-queue-clear.sh": "06d8ce52c119bc08af7d7166b95b2f8278006fdc4f677e4d2d12192a29c0ae4b",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  }
}
```

## Quellen und Pflege

- `bin/control.d/postfix-queue-clear.json`
- `bin/control.d/postfix-queue-clear.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
