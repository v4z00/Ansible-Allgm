# Skript- und Backup-Pfade pruefen

Skript- und Backup-Pfade pruefen

Aufruf: `bin/control prepare-paths [Optionen]`.

Vorhandene Kurzformen: `prepare-paths`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/prepare_paths.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "prepare-paths",
  "title": "Skript- und Backup-Pfade pruefen",
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
    "bin/control.d/prepare-paths.json",
    "bin/control.d/prepare-paths.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/prepare-paths.json": "bcca5ae97bba1bf37502a01a9f36218c5ce7f70d9325b836d5e172beb2563a3a",
    "bin/control.d/prepare-paths.sh": "eba203ca33f8266f0377064f0461c76debef5833018eb461923c63c6dc847261",
    "lib/control/helpers.sh": "2b74a20d4cca10749451010fe2b9239be3018926fcc5f3e56135b17b7e68d97f"
  }
}
```

## Quellen und Pflege

- `bin/control.d/prepare-paths.json`
- `bin/control.d/prepare-paths.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
