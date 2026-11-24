# Playbook playbooks/docker/get_docker_ips.yaml

Vorhandener Einstieg: `playbooks/docker/get_docker_ips.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Audit Docker Networks and IPs with Service Mapping
- Suche nach Netzwerken mit Dateizuordnung
- Suche nach statischen IPs mit Dateizuordnung
- Suche nach Host-Bindungen (Ports) mit Dateizuordnung
- Ausgabe der Ergebnisse

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/get_docker_ips.yaml",
  "title": "Playbook playbooks/docker/get_docker_ips.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/get_docker_ips.yaml"
  ],
  "source_hashes": {
    "playbooks/docker/get_docker_ips.yaml": "817c3dce8d875fb24ab47364e7d050629933f8c28932a9edbd06e61c73d2e695"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/get_docker_ips.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
