# Playbook playbooks/network/snmp_check.yml

Playbook: `playbooks/network/snmp_check.yml`.

Play and task names as written in the playbook:

- Check SNMP access to network devices
- Check the SNMP client on the controller
- Prompt privately for the missing SNMPv2 community
- Set the SNMPv2 community for this test
- Validate SNMP settings
- Test the SNMPv2 connection
- Classify the SNMPv2 access failure
- Test the SNMPv3 connection
- Classify the SNMPv3 access failure
- Report successful SNMP access

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/network/snmp_check.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/network/snmp_check.yml

Vorhandener Einstieg: `playbooks/network/snmp_check.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Check SNMP access to network devices
- Check the SNMP client on the controller
- Prompt privately for the missing SNMPv2 community
- Set the SNMPv2 community for this test
- Validate SNMP settings
- Test the SNMPv2 connection
- Classify the SNMPv2 access failure
- Test the SNMPv3 connection
- Classify the SNMPv3 access failure
- Report successful SNMP access

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/network/snmp_check.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/network/snmp_check.yml",
  "title": "Playbook playbooks/network/snmp_check.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/network/snmp_check.yml"
  ],
  "source_hashes": {
    "playbooks/network/snmp_check.yml": "ce6e38e4323e7c947302e6253a60d67861c6e4eafb60a5d3d81b4dcdb60ad507"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/network/snmp_check.yml",
      "description": "# Playbook playbooks/network/snmp_check.yml\n\nVorhandener Einstieg: `playbooks/network/snmp_check.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Check SNMP access to network devices\n- Check the SNMP client on the controller\n- Prompt privately for the missing SNMPv2 community\n- Set the SNMPv2 community for this test\n- Validate SNMP settings\n- Test the SNMPv2 connection\n- Classify the SNMPv2 access failure\n- Test the SNMPv3 connection\n- Classify the SNMPv3 access failure\n- Report successful SNMP access\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/network/snmp_check.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/network/snmp_check.yml",
      "description": "# Playbook playbooks/network/snmp_check.yml\n\nPlaybook: `playbooks/network/snmp_check.yml`.\n\nPlay and task names as written in the playbook:\n\n- Check SNMP access to network devices\n- Check the SNMP client on the controller\n- Prompt privately for the missing SNMPv2 community\n- Set the SNMPv2 community for this test\n- Validate SNMP settings\n- Test the SNMPv2 connection\n- Classify the SNMPv2 access failure\n- Test the SNMPv3 connection\n- Classify the SNMPv3 access failure\n- Report successful SNMP access\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/network/snmp_check.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
