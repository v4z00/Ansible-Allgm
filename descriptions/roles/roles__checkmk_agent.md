# Rolle checkmk_agent

Rolle: `roles/checkmk_agent`.

Im Bestand definierte Aufgaben:

- CheckMK-Konfiguration und Secrets pruefen
- CheckMK-Agentpaket lokal pruefen
- Fehlendes CheckMK-Agentpaket melden
- CheckMK-Hostname festlegen
- CheckMK-Host zentral anlegen oder verschieben
- {{ cmk_hostname }}
- CheckMK-Aenderungen vor Registrierung aktivieren
- CheckMK-Agentpaket kopieren
- CheckMK-Agent installieren
- CheckMK-Pluginliste bestimmen
- CheckMK-Pluginverzeichnisse anlegen
- Vorhandene CheckMK-Plugins verteilen
- CheckMK-TLS-Status auslesen
- CheckMK-Agent per TLS registrieren
- CheckMK-Agent-Socket aktivieren
- check-mk-agent.socket
- Temporaeres Agentpaket entfernen

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/checkmk_agent",
  "title": "Rolle checkmk_agent",
  "documented": false,
  "fields": [
    {
      "id": "checkmk_agent_package_tmp",
      "label": "checkmk_agent_package_tmp",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/tmp/check-mk-agent.deb"
    },
    {
      "id": "checkmk_plugin_base_dir",
      "label": "checkmk_plugin_base_dir",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/usr/lib/check_mk_agent/plugins"
    },
    {
      "id": "checkmk_local_base_dir",
      "label": "checkmk_local_base_dir",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "default": "/usr/lib/check_mk_agent/local"
    },
    {
      "id": "checkmk_linux_base_plugins",
      "label": "checkmk_linux_base_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_docker_plugins",
      "label": "checkmk_docker_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_smart_plugins",
      "label": "checkmk_smart_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_cups_plugins",
      "label": "checkmk_cups_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_webserver_plugins",
      "label": "checkmk_webserver_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    },
    {
      "id": "checkmk_database_plugins",
      "label": "checkmk_database_plugins",
      "description": "Rollen-Default; Bedeutung ueber die aufgefuehrten Tasks pruefen. Keine eigene Feldbeschreibung im Bestand.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "resolution": "dynamisch oder strukturierter Default; Quelle konsultieren"
    }
  ],
  "constraints": [],
  "sources": [
    "roles/checkmk_agent/tasks/main.yml",
    "roles/checkmk_agent/defaults/main.yml"
  ],
  "source_hashes": {
    "roles/checkmk_agent/defaults/main.yml": "3ac93cd4a2232d3e47a3e797cd5a0ca3db1b7343af439291fb90d5935adbdfaf",
    "roles/checkmk_agent/tasks/main.yml": "6c78d0c143ac37cfd2a9e01840dbfb5eb20f669dc471ff0b3ceada35da065392"
  }
}
```

## Quellen und Pflege

- `roles/checkmk_agent/tasks/main.yml`
- `roles/checkmk_agent/defaults/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.


## TLS-Zertifikatspruefung pro Aufgabe (1.1.0)

Optionale Eintraege unter `tls_validate_certs` in `group_vars/all/settings.yml`.
Fehlende Eintraege erben tls_validate_certs_default (ohne Standortstandard true); explizites false deaktiviert nur die genannte Pruefung.
- `tls_validate_certs.checkmk_managed_host`: CheckMK-Host zentral anlegen oder verschieben (Standard true).
- `tls_validate_certs.checkmk_agent_activation`: CheckMK-Aenderungen vor Registrierung aktivieren (Standard true).

Standortstandard: tls_validate_certs_default (ohne Eintrag true). Telegram-Aufgaben
verwenden unabhaengig davon true als Default, ausser bei explizitem Task-Override.
