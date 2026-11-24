# Playbook playbooks/network/snmp_check.yml

Vorhandener Einstieg: `playbooks/network/snmp_check.yml`.

Im Quelltext benannte Plays/Aufgaben:

- SNMP-Zugaenge der Netzwerkgeraete pruefen
- SNMP-Client auf dem Controller pruefen
- Fehlende SNMPv2-Community verdeckt abfragen
- SNMPv2-Community fuer den Test festlegen
- SNMP-Konfiguration validieren
- SNMPv2-Verbindung pruefen
- Fehlgeschlagenen SNMPv2-Zugriff einordnen
- SNMPv3-Verbindung pruefen
- Fehlgeschlagenen SNMPv3-Zugriff einordnen
- Erfolgreichen SNMP-Zugriff melden

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/network/snmp_check.yml",
  "title": "Playbook playbooks/network/snmp_check.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/network/snmp_check.yml"
  ],
  "source_hashes": {
    "playbooks/network/snmp_check.yml": "74f48869885be82c55e045078b28f910a8dee92206ef578082845416a0e11c69"
  }
}
```

## Quellen und Pflege

- `playbooks/network/snmp_check.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
