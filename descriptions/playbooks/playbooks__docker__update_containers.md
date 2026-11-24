# Playbook playbooks/docker/update_containers.yml

Vorhandener Einstieg: `playbooks/docker/update_containers.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker Container Updates (Ansible Watchtower)
- Clean Summary File
- Find Docker Compose Files
- Pro Stack die Images aktualisieren und bis zu 180 Sekunden auf laufende bzw. gesunde Dienste warten
- Fehler beim Start oder Healthcheck als fehlgeschlagenes Update melden
- Prune Images and Log
- Fetch Report to Management Server
- Docker-Quellen und Netze prüfen
- Portainer-TCP-Test für ausdrücklich aktivierte Hosts ausführen

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
    "playbooks/docker/update_containers.yml": "513144530ef76378ae40c8757d9375546bab2e3350989650bc620b6859e7b309"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/update_containers.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
