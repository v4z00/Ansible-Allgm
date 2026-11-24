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

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "checkmk-download",
  "title": "CheckMK-Agent/Plugins herunterladen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/checkmk-download.json",
    "bin/control.d/checkmk-download.sh",
    "scripts/download_checkmk_artifacts.sh"
  ],
  "source_hashes": {
    "bin/control.d/checkmk-download.json": "18b4d9532adf8ab35ea80178f4ab27a766f8bc30a653e79d5d11868312e29177",
    "bin/control.d/checkmk-download.sh": "9d6fa7c79982948e84952cb37d9b3afcd187bbaa98f89d2649fc9610b429cab9",
    "scripts/download_checkmk_artifacts.sh": "84b960c4956dcdf8ea3a6baabc00e0f440fdb2e72f74186267effd4f840893c1"
  }
}
```

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
Die drei Standorteinrichter setzen Telegram ausdruecklich auf true.
