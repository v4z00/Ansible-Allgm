# Testmail ueber die verwalteten Hosts senden

Testmail ueber die verwalteten Hosts senden

Aufruf: `bin/control mail-test [Optionen]`.

Vorhandene Kurzformen: `mail-test`.

Feature: postfix. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/test_mail.yaml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "mail-test",
  "title": "Testmail ueber die verwalteten Hosts senden",
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
    "bin/control.d/mail-test.json",
    "bin/control.d/mail-test.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/mail-test.json": "e44e79ee73d25fe58f485e89844a0457913d20c87922c2b77dd06595a95fe20d",
    "bin/control.d/mail-test.sh": "f6f45c47e729af1b2e62f3669d9f8556a631b6de9bd3ffa6549e5a29b89441dc",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/mail-test.json`
- `bin/control.d/mail-test.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
