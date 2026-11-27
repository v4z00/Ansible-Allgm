# Playbook playbooks/docker/stop_all_docker.yaml

Playbook: `playbooks/docker/stop_all_docker.yaml`.

Play and task names as written in the playbook:

- PLAY 1: Stop all Docker Compose stacks
- TASK 1.1: List running Compose projects
- TASK 1.2: Stop running Compose projects
- TASK 1.3: Summarize the stopped stacks

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/docker/stop_all_docker.yaml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/docker/stop_all_docker.yaml

Vorhandener Einstieg: `playbooks/docker/stop_all_docker.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- PLAY 1: Stop all Docker Compose stacks
- TASK 1.1: List running Compose projects
- TASK 1.2: Stop running Compose projects
- TASK 1.3: Summarize the stopped stacks

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/docker/stop_all_docker.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/stop_all_docker.yaml",
  "title": "Playbook playbooks/docker/stop_all_docker.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/stop_all_docker.yaml"
  ],
  "source_hashes": {
    "playbooks/docker/stop_all_docker.yaml": "19bcb6e4617108c304aa3534404c2b2677d59f89a785412fc5eaf690fa60c603"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/stop_all_docker.yaml",
      "description": "# Playbook playbooks/docker/stop_all_docker.yaml\n\nVorhandener Einstieg: `playbooks/docker/stop_all_docker.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- PLAY 1: Stop all Docker Compose stacks\n- TASK 1.1: List running Compose projects\n- TASK 1.2: Stop running Compose projects\n- TASK 1.3: Summarize the stopped stacks\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/stop_all_docker.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/stop_all_docker.yaml",
      "description": "# Playbook playbooks/docker/stop_all_docker.yaml\n\nPlaybook: `playbooks/docker/stop_all_docker.yaml`.\n\nPlay and task names as written in the playbook:\n\n- PLAY 1: Stop all Docker Compose stacks\n- TASK 1.1: List running Compose projects\n- TASK 1.2: Stop running Compose projects\n- TASK 1.3: Summarize the stopped stacks\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/stop_all_docker.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
