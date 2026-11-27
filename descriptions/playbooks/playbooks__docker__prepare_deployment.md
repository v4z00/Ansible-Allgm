# Playbook playbooks/docker/prepare_deployment.yml

Playbook: `playbooks/docker/prepare_deployment.yml`.

Play and task names as written in the playbook:

- Prepare local Docker deployment directories
- Require at least one Docker deployment target
- Create the local base directory
- Create a local host directory for each deployment target
- Prepare remote Docker deployment directories
- Create the remote base directory
- Check Docker and Compose availability

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/docker/prepare_deployment.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/docker/prepare_deployment.yml

Vorhandener Einstieg: `playbooks/docker/prepare_deployment.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Prepare local Docker deployment directories
- Require at least one Docker deployment target
- Create the local base directory
- Create a local host directory for each deployment target
- Prepare remote Docker deployment directories
- Create the remote base directory
- Check Docker and Compose availability

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/docker/prepare_deployment.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/prepare_deployment.yml",
  "title": "Playbook playbooks/docker/prepare_deployment.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/prepare_deployment.yml"
  ],
  "source_hashes": {
    "playbooks/docker/prepare_deployment.yml": "8b38a93c4b8e9a40b94329d49492846e5450154620f4621ff6130e95379e2edc"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/prepare_deployment.yml",
      "description": "# Playbook playbooks/docker/prepare_deployment.yml\n\nVorhandener Einstieg: `playbooks/docker/prepare_deployment.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Prepare local Docker deployment directories\n- Require at least one Docker deployment target\n- Create the local base directory\n- Create a local host directory for each deployment target\n- Prepare remote Docker deployment directories\n- Create the remote base directory\n- Check Docker and Compose availability\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/prepare_deployment.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/prepare_deployment.yml",
      "description": "# Playbook playbooks/docker/prepare_deployment.yml\n\nPlaybook: `playbooks/docker/prepare_deployment.yml`.\n\nPlay and task names as written in the playbook:\n\n- Prepare local Docker deployment directories\n- Require at least one Docker deployment target\n- Create the local base directory\n- Create a local host directory for each deployment target\n- Prepare remote Docker deployment directories\n- Create the remote base directory\n- Check Docker and Compose availability\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/prepare_deployment.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
