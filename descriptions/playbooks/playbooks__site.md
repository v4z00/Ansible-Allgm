# Playbook playbooks/site.yml

Playbook: `playbooks/site.yml`.

The playbook imports the following files in order.

- `playbooks/base.yml`
- `playbooks/checkmk.yml`
- `playbooks/optional.yml`
- `playbooks/lynis.yml`

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/site.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/site.yml

Vorhandener Einstieg: `playbooks/site.yml`.

Das Playbook importiert in dieser Reihenfolge.

- `playbooks/base.yml`
- `playbooks/checkmk.yml`
- `playbooks/optional.yml`
- `playbooks/lynis.yml`

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/site.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/site.yml",
  "title": "Playbook playbooks/site.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/site.yml"
  ],
  "source_hashes": {
    "playbooks/site.yml": "a1370917868ac4cb7aa2118cf0211e6d21a817d6d13fc41793bf079d1b48d325"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/site.yml",
      "description": "# Playbook playbooks/site.yml\n\nVorhandener Einstieg: `playbooks/site.yml`.\n\nDas Playbook importiert in dieser Reihenfolge.\n\n- `playbooks/base.yml`\n- `playbooks/checkmk.yml`\n- `playbooks/optional.yml`\n- `playbooks/lynis.yml`\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/site.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/site.yml",
      "description": "# Playbook playbooks/site.yml\n\nPlaybook: `playbooks/site.yml`.\n\nThe playbook imports the following files in order.\n\n- `playbooks/base.yml`\n- `playbooks/checkmk.yml`\n- `playbooks/optional.yml`\n- `playbooks/lynis.yml`\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/site.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
