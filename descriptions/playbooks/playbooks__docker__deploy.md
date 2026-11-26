# Playbook playbooks/docker/deploy.yml

Vorhandener Einstieg: `playbooks/docker/deploy.yml`.

Das Playbook importiert in dieser Reihenfolge.

- `playbooks/docker/prepare_deployment.yml`
- `playbooks/docker/deploy_docker_users.yml`
- `playbooks/docker/deploy_docker_networks.yaml`
- `playbooks/docker/deploy_docker_stacks.yml`

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/deploy.yml",
  "title": "Playbook playbooks/docker/deploy.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/deploy.yml"
  ],
  "source_hashes": {
    "playbooks/docker/deploy.yml": "2078ad5c8b19ca522c0ec2d2be03287efd2a2cac7d967fa183e6ad21f550a4da"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/deploy.yml",
      "description": "# Playbook playbooks/docker/deploy.yml\n\nVorhandener Einstieg: `playbooks/docker/deploy.yml`.\n\nDas Playbook importiert in dieser Reihenfolge.\n\n- `playbooks/docker/prepare_deployment.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/deploy.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/deploy.yml",
      "description": "# Playbook playbooks/docker/deploy.yml\n\nPlaybook: `playbooks/docker/deploy.yml`.\n\nThe playbook imports the following files in order.\n\n- `playbooks/docker/prepare_deployment.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/deploy.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/docker/deploy.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
