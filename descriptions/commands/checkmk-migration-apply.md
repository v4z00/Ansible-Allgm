# CheckMK sichern und den gespeicherten Plan anwenden

CheckMK sichern und den gespeicherten Plan anwenden

Aufruf: `bin/control checkmk-migration-apply [Optionen]`.

Vorhandene Kurzformen: `checkmk-migration-apply`.

Feature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `playbooks/checkmk/migrate_hosts.yml`

## Sicherung vor der Migration

`bin/control checkmk-migration-plan` erstellt den Plan. `bin/control checkmk-migration-apply --check` prüft Plan, Site und Einstellungen. Der Aufruf ohne `--check` sichert zuerst die vollständige OMD-Site und wendet danach den Plan über die Checkmk-API an.

In `group_vars/all/settings.yml` bezeichnet `checkmk_backup_target_host` genau einen Inventarhost. Der Standard `checkmk_backup_mode: docker` führt `omd backup` im Container `checkmk_container_name` aus. Mit `checkmk_backup_mode: native` läuft derselbe Befehl direkt auf dem OMD-Host. `checkmk_backup_dir` ist ein absoluter Pfad im jeweiligen Dateisystem (Standard `/backup`). Das Sicherungsziel außerhalb des Site-Verzeichnisses wählen, bei Docker auf einem persistenten Mount. [Checkmk-Handbuch](https://docs.checkmk.com/latest/de/omd_basics.html#backup)

Ohne `--limit` werden Sicherungshost und Controller automatisch ausgewählt. Bei einem Limit beide nennen, zum Beispiel `--limit localhost,backup-host`; `backup-host` durch den konfigurierten Inventarnamen ersetzen. Die Backup-Befehle laufen mit erhöhten Rechten auf dem Sicherungshost, die API-Aufrufe auf `localhost`. Ein unvollständiges Limit bricht den Lauf vor der Sicherung ab.

Das fertige Archiv hat Modus `0600`. Erst nach erfolgreichem Lesen mit `tar -tzf` und Verschieben des Archivs beginnen die API-Änderungen. Schlägt die Sicherung fehl, bricht die Migration ab. Der Lauf gibt den Pfad des fertigen Archivs aus.

`checkmk_migration_plan` legt bei Bedarf die genaue Plandatei fest. Sonst heißt sie `checkmk_migration_plan.yml` im Berichtsverzeichnis. Dafür gilt in dieser Reihenfolge `controller_reports_dir`, `ANSIBLE_REPORTS_DIR`, dann `x/reports` im Projekt. Relative Pfade beziehen sich auf `ANSIBLE_PROJECT_ROOT` oder das Projekt des Playbooks.

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "checkmk-migration-apply",
  "title": "CheckMK sichern und den gespeicherten Plan anwenden",
  "documented": true,
  "fields": [
    {
      "id": "targets",
      "label": "targets",
      "description": "Bei einem Limit localhost und den konfigurierten Sicherungshost auswählen.",
      "type": "array",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--limit",
        "separator": ","
      },
      "completion": {
        "source": "inventory.targets"
      }
    },
    {
      "id": "check",
      "label": "check",
      "description": "Prüft Plan und Sicherungseinstellungen. Backup und API-Änderungen starten erst beim Aufruf ohne --check.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--check"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/checkmk-migration-apply.json",
    "bin/control.d/checkmk-migration-apply.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/checkmk-migration-apply.json": "f18c353893a8f5eb19f63ad1514dcf4873226f6bb8bae600ee02e9b0de6f8e13",
    "bin/control.d/checkmk-migration-apply.sh": "041fcfd5f565220a914754e67dc9527eaa6b0ad3eee190d7517564af9e5e434f",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "CheckMK sichern und den gespeicherten Plan anwenden",
      "description": "# CheckMK sichern und den gespeicherten Plan anwenden\n\nCheckMK sichern und den gespeicherten Plan anwenden\n\nAufruf: `bin/control checkmk-migration-apply [Optionen]`.\n\nVorhandene Kurzformen: `checkmk-migration-apply`.\n\nFeature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `playbooks/checkmk/migrate_hosts.yml`\n\n## Sicherung vor der Migration\n\n`bin/control checkmk-migration-plan` erstellt den Plan. `bin/control checkmk-migration-apply --check` prüft Plan, Site und Einstellungen. Der Aufruf ohne `--check` sichert zuerst die vollständige OMD-Site und wendet danach den Plan über die Checkmk-API an.\n\nIn `group_vars/all/settings.yml` bezeichnet `checkmk_backup_target_host` genau einen Inventarhost. Der Standard `checkmk_backup_mode: docker` führt `omd backup` im Container `checkmk_container_name` aus. Mit `checkmk_backup_mode: native` läuft derselbe Befehl direkt auf dem OMD-Host. `checkmk_backup_dir` ist ein absoluter Pfad im jeweiligen Dateisystem (Standard `/backup`). Das Sicherungsziel außerhalb des Site-Verzeichnisses wählen, bei Docker auf einem persistenten Mount. [Checkmk-Handbuch](https://docs.checkmk.com/latest/de/omd_basics.html#backup)\n\nOhne `--limit` werden Sicherungshost und Controller automatisch ausgewählt. Bei einem Limit beide nennen, zum Beispiel `--limit localhost,backup-host`; `backup-host` durch den konfigurierten Inventarnamen ersetzen. Die Backup-Befehle laufen mit erhöhten Rechten auf dem Sicherungshost, die API-Aufrufe auf `localhost`. Ein unvollständiges Limit bricht den Lauf vor der Sicherung ab.\n\nDas fertige Archiv hat Modus `0600`. Erst nach erfolgreichem Lesen mit `tar -tzf` und Verschieben des Archivs beginnen die API-Änderungen. Schlägt die Sicherung fehl, bricht die Migration ab. Der Lauf gibt den Pfad des fertigen Archivs aus.\n\n`checkmk_migration_plan` legt bei Bedarf die genaue Plandatei fest. Sonst heißt sie `checkmk_migration_plan.yml` im Berichtsverzeichnis. Dafür gilt in dieser Reihenfolge `controller_reports_dir`, `ANSIBLE_REPORTS_DIR`, dann `x/reports` im Projekt. Relative Pfade beziehen sich auf `ANSIBLE_PROJECT_ROOT` oder das Projekt des Playbooks.\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/checkmk-migration-apply.json`\n- `bin/control.d/checkmk-migration-apply.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "targets": {
          "label": "targets",
          "description": "Bei einem Limit localhost und den konfigurierten Sicherungshost auswählen."
        },
        "check": {
          "label": "check",
          "description": "Prüft Plan und Sicherungseinstellungen. Backup und API-Änderungen starten erst beim Aufruf ohne --check."
        }
      }
    },
    "en": {
      "title": "Back up Checkmk and apply the saved migration plan",
      "description": "# Back up Checkmk and apply the saved migration plan\n\nBack up Checkmk and apply the saved migration plan\n\nRun: `bin/control checkmk-migration-apply [options]`.\n\nAliases: `checkmk-migration-apply`.\n\nFeature: checkmk. Control checks availability at runtime.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `playbooks/checkmk/migrate_hosts.yml`\n\n## Backup before migration\n\n`bin/control checkmk-migration-plan` creates the plan. Run `bin/control checkmk-migration-apply --check` to validate the plan, site and settings. Running the command without `--check` backs up the entire OMD site before applying the plan through the Checkmk API.\n\nIn `group_vars/all/settings.yml`, set `checkmk_backup_target_host` to a single inventory host. The default `checkmk_backup_mode: docker` runs `omd backup` inside `checkmk_container_name`. With `checkmk_backup_mode: native`, the command runs directly on the OMD host. `checkmk_backup_dir` is an absolute path in that filesystem (default `/backup`). Choose a directory outside the site and use a persistent mount for Docker. [Checkmk manual](https://docs.checkmk.com/latest/en/omd_basics.html#backup)\n\nWithout `--limit`, the play selects the backup host and controller automatically. When using a limit, include both, for example `--limit localhost,backup-host`. Replace `backup-host` with the configured inventory name. Backup commands run with elevated privileges on the backup host. API calls run on `localhost`. An incomplete limit stops the run before the backup.\n\nThe finished archive has mode `0600`. API changes start after `tar -tzf` reads the archive successfully and the archive has been moved into place. A backup failure stops migration. The play reports the final archive path.\n\nTo select a specific plan file, set `checkmk_migration_plan`. Otherwise the play reads `checkmk_migration_plan.yml` from the reports directory. It uses `controller_reports_dir` first, then `ANSIBLE_REPORTS_DIR`, then `x/reports` in the project. Relative paths resolve against `ANSIBLE_PROJECT_ROOT` or the project containing the playbook.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/checkmk-migration-apply.json`\n- `bin/control.d/checkmk-migration-apply.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "targets": {
          "label": "Target hosts or groups",
          "description": "When using a limit, select localhost and the configured backup host."
        },
        "check": {
          "label": "Check mode",
          "description": "Validate the plan and backup settings. Run without --check to create the backup and apply changes."
        }
      }
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/checkmk-migration-apply.json`
- `bin/control.d/checkmk-migration-apply.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
