# Playbook playbooks/docker/stop_auto_upgrade_docker.yaml

Vorhandener Einstieg: `playbooks/docker/stop_auto_upgrade_docker.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Lock Docker versions to prevent unattended-upgrades chaos
- Freeze Docker packages (set to hold)
- {{ item }}
- Ensure systemd is completely sane

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/stop_auto_upgrade_docker.yaml",
  "title": "Playbook playbooks/docker/stop_auto_upgrade_docker.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/stop_auto_upgrade_docker.yaml"
  ],
  "source_hashes": {
    "playbooks/docker/stop_auto_upgrade_docker.yaml": "088802adc2904b31970d8e555c94e2d417aa398dd37d583c0d263c0073e17409"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/stop_auto_upgrade_docker.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
