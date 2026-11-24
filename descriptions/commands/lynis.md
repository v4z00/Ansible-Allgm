# Lynis ausfuehren und Reports holen

Lynis ausfuehren und Reports holen

Aufruf: `bin/control lynis [Optionen]`.

Vorhandene Kurzformen: `sec-audit`, `lynis`.

Feature: lynis. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/lynis.yml`
- `playbooks/reporting/lynis_summary.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "lynis",
  "title": "Lynis ausfuehren und Reports holen",
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
    "bin/control.d/lynis.json",
    "bin/control.d/lynis.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/lynis.json": "967d9bdc120daa504e51a06d960a4d1a07e7e1dc56fcee03263c4e4955cad81d",
    "bin/control.d/lynis.sh": "af0c5f6f9255704c24741041209ead62452bd65197e2ee53f32dc303b331cfd8",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/lynis.json`
- `bin/control.d/lynis.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
