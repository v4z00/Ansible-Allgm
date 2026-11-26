# Playbook playbooks/docker/check_docker.yml

Vorhandener Einstieg: `playbooks/docker/check_docker.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Inspect Docker sources and existing networks
- Validate network definitions
- Check Compose sources on the controller without displaying configuration
- Show sanitized check results
- Require successful Compose validation
- Compare actual Docker networks with their definitions

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
    "playbooks/docker/check_docker.yml": "536aee9cb37c8181b0782f4ea0ce5b35ffada00edb79f456ca28cbfcdea58f87"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/check_docker.yml",
      "description": "# Playbook playbooks/docker/check_docker.yml\n\nVorhandener Einstieg: `playbooks/docker/check_docker.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Inspect Docker sources and existing networks\n- Validate network definitions\n- Check Compose sources on the controller without displaying configuration\n- Show sanitized check results\n- Require successful Compose validation\n- Compare actual Docker networks with their definitions\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/check_docker.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/check_docker.yml",
      "description": "# Playbook playbooks/docker/check_docker.yml\n\nPlaybook: `playbooks/docker/check_docker.yml`.\n\nPlay and task names as written in the playbook:\n\n- Inspect Docker sources and existing networks\n- Validate network definitions\n- Check Compose sources on the controller without displaying configuration\n- Show sanitized check results\n- Require successful Compose validation\n- Compare actual Docker networks with their definitions\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/check_docker.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/docker/check_docker.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
