# Playbook playbooks/docker/prepare_deployment.yml

Vorhandener Einstieg: `playbooks/docker/prepare_deployment.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Lokale Docker-Deployment-Struktur vorbereiten
- Mindestens ein Docker-Deployment-Ziel pruefen
- Lokales Basisverzeichnis anlegen
- Lokales Hostverzeichnis je Deployment-Ziel anlegen
- Remote Docker-Deployment-Struktur vorbereiten
- Remote Basisverzeichnis anlegen
- Docker und Compose-Verfuegbarkeit pruefen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

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
    "playbooks/docker/prepare_deployment.yml": "4f822703e1407cf4e5b82517ba55d9b0e1160db7a5bd4c46b9a0a0cae2bc5c84"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/prepare_deployment.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
