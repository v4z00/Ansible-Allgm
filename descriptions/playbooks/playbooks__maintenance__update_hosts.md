# Playbook playbooks/maintenance/update_hosts.yaml

Playbook: `playbooks/maintenance/update_hosts.yaml`.

Play and task names as written in the playbook:

- Update Debian packages
- Require an explicit target
- Validate the Debian target
- Update the package index and installed packages
- Check for an optional reboot after package updates
- Check for a pending reboot
- Reboot if required and wait for the host to return

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/maintenance/update_hosts.yaml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Optional reboot (added in 1.0.1)

Without `host_updates_reboot=true`, updates keep their usual parallelism. The separate launcher sets this option only for its limited run. Keep it out of global settings and group variables. When enabled, hosts update serially and reboot if `/var/run/reboot-required` exists. Ansible allows 600 seconds for reconnection, then waits another 15 seconds. Failure stops the play before the next host. Check mode never reboots and cannot predict a marker created only during package changes. The marker covers the reboot reasons reported by participating packages.

To opt in explicitly, use `--extra-vars '{"host_updates_reboot": true}'`. There is no verified form binding for this extra variable.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/maintenance/update_hosts.yaml

Vorhandener Einstieg: `playbooks/maintenance/update_hosts.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Update Debian packages
- Require an explicit target
- Validate the Debian target
- Update the package index and installed packages
- Check for an optional reboot after package updates
- Check for a pending reboot
- Reboot if required and wait for the host to return

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/maintenance/update_hosts.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

## Optionaler Neustart (Ergaenzung 1.0.1)

Ohne host_updates_reboot=true bleiben Updateverhalten und Parallelitaet erhalten.
Keine Aktivierung in settings.yml oder group_vars vornehmen: Der separate Starter
setzt die Option nur fuer seinen begrenzten Aufruf. Bei Aktivierung werden Hosts
einzeln aktualisiert und bei /var/run/reboot-required neu gestartet. Ansible
prueft die Rueckkehr bis zu 600 Sekunden und wartet danach 15 Sekunden. Fehler
stoppen den gesamten Play vor dem naechsten Host. Check-Mode rebootet nicht;
ein durch einen echten Paketlauf erst entstehender Marker ist dabei nicht vorhersehbar.
Die Markerpruefung ist keine allgemeine Erkennung aller Neustartgruende.

CLI-Uebergabe bei expliziter Anwendung: `--extra-vars '{"host_updates_reboot": true}'`.
Fuer diese Extra-Variable besteht kein geprueftes Formularbinding.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/update_hosts.yaml",
  "title": "Playbook playbooks/maintenance/update_hosts.yaml",
  "documented": false,
  "fields": [
    {
      "id": "host_updates_reboot",
      "label": "Neustart nach Paketupdate",
      "description": "Nur bei ausdruecklich true und vorhandenem /var/run/reboot-required. Dann seriell mit Abbruch bei Fehler; Standard false. Der Cronstarter aktiviert diese Option.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "default": false
    }
  ],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/update_hosts.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/update_hosts.yaml": "16c0376541ddf0882f68ed062119c7f89b22827d7154b94b6c17f8f6d213ea0d"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/maintenance/update_hosts.yaml",
      "description": "# Playbook playbooks/maintenance/update_hosts.yaml\n\nVorhandener Einstieg: `playbooks/maintenance/update_hosts.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Update Debian packages\n- Require an explicit target\n- Validate the Debian target\n- Update the package index and installed packages\n- Check for an optional reboot after package updates\n- Check for a pending reboot\n- Reboot if required and wait for the host to return\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/maintenance/update_hosts.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n## Optionaler Neustart (Ergaenzung 1.0.1)\n\nOhne host_updates_reboot=true bleiben Updateverhalten und Parallelitaet erhalten.\nKeine Aktivierung in settings.yml oder group_vars vornehmen: Der separate Starter\nsetzt die Option nur fuer seinen begrenzten Aufruf. Bei Aktivierung werden Hosts\neinzeln aktualisiert und bei /var/run/reboot-required neu gestartet. Ansible\nprueft die Rueckkehr bis zu 600 Sekunden und wartet danach 15 Sekunden. Fehler\nstoppen den gesamten Play vor dem naechsten Host. Check-Mode rebootet nicht;\nein durch einen echten Paketlauf erst entstehender Marker ist dabei nicht vorhersehbar.\nDie Markerpruefung ist keine allgemeine Erkennung aller Neustartgruende.\n\nCLI-Uebergabe bei expliziter Anwendung: `--extra-vars '{\"host_updates_reboot\": true}'`.\nFuer diese Extra-Variable besteht kein geprueftes Formularbinding.",
      "fields": {
        "host_updates_reboot": {
          "label": "Neustart nach Paketupdate",
          "description": "Nur bei ausdruecklich true und vorhandenem /var/run/reboot-required. Dann seriell mit Abbruch bei Fehler; Standard false. Der Cronstarter aktiviert diese Option."
        }
      }
    },
    "en": {
      "title": "Playbook playbooks/maintenance/update_hosts.yaml",
      "description": "# Playbook playbooks/maintenance/update_hosts.yaml\n\nPlaybook: `playbooks/maintenance/update_hosts.yaml`.\n\nPlay and task names as written in the playbook:\n\n- Update Debian packages\n- Require an explicit target\n- Validate the Debian target\n- Update the package index and installed packages\n- Check for an optional reboot after package updates\n- Check for a pending reboot\n- Reboot if required and wait for the host to return\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/maintenance/update_hosts.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Optional reboot (added in 1.0.1)\n\nWithout `host_updates_reboot=true`, updates keep their usual parallelism. The separate launcher sets this option only for its limited run. Keep it out of global settings and group variables. When enabled, hosts update serially and reboot if `/var/run/reboot-required` exists. Ansible allows 600 seconds for reconnection, then waits another 15 seconds. Failure stops the play before the next host. Check mode never reboots and cannot predict a marker created only during package changes. The marker covers the reboot reasons reported by participating packages.\n\nTo opt in explicitly, use `--extra-vars '{\"host_updates_reboot\": true}'`. There is no verified form binding for this extra variable.",
      "fields": {
        "host_updates_reboot": {
          "label": "Reboot after package updates",
          "description": "Reboot only when explicitly true and /var/run/reboot-required exists. Process one host at a time and stop on failure. Defaults to false. The cron launcher enables this option."
        }
      }
    }
  }
}
```

</details>
