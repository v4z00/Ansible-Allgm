# Playbook playbooks/maintenance/test_mail.yaml

Vorhandener Einstieg: `playbooks/maintenance/test_mail.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Testmail versenden
- Ausdrueckliches Ziel pruefen
- Feature pruefen
- Empfaenger explizit konfigurieren
- Testmail ueber lokalen MTA versenden

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
    "playbooks/maintenance/test_mail.yaml": "84d58fc4c883d2b02ce9d339995d4133147bdea0183c3a83bcc22bbaa0e2abed"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/test_mail.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
