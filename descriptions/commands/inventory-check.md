# Check a static inventory or the configured Proxmox inventory

Check a static inventory or the configured Proxmox inventory

Run: `bin/control inventory-check [options]`.

Aliases: `inv-check`, `inventory-check`.

This command is available without a feature switch.

No structured parameter list is available. Use the existing terminal workflow and its help.

Registry prerequisites:
- `lib/control/helpers.sh`
- `scripts/update_inventory.sh`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/inventory-check.json`
- `bin/control.d/inventory-check.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

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

## Quellen und Pflege

- `bin/control.d/inventory-check.json`
- `bin/control.d/inventory-check.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
  },
  "i18n": {
    "de": {
      "title": "Statisches oder konfiguriertes Proxmox-Inventory prüfen",
      "description": "# Statisches oder konfiguriertes Proxmox-Inventory prüfen\n\nStatisches oder konfiguriertes Proxmox-Inventory prüfen\n\nAufruf: `bin/control inventory-check [Optionen]`.\n\nVorhandene Kurzformen: `inv-check`, `inventory-check`.\n\nDer Befehl ist unabhängig von einem Feature-Schalter verfügbar.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/update_inventory.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/inventory-check.json`\n- `bin/control.d/inventory-check.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Check a static inventory or the configured Proxmox inventory",
      "description": "# Check a static inventory or the configured Proxmox inventory\n\nCheck a static inventory or the configured Proxmox inventory\n\nRun: `bin/control inventory-check [options]`.\n\nAliases: `inv-check`, `inventory-check`.\n\nThis command is available without a feature switch.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/update_inventory.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/inventory-check.json`\n- `bin/control.d/inventory-check.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
