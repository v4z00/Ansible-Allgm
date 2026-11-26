# Playbook playbooks/maintenance/test_mail.yaml

Vorhandener Einstieg: `playbooks/maintenance/test_mail.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Send a test email
- Require an explicit target
- Check the feature flag
- Require an explicit recipient
- Send a test email through the local MTA

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/test_mail.yaml",
  "title": "Playbook playbooks/maintenance/test_mail.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/test_mail.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/test_mail.yaml": "da672f005c45830fcdfa8376f8928bb9a21f83dcb05003dbbf949b1aac41bd0d"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/maintenance/test_mail.yaml",
      "description": "# Playbook playbooks/maintenance/test_mail.yaml\n\nVorhandener Einstieg: `playbooks/maintenance/test_mail.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Send a test email\n- Require an explicit target\n- Check the feature flag\n- Require an explicit recipient\n- Send a test email through the local MTA\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/maintenance/test_mail.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/maintenance/test_mail.yaml",
      "description": "# Playbook playbooks/maintenance/test_mail.yaml\n\nPlaybook: `playbooks/maintenance/test_mail.yaml`.\n\nPlay and task names as written in the playbook:\n\n- Send a test email\n- Require an explicit target\n- Check the feature flag\n- Require an explicit recipient\n- Send a test email through the local MTA\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/maintenance/test_mail.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/test_mail.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
