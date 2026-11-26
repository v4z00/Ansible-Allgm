# Playbook playbooks/reporting/lynis_summary.yml

Vorhandener Einstieg: `playbooks/reporting/lynis_summary.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Evaluate Lynis Reports
- Parse Lynis Hardening Index
- Parse Critical Warnings
- Render Summary to Variable
- Show the security audit summary
- Create CSV Export Header
- Update CSV Export data

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/reporting/lynis_summary.yml",
  "title": "Playbook playbooks/reporting/lynis_summary.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/reporting/lynis_summary.yml"
  ],
  "source_hashes": {
    "playbooks/reporting/lynis_summary.yml": "7a7011c25897687e6a72d9f568065d524180c612050bd9a595629430fba4cff0"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/reporting/lynis_summary.yml",
      "description": "# Playbook playbooks/reporting/lynis_summary.yml\n\nVorhandener Einstieg: `playbooks/reporting/lynis_summary.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Evaluate Lynis Reports\n- Parse Lynis Hardening Index\n- Parse Critical Warnings\n- Render Summary to Variable\n- Show the security audit summary\n- Create CSV Export Header\n- Update CSV Export data\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/reporting/lynis_summary.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/reporting/lynis_summary.yml",
      "description": "# Playbook playbooks/reporting/lynis_summary.yml\n\nPlaybook: `playbooks/reporting/lynis_summary.yml`.\n\nPlay and task names as written in the playbook:\n\n- Evaluate Lynis Reports\n- Parse Lynis Hardening Index\n- Parse Critical Warnings\n- Render Summary to Variable\n- Show the security audit summary\n- Create CSV Export Header\n- Update CSV Export data\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/reporting/lynis_summary.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/reporting/lynis_summary.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
