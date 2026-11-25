# Chrony gezielt entfernen

Chrony gezielt entfernen

Aufruf: `bin/control chrony-uninstall [Optionen]`.

Vorhandene Kurzformen: `chrony-uninstall`.

Feature: chrony. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/uninstall_chrony.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "chrony-uninstall",
  "title": "Chrony gezielt entfernen",
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
    "bin/control.d/chrony-uninstall.json",
    "bin/control.d/chrony-uninstall.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/chrony-uninstall.json": "987d06254be844b074d2491d23d43454563b471505ed9b5e952abfb3788505da",
    "bin/control.d/chrony-uninstall.sh": "bf6a3bff922417cf705016317d46b3eaa8380877394082f60edb42e00eddc3ea",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  }
}
```

## Quellen und Pflege

- `bin/control.d/chrony-uninstall.json`
- `bin/control.d/chrony-uninstall.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
