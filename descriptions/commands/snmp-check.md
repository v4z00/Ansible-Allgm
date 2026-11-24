# SNMPv2-/SNMPv3-Zugaenge pruefen

SNMPv2-/SNMPv3-Zugaenge pruefen

Aufruf: `bin/control snmp-check [Optionen]`.

Vorhandene Kurzformen: `snmp-check`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/network/snmp_check.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "snmp-check",
  "title": "SNMPv2-/SNMPv3-Zugaenge pruefen",
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
    "bin/control.d/snmp-check.json",
    "bin/control.d/snmp-check.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/snmp-check.json": "684268949ddc94febb49407cecc8f1bd6fc04bb5311e81abd6d6ac85e7c7d4ed",
    "bin/control.d/snmp-check.sh": "0b708cb015df8985707469e58b89725ea904457e2cc41fb9318a927a24a74940",
    "lib/control/helpers.sh": "2b74a20d4cca10749451010fe2b9239be3018926fcc5f3e56135b17b7e68d97f"
  }
}
```

## Quellen und Pflege

- `bin/control.d/snmp-check.json`
- `bin/control.d/snmp-check.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
