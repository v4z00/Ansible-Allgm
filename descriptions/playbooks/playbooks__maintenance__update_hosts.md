# Playbook playbooks/maintenance/update_hosts.yaml

Vorhandener Einstieg: `playbooks/maintenance/update_hosts.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Debian-Pakete aktualisieren
- Ausdrueckliches Ziel pruefen
- Debian-Ziel pruefen
- Paketindex und Pakete aktualisieren

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/update_hosts.yaml",
  "title": "Playbook playbooks/maintenance/update_hosts.yaml",
  "documented": false,
  "fields": [
    {
      "id": "host_updates_reboot",
      "label": "Neustart nach Paketupdate",
      "description": "Nur bei ausdruecklich true und vorhandenem /var/run/reboot-required. Dann seriell mit Abbruch bei Fehler; Standard false. Der Cronstarter aktiviert diese Option.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    }
  ],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/update_hosts.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/update_hosts.yaml": "e561e6ed2d1122f45a3807ab4e3aa518c1cb703c32370022904e9d0866562b36"
  }
}
```

## Quellen und Pflege

- `playbooks/maintenance/update_hosts.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

## Optionaler Neustart (Ergaenzung 1.0.1)

Ohne host_updates_reboot=true bleiben Updateverhalten und Parallelitaet erhalten.
Keine Aktivierung in settings.yml oder group_vars vornehmen: Der separate Starter
setzt die Option nur fuer seinen begrenzten Aufruf. Bei Aktivierung werden Hosts
einzeln aktualisiert und bei /var/run/reboot-required neu gestartet. Ansible
prueft die Rueckkehr bis zu 600 Sekunden und wartet danach 15 Sekunden. Fehler
stoppen den gesamten Play vor dem naechsten Host. Check-Mode rebootet nicht;
ein durch einen echten Paketlauf erst entstehender Marker ist dabei nicht vorhersehbar.
Die Markerpruefung ist keine allgemeine Erkennung aller Neustartgruende.

CLI-Uebergabe bei expliziter Anwendung: `--extra-vars '{"host_updates_reboot": true}'`.
Fuer diese Extra-Variable besteht kein geprueftes Formularbinding.
