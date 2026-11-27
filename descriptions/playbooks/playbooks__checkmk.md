# Playbook playbooks/checkmk.yml

Playbook: `playbooks/checkmk.yml`.

Play and task names as written in the playbook:

- Ensure the Checkmk folder hierarchy exists
- Validate the Checkmk API settings for folders
- Create Checkmk folders and their parents
- Manage Checkmk agents and hosts
- Register non-Linux hosts in Checkmk
- Validate the API settings and target folder for manual hosts
- Create the non-Linux host without attributes or ensure it is in the target folder
- Report the Checkmk host requiring manual configuration

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/checkmk.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Per-task TLS certificate validation (1.1.0)

In `group_vars/all/settings.yml`, `tls_validate_certs.checkmk_folders` controls certificate validation for creating Checkmk folders and parents. `tls_validate_certs.checkmk_manual_host` controls creating or placing non-Linux hosts without attributes. Each inherits `tls_validate_certs_default` (default true). An explicit false disables only that check.

The site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/checkmk.yml

Vorhandener Einstieg: `playbooks/checkmk.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Ensure the Checkmk folder hierarchy exists
- Validate the Checkmk API settings for folders
- Create Checkmk folders and their parents
- Manage Checkmk agents and hosts
- Register non-Linux hosts in Checkmk
- Validate the API settings and target folder for manual hosts
- Create the non-Linux host without attributes or ensure it is in the target folder
- Report the Checkmk host requiring manual configuration

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/checkmk.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.checkmk_folders`: CheckMK-Ordner und Elternordner anlegen (Standard true).
- `tls_validate_certs.checkmk_manual_host`: Nicht-Linux-Host ohne Attribute anlegen oder im Zielordner sicherstellen (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/checkmk.yml",
  "title": "Playbook playbooks/checkmk.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/checkmk.yml"
  ],
  "source_hashes": {
    "playbooks/checkmk.yml": "0c256095a4982713aea2890075150b26a794f19416612115aebd847f495300a1"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/checkmk.yml",
      "description": "# Playbook playbooks/checkmk.yml\n\nVorhandener Einstieg: `playbooks/checkmk.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Ensure the Checkmk folder hierarchy exists\n- Validate the Checkmk API settings for folders\n- Create Checkmk folders and their parents\n- Manage Checkmk agents and hosts\n- Register non-Linux hosts in Checkmk\n- Validate the API settings and target folder for manual hosts\n- Create the non-Linux host without attributes or ensure it is in the target folder\n- Report the Checkmk host requiring manual configuration\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/checkmk.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n\n## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)\n\nOptionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.\nFehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.\n- `tls_validate_certs.checkmk_folders`: CheckMK-Ordner und Elternordner anlegen (Standard true).\n- `tls_validate_certs.checkmk_manual_host`: Nicht-Linux-Host ohne Attribute anlegen oder im Zielordner sicherstellen (Standard true).\n\nStandortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben\nverwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/checkmk.yml",
      "description": "# Playbook playbooks/checkmk.yml\n\nPlaybook: `playbooks/checkmk.yml`.\n\nPlay and task names as written in the playbook:\n\n- Ensure the Checkmk folder hierarchy exists\n- Validate the Checkmk API settings for folders\n- Create Checkmk folders and their parents\n- Manage Checkmk agents and hosts\n- Register non-Linux hosts in Checkmk\n- Validate the API settings and target folder for manual hosts\n- Create the non-Linux host without attributes or ensure it is in the target folder\n- Report the Checkmk host requiring manual configuration\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/checkmk.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Per-task TLS certificate validation (1.1.0)\n\nIn `group_vars/all/settings.yml`, `tls_validate_certs.checkmk_folders` controls certificate validation for creating Checkmk folders and parents. `tls_validate_certs.checkmk_manual_host` controls creating or placing non-Linux hosts without attributes. Each inherits `tls_validate_certs_default` (default true). An explicit false disables only that check.\n\nThe site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.",
      "fields": {}
    }
  }
}
```

</details>
