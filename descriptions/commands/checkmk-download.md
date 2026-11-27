# Download the Checkmk agent and plugins

Download the Checkmk agent and plugins

Run: `bin/control checkmk-download [options]`.

Aliases: `checkmk-download`.

Feature: checkmk. Control checks availability at runtime.

No structured parameter list is available. Use the existing terminal workflow and its help.

Registry prerequisites:
- `lib/control/helpers.sh`
- `scripts/download_checkmk_artifacts.sh`

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `bin/control.d/checkmk-download.json`
- `bin/control.d/checkmk-download.sh`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

## Optional download setting

TLS download option 1.0.0. Certificate validation is enabled by default. For one download without validation, run `CHECKMK_DOWNLOAD_INSECURE=1 bin/control checkmk-download`. Allowed values are 0 (default) and 1. Other values stop the command before downloading. Applies to agent and plugins only. API access, TLS registration, sources, selected version, plugin list and other settings are unaffected.

## Per-task TLS certificate validation (1.1.0)

Add optional keys under `tls_validate_certs` in `group_vars/all/settings.yml`. Each inherits `tls_validate_certs_default`, which defaults to true. An explicit false disables only the named check. Agent packages use `tls_validate_certs.checkmk_agent_download` and agent plugins use `tls_validate_certs.checkmk_plugin_download`. Both default to true.

Explicit YAML entries for agent and plugin downloads take precedence over `CHECKMK_DOWNLOAD_INSECURE`. Otherwise the task inherits `tls_validate_certs_default` (default true). The environment setting is available as a one-time download override. Leave it unset when controlling the two downloads separately.

The site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.

Select `--platform linux|windows|all`; Linux is the unchanged default. Windows downloads the site MSI and explicitly selected Windows plugins.

<details>
<summary>Deutsch</summary>

# CheckMK-Agent/Plugins herunterladen

CheckMK-Agent/Plugins herunterladen

Aufruf: `bin/control checkmk-download [Optionen]`.

Vorhandene Kurzformen: `checkmk-download`.

Feature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/download_checkmk_artifacts.sh`

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `bin/control.d/checkmk-download.json`
- `bin/control.d/checkmk-download.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

## Optionaler Downloadschalter

TLS-DOWNLOADSCHALTER 1.0.0
Standard: TLS-Zertifikatspruefung aktiv.
Einmalig ohne Zertifikatspruefung:
  CHECKMK_DOWNLOAD_INSECURE=1 bin/control checkmk-download
Akzeptiert 0 (Standard) oder 1, andere Werte brechen vor Downloads ab.
Gilt fuer Agent und Plugins, nicht fuer Checkmk-API oder TLS-Registrierung.
Settings, Quelle, Versionsauswahl und Pluginliste bleiben unveraendert.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.checkmk_agent_download`: Agentpaket herunterladen (Standard true).
- `tls_validate_certs.checkmk_plugin_download`: Agentplugins herunterladen (Standard true).

Explizite YAML-Eintraege fuer Agent/Plugins haben Vorrang vor CHECKMK_DOWNLOAD_INSECURE. Ohne Aufgabenschalter gilt tls_validate_certs_default, ohne diesen true. Die bisherige einmalige ENV-Option bleibt als ausdruecklicher Download-Override verfuegbar; explizite Aufgabenschalter haben Vorrang. Fuer getrennte Steuerung keinen ENV-Override setzen.

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.

Mit `--platform linux|windows|all` wählen. Linux bleibt Standard. Windows lädt die Site-MSI und ausdrücklich ausgewählte Windows-Plugins.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "checkmk-download",
  "title": "CheckMK-Agent/Plugins herunterladen",
  "documented": false,
  "fields": [
    {
      "id": "platform",
      "label": "platform",
      "description": "Download platform: linux (default), windows or all.",
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
    "bin/control.d/checkmk-download.json",
    "bin/control.d/checkmk-download.sh",
    "scripts/download_checkmk_artifacts.sh"
  ],
  "source_hashes": {
    "bin/control.d/checkmk-download.json": "18b4d9532adf8ab35ea80178f4ab27a766f8bc30a653e79d5d11868312e29177",
    "bin/control.d/checkmk-download.sh": "ac3731d5aee2840a0c88b4cc59a58405ddc0101769e0d4a2965574e34b255408",
    "scripts/download_checkmk_artifacts.sh": "d8e84ccf2ca1f4a235e9081de370884d8e4bb624aa18914ac88014a3585da1c7"
  },
  "i18n": {
    "de": {
      "title": "CheckMK-Agent/Plugins herunterladen",
      "description": "# CheckMK-Agent/Plugins herunterladen\n\nCheckMK-Agent/Plugins herunterladen\n\nAufruf: `bin/control checkmk-download [Optionen]`.\n\nVorhandene Kurzformen: `checkmk-download`.\n\nFeature: checkmk. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/download_checkmk_artifacts.sh`\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/checkmk-download.json`\n- `bin/control.d/checkmk-download.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.\n\n## Optionaler Downloadschalter\n\nTLS-DOWNLOADSCHALTER 1.0.0\nStandard: TLS-Zertifikatspruefung aktiv.\nEinmalig ohne Zertifikatspruefung:\n  CHECKMK_DOWNLOAD_INSECURE=1 bin/control checkmk-download\nAkzeptiert 0 (Standard) oder 1, andere Werte brechen vor Downloads ab.\nGilt fuer Agent und Plugins, nicht fuer Checkmk-API oder TLS-Registrierung.\nSettings, Quelle, Versionsauswahl und Pluginliste bleiben unveraendert.\n\n\n## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)\n\nOptionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.\nFehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.\n- `tls_validate_certs.checkmk_agent_download`: Agentpaket herunterladen (Standard true).\n- `tls_validate_certs.checkmk_plugin_download`: Agentplugins herunterladen (Standard true).\n\nExplizite YAML-Eintraege fuer Agent/Plugins haben Vorrang vor CHECKMK_DOWNLOAD_INSECURE. Ohne Aufgabenschalter gilt tls_validate_certs_default, ohne diesen true. Die bisherige einmalige ENV-Option bleibt als ausdruecklicher Download-Override verfuegbar; explizite Aufgabenschalter haben Vorrang. Fuer getrennte Steuerung keinen ENV-Override setzen.\n\nStandortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben\nverwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.\n\nMit `--platform linux|windows|all` wählen. Linux bleibt Standard. Windows lädt die Site-MSI und ausdrücklich ausgewählte Windows-Plugins.\n",
      "fields": {
        "platform": {
          "label": "platform",
          "description": "Download platform: linux (default), windows or all."
        }
      }
    },
    "en": {
      "title": "Download the Checkmk agent and plugins",
      "description": "# Download the Checkmk agent and plugins\n\nDownload the Checkmk agent and plugins\n\nRun: `bin/control checkmk-download [options]`.\n\nAliases: `checkmk-download`.\n\nFeature: checkmk. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/download_checkmk_artifacts.sh`\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/checkmk-download.json`\n- `bin/control.d/checkmk-download.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.\n\n## Optional download setting\n\nTLS download option 1.0.0. Certificate validation is enabled by default. For one download without validation, run `CHECKMK_DOWNLOAD_INSECURE=1 bin/control checkmk-download`. Allowed values are 0 (default) and 1. Other values stop the command before downloading. Applies to agent and plugins only. API access, TLS registration, sources, selected version, plugin list and other settings are unaffected.\n\n## Per-task TLS certificate validation (1.1.0)\n\nAdd optional keys under `tls_validate_certs` in `group_vars/all/settings.yml`. Each inherits `tls_validate_certs_default`, which defaults to true. An explicit false disables only the named check. Agent packages use `tls_validate_certs.checkmk_agent_download` and agent plugins use `tls_validate_certs.checkmk_plugin_download`. Both default to true.\n\nExplicit YAML entries for agent and plugin downloads take precedence over `CHECKMK_DOWNLOAD_INSECURE`. Otherwise the task inherits `tls_validate_certs_default` (default true). The environment setting is available as a one-time download override. Leave it unset when controlling the two downloads separately.\n\nThe site default is `tls_validate_certs_default`, normally true. Telegram tasks independently default to true unless their own override is set.\n\nSelect `--platform linux|windows|all`; Linux is the unchanged default. Windows downloads the site MSI and explicitly selected Windows plugins.\n",
      "fields": {
        "platform": {
          "label": "platform",
          "description": "Download platform: linux (default), windows or all."
        }
      }
    }
  }
}
```

</details>
