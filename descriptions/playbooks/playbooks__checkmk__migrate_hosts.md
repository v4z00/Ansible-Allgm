# Playbook playbooks/checkmk/migrate_hosts.yml

Vorhandener Einstieg: `playbooks/checkmk/migrate_hosts.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Checkmk-Site vor Hostmigration sichern
- Migrationsplan vor dem Backup pruefen
- Ohne Migrationsplan vor jeder Aenderung abbrechen
- Migrationsplan fuer Vorpruefung laden
- checkmk_migration_preflight
- Site und mindestens ein Ziel vorpruefen
- Backup-Datei festlegen
- Backup-Verzeichnis im Checkmk-Container anlegen
- Checkmk-Site in temporaeres Archiv sichern
- Backup-Archiv pruefen
- Geprueftes Backup finalisieren
- Backup-Pfad ausgeben
- Geplante Checkmk-Hostmigration anwenden
- Migrationsplan pruefen
- Ohne Migrationsplan abbrechen
- Migrationsplan laden
- checkmk_migration
- Site und Planinhalt validieren
- Checkmk-Zielordner sicherstellen
- {{ item.name }}
- Ordneraenderungen vor der Hostmigration aktivieren
- Checkmk-Hosts seriell migrieren
- Alle Checkmk-Ziele auf Ordner, IP und Alias abgleichen
- {{ item.checkmk_hostname }}
- Checkmk-Aenderungen aktivieren

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
    "playbooks/checkmk/migrate_hosts.yml": "af5bb115f7151904689af456c5fa0137c433e6a92f80f79b5ee8f9955580fdb5"
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
Die drei Standorteinrichter setzen Telegram ausdruecklich auf true.
