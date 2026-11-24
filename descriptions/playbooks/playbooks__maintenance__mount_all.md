# Playbook playbooks/maintenance/mount_all.yaml

Vorhandener Einstieg: `playbooks/maintenance/mount_all.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Refresh Mount Points
- Execute mount -a to remount filesystems defined in fstab
- Debug output (optional)

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/mount_all.yaml",
  "title": "Playbook playbooks/maintenance/mount_all.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/mount_all.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/mount_all.yaml": "c8d51609933fbb3e8c0f6cdde5085e83aee33e7e1f150d31c446d463e2564fb6"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/mount_all.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
