# Playbook playbooks/maintenance/disable_syslog_forwarding.yml

Vorhandener Einstieg: `playbooks/maintenance/disable_syslog_forwarding.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Verwaltete Rsyslog-Weiterleitung entfernen
- Ausdrueckliches Ziel pruefen
- Feature pruefen
- Nur verwaltetes Drop-in entfernen
- Rsyslog-Konfiguration pruefen
- Rsyslog neu starten
- rsyslog

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/disable_syslog_forwarding.yml",
  "title": "Playbook playbooks/maintenance/disable_syslog_forwarding.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/disable_syslog_forwarding.yml"
  ],
  "source_hashes": {
    "playbooks/maintenance/disable_syslog_forwarding.yml": "d547d57cca67f34215e1cb1de3466027e9c4bdd4880a4ef4449cc8f8e997895e"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/disable_syslog_forwarding.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
