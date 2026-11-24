# SMB-Credentials in Kerberos-Keytabs ueberfuehren

SMB-Credentials in Kerberos-Keytabs ueberfuehren

Aufruf: `bin/control keytabs [Optionen]`.

Vorhandene Kurzformen: `gen-keytabs`, `keytabs`.

Feature: kerberos. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/identity/generate_keytabs.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "keytabs",
  "title": "SMB-Credentials in Kerberos-Keytabs ueberfuehren",
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
    "bin/control.d/keytabs.json",
    "bin/control.d/keytabs.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/keytabs.json": "1790131f74a92da0d55d81ca7662fb1f1b8f81f591ea743c8dfffd766bd22fd8",
    "bin/control.d/keytabs.sh": "d2669a58df867fb66f8e55e2724ec4b9240e92af7a90f765568d0d66456f447d",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/keytabs.json`
- `bin/control.d/keytabs.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
