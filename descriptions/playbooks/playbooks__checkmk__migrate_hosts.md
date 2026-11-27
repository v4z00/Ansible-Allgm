# Playbook playbooks/checkmk/migrate_hosts.yml

Playbook: `playbooks/checkmk/migrate_hosts.yml`.

## Backup before migration

`bin/control checkmk-migration-plan` creates the plan. Run `bin/control checkmk-migration-apply --check` to validate the plan, site and settings. Running the command without `--check` backs up the entire OMD site before applying the plan through the Checkmk API.

In `group_vars/all/settings.yml`, set `checkmk_backup_target_host` to a single inventory host. The default `checkmk_backup_mode: docker` runs `omd backup` inside `checkmk_container_name`. With `checkmk_backup_mode: native`, the command runs directly on the OMD host. `checkmk_backup_dir` is an absolute path in that filesystem (default `/backup`). Choose a directory outside the site and use a persistent mount for Docker. [Checkmk manual](https://docs.checkmk.com/latest/en/omd_basics.html#backup)

Without `--limit`, the play selects the backup host and controller automatically. When using a limit, include both, for example `--limit localhost,backup-host`. Replace `backup-host` with the configured inventory name. Backup commands run with elevated privileges on the backup host. API calls run on `localhost`. An incomplete limit stops the run before the backup.

The finished archive has mode `0600`. API changes start after `tar -tzf` reads the archive successfully and the archive has been moved into place. A backup failure stops migration. The play reports the final archive path.

To select a specific plan file, set `checkmk_migration_plan`. Otherwise the play reads `checkmk_migration_plan.yml` from the reports directory. It uses `controller_reports_dir` first, then `ANSIBLE_REPORTS_DIR`, then `x/reports` in the project. Relative paths resolve against `ANSIBLE_PROJECT_ROOT` or the project containing the playbook.

Play and task names as written in the playbook:

- Check the controller is included in the migration limit
- Require both the API controller and backup host in a limit
- Back up the Checkmk site and apply the saved host migration
- Validate the backup inventory host
- Validate the backup mode, site and directory
- Check that the saved migration plan exists
- Require a saved migration plan
- Load the saved migration plan
- Validate the site and migration targets
- Finish check mode after validating the plan and backup settings
- Create and verify the site archive on the backup host
- Ensure the backup directory exists
- Create a private working directory for the backup
- Publish the archive only after verification
- Back up the site using OMD
- Restrict archive permissions
- Verify the compressed tar archive
- Record the final archive path
- Move the verified archive into place
- Remove any incomplete archive
- Remove the private working directory
- Report the verified backup path
- Apply the plan after publishing the verified backup
- Ensure the target Checkmk folders exist
- Activate folder changes before migrating hosts
- Migrate Checkmk hosts one at a time
- Reconcile the folder, IP address and alias for all Checkmk targets
- Activate Checkmk changes

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/checkmk/migrate_hosts.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Per-task TLS certificate validation (1.1.0)

Set optional `tls_validate_certs` entries in `group_vars/all/settings.yml`. Each inherits `tls_validate_certs_default` (default true). Setting false disables only its own check. `tls_validate_certs.checkmk_migration_folders` covers destination folders, `tls_validate_certs.checkmk_migration_folders_activation` activates folder changes before host migration, `tls_validate_certs.checkmk_migration_attributes` checks folder/IP/alias on all destinations, and `tls_validate_certs.checkmk_migration_final_activation` activates final changes.

The site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/checkmk/migrate_hosts.yml

Vorhandener Einstieg: `playbooks/checkmk/migrate_hosts.yml`.

## Sicherung vor der Migration

`bin/control checkmk-migration-plan` erstellt den Plan. `bin/control checkmk-migration-apply --check` prüft Plan, Site und Einstellungen. Der Aufruf ohne `--check` sichert zuerst die vollständige OMD-Site und wendet danach den Plan über die Checkmk-API an.

In `group_vars/all/settings.yml` bezeichnet `checkmk_backup_target_host` genau einen Inventarhost. Der Standard `checkmk_backup_mode: docker` führt `omd backup` im Container `checkmk_container_name` aus. Mit `checkmk_backup_mode: native` läuft derselbe Befehl direkt auf dem OMD-Host. `checkmk_backup_dir` ist ein absoluter Pfad im jeweiligen Dateisystem (Standard `/backup`). Das Sicherungsziel außerhalb des Site-Verzeichnisses wählen, bei Docker auf einem persistenten Mount. [Checkmk-Handbuch](https://docs.checkmk.com/latest/de/omd_basics.html#backup)

Ohne `--limit` werden Sicherungshost und Controller automatisch ausgewählt. Bei einem Limit beide nennen, zum Beispiel `--limit localhost,backup-host`; `backup-host` durch den konfigurierten Inventarnamen ersetzen. Die Backup-Befehle laufen mit erhöhten Rechten auf dem Sicherungshost, die API-Aufrufe auf `localhost`. Ein unvollständiges Limit bricht den Lauf vor der Sicherung ab.

Das fertige Archiv hat Modus `0600`. Erst nach erfolgreichem Lesen mit `tar -tzf` und Verschieben des Archivs beginnen die API-Änderungen. Schlägt die Sicherung fehl, bricht die Migration ab. Der Lauf gibt den Pfad des fertigen Archivs aus.

`checkmk_migration_plan` legt bei Bedarf die genaue Plandatei fest. Sonst heißt sie `checkmk_migration_plan.yml` im Berichtsverzeichnis. Dafür gilt in dieser Reihenfolge `controller_reports_dir`, `ANSIBLE_REPORTS_DIR`, dann `x/reports` im Projekt. Relative Pfade beziehen sich auf `ANSIBLE_PROJECT_ROOT` oder das Projekt des Playbooks.

Im Quelltext benannte Plays/Aufgaben:

- Check the controller is included in the migration limit
- Require both the API controller and backup host in a limit
- Back up the Checkmk site and apply the saved host migration
- Validate the backup inventory host
- Validate the backup mode, site and directory
- Check that the saved migration plan exists
- Require a saved migration plan
- Load the saved migration plan
- Validate the site and migration targets
- Finish check mode after validating the plan and backup settings
- Create and verify the site archive on the backup host
- Ensure the backup directory exists
- Create a private working directory for the backup
- Publish the archive only after verification
- Back up the site using OMD
- Restrict archive permissions
- Verify the compressed tar archive
- Record the final archive path
- Move the verified archive into place
- Remove any incomplete archive
- Remove the private working directory
- Report the verified backup path
- Apply the plan after publishing the verified backup
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

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
    "playbooks/checkmk/migrate_hosts.yml": "3ba3d4f0087e8aa340c0de5712453aff5b4fba104f4d89db426e19a39ad01a6a"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/checkmk/migrate_hosts.yml",
      "description": "# Playbook playbooks/checkmk/migrate_hosts.yml\n\nVorhandener Einstieg: `playbooks/checkmk/migrate_hosts.yml`.\n\n## Sicherung vor der Migration\n\n`bin/control checkmk-migration-plan` erstellt den Plan. `bin/control checkmk-migration-apply --check` prüft Plan, Site und Einstellungen. Der Aufruf ohne `--check` sichert zuerst die vollständige OMD-Site und wendet danach den Plan über die Checkmk-API an.\n\nIn `group_vars/all/settings.yml` bezeichnet `checkmk_backup_target_host` genau einen Inventarhost. Der Standard `checkmk_backup_mode: docker` führt `omd backup` im Container `checkmk_container_name` aus. Mit `checkmk_backup_mode: native` läuft derselbe Befehl direkt auf dem OMD-Host. `checkmk_backup_dir` ist ein absoluter Pfad im jeweiligen Dateisystem (Standard `/backup`). Das Sicherungsziel außerhalb des Site-Verzeichnisses wählen, bei Docker auf einem persistenten Mount. [Checkmk-Handbuch](https://docs.checkmk.com/latest/de/omd_basics.html#backup)\n\nOhne `--limit` werden Sicherungshost und Controller automatisch ausgewählt. Bei einem Limit beide nennen, zum Beispiel `--limit localhost,backup-host`; `backup-host` durch den konfigurierten Inventarnamen ersetzen. Die Backup-Befehle laufen mit erhöhten Rechten auf dem Sicherungshost, die API-Aufrufe auf `localhost`. Ein unvollständiges Limit bricht den Lauf vor der Sicherung ab.\n\nDas fertige Archiv hat Modus `0600`. Erst nach erfolgreichem Lesen mit `tar -tzf` und Verschieben des Archivs beginnen die API-Änderungen. Schlägt die Sicherung fehl, bricht die Migration ab. Der Lauf gibt den Pfad des fertigen Archivs aus.\n\n`checkmk_migration_plan` legt bei Bedarf die genaue Plandatei fest. Sonst heißt sie `checkmk_migration_plan.yml` im Berichtsverzeichnis. Dafür gilt in dieser Reihenfolge `controller_reports_dir`, `ANSIBLE_REPORTS_DIR`, dann `x/reports` im Projekt. Relative Pfade beziehen sich auf `ANSIBLE_PROJECT_ROOT` oder das Projekt des Playbooks.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Check the controller is included in the migration limit\n- Require both the API controller and backup host in a limit\n- Back up the Checkmk site and apply the saved host migration\n- Validate the backup inventory host\n- Validate the backup mode, site and directory\n- Check that the saved migration plan exists\n- Require a saved migration plan\n- Load the saved migration plan\n- Validate the site and migration targets\n- Finish check mode after validating the plan and backup settings\n- Create and verify the site archive on the backup host\n- Ensure the backup directory exists\n- Create a private working directory for the backup\n- Publish the archive only after verification\n- Back up the site using OMD\n- Restrict archive permissions\n- Verify the compressed tar archive\n- Record the final archive path\n- Move the verified archive into place\n- Remove any incomplete archive\n- Remove the private working directory\n- Report the verified backup path\n- Apply the plan after publishing the verified backup\n- Ensure the target Checkmk folders exist\n- Activate folder changes before migrating hosts\n- Migrate Checkmk hosts one at a time\n- Reconcile the folder, IP address and alias for all Checkmk targets\n- Activate Checkmk changes\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/checkmk/migrate_hosts.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n\n## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)\n\nOptionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.\nFehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.\n- `tls_validate_certs.checkmk_migration_folders`: Checkmk-Zielordner sicherstellen (Standard true).\n- `tls_validate_certs.checkmk_migration_folders_activation`: Ordneraenderungen vor der Hostmigration aktivieren (Standard true).\n- `tls_validate_certs.checkmk_migration_attributes`: Alle Checkmk-Ziele auf Ordner, IP und Alias abgleichen (Standard true).\n- `tls_validate_certs.checkmk_migration_final_activation`: Checkmk-Aenderungen aktivieren (Standard true).\n\nStandortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben\nverwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/checkmk/migrate_hosts.yml",
      "description": "# Playbook playbooks/checkmk/migrate_hosts.yml\n\nPlaybook: `playbooks/checkmk/migrate_hosts.yml`.\n\n## Backup before migration\n\n`bin/control checkmk-migration-plan` creates the plan. Run `bin/control checkmk-migration-apply --check` to validate the plan, site and settings. Running the command without `--check` backs up the entire OMD site before applying the plan through the Checkmk API.\n\nIn `group_vars/all/settings.yml`, set `checkmk_backup_target_host` to a single inventory host. The default `checkmk_backup_mode: docker` runs `omd backup` inside `checkmk_container_name`. With `checkmk_backup_mode: native`, the command runs directly on the OMD host. `checkmk_backup_dir` is an absolute path in that filesystem (default `/backup`). Choose a directory outside the site and use a persistent mount for Docker. [Checkmk manual](https://docs.checkmk.com/latest/en/omd_basics.html#backup)\n\nWithout `--limit`, the play selects the backup host and controller automatically. When using a limit, include both, for example `--limit localhost,backup-host`. Replace `backup-host` with the configured inventory name. Backup commands run with elevated privileges on the backup host. API calls run on `localhost`. An incomplete limit stops the run before the backup.\n\nThe finished archive has mode `0600`. API changes start after `tar -tzf` reads the archive successfully and the archive has been moved into place. A backup failure stops migration. The play reports the final archive path.\n\nTo select a specific plan file, set `checkmk_migration_plan`. Otherwise the play reads `checkmk_migration_plan.yml` from the reports directory. It uses `controller_reports_dir` first, then `ANSIBLE_REPORTS_DIR`, then `x/reports` in the project. Relative paths resolve against `ANSIBLE_PROJECT_ROOT` or the project containing the playbook.\n\nPlay and task names as written in the playbook:\n\n- Check the controller is included in the migration limit\n- Require both the API controller and backup host in a limit\n- Back up the Checkmk site and apply the saved host migration\n- Validate the backup inventory host\n- Validate the backup mode, site and directory\n- Check that the saved migration plan exists\n- Require a saved migration plan\n- Load the saved migration plan\n- Validate the site and migration targets\n- Finish check mode after validating the plan and backup settings\n- Create and verify the site archive on the backup host\n- Ensure the backup directory exists\n- Create a private working directory for the backup\n- Publish the archive only after verification\n- Back up the site using OMD\n- Restrict archive permissions\n- Verify the compressed tar archive\n- Record the final archive path\n- Move the verified archive into place\n- Remove any incomplete archive\n- Remove the private working directory\n- Report the verified backup path\n- Apply the plan after publishing the verified backup\n- Ensure the target Checkmk folders exist\n- Activate folder changes before migrating hosts\n- Migrate Checkmk hosts one at a time\n- Reconcile the folder, IP address and alias for all Checkmk targets\n- Activate Checkmk changes\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/checkmk/migrate_hosts.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Per-task TLS certificate validation (1.1.0)\n\nSet optional `tls_validate_certs` entries in `group_vars/all/settings.yml`. Each inherits `tls_validate_certs_default` (default true). Setting false disables only its own check. `tls_validate_certs.checkmk_migration_folders` covers destination folders, `tls_validate_certs.checkmk_migration_folders_activation` activates folder changes before host migration, `tls_validate_certs.checkmk_migration_attributes` checks folder/IP/alias on all destinations, and `tls_validate_certs.checkmk_migration_final_activation` activates final changes.\n\nThe site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.",
      "fields": {}
    }
  }
}
```

</details>
