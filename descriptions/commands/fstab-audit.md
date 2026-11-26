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

Der Audit legt die Dateien unter `controller_reports_dir/fstab_audit` ab. Ohne Vorgabe gilt `ANSIBLE_REPORTS_DIR`, andernfalls `x/reports` im Controllerprojekt. Relative Pfade beginnen im Projektverzeichnis.

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
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "fstab-Dateien einsammeln",
      "description": "# fstab-Dateien einsammeln\n\nfstab-Dateien einsammeln\n\nAufruf: `bin/control fstab-audit [Optionen]`.\n\nVorhandene Kurzformen: `audit-fstab`, `fstab-audit`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/maintenance/audit_fstab.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/fstab-audit.json`\n- `bin/control.d/fstab-audit.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\nDer Audit legt die Dateien unter `controller_reports_dir/fstab_audit` ab. Ohne Vorgabe gilt `ANSIBLE_REPORTS_DIR`, andernfalls `x/reports` im Controllerprojekt. Relative Pfade beginnen im Projektverzeichnis.",
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
      "title": "Collect fstab files",
      "description": "# Collect fstab files\n\nCollect fstab files\n\nRun: `bin/control fstab-audit [options]`.\n\nAliases: `audit-fstab`, `fstab-audit`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/maintenance/audit_fstab.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/fstab-audit.json`\n- `bin/control.d/fstab-audit.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\nThe audit writes files under `controller_reports_dir/fstab_audit`. The fallback is `ANSIBLE_REPORTS_DIR`, then `x/reports` in the controller project. Relative paths start at the project root.",
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
