# Telegraf ausrollen

Telegraf ausrollen

Aufruf: `bin/control telegraf [Optionen]`.

Vorhandene Kurzformen: `telegraf`.

Feature: telegraf. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/monitoring/deploy_telegraf.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "telegraf",
  "title": "Telegraf ausrollen",
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
    "bin/control.d/telegraf.json",
    "bin/control.d/telegraf.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/telegraf.json": "b0aebab888b98d6a7e39064b391c54aef27249a03a04c67a67a04def84e1570d",
    "bin/control.d/telegraf.sh": "e561b9767b3dba2a71f9f667f1a6c42789d9518a76f1b240477c283693c7f74b",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/telegraf.json`
- `bin/control.d/telegraf.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
