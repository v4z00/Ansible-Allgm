# Docker vorbereiten, Benutzer/Netze/Stacks ausrollen

Docker vorbereiten, Benutzer/Netze/Stacks ausrollen

Aufruf: `bin/control docker-deploy [Optionen]`.

Vorhandene Kurzformen: `docker-push`, `docker-deploy`.

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
  "ref": "docker-deploy",
  "title": "Docker vorbereiten, Benutzer/Netze/Stacks ausrollen",
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
    "bin/control.d/docker-deploy.json",
    "bin/control.d/docker-deploy.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-deploy.json": "7a71493fdf5f867af79ce6c97bcc8b2d5ace45bfb2cba7bb95766ffaac9dcbec",
    "bin/control.d/docker-deploy.sh": "fe6f9551e3f43115d7797caef6f764c82c2b0f4293b32e238a78a420c80fb92d",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "Docker vorbereiten, Benutzer/Netze/Stacks ausrollen",
      "description": "# Docker vorbereiten, Benutzer/Netze/Stacks ausrollen\n\nDocker vorbereiten, Benutzer/Netze/Stacks ausrollen\n\nAufruf: `bin/control docker-deploy [Optionen]`.\n\nVorhandene Kurzformen: `docker-push`, `docker-deploy`.\n\nFeature: docker. Die aktuelle Aktivierung prueft weiterhin Control.\n\nDer vorhandene Ablauf bearbeitet die verwalteten Stacks der ausgewaehlten Hosts. Ein einzelner Stackfilter ist nicht behauptet. Vorhandene Rueckfragen zu Netzwerken, Benutzern und Waisen-Stacks bleiben aktiv.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/prepare_deployment.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/docker-deploy.json`\n- `bin/control.d/docker-deploy.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "targets": {
          "label": "targets",
          "description": "Ausgewaehlte Inventory-Hosts/-Gruppen als --limit fuer bestehenden Docker-Ablauf."
        }
      }
    },
    "en": {
      "title": "Prepare Docker and deploy users, networks and stacks",
      "description": "# Prepare Docker and deploy users, networks and stacks\n\nPrepare Docker and deploy users, networks and stacks\n\nRun: `bin/control docker-deploy [options]`.\n\nAliases: `docker-push`, `docker-deploy`.\n\nFeature: docker. Control checks availability at runtime.\n\nThe workflow processes managed stacks on the selected hosts. There is no documented single-stack filter. Existing confirmations for networks, users and orphaned stacks remain active.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/prepare_deployment.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/docker-deploy.json`\n- `bin/control.d/docker-deploy.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
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

- `bin/control.d/docker-deploy.json`
- `bin/control.d/docker-deploy.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
