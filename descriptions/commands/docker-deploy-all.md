# Run all Docker deployment steps

Run all Docker deployment steps

Run: `bin/control docker-deploy-all [options]`.

Aliases: `docker-deploy-all`.

Feature: docker. Control checks availability at runtime.

Set `docker_deploy_pause_summary: false` in your settings or pass `-e '{"docker_deploy_pause_summary":false}'` to print the summary without waiting for Enter. The default is to pause. The report is saved under `x/reports/docker/`. Removing orphan stacks still requires typing `yes` at the terminal. An unattended run leaves them in place. When limiting hosts, include `localhost` for the confirmation and report plays, for example `--limit 'docker-test,localhost'`.

By default, Compose sources live in `docker-configs` next to the controller project (`/root/docker-configs` for `/root/ansible`). The controller uses `local_base_dir`, then `docker_local_base_dir`, then `ANSIBLE_DOCKER_CONFIG_ROOT`. For targets it uses `remote_base_dir`, then `docker_remote_base_dir`, or `/srv/docker-configs` by default. For reports, `controller_reports_dir` takes precedence over `ANSIBLE_REPORTS_DIR`. The default is `x/reports` inside the project. Set `ANSIBLE_PROJECT_ROOT` to override the project path.

Registry prerequisites:
- `playbooks/docker/vars/paths.yml`
- `lib/control/helpers.sh`
- `playbooks/docker/deploy_docker_networks.yaml`
- `playbooks/docker/deploy_docker_stacks.yml`
- `playbooks/docker/deploy_docker_users.yml`
- `playbooks/docker/prepare_deployment.yml`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/docker-deploy-all.json`
- `bin/control.d/docker-deploy-all.sh`
- `lib/control/helpers.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Alle Docker-Schritte ausrollen

Alle Docker-Schritte ausrollen

Aufruf: `bin/control docker-deploy-all [Optionen]`.

Vorhandene Kurzformen: `docker-deploy-all`.

Feature: docker. Die aktuelle Aktivierung prueft weiterhin Control.

Für einen Lauf ohne abschließende Enter-Pause setze `docker_deploy_pause_summary: false` in den Einstellungen oder übergib `-e '{"docker_deploy_pause_summary":false}'`. Das Playbook gibt die Zusammenfassung aus und speichert sie unter `x/reports/docker/`. Ohne Angabe wartet es am Ende auf Enter. Zum Entfernen verwaister Stacks ist weiterhin die Eingabe `yes` am Terminal erforderlich. Ohne Bestätigung bleiben sie bestehen. Bei einem Hostlimit schließe `localhost` für die Bestätigung und die Berichtserstellung ein, zum Beispiel `--limit 'docker-test,localhost'`.

Die Compose-Quellen liegen standardmäßig im Ordner `docker-configs` neben dem Controllerprojekt (`/root/docker-configs` bei `/root/ansible`). Ein gesetztes `local_base_dir` oder `docker_local_base_dir` geht vor `ANSIBLE_DOCKER_CONFIG_ROOT`. Auf den Zielhosts gilt `remote_base_dir`, danach `docker_remote_base_dir`, sonst `/srv/docker-configs`. Für Berichte überschreibt `controller_reports_dir` den Umgebungspfad `ANSIBLE_REPORTS_DIR`. Ohne Vorgabe gilt `x/reports` im Projekt. `ANSIBLE_PROJECT_ROOT` kann den Projektpfad vorgeben.

Voraussetzungen laut Registry:
- `playbooks/docker/vars/paths.yml`
- `lib/control/helpers.sh`
- `playbooks/docker/deploy_docker_networks.yaml`
- `playbooks/docker/deploy_docker_stacks.yml`
- `playbooks/docker/deploy_docker_users.yml`
- `playbooks/docker/prepare_deployment.yml`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `bin/control.d/docker-deploy-all.json`
- `bin/control.d/docker-deploy-all.sh`
- `lib/control/helpers.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "docker-deploy-all",
  "title": "Alle Docker-Schritte ausrollen",
  "documented": true,
  "fields": [
    {
      "id": "targets",
      "label": "targets",
      "description": "Ausgewaehlte Inventory-Hosts/-Gruppen als --limit fuer bestehenden Docker-Ablauf.",
      "type": "array",
      "required": true,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--limit",
        "separator": ","
      },
      "completion": {
        "source": "inventory.targets"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/docker-deploy-all.json",
    "bin/control.d/docker-deploy-all.sh",
    "lib/control/helpers.sh"
  ],
  "source_hashes": {
    "bin/control.d/docker-deploy-all.json": "c8725a3fb371fe2e0cf2685c1b626e3af2fa48d39823ae42f9a69e1be22920cc",
    "bin/control.d/docker-deploy-all.sh": "6b68ffcd6b2aad57fcc3dcad565edd6a59da0b9faa86347bf42acb61ae5634c1",
    "lib/control/helpers.sh": "71898aff95dfffd6873a1e6c4f90e3bdce23c25f6eed0df640dde87afd3bc19e"
  },
  "i18n": {
    "de": {
      "title": "Alle Docker-Schritte ausrollen",
      "description": "# Alle Docker-Schritte ausrollen\n\nAlle Docker-Schritte ausrollen\n\nAufruf: `bin/control docker-deploy-all [Optionen]`.\n\nVorhandene Kurzformen: `docker-deploy-all`.\n\nFeature: docker. Die aktuelle Aktivierung prueft weiterhin Control.\n\nFür einen Lauf ohne abschließende Enter-Pause setze `docker_deploy_pause_summary: false` in den Einstellungen oder übergib `-e '{\"docker_deploy_pause_summary\":false}'`. Das Playbook gibt die Zusammenfassung aus und speichert sie unter `x/reports/docker/`. Ohne Angabe wartet es am Ende auf Enter. Zum Entfernen verwaister Stacks ist weiterhin die Eingabe `yes` am Terminal erforderlich. Ohne Bestätigung bleiben sie bestehen. Bei einem Hostlimit schließe `localhost` für die Bestätigung und die Berichtserstellung ein, zum Beispiel `--limit 'docker-test,localhost'`.\n\nDie Compose-Quellen liegen standardmäßig im Ordner `docker-configs` neben dem Controllerprojekt (`/root/docker-configs` bei `/root/ansible`). Ein gesetztes `local_base_dir` oder `docker_local_base_dir` geht vor `ANSIBLE_DOCKER_CONFIG_ROOT`. Auf den Zielhosts gilt `remote_base_dir`, danach `docker_remote_base_dir`, sonst `/srv/docker-configs`. Für Berichte überschreibt `controller_reports_dir` den Umgebungspfad `ANSIBLE_REPORTS_DIR`. Ohne Vorgabe gilt `x/reports` im Projekt. `ANSIBLE_PROJECT_ROOT` kann den Projektpfad vorgeben.\n\nVoraussetzungen laut Registry:\n- `playbooks/docker/vars/paths.yml`\n- `lib/control/helpers.sh`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/prepare_deployment.yml`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/docker-deploy-all.json`\n- `bin/control.d/docker-deploy-all.sh`\n- `lib/control/helpers.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {
        "targets": {
          "label": "targets",
          "description": "Ausgewaehlte Inventory-Hosts/-Gruppen als --limit fuer bestehenden Docker-Ablauf."
        }
      }
    },
    "en": {
      "title": "Run all Docker deployment steps",
      "description": "# Run all Docker deployment steps\n\nRun all Docker deployment steps\n\nRun: `bin/control docker-deploy-all [options]`.\n\nAliases: `docker-deploy-all`.\n\nFeature: docker. Control checks availability at runtime.\n\nSet `docker_deploy_pause_summary: false` in your settings or pass `-e '{\"docker_deploy_pause_summary\":false}'` to print the summary without waiting for Enter. The default is to pause. The report is saved under `x/reports/docker/`. Removing orphan stacks still requires typing `yes` at the terminal. An unattended run leaves them in place. When limiting hosts, include `localhost` for the confirmation and report plays, for example `--limit 'docker-test,localhost'`.\n\nBy default, Compose sources live in `docker-configs` next to the controller project (`/root/docker-configs` for `/root/ansible`). The controller uses `local_base_dir`, then `docker_local_base_dir`, then `ANSIBLE_DOCKER_CONFIG_ROOT`. For targets it uses `remote_base_dir`, then `docker_remote_base_dir`, or `/srv/docker-configs` by default. For reports, `controller_reports_dir` takes precedence over `ANSIBLE_REPORTS_DIR`. The default is `x/reports` inside the project. Set `ANSIBLE_PROJECT_ROOT` to override the project path.\n\nRegistry prerequisites:\n- `playbooks/docker/vars/paths.yml`\n- `lib/control/helpers.sh`\n- `playbooks/docker/deploy_docker_networks.yaml`\n- `playbooks/docker/deploy_docker_stacks.yml`\n- `playbooks/docker/deploy_docker_users.yml`\n- `playbooks/docker/prepare_deployment.yml`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/docker-deploy-all.json`\n- `bin/control.d/docker-deploy-all.sh`\n- `lib/control/helpers.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {
        "targets": {
          "label": "Target hosts or groups",
          "description": "Pass the selected hosts or inventory groups to the existing Docker workflow as --limit."
        }
      }
    }
  }
}
```

</details>
