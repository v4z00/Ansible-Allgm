# Playbook playbooks/maintenance/rotate_service_user_passwords.yml

Playbook: `playbooks/maintenance/rotate_service_user_passwords.yml`.

Play and task names as written in the playbook:

- Set configured service account passwords
- Require an explicit target
- Validate configured password hashes
- Update service accounts

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/maintenance/rotate_service_user_passwords.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/maintenance/rotate_service_user_passwords.yml

Vorhandener Einstieg: `playbooks/maintenance/rotate_service_user_passwords.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Set configured service account passwords
- Require an explicit target
- Validate configured password hashes
- Update service accounts

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/maintenance/rotate_service_user_passwords.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/rotate_service_user_passwords.yml",
  "title": "Playbook playbooks/maintenance/rotate_service_user_passwords.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/rotate_service_user_passwords.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/rotate_service_user_passwords.yml": "b0ba5462d63a5c2befd36ef6cd4f4a78cf05c47025216237fca2262d1bdfdb89"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/maintenance/rotate_service_user_passwords.yml",
      "description": "# Playbook playbooks/maintenance/rotate_service_user_passwords.yml\n\nVorhandener Einstieg: `playbooks/maintenance/rotate_service_user_passwords.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Set configured service account passwords\n- Require an explicit target\n- Validate configured password hashes\n- Update service accounts\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/maintenance/rotate_service_user_passwords.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/maintenance/rotate_service_user_passwords.yml",
      "description": "# Playbook playbooks/maintenance/rotate_service_user_passwords.yml\n\nPlaybook: `playbooks/maintenance/rotate_service_user_passwords.yml`.\n\nPlay and task names as written in the playbook:\n\n- Set configured service account passwords\n- Require an explicit target\n- Validate configured password hashes\n- Update service accounts\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/maintenance/rotate_service_user_passwords.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
