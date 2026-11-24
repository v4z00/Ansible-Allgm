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
    "playbooks/pki/distribute_root_ca.yml": "65499152a5c1c81a8ff0aedaceba11c840713fcb0e55ec1b653a4eadab22e8ed"
  }
}
```

## Quellen und Pflege

- `playbooks/pki/distribute_root_ca.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
