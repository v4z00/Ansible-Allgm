# Playbook playbooks/monitoring/deploy_telegraf.yml

Vorhandener Einstieg: `playbooks/monitoring/deploy_telegraf.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Deploy Telegraf the Secure Way
- Telegraf-Funktion muss aktiviert sein
- Install repository prerequisites
- Create keyring directory
- InfluxData Repository-Schluessel herunterladen
- Fingerabdruck des InfluxData-Schluessels lesen
- InfluxData-Schluessel gegen den erwarteten Fingerabdruck pruefen
- Geprueften InfluxData-Schluessel installieren
- Ensure correct permissions on the key
- Add InfluxData Repository
- Install Telegraf
- telegraf
- Deploy Telegraf Configuration
- Heruntergeladenen Repository-Schluessel entfernen
- Force restart Telegraf
- restart_telegraf

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/monitoring/deploy_telegraf.yml",
  "title": "Playbook playbooks/monitoring/deploy_telegraf.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/monitoring/deploy_telegraf.yml"
  ],
  "source_hashes": {
    "playbooks/monitoring/deploy_telegraf.yml": "1083b693d95153cab46e7dc29f616023f4ab30b86bd092402b879eb32c776bb0"
  }
}
```

## Quellen und Pflege

- `playbooks/monitoring/deploy_telegraf.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.telegraf_repository_key`: InfluxData Repository-Schluessel herunterladen (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.
