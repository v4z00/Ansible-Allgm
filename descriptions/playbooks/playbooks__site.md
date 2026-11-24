# Playbook playbooks/site.yml

Vorhandener Einstieg: `playbooks/site.yml`.

Das Playbook importiert in dieser Reihenfolge.

- `playbooks/base.yml`
- `playbooks/checkmk.yml`
- `playbooks/optional.yml`
- `playbooks/lynis.yml`

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/site.yml",
  "title": "Playbook playbooks/site.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/site.yml"
  ],
  "source_hashes": {
    "playbooks/site.yml": "a1370917868ac4cb7aa2118cf0211e6d21a817d6d13fc41793bf079d1b48d325"
  }
}
```

## Quellen und Pflege

- `playbooks/site.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
