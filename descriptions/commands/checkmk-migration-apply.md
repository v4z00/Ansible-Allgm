# CheckMK sichern und den gespeicherten Plan anwenden

CheckMK sichern und den gespeicherten Plan anwenden

Aufruf: `bin/control checkmk-migration-apply [Optionen]`.

Vorhandene Kurzformen: `checkmk-migration-apply`.

Feature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/checkmk/migrate_hosts.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "checkmk-migration-apply",
  "title": "CheckMK sichern und den gespeicherten Plan anwenden",
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
    "bin/control.d/checkmk-migration-apply.json",
    "bin/control.d/checkmk-migration-apply.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/checkmk-migration-apply.json": "f18c353893a8f5eb19f63ad1514dcf4873226f6bb8bae600ee02e9b0de6f8e13",
    "bin/control.d/checkmk-migration-apply.sh": "041fcfd5f565220a914754e67dc9527eaa6b0ad3eee190d7517564af9e5e434f",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  }
}
```

## Quellen und Pflege

- `bin/control.d/checkmk-migration-apply.json`
- `bin/control.d/checkmk-migration-apply.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
