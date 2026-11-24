# Playbook playbooks/maintenance/set_fstab.yaml

Vorhandener Einstieg: `playbooks/maintenance/set_fstab.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Zentral definierte Mounts verwalten
- Hostbezogene Storage-Definition suchen
- Hostbezogene Storage-Definition laden
- storage_definition
- Verwaltete Mounts festlegen
- Eindeutige Mountnamen und Mountpunkte pruefen
- Mountdefinitionen validieren
- Benoetigte Mounttypen bestimmen
- CIFS-Client installieren
- cifs-utils
- NFS-Client installieren
- nfs-common
- BindFS installieren
- bindfs
- Bereits eingehängte Mountpunkte erkennen
- Mountpunkte anlegen
- Mounts in fstab eintragen und optional einhaengen
- Optionalen Mount-Healthcheck als Cronjob pflegen
- Managed mount healthcheck - {{ item.name }}
- Optionalen Kerberos-Refresh als Cronjob pflegen
- Managed mount refresh - {{ item.name }}
- fstab-Handler jetzt ausfuehren
- fstab validieren
- systemd nach fstab-Aenderung neu laden

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/set_fstab.yaml",
  "title": "Playbook playbooks/maintenance/set_fstab.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/set_fstab.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/set_fstab.yaml": "2470aacd1df703250783e699ea025e25154cee355568039691e460f1a147c2c1"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/set_fstab.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
