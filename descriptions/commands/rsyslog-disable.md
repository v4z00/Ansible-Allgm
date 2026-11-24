# Zentrale Syslog-Weiterleitung deaktivieren

Zentrale Syslog-Weiterleitung deaktivieren

Aufruf: `bin/control rsyslog-disable [Optionen]`.

Vorhandene Kurzformen: `rsyslog-disable`.

Feature: rsyslog. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/disable_syslog_forwarding.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "rsyslog-disable",
  "title": "Zentrale Syslog-Weiterleitung deaktivieren",
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
    "bin/control.d/rsyslog-disable.json",
    "bin/control.d/rsyslog-disable.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/rsyslog-disable.json": "472e8608e051263b01c2b4705284a237b0efd5fcab7f36adc0608d772e6d3ce5",
    "bin/control.d/rsyslog-disable.sh": "26fa6c31a2f21311d751f5e3d6b69e36e113d9be156804531b2a3454c3ed058d",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/rsyslog-disable.json`
- `bin/control.d/rsyslog-disable.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
