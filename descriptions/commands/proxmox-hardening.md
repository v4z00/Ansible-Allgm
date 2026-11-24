# PVE-GUI und PBS-Port haerten

PVE-GUI und PBS-Port haerten

Aufruf: `bin/control proxmox-hardening [Optionen]`.

Vorhandene Kurzformen: `proxmox-hardening`.

Feature: proxmox. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/security/proxmox_stack_hardening.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "proxmox-hardening",
  "title": "PVE-GUI und PBS-Port haerten",
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
    "bin/control.d/proxmox-hardening.json",
    "bin/control.d/proxmox-hardening.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/proxmox-hardening.json": "f292bf1a0bb7dbdfbe2b0650ddda45e60db219efd2c2f253aed8620d8e909392",
    "bin/control.d/proxmox-hardening.sh": "40e479417ae3705f581fecccbc5a6bd70472bda274c46ec70b14d2711f281501",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/proxmox-hardening.json`
- `bin/control.d/proxmox-hardening.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
