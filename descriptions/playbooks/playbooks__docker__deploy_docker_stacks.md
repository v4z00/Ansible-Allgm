# Playbook playbooks/docker/deploy_docker_stacks.yml

Vorhandener Einstieg: `playbooks/docker/deploy_docker_stacks.yml`.

Im Quelltext benannte Plays/Aufgaben:

- PLAY 1: Prepare the deployment
- TASK 1.1: Initialize deployment results
- TASK 1.2: Validate base variables
- PLAY 2: Find unmanaged Docker stacks
- TASK 2.1: Find managed Compose files for this host on the controller
- TASK 2.2: Collect managed Compose project names
- TASK 2.3: List running Compose projects on the host
- TASK 2.4: Parse running Compose projects
- TASK 2.5: Initialize orphan stack candidates
- TASK 2.6: Collect orphan stacks by project name
- TASK 2.7: Show orphan stack candidates
- PLAY 2.5: Confirm orphan stack removal on the controller
- TASK 2.5.1: Count orphan stack candidates across hosts
- TASK 2.5.2: Ask for confirmation before removing orphan stacks
- TASK 2.5.3: Record the global prune decision
- PLAY 2.6: Remove confirmed orphan stacks
- TASK 2.6.1: Remove orphan stacks
- TASK 2.6.2: Record the cleanup result
- TASK 2.6.3: Show the stacks removed
- PLAY 3: Synchronize configuration
- TASK 3.1: Create the target directory
- TASK 3.2: Synchronize project directories
- TASK 3.3: Find Compose projects on the target host
- TASK 3.4: Check whether any Compose projects were found
- PLAY 4: Set file permissions from host_vars before deployment
- TASK 4.1: Validate file rules
- TASK 4.2: Check target paths
- TASK 4.3: Apply configured file permissions
- PLAY 6: Deploy Docker stacks
- TASK 6.1: Select critical Compose projects
- TASK 6.2: Select standard Compose projects
- TASK 6.3: Deploy critical stacks
- TASK 6.4: Wait for base services
- TASK 6.5: Deploy standard stacks
- TASK 6.6: Combine deployment results
- PLAY 7: Check container health
- TASK 7.1: Read Compose files
- TASK 7.2: Determine expected container names
- TASK 7.3: Report when no explicit container names are configured
- TASK 7.4: Wait for all explicitly named containers to start
- TASK 7.5: Record container status
- TASK 7.6: Show unhealthy or missing containers
- PLAY 8: Aggregate results across hosts
- TASK 8.1: Collect deployment results from all hosts
- PLAY 9: Write the deployment summary and log
- TASK 9.1: Create the log directory
- TASK 9.2: Generate the deployment summary
- TASK 9.3: Display the deployment summary and wait for acknowledgement

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/deploy_docker_stacks.yml",
  "title": "Playbook playbooks/docker/deploy_docker_stacks.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/deploy_docker_stacks.yml"
  ],
  "source_hashes": {
    "playbooks/docker/deploy_docker_stacks.yml": "a578cd0d88885ac0d4415a1fd14f3dbdebc64396354bc228331f2488f78bbf6c"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/deploy_docker_stacks.yml",
      "description": "# Playbook playbooks/docker/deploy_docker_stacks.yml\n\nVorhandener Einstieg: `playbooks/docker/deploy_docker_stacks.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- PLAY 1: Prepare the deployment\n- TASK 1.1: Initialize deployment results\n- TASK 1.2: Validate base variables\n- PLAY 2: Find unmanaged Docker stacks\n- TASK 2.1: Find managed Compose files for this host on the controller\n- TASK 2.2: Collect managed Compose project names\n- TASK 2.3: List running Compose projects on the host\n- TASK 2.4: Parse running Compose projects\n- TASK 2.5: Initialize orphan stack candidates\n- TASK 2.6: Collect orphan stacks by project name\n- TASK 2.7: Show orphan stack candidates\n- PLAY 2.5: Confirm orphan stack removal on the controller\n- TASK 2.5.1: Count orphan stack candidates across hosts\n- TASK 2.5.2: Ask for confirmation before removing orphan stacks\n- TASK 2.5.3: Record the global prune decision\n- PLAY 2.6: Remove confirmed orphan stacks\n- TASK 2.6.1: Remove orphan stacks\n- TASK 2.6.2: Record the cleanup result\n- TASK 2.6.3: Show the stacks removed\n- PLAY 3: Synchronize configuration\n- TASK 3.1: Create the target directory\n- TASK 3.2: Synchronize project directories\n- TASK 3.3: Find Compose projects on the target host\n- TASK 3.4: Check whether any Compose projects were found\n- PLAY 4: Set file permissions from host_vars before deployment\n- TASK 4.1: Validate file rules\n- TASK 4.2: Check target paths\n- TASK 4.3: Apply configured file permissions\n- PLAY 6: Deploy Docker stacks\n- TASK 6.1: Select critical Compose projects\n- TASK 6.2: Select standard Compose projects\n- TASK 6.3: Deploy critical stacks\n- TASK 6.4: Wait for base services\n- TASK 6.5: Deploy standard stacks\n- TASK 6.6: Combine deployment results\n- PLAY 7: Check container health\n- TASK 7.1: Read Compose files\n- TASK 7.2: Determine expected container names\n- TASK 7.3: Report when no explicit container names are configured\n- TASK 7.4: Wait for all explicitly named containers to start\n- TASK 7.5: Record container status\n- TASK 7.6: Show unhealthy or missing containers\n- PLAY 8: Aggregate results across hosts\n- TASK 8.1: Collect deployment results from all hosts\n- PLAY 9: Write the deployment summary and log\n- TASK 9.1: Create the log directory\n- TASK 9.2: Generate the deployment summary\n- TASK 9.3: Display the deployment summary and wait for acknowledgement\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/deploy_docker_stacks.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/deploy_docker_stacks.yml",
      "description": "# Playbook playbooks/docker/deploy_docker_stacks.yml\n\nPlaybook: `playbooks/docker/deploy_docker_stacks.yml`.\n\nPlay and task names as written in the playbook:\n\n- PLAY 1: Prepare the deployment\n- TASK 1.1: Initialize deployment results\n- TASK 1.2: Validate base variables\n- PLAY 2: Find unmanaged Docker stacks\n- TASK 2.1: Find managed Compose files for this host on the controller\n- TASK 2.2: Collect managed Compose project names\n- TASK 2.3: List running Compose projects on the host\n- TASK 2.4: Parse running Compose projects\n- TASK 2.5: Initialize orphan stack candidates\n- TASK 2.6: Collect orphan stacks by project name\n- TASK 2.7: Show orphan stack candidates\n- PLAY 2.5: Confirm orphan stack removal on the controller\n- TASK 2.5.1: Count orphan stack candidates across hosts\n- TASK 2.5.2: Ask for confirmation before removing orphan stacks\n- TASK 2.5.3: Record the global prune decision\n- PLAY 2.6: Remove confirmed orphan stacks\n- TASK 2.6.1: Remove orphan stacks\n- TASK 2.6.2: Record the cleanup result\n- TASK 2.6.3: Show the stacks removed\n- PLAY 3: Synchronize configuration\n- TASK 3.1: Create the target directory\n- TASK 3.2: Synchronize project directories\n- TASK 3.3: Find Compose projects on the target host\n- TASK 3.4: Check whether any Compose projects were found\n- PLAY 4: Set file permissions from host_vars before deployment\n- TASK 4.1: Validate file rules\n- TASK 4.2: Check target paths\n- TASK 4.3: Apply configured file permissions\n- PLAY 6: Deploy Docker stacks\n- TASK 6.1: Select critical Compose projects\n- TASK 6.2: Select standard Compose projects\n- TASK 6.3: Deploy critical stacks\n- TASK 6.4: Wait for base services\n- TASK 6.5: Deploy standard stacks\n- TASK 6.6: Combine deployment results\n- PLAY 7: Check container health\n- TASK 7.1: Read Compose files\n- TASK 7.2: Determine expected container names\n- TASK 7.3: Report when no explicit container names are configured\n- TASK 7.4: Wait for all explicitly named containers to start\n- TASK 7.5: Record container status\n- TASK 7.6: Show unhealthy or missing containers\n- PLAY 8: Aggregate results across hosts\n- TASK 8.1: Collect deployment results from all hosts\n- PLAY 9: Write the deployment summary and log\n- TASK 9.1: Create the log directory\n- TASK 9.2: Generate the deployment summary\n- TASK 9.3: Display the deployment summary and wait for acknowledgement\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/deploy_docker_stacks.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/docker/deploy_docker_stacks.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
