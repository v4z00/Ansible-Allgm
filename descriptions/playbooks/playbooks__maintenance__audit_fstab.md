# Playbook playbooks/maintenance/audit_fstab.yml

Vorhandener Einstieg: `playbooks/maintenance/audit_fstab.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Audit: Alle fstab Dateien einsammeln
- Ordner für Audit-Logs lokal erstellen
- fstab Datei vom Host abholen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/audit_fstab.yml",
  "title": "Playbook playbooks/maintenance/audit_fstab.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/audit_fstab.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/audit_fstab.yml": "c3019678df30343f53efdee7dd6d6988344620da730dbc17475496ce5439e8d4"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/audit_fstab.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
