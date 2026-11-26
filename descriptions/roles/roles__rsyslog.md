# Rolle rsyslog

Rolle: `roles/rsyslog`.

Im Bestand definierte Aufgaben:

- Validate the rsyslog destination
- Install rsyslog
- Disable kernel logging in LXC
- Configure remote forwarding
- Enable rsyslog

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/rsyslog",
  "title": "Rolle rsyslog",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/rsyslog/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/rsyslog/tasks/main.yml": "f4b6e1a301065377e24cbd7ffacf989fa399d79ec2b648a141750f83bf4c5019"
  },
  "i18n": {
    "de": {
      "title": "Rolle rsyslog",
      "description": "# Rolle rsyslog\n\nRolle: `roles/rsyslog`.\n\nIm Bestand definierte Aufgaben:\n\n- Validate the rsyslog destination\n- Install rsyslog\n- Disable kernel logging in LXC\n- Configure remote forwarding\n- Enable rsyslog\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/rsyslog/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role rsyslog",
      "description": "# Role rsyslog\n\nRole: `roles/rsyslog`.\n\nTask names as written in the role:\n\n- Validate the rsyslog destination\n- Install rsyslog\n- Disable kernel logging in LXC\n- Configure remote forwarding\n- Enable rsyslog\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/rsyslog/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `roles/rsyslog/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
