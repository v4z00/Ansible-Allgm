# Playbook playbooks/docker/prepare_macvlan_parents.yml

Vorhandener Einstieg: `playbooks/docker/prepare_macvlan_parents.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Docker-Macvlan-Konfigurationsnetze vorbereiten
- Macvlan-Definitionen validieren
- Config-only-Macvlan-Netze ermitteln
- Fehlende Config-only-Macvlan-Netze anlegen

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/prepare_macvlan_parents.yml",
  "title": "Playbook playbooks/docker/prepare_macvlan_parents.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/prepare_macvlan_parents.yml"
  ],
  "source_hashes": {
    "playbooks/docker/prepare_macvlan_parents.yml": "b9733dabc973c20f8889f43bcb8591bb5e11bb152832d311e55f62ef675421f0"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/prepare_macvlan_parents.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
