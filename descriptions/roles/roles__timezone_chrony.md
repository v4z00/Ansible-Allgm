# Rolle timezone_chrony

Rolle: `roles/timezone_chrony`.

Im Bestand definierte Aufgaben:

- Configure the time zone
- Detect LXC and other containers
- Configure Chrony on virtual machines and physical hosts
- Install Chrony
- Disable competing time services
- Deploy the Chrony configuration
- Enable Chrony
- Report how LXC obtains the host time

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/timezone_chrony",
  "title": "Rolle timezone_chrony",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/timezone_chrony/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/timezone_chrony/tasks/main.yml": "dbd1c42b998f076d5f4a7bf7560943a609c5049d5b92a5ca88abfd027379a377"
  },
  "i18n": {
    "de": {
      "title": "Rolle timezone_chrony",
      "description": "# Rolle timezone_chrony\n\nRolle: `roles/timezone_chrony`.\n\nIm Bestand definierte Aufgaben:\n\n- Configure the time zone\n- Detect LXC and other containers\n- Configure Chrony on virtual machines and physical hosts\n- Install Chrony\n- Disable competing time services\n- Deploy the Chrony configuration\n- Enable Chrony\n- Report how LXC obtains the host time\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/timezone_chrony/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role timezone_chrony",
      "description": "# Role timezone_chrony\n\nRole: `roles/timezone_chrony`.\n\nTask names as written in the role:\n\n- Configure the time zone\n- Detect LXC and other containers\n- Configure Chrony on virtual machines and physical hosts\n- Install Chrony\n- Disable competing time services\n- Deploy the Chrony configuration\n- Enable Chrony\n- Report how LXC obtains the host time\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/timezone_chrony/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `roles/timezone_chrony/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
