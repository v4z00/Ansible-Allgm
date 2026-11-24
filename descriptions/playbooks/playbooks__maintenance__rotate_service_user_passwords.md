# Playbook playbooks/maintenance/rotate_service_user_passwords.yml

Vorhandener Einstieg: `playbooks/maintenance/rotate_service_user_passwords.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Konfigurierte Service-Passwoerter setzen
- Ausdrueckliches Ziel pruefen
- Konfigurierte Passwort-Hashes pruefen
- Service-Benutzer aktualisieren
- {{ item.name }}

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

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
    "playbooks/maintenance/rotate_service_user_passwords.yml": "e59b2a52fbb956e2b02c430a77d9877964b8a800f1067b7cfaceb4af74370f61"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/rotate_service_user_passwords.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
