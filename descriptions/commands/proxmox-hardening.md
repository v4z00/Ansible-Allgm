# PVE-GUI und PBS-Port haerten

PVE-GUI und PBS-Port haerten

Aufruf: `bin/control proxmox-hardening [Optionen]`.

Vorhandene Kurzformen: `proxmox-hardening`.

Feature: proxmox. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/security/proxmox_stack_hardening.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "proxmox-hardening",
  "title": "PVE-GUI und PBS-Port haerten",
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
    "bin/control.d/proxmox-hardening.json",
    "bin/control.d/proxmox-hardening.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/proxmox-hardening.json": "f292bf1a0bb7dbdfbe2b0650ddda45e60db219efd2c2f253aed8620d8e909392",
    "bin/control.d/proxmox-hardening.sh": "40e479417ae3705f581fecccbc5a6bd70472bda274c46ec70b14d2711f281501",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "PVE-GUI und PBS-Port haerten",
      "description": "# PVE-GUI und PBS-Port haerten\n\nPVE-GUI und PBS-Port haerten\n\nAufruf: `bin/control proxmox-hardening [Optionen]`.\n\nVorhandene Kurzformen: `proxmox-hardening`.\n\nFeature: proxmox. Die aktuelle Aktivierung prueft weiterhin Control.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/security/proxmox_stack_hardening.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/proxmox-hardening.json`\n- `bin/control.d/proxmox-hardening.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
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
      "title": "Harden the PVE web interface and PBS port",
      "description": "# Harden the PVE web interface and PBS port\n\nHarden the PVE web interface and PBS port\n\nRun: `bin/control proxmox-hardening [options]`.\n\nAliases: `proxmox-hardening`.\n\nFeature: proxmox. Control checks availability at runtime.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/security/proxmox_stack_hardening.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/proxmox-hardening.json`\n- `bin/control.d/proxmox-hardening.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
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

- `bin/control.d/proxmox-hardening.json`
- `bin/control.d/proxmox-hardening.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
