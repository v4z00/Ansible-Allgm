# Proxmox-Inventory aktualisieren

Proxmox-Inventory aktualisieren

Aufruf: `bin/control inventory [Optionen]`.

Vorhandene Kurzformen: `inv-update`, `inventory`.

Feature: proxmox. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/update_inventory.sh`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "inventory",
  "title": "Proxmox-Inventory aktualisieren",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/inventory.json",
    "bin/control.d/inventory.sh"
  ],
  "source_hashes": {
    "bin/control.d/inventory.json": "44b3088380337f845465df29fa9543843ebfdc0443c4a448ebf8a09cea464173",
    "bin/control.d/inventory.sh": "6024609527250f4a1c286241dc7704f9148b7f364756d25254732fa3844eef22"
  }
}
```

## Quellen und Pflege

- `bin/control.d/inventory.json`
- `bin/control.d/inventory.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
