# Playbook playbooks/maintenance/uninstall_chrony.yml

Vorhandener Einstieg: `playbooks/maintenance/uninstall_chrony.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Chrony gezielt deinstallieren
- Ausdrueckliches Ziel pruefen
- Feature pruefen
- Nur Chrony entfernen
- chrony

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/uninstall_chrony.yml",
  "title": "Playbook playbooks/maintenance/uninstall_chrony.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/uninstall_chrony.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/uninstall_chrony.yml": "e37c712578d93c9257aeb0f4775b29cbdb5e001fff92359b403cfa930983d557"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/uninstall_chrony.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
