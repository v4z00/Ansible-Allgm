# SSH-Key verteilen; Passwortabschaltung nur bei Freigabe

SSH-Key verteilen; Passwortabschaltung nur bei Freigabe

Aufruf: `bin/control bootstrap [Optionen]`.

Vorhandene Kurzformen: `bootstrap`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/run_bootstrap.py`
- `playbooks/bootstrap.yml`
- `playbooks/bootstrap/root_access.yml`
- `playbooks/bootstrap/tasks/prepare_target.yml`
- `roles/bootstrap_ssh/tasks/main.yml`
- `roles/bootstrap_ssh/defaults/main.yml`
- `roles/bootstrap_ssh/handlers/main.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "bootstrap",
  "title": "SSH-Key verteilen; Passwortabschaltung nur bei Freigabe",
  "documented": true,
  "fields": [
    {
      "id": "target",
      "label": "target",
      "description": "Vorgabe fuer interaktive Auswahl; --target/--limit wird hier NICHT als Playbook-Limit weitergereicht.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--target"
      },
      "completion": {
        "source": "inventory.targets"
      }
    },
    {
      "id": "list_hosts",
      "label": "list_hosts",
      "description": "Nur aufgeloeste Zielauswahl anzeigen; kein Bootstrap.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--list-hosts"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/bootstrap.json",
    "bin/control.d/bootstrap.sh",
    "scripts/run_bootstrap.py",
    "playbooks/bootstrap/root_access.yml",
    "playbooks/bootstrap/tasks/prepare_target.yml",
    "playbooks/bootstrap.yml",
    "roles/bootstrap_ssh/defaults/main.yml",
    "roles/bootstrap_ssh/handlers/main.yml",
    "roles/bootstrap_ssh/tasks/main.yml"
  ],
  "source_hashes": {
    "bin/control.d/bootstrap.json": "6658fd49d960fd8db800c65d6b2d5abf8d5c0b0d0adc532a2b04020be35bffb5",
    "bin/control.d/bootstrap.sh": "a3938ada49e2ca3b1961571ef25d4cdca5179f5c954bda2b86c69f16a9a2ec9c",
    "scripts/run_bootstrap.py": "8458baf711fdcd1bb9dc504d02112e46d8e1eb3b3b200723f9111c9b5e69d808",
    "playbooks/bootstrap/root_access.yml": "a581fbf803c90c5d99fb97474d678b1af32e5b21895ea0a86237f4ee1530d51a",
    "playbooks/bootstrap/tasks/prepare_target.yml": "496418cf05d6b304b76fd48a0befd07ecf1a4ae6c83f9f4993c005f6d575e013",
    "playbooks/bootstrap.yml": "2b6d94e35d327ec6851ba33d9f4f2050b106ae133431028d77f2506969570851",
    "roles/bootstrap_ssh/defaults/main.yml": "ea2e0ef76b455a623e9609948662247fb3dc0e7bda7c8dbe34bfb888a2ec4915",
    "roles/bootstrap_ssh/handlers/main.yml": "47b649e417080fe52e689d372116a4caecc68db824175576999350d9117cf2c7",
    "roles/bootstrap_ssh/tasks/main.yml": "3641ade83ffefabdf568f3a4a2b2e67183fc7a6c17cee0c44e9dea8361dfbc4c"
  }
}
```

## Quellen und Pflege

- `bin/control.d/bootstrap.json`
- `bin/control.d/bootstrap.sh`
- `scripts/run_bootstrap.py`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

Die Registry prueft die vollstaendigen Bootstrap-Bestandteile vor dem Aufruf.
