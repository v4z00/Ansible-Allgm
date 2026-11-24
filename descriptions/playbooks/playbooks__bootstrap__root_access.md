# Playbook playbooks/bootstrap/root_access.yml

Vorhandener Einstieg: `playbooks/bootstrap/root_access.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Root-Bootstrap vorbereiten
- Bootstrap-Profile muessen konfiguriert sein
- Gewaehltes Bootstrap-Profil muss vorhanden sein
- Controller-Key pruefen
- Controller-Key muss vorhanden sein
- Ausgewaehlte Bootstrap-Profile pruefen
- Root-Key oder individuellen Erstzugang vorbereiten
- Root-Zugang ueber sudo oder su herstellen
- Verbindung mit dem Erstzugang pruefen
- sudo zu root testen
- su zu root testen
- Funktionierende Become-Methode bestimmen
- Ohne funktionierenden Root-Aufstieg abbrechen
- Root-Key-Zugang einrichten
- Root-SSH-Verzeichnis anlegen
- Controller-Key fuer root hinterlegen
- Root-Key-Anmeldung freigeben
- SSH-Konfiguration validieren
- SSH neu laden
- ssh
- Verwendete Become-Methode ausgeben
- Bereits vorhandenen Root-Key bestaetigen
- Root-Key-Verbindung mit Ansible pruefen
- Vorhandenen Root-Key melden

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/bootstrap/root_access.yml",
  "title": "Playbook playbooks/bootstrap/root_access.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/bootstrap/root_access.yml"
  ],
  "source_hashes": {
    "playbooks/bootstrap/root_access.yml": "a581fbf803c90c5d99fb97474d678b1af32e5b21895ea0a86237f4ee1530d51a"
  }
}
```

## Quellen und Pflege

- `playbooks/bootstrap/root_access.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
