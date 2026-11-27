# Playbook playbooks/maintenance/clear_postfix_que.yaml

Playbook: `playbooks/maintenance/clear_postfix_que.yaml`.

Play and task names as written in the playbook:

- Retry delivery of the Postfix queue
- Require an explicit target
- Check the feature flag
- Flush the queue

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/maintenance/clear_postfix_que.yaml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/maintenance/clear_postfix_que.yaml

Vorhandener Einstieg: `playbooks/maintenance/clear_postfix_que.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Retry delivery of the Postfix queue
- Require an explicit target
- Check the feature flag
- Flush the queue

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/maintenance/clear_postfix_que.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/clear_postfix_que.yaml",
  "title": "Playbook playbooks/maintenance/clear_postfix_que.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/clear_postfix_que.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/clear_postfix_que.yaml": "1b46b6b0dfdd8c40c65f81f44f9446236e710a326afc668e05d1e71ae71318c7"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/maintenance/clear_postfix_que.yaml",
      "description": "# Playbook playbooks/maintenance/clear_postfix_que.yaml\n\nVorhandener Einstieg: `playbooks/maintenance/clear_postfix_que.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Retry delivery of the Postfix queue\n- Require an explicit target\n- Check the feature flag\n- Flush the queue\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/maintenance/clear_postfix_que.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/maintenance/clear_postfix_que.yaml",
      "description": "# Playbook playbooks/maintenance/clear_postfix_que.yaml\n\nPlaybook: `playbooks/maintenance/clear_postfix_que.yaml`.\n\nPlay and task names as written in the playbook:\n\n- Retry delivery of the Postfix queue\n- Require an explicit target\n- Check the feature flag\n- Flush the queue\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/maintenance/clear_postfix_que.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
