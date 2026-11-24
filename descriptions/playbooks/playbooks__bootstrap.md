# Playbook playbooks/bootstrap.yml

Vorhandener Einstieg: `playbooks/bootstrap.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Gemeinsamen Root-Zugangsbootstrap laden

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/bootstrap.yml",
  "title": "Playbook playbooks/bootstrap.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/bootstrap.yml"
  ],
  "source_hashes": {
    "playbooks/bootstrap.yml": "2b6d94e35d327ec6851ba33d9f4f2050b106ae133431028d77f2506969570851"
  }
}
```

## Quellen und Pflege

- `playbooks/bootstrap.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
