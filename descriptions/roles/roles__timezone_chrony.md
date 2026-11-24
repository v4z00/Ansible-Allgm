# Rolle timezone_chrony

Rolle: `roles/timezone_chrony`.

Im Bestand definierte Aufgaben:

- Zeitzone konfigurieren
- {{ system_timezone }}
- LXC-/Containerstatus bestimmen
- Chrony nur auf VM oder Hardware konfigurieren
- Chrony installieren
- chrony
- Konkurrierende Zeitdienste deaktivieren
- {{ item }}
- Chrony-Konfiguration verteilen
- Chrony aktivieren
- LXC-Zeitbehandlung dokumentieren

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/timezone_chrony",
  "title": "Rolle timezone_chrony",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/timezone_chrony/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/timezone_chrony/tasks/main.yml": "4ac0e7e107245b6c86f78138a39b2c9f4a68c558ac4d0387c970356a6ba239c1"
  }
}
```

## Quellen und Pflege

- `roles/timezone_chrony/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
