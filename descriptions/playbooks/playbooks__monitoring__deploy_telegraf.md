# Playbook playbooks/monitoring/deploy_telegraf.yml

Playbook: `playbooks/monitoring/deploy_telegraf.yml`.

Play and task names as written in the playbook:

- Deploy Telegraf
- Require the Telegraf feature
- Install repository prerequisites
- Create keyring directory
- Download the InfluxData repository key
- Read the InfluxData key fingerprint
- Verify the InfluxData key against the expected fingerprint
- Install the verified InfluxData key
- Ensure correct permissions on the key
- Add InfluxData Repository
- Install Telegraf
- Deploy Telegraf Configuration
- Remove the downloaded repository key
- Force restart Telegraf
- restart_telegraf

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/monitoring/deploy_telegraf.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Per-task TLS certificate validation (1.1.0)

`tls_validate_certs.telegraf_repository_key` in `group_vars/all/settings.yml` controls verification when downloading the InfluxData repository key. It inherits `tls_validate_certs_default` (default true). Explicit false disables this check only.

The site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/monitoring/deploy_telegraf.yml

Vorhandener Einstieg: `playbooks/monitoring/deploy_telegraf.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Deploy Telegraf
- Require the Telegraf feature
- Install repository prerequisites
- Create keyring directory
- Download the InfluxData repository key
- Read the InfluxData key fingerprint
- Verify the InfluxData key against the expected fingerprint
- Install the verified InfluxData key
- Ensure correct permissions on the key
- Add InfluxData Repository
- Install Telegraf
- Deploy Telegraf Configuration
- Remove the downloaded repository key
- Force restart Telegraf
- restart_telegraf

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/monitoring/deploy_telegraf.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.telegraf_repository_key`: InfluxData Repository-Schluessel herunterladen (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/monitoring/deploy_telegraf.yml",
  "title": "Playbook playbooks/monitoring/deploy_telegraf.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/monitoring/deploy_telegraf.yml"
  ],
  "source_hashes": {
    "playbooks/monitoring/deploy_telegraf.yml": "1464f13d88625f105416f05c21b67ce1aa34d1ae30c067d91e374582be4c356c"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/monitoring/deploy_telegraf.yml",
      "description": "# Playbook playbooks/monitoring/deploy_telegraf.yml\n\nVorhandener Einstieg: `playbooks/monitoring/deploy_telegraf.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Deploy Telegraf\n- Require the Telegraf feature\n- Install repository prerequisites\n- Create keyring directory\n- Download the InfluxData repository key\n- Read the InfluxData key fingerprint\n- Verify the InfluxData key against the expected fingerprint\n- Install the verified InfluxData key\n- Ensure correct permissions on the key\n- Add InfluxData Repository\n- Install Telegraf\n- Deploy Telegraf Configuration\n- Remove the downloaded repository key\n- Force restart Telegraf\n- restart_telegraf\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/monitoring/deploy_telegraf.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n\n## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)\n\nOptionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.\nFehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.\n- `tls_validate_certs.telegraf_repository_key`: InfluxData Repository-Schluessel herunterladen (Standard true).\n\nStandortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben\nverwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/monitoring/deploy_telegraf.yml",
      "description": "# Playbook playbooks/monitoring/deploy_telegraf.yml\n\nPlaybook: `playbooks/monitoring/deploy_telegraf.yml`.\n\nPlay and task names as written in the playbook:\n\n- Deploy Telegraf\n- Require the Telegraf feature\n- Install repository prerequisites\n- Create keyring directory\n- Download the InfluxData repository key\n- Read the InfluxData key fingerprint\n- Verify the InfluxData key against the expected fingerprint\n- Install the verified InfluxData key\n- Ensure correct permissions on the key\n- Add InfluxData Repository\n- Install Telegraf\n- Deploy Telegraf Configuration\n- Remove the downloaded repository key\n- Force restart Telegraf\n- restart_telegraf\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/monitoring/deploy_telegraf.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Per-task TLS certificate validation (1.1.0)\n\n`tls_validate_certs.telegraf_repository_key` in `group_vars/all/settings.yml` controls verification when downloading the InfluxData repository key. It inherits `tls_validate_certs_default` (default true). Explicit false disables this check only.\n\nThe site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.",
      "fields": {}
    }
  }
}
```

</details>
