# Playbook playbooks/docker/update_containers.yml

Vorhandener Einstieg: `playbooks/docker/update_containers.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker Container Updates (Ansible Watchtower)
- Clean Summary File
- Find Docker Compose Files
- Check and Update
- Prune Images and Log
- Fetch Report to Management Server

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
    "playbooks/docker/update_containers.yml": "d0a7b2e6df7cafc3921fb6672943eeaa87992c3c31c95d34267b7f435865aa0a"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/update_containers.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
