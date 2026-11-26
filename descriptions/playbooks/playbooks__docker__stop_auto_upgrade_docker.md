# Playbook playbooks/docker/stop_auto_upgrade_docker.yaml

Vorhandener Einstieg: `playbooks/docker/stop_auto_upgrade_docker.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Hold Docker package versions during unattended upgrades
- Hold Docker packages
- Reload the systemd manager

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
    "playbooks/docker/stop_auto_upgrade_docker.yaml": "f52779a36c1891fa0d65b6bad59952741b53ed1e021555a82cf7df8f3ea793fe"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/stop_auto_upgrade_docker.yaml",
      "description": "# Playbook playbooks/docker/stop_auto_upgrade_docker.yaml\n\nVorhandener Einstieg: `playbooks/docker/stop_auto_upgrade_docker.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Hold Docker package versions during unattended upgrades\n- Hold Docker packages\n- Reload the systemd manager\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/stop_auto_upgrade_docker.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/stop_auto_upgrade_docker.yaml",
      "description": "# Playbook playbooks/docker/stop_auto_upgrade_docker.yaml\n\nPlaybook: `playbooks/docker/stop_auto_upgrade_docker.yaml`.\n\nPlay and task names as written in the playbook:\n\n- Hold Docker package versions during unattended upgrades\n- Hold Docker packages\n- Reload the systemd manager\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/stop_auto_upgrade_docker.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/docker/stop_auto_upgrade_docker.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
