# Rolle security_base

Rolle: `roles/security_base`.

Im Bestand definierte Aufgaben:

- Set the legal login banner
- Harden login.defs
- Optionally remove orphaned packages

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/security_base",
  "title": "Rolle security_base",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/security_base/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/security_base/tasks/main.yml": "b4cf8a30674dedbdde7d208939dedecd3f9dd866659d795fc74e3debb4ae33c4"
  },
  "i18n": {
    "de": {
      "title": "Rolle security_base",
      "description": "# Rolle security_base\n\nRolle: `roles/security_base`.\n\nIm Bestand definierte Aufgaben:\n\n- Set the legal login banner\n- Harden login.defs\n- Optionally remove orphaned packages\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/security_base/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role security_base",
      "description": "# Role security_base\n\nRole: `roles/security_base`.\n\nTask names as written in the role:\n\n- Set the legal login banner\n- Harden login.defs\n- Optionally remove orphaned packages\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/security_base/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `roles/security_base/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
