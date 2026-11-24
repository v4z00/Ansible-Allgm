# Playbook playbooks/maintenance/prepare_paths.yml

Vorhandener Einstieg: `playbooks/maintenance/prepare_paths.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Explizit konfigurierte Arbeitsverzeichnisse anlegen
- Ausdrueckliches Ziel pruefen
- Absolute Pfade pruefen
- Arbeitsverzeichnisse erstellen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/prepare_paths.yml",
  "title": "Playbook playbooks/maintenance/prepare_paths.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/prepare_paths.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/prepare_paths.yml": "016129444b45fe81222626465482c8b9d1622f48cb62e2046902b431f83d7a95"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/prepare_paths.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
