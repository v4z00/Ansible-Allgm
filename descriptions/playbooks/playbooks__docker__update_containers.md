# Playbook playbooks/docker/update_containers.yml

Playbook: `playbooks/docker/update_containers.yml`.

Play and task names as written in the playbook:

- Docker Container Updates (Ansible Watchtower)
- Clean Summary File
- Find Docker Compose Files
- Require Compose files for the mandatory check
- Pull registry images with bounded retries before changing containers
- Build locally defined images before changing containers
- Update containers and wait for running or healthy services
- Record changed stacks in the update report
- Prune Images and Log
- Fetch Report to Management Server
- Check Docker sources and networks on the updated hosts
- Run the site-specific Portainer check

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/docker/update_containers.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Registry retries and local builds

Registry images are pulled first with bounded retries and a 20-second delay. COMPOSE_PARALLEL_LIMIT=1 limits simultaneous pulls per stack. Buildable images are excluded from that pull; Docker Compose then builds local images with --pull before up --no-build --pull never --wait. A failed pull or build prevents container changes for that host. The existing mandatory source/network and container-health checks remain. Set the boolean docker_compose_build: false in local host/group variables to disable builds explicitly; default true. Build output stays hidden because it may contain private build arguments.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/docker/update_containers.yml

Vorhandener Einstieg: `playbooks/docker/update_containers.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker Container Updates (Ansible Watchtower)
- Clean Summary File
- Find Docker Compose Files
- Require Compose files for the mandatory check
- Pull registry images with bounded retries before changing containers
- Build locally defined images before changing containers
- Update containers and wait for running or healthy services
- Record changed stacks in the update report
- Prune Images and Log
- Fetch Report to Management Server
- Check Docker sources and networks on the updated hosts
- Run the site-specific Portainer check

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/docker/update_containers.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

## Image-Abruf und lokale Builds

Registry-Images werden zuerst mit begrenzten Wiederholungen und 20 Sekunden Abstand abgerufen. COMPOSE_PARALLEL_LIMIT=1 begrenzt parallele Abrufe je Stack. Lokal baubare Images werden dabei ausgelassen; anschließend baut Compose sie mit --pull, bevor up --no-build --pull never --wait startet. Ein fehlgeschlagener Abruf oder Build verhindert die Containerumstellung dieses Hosts. Quell-/Netzprüfungen und Container-Healthchecks bleiben verpflichtend. Der boolesche Host-/Gruppenwert docker_compose_build: false schaltet Builds ausdrücklich ab; Standard ist true. Build-Ausgaben bleiben wegen möglicher privater Build-Argumente verborgen.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/update_containers.yml",
  "title": "Playbook playbooks/docker/update_containers.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/update_containers.yml"
  ],
  "source_hashes": {
    "playbooks/docker/update_containers.yml": "e066d2bb216623960332be7d82b20505011daa4630617e23c01a18ca923e9147"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/update_containers.yml",
      "description": "# Playbook playbooks/docker/update_containers.yml\n\nVorhandener Einstieg: `playbooks/docker/update_containers.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Docker Container Updates (Ansible Watchtower)\n- Clean Summary File\n- Find Docker Compose Files\n- Require Compose files for the mandatory check\n- Pull registry images with bounded retries before changing containers\n- Build locally defined images before changing containers\n- Update containers and wait for running or healthy services\n- Record changed stacks in the update report\n- Prune Images and Log\n- Fetch Report to Management Server\n- Check Docker sources and networks on the updated hosts\n- Run the site-specific Portainer check\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/update_containers.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n## Image-Abruf und lokale Builds\n\nRegistry-Images werden zuerst mit begrenzten Wiederholungen und 20 Sekunden Abstand abgerufen. COMPOSE_PARALLEL_LIMIT=1 begrenzt parallele Abrufe je Stack. Lokal baubare Images werden dabei ausgelassen; anschließend baut Compose sie mit --pull, bevor up --no-build --pull never --wait startet. Ein fehlgeschlagener Abruf oder Build verhindert die Containerumstellung dieses Hosts. Quell-/Netzprüfungen und Container-Healthchecks bleiben verpflichtend. Der boolesche Host-/Gruppenwert docker_compose_build: false schaltet Builds ausdrücklich ab; Standard ist true. Build-Ausgaben bleiben wegen möglicher privater Build-Argumente verborgen.\n",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/update_containers.yml",
      "description": "# Playbook playbooks/docker/update_containers.yml\n\nPlaybook: `playbooks/docker/update_containers.yml`.\n\nPlay and task names as written in the playbook:\n\n- Docker Container Updates (Ansible Watchtower)\n- Clean Summary File\n- Find Docker Compose Files\n- Require Compose files for the mandatory check\n- Pull registry images with bounded retries before changing containers\n- Build locally defined images before changing containers\n- Update containers and wait for running or healthy services\n- Record changed stacks in the update report\n- Prune Images and Log\n- Fetch Report to Management Server\n- Check Docker sources and networks on the updated hosts\n- Run the site-specific Portainer check\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/update_containers.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Registry retries and local builds\n\nRegistry images are pulled first with bounded retries and a 20-second delay. COMPOSE_PARALLEL_LIMIT=1 limits simultaneous pulls per stack. Buildable images are excluded from that pull; Docker Compose then builds local images with --pull before up --no-build --pull never --wait. A failed pull or build prevents container changes for that host. The existing mandatory source/network and container-health checks remain. Set the boolean docker_compose_build: false in local host/group variables to disable builds explicitly; default true. Build output stays hidden because it may contain private build arguments.\n",
      "fields": {}
    }
  }
}
```
</details>
