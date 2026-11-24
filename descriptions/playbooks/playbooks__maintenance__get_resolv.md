# Playbook playbooks/maintenance/get_resolv.yml

Vorhandener Einstieg: `playbooks/maintenance/get_resolv.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Resolverkonfiguration anzeigen
- resolv.conf lesen
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
  "ref": "playbooks/maintenance/get_resolv.yml",
  "title": "Playbook playbooks/maintenance/get_resolv.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/get_resolv.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/get_resolv.yml": "446a07009858504cc0235469896ef2d2550ce5780606f4f8ca03641e9a131fb5"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/get_resolv.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
