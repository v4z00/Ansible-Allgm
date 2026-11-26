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
  },
  "i18n": {
    "de": {
      "title": "Proxmox-Inventory aktualisieren",
      "description": "# Proxmox-Inventory aktualisieren\n\nProxmox-Inventory aktualisieren\n\nAufruf: `bin/control inventory [Optionen]`.\n\nVorhandene Kurzformen: `inv-update`, `inventory`.\n\nFeature: proxmox. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/update_inventory.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/inventory.json`\n- `bin/control.d/inventory.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Refresh the Proxmox inventory",
      "description": "# Refresh the Proxmox inventory\n\nRefresh the Proxmox inventory\n\nRun: `bin/control inventory [options]`.\n\nAliases: `inv-update`, `inventory`.\n\nFeature: proxmox. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/update_inventory.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/inventory.json`\n- `bin/control.d/inventory.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/inventory.json`
- `bin/control.d/inventory.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
