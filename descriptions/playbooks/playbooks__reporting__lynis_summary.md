# Playbook playbooks/reporting/lynis_summary.yml

Vorhandener Einstieg: `playbooks/reporting/lynis_summary.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Evaluate Lynis Reports
- Parse Lynis Hardening Index
- Parse Critical Warnings
- Render Summary to Variable
- SECURITY AUDIT ZUSAMMENFASSUNG
- Create CSV Export Header
- Update CSV Export data

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/reporting/lynis_summary.yml",
  "title": "Playbook playbooks/reporting/lynis_summary.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/reporting/lynis_summary.yml"
  ],
  "source_hashes": {
    "playbooks/reporting/lynis_summary.yml": "e25b8ca86a25a895d213bfda2d132d99977e01319cf155e87dcef94a83b90af1"
  }
}
```

## Quellen und Pflege

- `playbooks/reporting/lynis_summary.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
