# Rolle motd

Rolle: `roles/motd`.

Im Bestand definierte Aufgaben:

- MOTD-Hilfspakete installieren
- MOTD-Verzeichnis sicherstellen
- Vorhandene dynamische MOTD-Skripte ermitteln
- Dynamische MOTD-Skripte deaktivieren
- Verwaltete dynamische MOTD-Skripte verteilen
- Einheitliche statische MOTD setzen
- Fehlenden HAP bei aktivierter Anzeige melden
- MOTD-Anzeigebefehl installieren
- MOTD-Shellalias bereitstellen
- Doppelte statische SSH-MOTD deaktivieren
- Redundante PAM-MOTD-Zeile deaktivieren

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/motd",
  "title": "Rolle motd",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/motd/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/motd/tasks/main.yml": "77a6b0770712e7cd3cfc6650921a9782bbbfbf5deaee62eebc0b4526bc76be0f"
  }
}
```

## Quellen und Pflege

- `roles/motd/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
