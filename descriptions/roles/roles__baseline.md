# Rolle baseline

Rolle: `roles/baseline`.

Im Bestand definierte Aufgaben:

- Refresh the APT cache and install base packages

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/baseline",
  "title": "Rolle baseline",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/baseline/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/baseline/tasks/main.yml": "d122b75c8a034516cbdc680d4fdf49525442e31ee47710d696b3e8243f9cf689"
  },
  "i18n": {
    "de": {
      "title": "Rolle baseline",
      "description": "# Rolle baseline\n\nRolle: `roles/baseline`.\n\nIm Bestand definierte Aufgaben:\n\n- Refresh the APT cache and install base packages\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/baseline/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role baseline",
      "description": "# Role baseline\n\nRole: `roles/baseline`.\n\nTask names as written in the role:\n\n- Refresh the APT cache and install base packages\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/baseline/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `roles/baseline/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
