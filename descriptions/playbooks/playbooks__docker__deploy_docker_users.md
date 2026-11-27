# Playbook playbooks/docker/deploy_docker_users.yml

Playbook: `playbooks/docker/deploy_docker_users.yml`.

Play and task names as written in the playbook:

- Manage Docker service accounts from host_vars
- Validate approved service accounts
- Reject duplicate UIDs among approved accounts
- Create primary groups for Docker service accounts
- Create Docker service accounts

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/docker/deploy_docker_users.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/docker/deploy_docker_users.yml

Vorhandener Einstieg: `playbooks/docker/deploy_docker_users.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Manage Docker service accounts from host_vars
- Validate approved service accounts
- Reject duplicate UIDs among approved accounts
- Create primary groups for Docker service accounts
- Create Docker service accounts

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/docker/deploy_docker_users.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/deploy_docker_users.yml",
  "title": "Playbook playbooks/docker/deploy_docker_users.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/deploy_docker_users.yml"
  ],
  "source_hashes": {
    "playbooks/docker/deploy_docker_users.yml": "5e1b7f71434e57d1645d093540753a0ae406f63afcb3396102bd41998599229d"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/deploy_docker_users.yml",
      "description": "# Playbook playbooks/docker/deploy_docker_users.yml\n\nVorhandener Einstieg: `playbooks/docker/deploy_docker_users.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Manage Docker service accounts from host_vars\n- Validate approved service accounts\n- Reject duplicate UIDs among approved accounts\n- Create primary groups for Docker service accounts\n- Create Docker service accounts\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/deploy_docker_users.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/deploy_docker_users.yml",
      "description": "# Playbook playbooks/docker/deploy_docker_users.yml\n\nPlaybook: `playbooks/docker/deploy_docker_users.yml`.\n\nPlay and task names as written in the playbook:\n\n- Manage Docker service accounts from host_vars\n- Validate approved service accounts\n- Reject duplicate UIDs among approved accounts\n- Create primary groups for Docker service accounts\n- Create Docker service accounts\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/deploy_docker_users.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
