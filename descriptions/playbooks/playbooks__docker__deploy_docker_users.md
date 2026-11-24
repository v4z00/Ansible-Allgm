# Playbook playbooks/docker/deploy_docker_users.yml

Vorhandener Einstieg: `playbooks/docker/deploy_docker_users.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker-Service-User aus host_vars verwalten
- Freigegebene Service-User validieren
- Doppelte freigegebene UIDs verhindern
- Primaergruppen der Docker-Service-User anlegen
- {{ item.name }}
- Docker-Service-User anlegen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/deploy_docker_users.yml",
  "title": "Playbook playbooks/docker/deploy_docker_users.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/deploy_docker_users.yml"
  ],
  "source_hashes": {
    "playbooks/docker/deploy_docker_users.yml": "868e212e6db7f4deb3c8f20835e1ab9c8b9f2d2c632e9db0116f394d2cafac79"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/deploy_docker_users.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
