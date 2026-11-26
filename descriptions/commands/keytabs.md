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
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "SMB-Credentials in Kerberos-Keytabs ueberfuehren",
      "description": "# SMB-Credentials in Kerberos-Keytabs ueberfuehren\n\nSMB-Credentials in Kerberos-Keytabs ueberfuehren\n\nAufruf: `bin/control keytabs [Optionen]`.\n\nVorhandene Kurzformen: `gen-keytabs`, `keytabs`.\n\nFeature: kerberos. Die aktuelle Aktivierung prueft weiterhin Control.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/identity/generate_keytabs.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/keytabs.json`\n- `bin/control.d/keytabs.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "targets": {
          "label": "targets",
          "description": "Inventory-Hosts/-Gruppen als Ansible --limit. Fachliche Pruefungen bleiben aktiv."
        },
        "check": {
          "label": "check",
          "description": "Ansible-Check-Mode anfordern. Ob Aktionen diesen vollstaendig unterstuetzen, bestimmt das Playbook."
        }
      }
    },
    "en": {
      "title": "Convert SMB credentials to Kerberos keytabs",
      "description": "# Convert SMB credentials to Kerberos keytabs\n\nConvert SMB credentials to Kerberos keytabs\n\nRun: `bin/control keytabs [options]`.\n\nAliases: `gen-keytabs`, `keytabs`.\n\nFeature: kerberos. Control checks availability at runtime.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/identity/generate_keytabs.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/keytabs.json`\n- `bin/control.d/keytabs.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "targets": {
          "label": "Target hosts or groups",
          "description": "Limit Ansible to the selected inventory hosts or groups. The playbook still applies its own checks."
        },
        "check": {
          "label": "Check mode",
          "description": "Request Ansible check mode. Coverage depends on the playbook."
        }
      }
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/keytabs.json`
- `bin/control.d/keytabs.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
