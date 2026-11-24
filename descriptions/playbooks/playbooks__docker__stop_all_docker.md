# Playbook playbooks/docker/stop_all_docker.yaml

Vorhandener Einstieg: `playbooks/docker/stop_all_docker.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- PLAY 1: Alle Docker Compose Stacks stoppen
- TASK 1.1: Alle laufenden Compose-Projekte abrufen
- TASK 1.2: Stacks stoppen (Finale, robuste Korrektur)
- TASK 1.3: Zusammenfassung der Stopp-Aktion

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

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
    "playbooks/docker/stop_all_docker.yaml": "8065e4db34bdebfafc6cf500bf29562052c7ca4fdfb6371c192f573180b272ff"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/stop_all_docker.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
