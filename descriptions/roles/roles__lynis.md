# Rolle lynis

Rolle: `roles/lynis`.

Im Bestand definierte Aufgaben:

- Install Lynis
- Run the Lynis audit
- Create the local report directory
- Fetch Lynis results

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/lynis",
  "title": "Rolle lynis",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/lynis/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/lynis/tasks/main.yml": "be2dc31e41468774497e3161e75b651e6171d03665b12fd29285b59195424185"
  },
  "i18n": {
    "de": {
      "title": "Rolle lynis",
      "description": "# Rolle lynis\n\nRolle: `roles/lynis`.\n\nIm Bestand definierte Aufgaben:\n\n- Install Lynis\n- Run the Lynis audit\n- Create the local report directory\n- Fetch Lynis results\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/lynis/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role lynis",
      "description": "# Role lynis\n\nRole: `roles/lynis`.\n\nTask names as written in the role:\n\n- Install Lynis\n- Run the Lynis audit\n- Create the local report directory\n- Fetch Lynis results\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/lynis/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `roles/lynis/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
