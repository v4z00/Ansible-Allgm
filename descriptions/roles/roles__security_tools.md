# Rolle security_tools

Rolle: `roles/security_tools`.

Im Bestand definierte Aufgaben:

- Install PAM and security utilities
- Configure needrestart for unattended use

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/security_tools",
  "title": "Rolle security_tools",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/security_tools/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/security_tools/tasks/main.yml": "a2fae472c5679d34d994d935463f13ab67668fa573251cd26e9b6797f5eaafda"
  },
  "i18n": {
    "de": {
      "title": "Rolle security_tools",
      "description": "# Rolle security_tools\n\nRolle: `roles/security_tools`.\n\nIm Bestand definierte Aufgaben:\n\n- Install PAM and security utilities\n- Configure needrestart for unattended use\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/security_tools/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role security_tools",
      "description": "# Role security_tools\n\nRole: `roles/security_tools`.\n\nTask names as written in the role:\n\n- Install PAM and security utilities\n- Configure needrestart for unattended use\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/security_tools/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `roles/security_tools/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
