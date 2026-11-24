# Playbook playbooks/maintenance/wan_check.yaml

Vorhandener Einstieg: `playbooks/maintenance/wan_check.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- HTTP-Erreichbarkeit pruefen
- HTTPS-Ziel abrufen
- Ergebnis anzeigen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/wan_check.yaml",
  "title": "Playbook playbooks/maintenance/wan_check.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/wan_check.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/wan_check.yaml": "6f0447b10a53a1e0034309699904952cc044fe2023a2979018a8467a58588223"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/wan_check.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.wan_check`: HTTPS-Ziel abrufen (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.
