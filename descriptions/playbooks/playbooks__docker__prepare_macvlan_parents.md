# Playbook playbooks/docker/prepare_macvlan_parents.yml

Playbook: `playbooks/docker/prepare_macvlan_parents.yml`.

Play and task names as written in the playbook:

- Prepare Docker macvlan configuration networks
- Validate macvlan definitions
- Identify config-only macvlan networks
- Create missing config-only macvlan networks

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/docker/prepare_macvlan_parents.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/docker/prepare_macvlan_parents.yml

Vorhandener Einstieg: `playbooks/docker/prepare_macvlan_parents.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Prepare Docker macvlan configuration networks
- Validate macvlan definitions
- Identify config-only macvlan networks
- Create missing config-only macvlan networks

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/docker/prepare_macvlan_parents.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/prepare_macvlan_parents.yml",
  "title": "Playbook playbooks/docker/prepare_macvlan_parents.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/prepare_macvlan_parents.yml"
  ],
  "source_hashes": {
    "playbooks/docker/prepare_macvlan_parents.yml": "75ab4b436c1b008aa0afa793181cddc66c142f3014618cdf16bf3255af768d51"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/docker/prepare_macvlan_parents.yml",
      "description": "# Playbook playbooks/docker/prepare_macvlan_parents.yml\n\nVorhandener Einstieg: `playbooks/docker/prepare_macvlan_parents.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Prepare Docker macvlan configuration networks\n- Validate macvlan definitions\n- Identify config-only macvlan networks\n- Create missing config-only macvlan networks\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/docker/prepare_macvlan_parents.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/docker/prepare_macvlan_parents.yml",
      "description": "# Playbook playbooks/docker/prepare_macvlan_parents.yml\n\nPlaybook: `playbooks/docker/prepare_macvlan_parents.yml`.\n\nPlay and task names as written in the playbook:\n\n- Prepare Docker macvlan configuration networks\n- Validate macvlan definitions\n- Identify config-only macvlan networks\n- Create missing config-only macvlan networks\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/docker/prepare_macvlan_parents.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
