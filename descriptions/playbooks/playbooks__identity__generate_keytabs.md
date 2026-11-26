# Playbook playbooks/identity/generate_keytabs.yml

Vorhandener Einstieg: `playbooks/identity/generate_keytabs.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Manage Kerberos keytabs, schedule renewal and check tickets
- Require the Kerberos keytab feature
- Set the search path
- Find eligible credential files
- Check whether ktutil is installed
- Stop if ktutil is missing
- Check for existing keytabs
- Generate missing keytabs from credential files
- Check the generated keytabs
- Report any missing keytab
- Request a Kerberos ticket immediately
- Report the ticket check result
- Schedule ticket renewal every four hours
- Schedule ticket renewal at boot

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/identity/generate_keytabs.yml",
  "title": "Playbook playbooks/identity/generate_keytabs.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/identity/generate_keytabs.yml"
  ],
  "source_hashes": {
    "playbooks/identity/generate_keytabs.yml": "b15f5bba4b775a3b94baff2b16d1064c43624b1bcd246e5f5f6313abc9b2b2f1"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/identity/generate_keytabs.yml",
      "description": "# Playbook playbooks/identity/generate_keytabs.yml\n\nVorhandener Einstieg: `playbooks/identity/generate_keytabs.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Manage Kerberos keytabs, schedule renewal and check tickets\n- Require the Kerberos keytab feature\n- Set the search path\n- Find eligible credential files\n- Check whether ktutil is installed\n- Stop if ktutil is missing\n- Check for existing keytabs\n- Generate missing keytabs from credential files\n- Check the generated keytabs\n- Report any missing keytab\n- Request a Kerberos ticket immediately\n- Report the ticket check result\n- Schedule ticket renewal every four hours\n- Schedule ticket renewal at boot\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/identity/generate_keytabs.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/identity/generate_keytabs.yml",
      "description": "# Playbook playbooks/identity/generate_keytabs.yml\n\nPlaybook: `playbooks/identity/generate_keytabs.yml`.\n\nPlay and task names as written in the playbook:\n\n- Manage Kerberos keytabs, schedule renewal and check tickets\n- Require the Kerberos keytab feature\n- Set the search path\n- Find eligible credential files\n- Check whether ktutil is installed\n- Stop if ktutil is missing\n- Check for existing keytabs\n- Generate missing keytabs from credential files\n- Check the generated keytabs\n- Report any missing keytab\n- Request a Kerberos ticket immediately\n- Report the ticket check result\n- Schedule ticket renewal every four hours\n- Schedule ticket renewal at boot\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/identity/generate_keytabs.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/identity/generate_keytabs.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
