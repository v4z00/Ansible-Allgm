# Rolle rsyslog

Rolle: `roles/rsyslog`.

Im Bestand definierte Aufgaben:

- Rsyslog-Ziel pruefen
- Rsyslog installieren
- rsyslog
- Kernel-Logging in LXC deaktivieren
- Remote-Weiterleitung konfigurieren
- Rsyslog aktivieren

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/rsyslog",
  "title": "Rolle rsyslog",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/rsyslog/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/rsyslog/tasks/main.yml": "870bef1a818ecd78d13da0bb88ddd5bdfea01dcda2a30fc251d84d20e9d0045e"
  }
}
```

## Quellen und Pflege

- `roles/rsyslog/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
