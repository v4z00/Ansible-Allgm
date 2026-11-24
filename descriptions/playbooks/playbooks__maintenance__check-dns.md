# Playbook playbooks/maintenance/check-dns.yml

Vorhandener Einstieg: `playbooks/maintenance/check-dns.yml`.

Im Quelltext benannte Plays/Aufgaben:

- DNS-Aufloesung pruefen
- Domains aufloesen
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
  "ref": "playbooks/maintenance/check-dns.yml",
  "title": "Playbook playbooks/maintenance/check-dns.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/check-dns.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/check-dns.yml": "a37175b0984ee88c470ff086e1a3569b2e23ae7b875ab938cbdad25f0341641a"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/check-dns.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
