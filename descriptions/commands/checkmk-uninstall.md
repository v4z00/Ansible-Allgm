# CheckMK-Agent gezielt entfernen

CheckMK-Agent gezielt entfernen

Aufruf: `bin/control checkmk-uninstall [Optionen]`.

Vorhandene Kurzformen: `checkmk-uninstall`.

Feature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/checkmk/uninstall_agent.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "checkmk-uninstall",
  "title": "CheckMK-Agent gezielt entfernen",
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
    "bin/control.d/checkmk-uninstall.json",
    "bin/control.d/checkmk-uninstall.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/checkmk-uninstall.json": "93c02a059c2baa8b4590dae2853bef3e73b7e18175aabf77ca18ef5ec5610e0f",
    "bin/control.d/checkmk-uninstall.sh": "ab21cfddbae1de6bd5fc8d62d559347927fc97373797953ba0a834e77fd5e180",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/checkmk-uninstall.json`
- `bin/control.d/checkmk-uninstall.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
