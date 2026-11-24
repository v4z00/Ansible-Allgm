# Verwaltete Mounts in fstab setzen

Verwaltete Mounts in fstab setzen

Aufruf: `bin/control set-fstab [Optionen]`.

Vorhandene Kurzformen: `set-fstab`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/set_fstab.yaml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "set-fstab",
  "title": "Verwaltete Mounts in fstab setzen",
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
    "bin/control.d/set-fstab.json",
    "bin/control.d/set-fstab.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/set-fstab.json": "ab0a259566df8956373e5572c29d6b1297db0cedf1fbdc7c9a0dca1f731f71d0",
    "bin/control.d/set-fstab.sh": "9bbb1799eeb2464ce8c0684afea26a9e3d58b6af5351ea6a3dba1c0426248350",
    "lib/control/helpers.sh": "2b74a20d4cca10749451010fe2b9239be3018926fcc5f3e56135b17b7e68d97f"
  }
}
```

## Quellen und Pflege

- `bin/control.d/set-fstab.json`
- `bin/control.d/set-fstab.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
