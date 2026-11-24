# Playbook playbooks/base.yml

Vorhandener Einstieg: `playbooks/base.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Gemeinsame Linux-Baseline
- Unterstuetztes Betriebssystem pruefen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/base.yml",
  "title": "Playbook playbooks/base.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/base.yml"
  ],
  "source_hashes": {
    "playbooks/base.yml": "cc3a40a6d53006ed02c6b668ee00dfc8fcb5851fdb4224079213836a8a8f7114"
  }
}
```

## Quellen und Pflege

- `playbooks/base.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
