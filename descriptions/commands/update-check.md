Controllerpruefung 1.1.0: Profile, Datei-SHA und optionale Bereinigung.
Mit `--remote` den freigegebenen Branch `main` über HTTPS prüfen, mit `--apply`
übernehmen. `--auto` nutzt dieselben Zugangsdaten im Cronlauf. Die lokale
`versions.txt` enthält pro Modul Version, HTTPS-Origin und optional den Pfad
zur Token-Datei. Öffentliche Module verwenden anonymen Zugriff. Bei einem
privaten Modul muss die externe Token-Datei dem ausführenden Benutzer gehören
und Modus `0600` haben.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "update-check",
  "title": "Versionen, Settings und Initialkonfiguration",
  "documented": true,
  "fields": [
    {
      "id": "check",
      "label": "check",
      "description": "Erweiterte lokale Konfigurations-/GET-API-Pruefung, keine Schreib-API.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--check"
      }
    },
    {
      "id": "offline",
      "label": "offline",
      "description": "Mit --check keine Netzwerkaufrufe.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--offline"
      }
    },
    {
      "id": "configure",
      "label": "configure",
      "description": "Interaktive Einrichtung mit Vorschau/YES; Terminal erforderlich, nicht mit --json.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--configure"
      }
    },
    {
      "id": "sort_settings",
      "label": "sort-settings",
      "description": "Nur Settings ordnen mit Vorschau/YES; Terminal erforderlich.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--sort-settings"
      }
    },
    {
      "id": "details",
      "label": "details",
      "description": "Auch passende/optionale Feldbefunde anzeigen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--details"
      }
    },
    {
      "id": "json",
      "label": "json",
      "description": "Strukturierter Nur-Lese-Bericht ohne Credentialwerte.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--json"
      }
    },
    {
      "id": "only",
      "label": "only",
      "description": "Komponente, settings, registry oder nxts3 pruefen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--only"
      }
    },
    {
      "id": "field",
      "label": "field",
      "description": "Mit --configure gezielt bekannten Schluessel abfragen; im Terminal wiederholbar.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--field"
      }
    },
    {
      "id": "find_usage",
      "label": "find-usage",
      "description": "Statische Fundstellen einer Variable, keine automatische Loeschung.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--find-usage"
      }
    },
    {
      "id": "timeout",
      "label": "timeout",
      "description": "API-Timeout 1 bis 30 Sekunden, Standard 8.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--timeout"
      }
    },
    {
      "id": "color",
      "label": "Farbausgabe",
      "description": "auto: nur Terminal; always: erzwingen; never: ausschalten. JSON immer farbfrei.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--color"
      }
    },
    {
      "id": "cleanup",
      "label": "cleanup",
      "description": "Freigegebene Altdateien nach Projekt-/Cron-/Systemd-Pruefung, Vorschau und YES archivieren; keine aktiven Dateien loeschen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--cleanup"
      }
    },
    {
      "id": "no-prompt",
      "label": "no-prompt",
      "description": "Keine optionale Bereinigungsfrage im normalen Terminalprueflauf.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--no-prompt"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/update-check.json",
    "bin/control.d/update-check.sh",
    "update_check/check.py",
    "update_check/configure.py",
    "update_check/probes.py",
    "update_check/cleanup.py"
  ],
  "source_hashes": {
    "bin/control.d/update-check.json": "6831f40480f7f59fc7aad9ea2c7870711732800df934ac38539786a97c3a48aa",
    "bin/control.d/update-check.sh": "7cc1fc9287cff92e352ad038519366d7dfd04d4efe99d1c70d980de0c62ac807",
    "update_check/check.py": "0772f74e4c72ce0617c61b1080e13e86657cb791cc4b3bcbb696d6c34740b94e",
    "update_check/configure.py": "c6c675198f99121dbd1d6f550481b2a9190bdb25a4c19d5ec45e7da4fb1340d3",
    "update_check/probes.py": "22dbb65098b7adfce12c0dc0a39df14440748bbf3926416c432f2a7fbf69c75a",
    "update_check/cleanup.py": "b075547b1bfbfc3483563c2d3e79ff5ec2a5b9901a879b352ed45635228b2a36"
  }
}
```
