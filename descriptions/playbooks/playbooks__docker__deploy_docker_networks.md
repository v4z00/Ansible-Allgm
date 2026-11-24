# Playbook playbooks/docker/deploy_docker_networks.yaml

Vorhandener Einstieg: `playbooks/docker/deploy_docker_networks.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker-Netzwerke aus host_vars verwalten
- Netzwerkdefinitionen vor jeder Aenderung pruefen
- Docker-Netzwerke anlegen oder aktualisieren
- {{ item.name }}
- Explizit entfernte Docker-Netzwerke loeschen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/deploy_docker_networks.yaml",
  "title": "Playbook playbooks/docker/deploy_docker_networks.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/deploy_docker_networks.yaml"
  ],
  "source_hashes": {
    "playbooks/docker/deploy_docker_networks.yaml": "8f6244906342b88ce6f6c548d93df2908590a038cd6dc10a1f4c662b535e4020"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/deploy_docker_networks.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
