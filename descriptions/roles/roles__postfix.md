# Rolle postfix

Rolle: `roles/postfix`.

Im Bestand definierte Aufgaben:

- Postfix-Konfiguration pruefen
- Postfix-Pakete installieren
- Postfix main.cf verteilen
- Absenderadresse fuer diesen Host bestimmen
- Sender-Canonical-Map verteilen
- SASL-Credentials schreiben
- Postfix aktivieren
- postfix

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/postfix",
  "title": "Rolle postfix",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/postfix/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/postfix/tasks/main.yml": "f22d64fd1eb91a845d293b76ad166d54a0bad82773a6c1e7205dd642525a0ea7"
  }
}
```

## Quellen und Pflege

- `roles/postfix/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
