# Playbook playbooks/docker/update_containers.yml

Vorhandener Einstieg: `playbooks/docker/update_containers.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker Container Updates (Ansible Watchtower)
- Clean Summary File
- Find Docker Compose Files
- Require Compose files for the mandatory check
- Update images and wait for running or healthy services
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
    "playbooks/docker/update_containers.yml": "5032c4ae4bded8b5fd8aeae85ee0bc473993ed5727d20c2870c0a12f22ba5c61"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/update_containers.yml",
      "description": "# Playbook playbooks/docker/update_containers.yml\n\nVorhandener Einstieg: `playbooks/docker/update_containers.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Docker Container Updates (Ansible Watchtower)\n- Clean Summary File\n- Find Docker Compose Files\n- Require Compose files for the mandatory check\n- Update images and wait for running or healthy services\n- Record changed stacks in the update report\n- Prune Images and Log\n- Fetch Report to Management Server\n- Check Docker sources and networks on the updated hosts\n- Run the site-specific Portainer check\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/update_containers.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/update_containers.yml",
      "description": "# Playbook playbooks/docker/update_containers.yml\n\nPlaybook: `playbooks/docker/update_containers.yml`.\n\nPlay and task names as written in the playbook:\n\n- Docker Container Updates (Ansible Watchtower)\n- Clean Summary File\n- Find Docker Compose Files\n- Require Compose files for the mandatory check\n- Update images and wait for running or healthy services\n- Record changed stacks in the update report\n- Prune Images and Log\n- Fetch Report to Management Server\n- Check Docker sources and networks on the updated hosts\n- Run the site-specific Portainer check\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/update_containers.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/docker/update_containers.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
