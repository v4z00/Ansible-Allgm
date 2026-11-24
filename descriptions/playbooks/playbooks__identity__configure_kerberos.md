# Playbook playbooks/identity/configure_kerberos.yml

Vorhandener Einstieg: `playbooks/identity/configure_kerberos.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Kerberos-Client konfigurieren

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/identity/configure_kerberos.yml",
  "title": "Playbook playbooks/identity/configure_kerberos.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/identity/configure_kerberos.yml"
  ],
  "source_hashes": {
    "playbooks/identity/configure_kerberos.yml": "456d44fe33043a503558ae76bb48cf363dea074837b8694b51cc5cbb9c1fc787"
  }
}
```

## Quellen und Pflege

- `playbooks/identity/configure_kerberos.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
