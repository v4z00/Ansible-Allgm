# Rolle accounting

Rolle: `roles/accounting`.

Im Bestand definierte Aufgaben:

- LXC-Umgebung fuer Accounting erkennen
- Passende Accounting-Pakete installieren
- {{ ['sysstat'] if accounting_is_lxc | bool else ['auditd', 'acct', 'sysstat'] }}
- Sysstat-Datensammlung aktivieren
- Sysstat aktivieren
- sysstat
- Prozess-Accounting nur ausserhalb von LXC aktivieren
- acct
- Auditd nur ausserhalb von LXC aktivieren
- auditd
- Accounting-Einschraenkung fuer LXC dokumentieren

Die Parameterliste beschreibt vorhandene oeffentliche Defaults. Task-interne Fakten, Registerwerte und Hostsecrets werden nicht in Eingabeparameter umgedeutet.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/accounting",
  "title": "Rolle accounting",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/accounting/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/accounting/tasks/main.yml": "f4b5f53a6c763381adb97790326b498d3717636b019e2aac32408b0962166f7e"
  }
}
```

## Quellen und Pflege

- `roles/accounting/tasks/main.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
