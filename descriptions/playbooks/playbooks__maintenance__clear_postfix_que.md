# Playbook playbooks/maintenance/clear_postfix_que.yaml

Vorhandener Einstieg: `playbooks/maintenance/clear_postfix_que.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Postfix-Warteschlange erneut zustellen
- Ausdrueckliches Ziel pruefen
- Feature pruefen
- Warteschlange flushen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/clear_postfix_que.yaml",
  "title": "Playbook playbooks/maintenance/clear_postfix_que.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/clear_postfix_que.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/clear_postfix_que.yaml": "23413bdf20510665cd2f98056c294ca64888dd053f2dfe6efb32b5a91c2dbb28"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/clear_postfix_que.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
