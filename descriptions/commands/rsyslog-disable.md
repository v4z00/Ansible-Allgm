# Disable central syslog forwarding

Disable central syslog forwarding

Run: `bin/control rsyslog-disable [options]`.

Aliases: `rsyslog-disable`.

Feature: rsyslog. Control checks availability at runtime.

Registry prerequisites:
- `lib/control/helpers.sh`
- `playbooks/maintenance/disable_syslog_forwarding.yml`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/rsyslog-disable.json`
- `bin/control.d/rsyslog-disable.sh`
- `lib/control/helpers.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Zentrale Syslog-Weiterleitung deaktivieren

Zentrale Syslog-Weiterleitung deaktivieren

Aufruf: `bin/control rsyslog-disable [Optionen]`.

Vorhandene Kurzformen: `rsyslog-disable`.

Feature: rsyslog. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/maintenance/disable_syslog_forwarding.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `bin/control.d/rsyslog-disable.json`
- `bin/control.d/rsyslog-disable.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "rsyslog-disable",
  "title": "Zentrale Syslog-Weiterleitung deaktivieren",
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
    "bin/control.d/rsyslog-disable.json",
    "bin/control.d/rsyslog-disable.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/rsyslog-disable.json": "472e8608e051263b01c2b4705284a237b0efd5fcab7f36adc0608d772e6d3ce5",
    "bin/control.d/rsyslog-disable.sh": "26fa6c31a2f21311d751f5e3d6b69e36e113d9be156804531b2a3454c3ed058d",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "Zentrale Syslog-Weiterleitung deaktivieren",
      "description": "# Zentrale Syslog-Weiterleitung deaktivieren\n\nZentrale Syslog-Weiterleitung deaktivieren\n\nAufruf: `bin/control rsyslog-disable [Optionen]`.\n\nVorhandene Kurzformen: `rsyslog-disable`.\n\nFeature: rsyslog. Die aktuelle Aktivierung prueft weiterhin Control.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/maintenance/disable_syslog_forwarding.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/rsyslog-disable.json`\n- `bin/control.d/rsyslog-disable.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
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
      "title": "Disable central syslog forwarding",
      "description": "# Disable central syslog forwarding\n\nDisable central syslog forwarding\n\nRun: `bin/control rsyslog-disable [options]`.\n\nAliases: `rsyslog-disable`.\n\nFeature: rsyslog. Control checks availability at runtime.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/maintenance/disable_syslog_forwarding.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/rsyslog-disable.json`\n- `bin/control.d/rsyslog-disable.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
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

</details>
