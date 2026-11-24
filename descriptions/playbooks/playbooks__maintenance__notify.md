# Playbook playbooks/maintenance/notify.yml

Vorhandener Einstieg: `playbooks/maintenance/notify.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Betriebsnachricht senden
- Nachrichtendatei lesen
- Telegram-Nachricht senden
- Fehlende optionale Telegram-Konfiguration anzeigen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/notify.yml",
  "title": "Playbook playbooks/maintenance/notify.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/notify.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/notify.yml": "af8c4189415c7c8371dfcfbbda26c59fbea75be3101f6012315e08b1784c3dc0"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/notify.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.telegram_notification`: Telegram-Nachricht senden (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.
