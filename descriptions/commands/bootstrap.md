# Distribute the SSH key and disable password login only when approved

Distribute the SSH key and disable password login only when approved

Run: `bin/control bootstrap [options]`.

Aliases: `bootstrap`.

Available without a separate feature switch. Control checks availability at runtime.

Registry prerequisites:
- `lib/control/helpers.sh`
- `scripts/run_bootstrap.py`
- `playbooks/bootstrap.yml`
- `playbooks/bootstrap/root_access.yml`
- `playbooks/bootstrap/tasks/prepare_target.yml`
- `roles/bootstrap_ssh/tasks/main.yml`
- `roles/bootstrap_ssh/defaults/main.yml`
- `roles/bootstrap_ssh/handlers/main.yml`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/bootstrap.json`
- `bin/control.d/bootstrap.sh`
- `scripts/run_bootstrap.py`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

The command registry checks that all bootstrap components are present before starting.

For Windows use `bin/control bootstrap --platform windows --limit example-host`. This routes to a separate HTTPS bootstrap (paths, private SIDs, optional timezone and explicit firewall rules), without SSH setup. Linux remains the default interactive workflow.

<details>
<summary>Deutsch</summary>

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

## Quellen und Pflege

- `bin/control.d/bootstrap.json`
- `bin/control.d/bootstrap.sh`
- `scripts/run_bootstrap.py`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

Die Registry prueft die vollstaendigen Bootstrap-Bestandteile vor dem Aufruf.

Windows verwendet `bin/control bootstrap --platform windows --limit example-host`: getrennte HTTPS-Basis mit Pfaden, privaten SIDs und ausdrücklich gewählten Firewall-/Zeitzonenwerten. Linux bleibt der bisherige interaktive Standard.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

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
    },
    {
      "id": "platform",
      "label": "platform",
      "description": "Target platform: linux (default) or windows.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--platform"
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
    "roles/bootstrap_ssh/tasks/main.yml",
    "scripts/run_platform_bootstrap.py",
    "playbooks/windows/bootstrap.yml",
    "roles/windows_bootstrap/tasks/main.yml",
    "roles/windows_private_paths/tasks/main.yml"
  ],
  "source_hashes": {
    "bin/control.d/bootstrap.json": "1282ad2c0e9e4618a7c81f2113b0d680eb43061ef18c9c24a149f29d20436d1f",
    "bin/control.d/bootstrap.sh": "cdd6bdc25caa2802e4c1ad5f360c98329ca18fbfae16375e2f67c76000cb2067",
    "scripts/run_bootstrap.py": "f3d018a7e0487ded4bd39135cae7d315102befb6721bca68f72c59b95454a85f",
    "playbooks/bootstrap/root_access.yml": "2849bfd465ea29572683a29bc70404d43f28ece511b70498de3cea98fdbe435a",
    "playbooks/bootstrap/tasks/prepare_target.yml": "2aa203c91abf438d5db671e64b39c6f9b2b8887e2c927c4d2a22bcad7ccb420e",
    "playbooks/bootstrap.yml": "871d520b4dd81e93c450714e99afaaa48b1a7d1d4f53f3b418820d807372cbf7",
    "roles/bootstrap_ssh/defaults/main.yml": "ea2e0ef76b455a623e9609948662247fb3dc0e7bda7c8dbe34bfb888a2ec4915",
    "roles/bootstrap_ssh/handlers/main.yml": "873766115e1175bc4a93a7a6af88803d4998e945417b008921b5f4af57bca85a",
    "roles/bootstrap_ssh/tasks/main.yml": "d168265533ba97af5f81e007f50a154e4a788f74ba9543ade1cf100e19df228d",
    "scripts/run_platform_bootstrap.py": "207b53757399c2e60ebb6135a10bc1d34889f410675708c9c65bdaa22f90b420",
    "playbooks/windows/bootstrap.yml": "b4a87046013c89827d98bcc07cda098b81fe1767c83b64dd9efd8afce885b3a4",
    "roles/windows_bootstrap/tasks/main.yml": "fea094022dbcfd894b29adcd041afb05b3d799d4c2ba6d3480cf6d864b5cc772",
    "roles/windows_private_paths/tasks/main.yml": "339efbc5858ac5acb1fbd2a53a988be36e60d03aa6f47bc19a80f3b0a9fdb38e"
  },
  "i18n": {
    "de": {
      "title": "SSH-Key verteilen; Passwortabschaltung nur bei Freigabe",
      "description": "# SSH-Key verteilen; Passwortabschaltung nur bei Freigabe\n\nSSH-Key verteilen; Passwortabschaltung nur bei Freigabe\n\nAufruf: `bin/control bootstrap [Optionen]`.\n\nVorhandene Kurzformen: `bootstrap`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/run_bootstrap.py`\n- `playbooks/bootstrap.yml`\n- `playbooks/bootstrap/root_access.yml`\n- `playbooks/bootstrap/tasks/prepare_target.yml`\n- `roles/bootstrap_ssh/tasks/main.yml`\n- `roles/bootstrap_ssh/defaults/main.yml`\n- `roles/bootstrap_ssh/handlers/main.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/bootstrap.json`\n- `bin/control.d/bootstrap.sh`\n- `scripts/run_bootstrap.py`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\nDie Registry prueft die vollstaendigen Bootstrap-Bestandteile vor dem Aufruf.\n\nWindows verwendet `bin/control bootstrap --platform windows --limit example-host`: getrennte HTTPS-Basis mit Pfaden, privaten SIDs und ausdrücklich gewählten Firewall-/Zeitzonenwerten. Linux bleibt der bisherige interaktive Standard.\n",
      "fields": {
        "target": {
          "label": "target",
          "description": "Vorgabe fuer interaktive Auswahl; --target/--limit wird hier NICHT als Playbook-Limit weitergereicht."
        },
        "list_hosts": {
          "label": "list_hosts",
          "description": "Nur aufgeloeste Zielauswahl anzeigen; kein Bootstrap."
        },
        "platform": {
          "label": "platform",
          "description": "Target platform: linux (default) or windows."
        }
      }
    },
    "en": {
      "title": "Distribute the SSH key and disable password login only when approved",
      "description": "# Distribute the SSH key and disable password login only when approved\n\nDistribute the SSH key and disable password login only when approved\n\nRun: `bin/control bootstrap [options]`.\n\nAliases: `bootstrap`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/run_bootstrap.py`\n- `playbooks/bootstrap.yml`\n- `playbooks/bootstrap/root_access.yml`\n- `playbooks/bootstrap/tasks/prepare_target.yml`\n- `roles/bootstrap_ssh/tasks/main.yml`\n- `roles/bootstrap_ssh/defaults/main.yml`\n- `roles/bootstrap_ssh/handlers/main.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/bootstrap.json`\n- `bin/control.d/bootstrap.sh`\n- `scripts/run_bootstrap.py`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\nThe command registry checks that all bootstrap components are present before starting.\n\nFor Windows use `bin/control bootstrap --platform windows --limit example-host`. This routes to a separate HTTPS bootstrap (paths, private SIDs, optional timezone and explicit firewall rules), without SSH setup. Linux remains the default interactive workflow.\n",
      "fields": {
        "target": {
          "label": "target",
          "description": "Preset the interactive selection. In this workflow --target/--limit is not forwarded as a playbook limit."
        },
        "list_hosts": {
          "label": "list_hosts",
          "description": "Show the resolved targets without running bootstrap."
        },
        "platform": {
          "label": "platform",
          "description": "Target platform: linux (default) or windows."
        }
      }
    }
  }
}
```

</details>
