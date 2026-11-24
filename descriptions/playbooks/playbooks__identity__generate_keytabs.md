# Playbook playbooks/identity/generate_keytabs.yml

Vorhandener Einstieg: `playbooks/identity/generate_keytabs.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Kerberos: Keytabs, Cron-Einträge & Sofort-Check (Ohne Hetzner)
- Kerberos-Keytab-Funktion muss aktiviert sein
- Suchpfad festlegen
- Nach Credential-Dateien suchen (Hetzner wird ignoriert)
- Prüfen, ob ktutil installiert ist
- Abbrechen, wenn ktutil nicht installiert ist
- Prüfen, welche Keytabs bereits existieren
- Fehlende Keytabs aus Credential-Dateien erzeugen
- Keytabs nach der Erzeugung erneut prüfen
- Fehler melden, falls eine Keytab weiterhin fehlt
- Live-Check | Kerberos-Ticket sofort beziehen
- Ergebnis der Ticket-Prüfung anzeigen
- Cron-Einträge erstellen (alle vier Stunden)
- Kinit für {{ item.item.path | basename }} (Intervall)
- Cron-Einträge erstellen (@reboot)
- Kinit für {{ item.item.path | basename }} (Reboot)

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/identity/generate_keytabs.yml",
  "title": "Playbook playbooks/identity/generate_keytabs.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/identity/generate_keytabs.yml"
  ],
  "source_hashes": {
    "playbooks/identity/generate_keytabs.yml": "84d8a3604125e6a9b6faaffa273237bbe7a2be790ce5d26cbca42e5738ea6416"
  }
}
```

## Quellen und Pflege

- `playbooks/identity/generate_keytabs.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
