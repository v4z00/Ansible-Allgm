# Playbook playbooks/lynis.yml

Vorhandener Einstieg: `playbooks/lynis.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Lynis Security Audit

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/lynis.yml",
  "title": "Playbook playbooks/lynis.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/lynis.yml"
  ],
  "source_hashes": {
    "playbooks/lynis.yml": "4a395bd1b768357a60a69b1fa97db2d32ef6fa094ff5f690a3476203966d3333"
  }
}
```

## Quellen und Pflege

- `playbooks/lynis.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
