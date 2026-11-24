# Playbook playbooks/docker/check_docker.yml

Vorhandener Einstieg: `playbooks/docker/check_docker.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker-Quellen und vorhandene Netzwerke nur lesend pruefen
- Netzwerkdefinitionen pruefen
- Compose-Quellen auf dem Controller pruefen ohne Konfiguration auszugeben
- Ausschliesslich bereinigte Pruefergebnisse anzeigen
- Compose-Pruefung muss erfolgreich sein
- Tatsächliche Docker-Netze mit dem Soll vergleichen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/check_docker.yml",
  "title": "Playbook playbooks/docker/check_docker.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/check_docker.yml"
  ],
  "source_hashes": {
    "playbooks/docker/check_docker.yml": "c7984855179dc0e6ab62908b3261b02f1dfd63f506eb1582905d2fc2bd9fa915"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/check_docker.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
