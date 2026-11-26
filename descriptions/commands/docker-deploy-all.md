# Alle Docker-Schritte ohne Rueckfragen ausrollen

Alle Docker-Schritte ohne Rueckfragen ausrollen

Aufruf: `bin/control docker-deploy-all [Optionen]`.

Vorhandene Kurzformen: `docker-deploy-all`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Der vorhandene Ablauf bearbeitet die verwalteten Stacks der ausgewaehlten Hosts. Ein einzelner Stackfilter ist nicht behauptet. Vorhandene Rueckfragen zu Netzwerken, Benutzern und Waisen-Stacks bleiben aktiv.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/docker/deploy_docker_networks.yaml`
- `playbooks/docker/deploy_docker_stacks.yml`
- `playbooks/docker/deploy_docker_users.yml`
- `playbooks/docker/prepare_deployment.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-deploy-all",
  "title": "Alle Docker-Schritte ohne Rueckfragen ausrollen",
  "documented": true,
  "fields": [
    {
      "id": "targets",
      "label": "targets",
      "description": "Ausgewaehlte Inventory-Hosts/-Gruppen als --limit fuer bestehenden Docker-Ablauf.",
      "type": "array",
      "required": true,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--limit",
        "separator": ","
      },
      "completion": {
        "source": "inventory.targets"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/docker-deploy-all.json",
    "bin/control.d/docker-deploy-all.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-deploy-all.json": "179787ef9b0a276f74d61362e81ba5a905d3934ddd414c76c0e9240c6b72b999",
    "bin/control.d/docker-deploy-all.sh": "6b68ffcd6b2aad57fcc3dcad565edd6a59da0b9faa86347bf42acb61ae5634c1",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "Alle Docker-Schritte ohne Rueckfragen ausrollen",
      "description": "# Alle Docker-Schritte ohne Rueckfragen ausrollen\n\nAlle Docker-Schritte ohne Rueckfragen ausrollen\n\nAufruf: `bin/control docker-deploy-all [Optionen]`.\n\nVorhandene Kurzformen: `docker-deploy-all`.\n\nFeature: docker. Die aktuelle Aktivierung prueft weiterhin Control.\n\nDer vorhandene Ablauf bearbeitet die verwalteten Stacks der ausgewaehlten Hosts. Ein einzelner Stackfilter ist nicht behauptet. Vorhandene Rueckfragen zu Netzwerken, Benutzern und Waisen-Stacks bleiben aktiv.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/prepare_deployment.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/docker-deploy-all.json`\n- `bin/control.d/docker-deploy-all.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "targets": {
          "label": "targets",
          "description": "Ausgewaehlte Inventory-Hosts/-Gruppen als --limit fuer bestehenden Docker-Ablauf."
        }
      }
    },
    "en": {
      "title": "Run the full Docker deployment without prompts",
      "description": "# Run the full Docker deployment without prompts\n\nRun the full Docker deployment without prompts\n\nRun: `bin/control docker-deploy-all [options]`.\n\nAliases: `docker-deploy-all`.\n\nFeature: docker. Control checks availability at runtime.\n\nThe workflow processes managed stacks on the selected hosts. There is no documented single-stack filter. Existing confirmations for networks, users and orphaned stacks remain active.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/prepare_deployment.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/docker-deploy-all.json`\n- `bin/control.d/docker-deploy-all.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "targets": {
          "label": "Target hosts or groups",
          "description": "Pass the selected hosts or inventory groups to the existing Docker workflow as --limit."
        }
      }
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-deploy-all.json`
- `bin/control.d/docker-deploy-all.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
