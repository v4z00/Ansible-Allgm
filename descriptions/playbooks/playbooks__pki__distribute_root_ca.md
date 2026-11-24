# Playbook playbooks/pki/distribute_root_ca.yml

Vorhandener Einstieg: `playbooks/pki/distribute_root_ca.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Interne Root-CA verteilen
- Ausdrueckliches Ziel pruefen
- Lokale CA-Quelle konfigurieren
- CA-Zertifikat kopieren
- Trust Store aktualisieren

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/pki/distribute_root_ca.yml",
  "title": "Playbook playbooks/pki/distribute_root_ca.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/pki/distribute_root_ca.yml"
  ],
  "source_hashes": {
    "playbooks/pki/distribute_root_ca.yml": "cc023d03ab603feae4cd2d59e9634e0a7a5cb306e58d65f92ec1a286cdabbcbf"
  }
}
```

## Quellen und Pflege

- `playbooks/pki/distribute_root_ca.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
