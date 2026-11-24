# Playbook playbooks/security/proxmox_stack_hardening.yml

Vorhandener Einstieg: `playbooks/security/proxmox_stack_hardening.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Proxmox-Weboberflaeche an Management-IP binden
- PVEProxy an die Inventory-Adresse binden
- PVEProxy neu starten
- pveproxy
- PBS-Port auf das Storage-Netz beschraenken
- Persistente iptables-Unterstuetzung installieren
- iptables-persistent
- Erlaubte Quellen fuer PBS-Port eintragen
- Andere Zugriffe auf PBS an der Storage-IP verwerfen
- Firewallregeln persistent speichern

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/security/proxmox_stack_hardening.yml",
  "title": "Playbook playbooks/security/proxmox_stack_hardening.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/security/proxmox_stack_hardening.yml"
  ],
  "source_hashes": {
    "playbooks/security/proxmox_stack_hardening.yml": "ba2f8fd96c3ec230317e1050b869f96ccb493749dea544ceacdedcbb30a47ea3"
  }
}
```

## Quellen und Pflege

- `playbooks/security/proxmox_stack_hardening.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
