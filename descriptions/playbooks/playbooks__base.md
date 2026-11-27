# Playbook playbooks/base.yml

Playbook: `playbooks/base.yml`.

Play and task names as written in the playbook:

- Apply the shared Linux baseline
- Check for a supported operating system

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/base.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/base.yml

Vorhandener Einstieg: `playbooks/base.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Apply the shared Linux baseline
- Check for a supported operating system

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/base.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/base.yml",
  "title": "Playbook playbooks/base.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/base.yml"
  ],
  "source_hashes": {
    "playbooks/base.yml": "c212a7d14461f1d1a95fb9c1869f7a0a50fbf348c0515cbad3d352e2fdba9ac4"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/base.yml",
      "description": "# Playbook playbooks/base.yml\n\nVorhandener Einstieg: `playbooks/base.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Apply the shared Linux baseline\n- Check for a supported operating system\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/base.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/base.yml",
      "description": "# Playbook playbooks/base.yml\n\nPlaybook: `playbooks/base.yml`.\n\nPlay and task names as written in the playbook:\n\n- Apply the shared Linux baseline\n- Check for a supported operating system\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/base.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
