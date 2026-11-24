# Statisches oder konfiguriertes Proxmox-Inventory prüfen

Statisches oder konfiguriertes Proxmox-Inventory prüfen

Aufruf: `bin/control inventory-check [Optionen]`.

Vorhandene Kurzformen: `inv-check`, `inventory-check`.

Der Befehl ist unabhängig von einem Feature-Schalter verfügbar.

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
  "ref": "inventory-check",
  "title": "Statisches oder konfiguriertes Proxmox-Inventory prüfen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/inventory-check.json",
    "bin/control.d/inventory-check.sh"
  ],
  "source_hashes": {
    "bin/control.d/inventory-check.json": "25afaa0da09a7e798fc50cf94c5de74aa29d5e06ef7b11ec5b3d8a7905bb7913",
    "bin/control.d/inventory-check.sh": "44d1d81bad4b4fede338786a46b81c0ff7ebbe1addc0dcb0dbfcf79b94b8e95e"
  }
}
```

## Quellen und Pflege

- `bin/control.d/inventory-check.json`
- `bin/control.d/inventory-check.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
