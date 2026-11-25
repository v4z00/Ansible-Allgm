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
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-deploy.json`
- `bin/control.d/docker-deploy.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
