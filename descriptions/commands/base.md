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
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "Baseline; erfordert --limit ZIEL oder ausdruecklich --all",
      "description": "# Baseline; erfordert --limit ZIEL oder ausdruecklich --all\n\nBaseline; erfordert --limit ZIEL oder ausdruecklich --all\n\nAufruf: `bin/control base [Optionen]`.\n\nVorhandene Kurzformen: `base`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/base.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/base.json`\n- `bin/control.d/base.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "targets": {
          "label": "targets",
          "description": "Explizite Inventory-Hosts oder -Gruppen; als bestehendes --limit uebergeben."
        },
        "all": {
          "label": "all",
          "description": "Bewusst alle Ziele statt --limit auswaehlen."
        }
      }
    },
    "en": {
      "title": "Apply the baseline to the hosts in --limit or explicitly choose --all",
      "description": "# Apply the baseline to the hosts in --limit or explicitly choose --all\n\nApply the baseline to the hosts in --limit or explicitly choose --all\n\nRun: `bin/control base [options]`.\n\nAliases: `base`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/base.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/base.json`\n- `bin/control.d/base.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "targets": {
          "label": "Target hosts or groups",
          "description": "Pass the selected inventory hosts or groups as --limit."
        },
        "all": {
          "label": "All targets",
          "description": "Explicitly select all targets in place of --limit."
        }
      }
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/base.json`
- `bin/control.d/base.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
