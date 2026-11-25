# Passwoerter lokaler Service-Accounts rotieren

Passwoerter lokaler Service-Accounts rotieren

Aufruf: `bin/control rotate-service-passwords [Optionen]`.

Vorhandene Kurzformen: `rotate-service-pw`, `rotate-service-passwords`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/rotate_service_user_passwords.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "rotate-service-passwords",
  "title": "Passwoerter lokaler Service-Accounts rotieren",
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
    "bin/control.d/rotate-service-passwords.json",
    "bin/control.d/rotate-service-passwords.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/rotate-service-passwords.json": "4f003b4a05d6d51e1204f8db9b6c9d64992b5d6d3b5e17da185a63e0bc8cd398",
    "bin/control.d/rotate-service-passwords.sh": "939e4f7a1db86e445de5358e740d992ed0f0d7f36c276379de4ef37ad8a68f0e",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  }
}
```

## Quellen und Pflege

- `bin/control.d/rotate-service-passwords.json`
- `bin/control.d/rotate-service-passwords.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
