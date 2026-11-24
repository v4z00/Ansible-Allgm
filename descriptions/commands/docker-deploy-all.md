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
    "lib/control/helpers.sh": "8f1be83385316cb375b5c070c53f47e5d2d9da958621836da96530bbb2a4038c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/docker-deploy-all.json`
- `bin/control.d/docker-deploy-all.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
