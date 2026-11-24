# UID-1000-Belegung pruefen

UID-1000-Belegung pruefen

Aufruf: `bin/control uid-audit [Optionen]`.

Vorhandene Kurzformen: `uid-audit`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/audit_uid_1000.yaml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "uid-audit",
  "title": "UID-1000-Belegung pruefen",
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
    "bin/control.d/uid-audit.json",
    "bin/control.d/uid-audit.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/uid-audit.json": "5ff00f1fd19e01f784deee8f2006364451673587da50d6c54d2eb299ad82cda5",
    "bin/control.d/uid-audit.sh": "8966861e8691ccfcdb9f9ca244aba6cd673a6249fbb8858195ade169fe5891cd",
    "lib/control/helpers.sh": "2b74a20d4cca10749451010fe2b9239be3018926fcc5f3e56135b17b7e68d97f"
  }
}
```

## Quellen und Pflege

- `bin/control.d/uid-audit.json`
- `bin/control.d/uid-audit.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
