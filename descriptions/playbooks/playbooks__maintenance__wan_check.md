# Playbook playbooks/maintenance/wan_check.yaml

Playbook: `playbooks/maintenance/wan_check.yaml`.

Play and task names as written in the playbook:

- Check HTTP availability
- Request the HTTPS endpoint
- Show the result

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/maintenance/wan_check.yaml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Per-task TLS certificate validation (1.1.0)

`tls_validate_certs.wan_check` in `group_vars/all/settings.yml` controls verification when requesting the HTTPS target. It inherits `tls_validate_certs_default` (default true). Explicit false disables this check only.

The site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/maintenance/wan_check.yaml

Vorhandener Einstieg: `playbooks/maintenance/wan_check.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Check HTTP availability
- Request the HTTPS endpoint
- Show the result

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/maintenance/wan_check.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.wan_check`: HTTPS-Ziel abrufen (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/wan_check.yaml",
  "title": "Playbook playbooks/maintenance/wan_check.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/wan_check.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/wan_check.yaml": "55f93f1f3805e8fb384510967e8d5ccfa9084b02bc5bdfa23fba739f1cf21ad2"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/maintenance/wan_check.yaml",
      "description": "# Playbook playbooks/maintenance/wan_check.yaml\n\nVorhandener Einstieg: `playbooks/maintenance/wan_check.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Check HTTP availability\n- Request the HTTPS endpoint\n- Show the result\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/maintenance/wan_check.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n\n## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)\n\nOptionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.\nFehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.\n- `tls_validate_certs.wan_check`: HTTPS-Ziel abrufen (Standard true).\n\nStandortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben\nverwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/maintenance/wan_check.yaml",
      "description": "# Playbook playbooks/maintenance/wan_check.yaml\n\nPlaybook: `playbooks/maintenance/wan_check.yaml`.\n\nPlay and task names as written in the playbook:\n\n- Check HTTP availability\n- Request the HTTPS endpoint\n- Show the result\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/maintenance/wan_check.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Per-task TLS certificate validation (1.1.0)\n\n`tls_validate_certs.wan_check` in `group_vars/all/settings.yml` controls verification when requesting the HTTPS target. It inherits `tls_validate_certs_default` (default true). Explicit false disables this check only.\n\nThe site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.",
      "fields": {}
    }
  }
}
```

</details>
