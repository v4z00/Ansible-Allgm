# Playbook playbooks/checkmk/migrate_hosts.yml

Vorhandener Einstieg: `playbooks/checkmk/migrate_hosts.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Back up the Checkmk site before host migration
- Check the migration plan before backup
- Stop before making changes if the migration plan is missing
- Load the migration plan for validation
- Validate the site and at least one migration target
- Set the backup file path
- Create the backup directory in the Checkmk container
- Back up the Checkmk site to a temporary archive
- Verify the backup archive
- Finalize the verified backup
- Report the backup path
- Record the verified backup for this run
- Apply the planned Checkmk host migration
- Check confirmation from the backup host
- Check the migration plan
- Stop if the migration plan is missing
- Load the migration plan
- Validate the site and plan contents
- Ensure the target Checkmk folders exist
- Activate folder changes before migrating hosts
- Migrate Checkmk hosts one at a time
- Reconcile the folder, IP address and alias for all Checkmk targets
- Activate Checkmk changes

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/checkmk/migrate_hosts.yml",
  "title": "Playbook playbooks/checkmk/migrate_hosts.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/checkmk/migrate_hosts.yml"
  ],
  "source_hashes": {
    "playbooks/checkmk/migrate_hosts.yml": "b611cda4de73246ce8cd36c7047a33649c3cb146e48c1e889adcb12a0e823e40"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/checkmk/migrate_hosts.yml",
      "description": "# Playbook playbooks/checkmk/migrate_hosts.yml\n\nVorhandener Einstieg: `playbooks/checkmk/migrate_hosts.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Back up the Checkmk site before host migration\n- Check the migration plan before backup\n- Stop before making changes if the migration plan is missing\n- Load the migration plan for validation\n- Validate the site and at least one migration target\n- Set the backup file path\n- Create the backup directory in the Checkmk container\n- Back up the Checkmk site to a temporary archive\n- Verify the backup archive\n- Finalize the verified backup\n- Report the backup path\n- Record the verified backup for this run\n- Apply the planned Checkmk host migration\n- Check confirmation from the backup host\n- Check the migration plan\n- Stop if the migration plan is missing\n- Load the migration plan\n- Validate the site and plan contents\n- Ensure the target Checkmk folders exist\n- Activate folder changes before migrating hosts\n- Migrate Checkmk hosts one at a time\n- Reconcile the folder, IP address and alias for all Checkmk targets\n- Activate Checkmk changes\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/checkmk/migrate_hosts.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n\n## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)\n\nOptionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.\nFehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.\n- `tls_validate_certs.checkmk_migration_folders`: Checkmk-Zielordner sicherstellen (Standard true).\n- `tls_validate_certs.checkmk_migration_folders_activation`: Ordneraenderungen vor der Hostmigration aktivieren (Standard true).\n- `tls_validate_certs.checkmk_migration_attributes`: Alle Checkmk-Ziele auf Ordner, IP und Alias abgleichen (Standard true).\n- `tls_validate_certs.checkmk_migration_final_activation`: Checkmk-Aenderungen aktivieren (Standard true).\n\nStandortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben\nverwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/checkmk/migrate_hosts.yml",
      "description": "# Playbook playbooks/checkmk/migrate_hosts.yml\n\nPlaybook: `playbooks/checkmk/migrate_hosts.yml`.\n\nPlay and task names as written in the playbook:\n\n- Back up the Checkmk site before host migration\n- Check the migration plan before backup\n- Stop before making changes if the migration plan is missing\n- Load the migration plan for validation\n- Validate the site and at least one migration target\n- Set the backup file path\n- Create the backup directory in the Checkmk container\n- Back up the Checkmk site to a temporary archive\n- Verify the backup archive\n- Finalize the verified backup\n- Report the backup path\n- Record the verified backup for this run\n- Apply the planned Checkmk host migration\n- Check confirmation from the backup host\n- Check the migration plan\n- Stop if the migration plan is missing\n- Load the migration plan\n- Validate the site and plan contents\n- Ensure the target Checkmk folders exist\n- Activate folder changes before migrating hosts\n- Migrate Checkmk hosts one at a time\n- Reconcile the folder, IP address and alias for all Checkmk targets\n- Activate Checkmk changes\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/checkmk/migrate_hosts.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Per-task TLS certificate validation (1.1.0)\n\nSet optional `tls_validate_certs` entries in `group_vars/all/settings.yml`. Each inherits `tls_validate_certs_default` (default true). Setting false disables only its own check. `tls_validate_certs.checkmk_migration_folders` covers destination folders, `tls_validate_certs.checkmk_migration_folders_activation` activates folder changes before host migration, `tls_validate_certs.checkmk_migration_attributes` checks folder/IP/alias on all destinations, and `tls_validate_certs.checkmk_migration_final_activation` activates final changes.\n\nThe site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/checkmk/migrate_hosts.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.checkmk_migration_folders`: Checkmk-Zielordner sicherstellen (Standard true).
- `tls_validate_certs.checkmk_migration_folders_activation`: Ordneraenderungen vor der Hostmigration aktivieren (Standard true).
- `tls_validate_certs.checkmk_migration_attributes`: Alle Checkmk-Ziele auf Ordner, IP und Alias abgleichen (Standard true).
- `tls_validate_certs.checkmk_migration_final_activation`: Checkmk-Aenderungen aktivieren (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.
