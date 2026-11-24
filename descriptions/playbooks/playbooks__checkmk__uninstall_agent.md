# Playbook playbooks/checkmk/uninstall_agent.yml

Vorhandener Einstieg: `playbooks/checkmk/uninstall_agent.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Checkmk Agent entfernen
- Checkmk Agent Socket stoppen, falls vorhanden
- check-mk-agent.socket
- Checkmk Agent Service stoppen, falls vorhanden
- check-mk-agent.service
- Checkmk Agent Pakete entfernen
- Alte Checkmk Agent Verzeichnisse entfernen
- Systemd neu laden
- Prüfen ob Checkmk Agent noch installiert ist
- Ergebnis anzeigen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/checkmk/uninstall_agent.yml",
  "title": "Playbook playbooks/checkmk/uninstall_agent.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/checkmk/uninstall_agent.yml"
  ],
  "source_hashes": {
    "playbooks/checkmk/uninstall_agent.yml": "197d5c7b1bacb2feb264f483cb6cffa3acc81d996ad9895646c332d720b382fe"
  }
}
```

## Quellen und Pflege

- `playbooks/checkmk/uninstall_agent.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
