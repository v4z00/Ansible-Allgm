# fstab-Dateien einsammeln

fstab-Dateien einsammeln

Aufruf: `bin/control fstab-audit [Optionen]`.

Vorhandene Kurzformen: `audit-fstab`, `fstab-audit`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/audit_fstab.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "fstab-audit",
  "title": "fstab-Dateien einsammeln",
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
    "bin/control.d/fstab-audit.json",
    "bin/control.d/fstab-audit.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/fstab-audit.json": "25b5cadf8d93116199975bac9f20f88f456da966013f3cf5c2380b0f5c4a0e92",
    "bin/control.d/fstab-audit.sh": "40acea74522a3fe7802a4e953b5efbcc55e9d0925c9b6f7e098dd97948517a40",
    "lib/control/helpers.sh": "2b74a20d4cca10749451010fe2b9239be3018926fcc5f3e56135b17b7e68d97f"
  }
}
```

## Quellen und Pflege

- `bin/control.d/fstab-audit.json`
- `bin/control.d/fstab-audit.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
