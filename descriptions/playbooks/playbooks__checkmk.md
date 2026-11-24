# Playbook playbooks/checkmk.yml

Vorhandener Einstieg: `playbooks/checkmk.yml`.

Im Quelltext benannte Plays/Aufgaben:

- CheckMK-Ordnerstruktur sicherstellen
- CheckMK-API-Konfiguration fuer Ordner pruefen
- CheckMK-Ordner und Elternordner anlegen
- {{ item.name }}
- CheckMK-Agent und Hostverwaltung
- Nicht-Linux-Hosts nur in CheckMK anlegen
- API-Konfiguration und Zielordner fuer manuelle Hosts pruefen
- Nicht-Linux-Host ohne Attribute anlegen oder im Zielordner sicherstellen
- {{ checkmk_hostname | default(inventory_hostname) }}
- Manuell zu konfigurierenden CheckMK-Host ausgeben

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/checkmk.yml",
  "title": "Playbook playbooks/checkmk.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/checkmk.yml"
  ],
  "source_hashes": {
    "playbooks/checkmk.yml": "302abd08cb511631a0e8efdc87986ccb9ddb9d5ca91b9edf9b57c2a0f21e8058"
  }
}
```

## Quellen und Pflege

- `playbooks/checkmk.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.checkmk_folders`: CheckMK-Ordner und Elternordner anlegen (Standard true).
- `tls_validate_certs.checkmk_manual_host`: Nicht-Linux-Host ohne Attribute anlegen oder im Zielordner sicherstellen (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.
