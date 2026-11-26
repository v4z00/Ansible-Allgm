# Rolle motd

Rolle: `roles/motd`.

Im Bestand definierte Aufgaben:

- Install MOTD utilities
- Create the MOTD directory
- Find existing dynamic MOTD scripts
- Disable dynamic MOTD scripts
- Deploy managed dynamic MOTD scripts
- Set the static MOTD
- Report a missing HAP when its display is enabled
- Install the MOTD display command
- Install the MOTD shell alias
- Disable the duplicate static SSH MOTD
- Disable the redundant PAM MOTD entry

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/motd",
  "title": "Rolle motd",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/motd/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/motd/tasks/main.yml": "b801a3e8ae9175c29d6b7ff806f20a870b682a8d6bf01ba4d223ea1f80b6058e"
  },
  "i18n": {
    "de": {
      "title": "Rolle motd",
      "description": "# Rolle motd\n\nRolle: `roles/motd`.\n\nIm Bestand definierte Aufgaben:\n\n- Install MOTD utilities\n- Create the MOTD directory\n- Find existing dynamic MOTD scripts\n- Disable dynamic MOTD scripts\n- Deploy managed dynamic MOTD scripts\n- Set the static MOTD\n- Report a missing HAP when its display is enabled\n- Install the MOTD display command\n- Install the MOTD shell alias\n- Disable the duplicate static SSH MOTD\n- Disable the redundant PAM MOTD entry\n\nDie Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `roles/motd/tasks/main.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Role motd",
      "description": "# Role motd\n\nRole: `roles/motd`.\n\nTask names as written in the role:\n\n- Install MOTD utilities\n- Create the MOTD directory\n- Find existing dynamic MOTD scripts\n- Disable dynamic MOTD scripts\n- Deploy managed dynamic MOTD scripts\n- Set the static MOTD\n- Report a missing HAP when its display is enabled\n- Install the MOTD display command\n- Install the MOTD shell alias\n- Disable the duplicate static SSH MOTD\n- Disable the redundant PAM MOTD entry\n\nThe parameters list public role defaults. Internal facts, registered values and private host credentials are not form inputs.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `roles/motd/tasks/main.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `roles/motd/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
