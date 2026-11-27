# Playbook playbooks/checkmk/uninstall_agent.yml

Playbook: `playbooks/checkmk/uninstall_agent.yml`.

Play and task names as written in the playbook:

- Remove the Checkmk agent
- Stop the Checkmk agent socket if present
- Stop the Checkmk agent service if present
- Remove Checkmk agent packages
- Remove obsolete Checkmk agent directories
- Reload systemd
- Check whether the Checkmk agent is still installed
- Show the result

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/checkmk/uninstall_agent.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/checkmk/uninstall_agent.yml

Vorhandener Einstieg: `playbooks/checkmk/uninstall_agent.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Remove the Checkmk agent
- Stop the Checkmk agent socket if present
- Stop the Checkmk agent service if present
- Remove Checkmk agent packages
- Remove obsolete Checkmk agent directories
- Reload systemd
- Check whether the Checkmk agent is still installed
- Show the result

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/checkmk/uninstall_agent.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/checkmk/uninstall_agent.yml",
  "title": "Playbook playbooks/checkmk/uninstall_agent.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/checkmk/uninstall_agent.yml"
  ],
  "source_hashes": {
    "playbooks/checkmk/uninstall_agent.yml": "c32400ee3e86948724b83cd313584f91cfd36f82cd3b2322b5bb513861fc6d2c"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/checkmk/uninstall_agent.yml",
      "description": "# Playbook playbooks/checkmk/uninstall_agent.yml\n\nVorhandener Einstieg: `playbooks/checkmk/uninstall_agent.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Remove the Checkmk agent\n- Stop the Checkmk agent socket if present\n- Stop the Checkmk agent service if present\n- Remove Checkmk agent packages\n- Remove obsolete Checkmk agent directories\n- Reload systemd\n- Check whether the Checkmk agent is still installed\n- Show the result\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/checkmk/uninstall_agent.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/checkmk/uninstall_agent.yml",
      "description": "# Playbook playbooks/checkmk/uninstall_agent.yml\n\nPlaybook: `playbooks/checkmk/uninstall_agent.yml`.\n\nPlay and task names as written in the playbook:\n\n- Remove the Checkmk agent\n- Stop the Checkmk agent socket if present\n- Stop the Checkmk agent service if present\n- Remove Checkmk agent packages\n- Remove obsolete Checkmk agent directories\n- Reload systemd\n- Check whether the Checkmk agent is still installed\n- Show the result\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/checkmk/uninstall_agent.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
