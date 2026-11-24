# Playbook playbooks/optional.yml

Vorhandener Einstieg: `playbooks/optional.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Optionale zentrale Dienste

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/optional.yml",
  "title": "Playbook playbooks/optional.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/optional.yml"
  ],
  "source_hashes": {
    "playbooks/optional.yml": "f07d79d7af5eea9e50d70d8ad1d3baab4d7757c11d9d35c3069006edd3136753"
  }
}
```

## Quellen und Pflege

- `playbooks/optional.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
