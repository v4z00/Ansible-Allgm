# Baseline; erfordert --limit ZIEL oder ausdruecklich --all

Baseline; erfordert --limit ZIEL oder ausdruecklich --all

Aufruf: `bin/control base [Optionen]`.

Vorhandene Kurzformen: `base`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/base.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "base",
  "title": "Baseline; erfordert --limit ZIEL oder ausdruecklich --all",
  "documented": true,
  "fields": [
    {
      "id": "targets",
      "label": "targets",
      "description": "Explizite Inventory-Hosts oder -Gruppen; als bestehendes --limit uebergeben.",
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
      "id": "all",
      "label": "all",
      "description": "Bewusst alle Ziele statt --limit auswaehlen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--all"
      }
    }
  ],
  "constraints": [
    {
      "kind": "exactly_one_of",
      "fields": [
        "targets",
        "all"
      ]
    }
  ],
  "sources": [
    "bin/control.d/base.json",
    "bin/control.d/base.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/base.json": "ac8d110c7c0fc83fd2442e61e4398a02c2e213779c744e66cbab9cf782edafe7",
    "bin/control.d/base.sh": "82162c17f96daf8b7609194cff00c76eb5f34f7795257e74b49fcddb01b7738a",
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/base.json`
- `bin/control.d/base.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
