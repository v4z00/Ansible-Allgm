# Job-Zusammenfassung senden

`bin/control jobs-summary` sammelt gespeicherte Ergebnisse der privaten
Controllerzielgruppe. `--limit example-host` begrenzt die Abfrage für diesen Lauf.
Es werden keine Jobs gestartet. Telegram und Mail versendet ausschließlich der
Controller, mit `telegram_bot_token`, `telegram_chat_id` und `script_jobs_mail_to`.
Neue Bots, Topics oder Versandzugangsdaten auf den Hosts sind nicht erforderlich.

```text
Job-Zusammenfassung

ServerA Backup ✅
ServerB Backup ❌
  Quelldatei fehlt.
```

Pro Host/Job erscheint eine Zeile mit automatisch gewähltem Symbol. Erfolge
benötigen keine Details. Fehler und Warnungen erhalten kurze Erläuterungen.
Interne Bericht- und Lauf-IDs, Erfolgszähler und technische Statuscodes bleiben
in SQLite und der Detailabfrage. Mehrere ungemeldete Läufe werden zusammengefasst;
ein Fehler bleibt sichtbar, auch wenn danach ein Lauf erfolgreich war.
Erfolgreiche Einzelobjekte bleiben in SQLite. Telegram bleibt UTF-8; Mail verwendet
die feste ASCII-Tabelle einschließlich ae/oe/ue/ss.

Vzdump wird getrennt zusammengefasst und ebenfalls zentral gesendet. Fehlende
oder überfällige geplante Läufe erscheinen in ihrer jeweiligen Kategorie.
Es gibt keine Meldung „wieder erfolgreich“ und keine Sofortmeldungen der Hosts.
Bei einem Controllerausfall laufen Skripte und Cron lokal weiter. Gespeicherte
Ergebnisse werden beim nächsten Sammellauf innerhalb der Aufbewahrung nachgeholt.

Mail und Telegram werden getrennt bestätigt. Scheitert ein Kanal, bleibt nur
dessen Versand offen. Netzwerkversand hält keine SQLite-Transaktion offen.
Nach einem Abbruch zwischen Versand und Bestätigung ist eine Dublette möglich.
Pro Aufruf wird je Kategorie höchstens ein Bericht aus maximal 2000 Läufen
verarbeitet. Ein größerer Rückstand wird sichtbar gemeldet und später abgearbeitet.

Die Einrichtung erfolgt ausdrücklich über `playbooks/scripts/setup_controller.yml`.
Zeitplan, Zielgruppe und mindestens ein vollständiger Nachrichtenkanal sind Pflicht.
Git-Aktualisierung allein aktiviert keinen Summary-Cron. Nach der Einrichtung
erfassen die Control-Einstiege auch eigene Ansible-Ergebnisse; Homelab-Backups
benötigen dazu den passenden Homelab-Stand. Alte sofortige Control-Meldungen
werden dann durch die Summary ersetzt.

`--config /ABSOLUT/controller-test.json` wählt eine eigene private Konfiguration
mit `database`, `targets`, optional `labels` und `source_overrides`. Damit können
bestehende Testdatenbanken abgefragt werden. `source_overrides` erlaubt je
Inventory-Host nur absolute `root`- und `database`-Pfade. Das vorhandene Inventory
und seine SSH-/Become-Einstellungen werden verwendet.

Eine unvollständige Hostabfrage erscheint als Abfragefehler, nicht als erfolgreicher
Backupjob; der Sammellauf endet dann ungleich null. Interne Abfrage-/Summary-Läufe
erzeugen keinen rekursiven Berichtsinhalt.

Direkte manuelle Ansible-Aufrufe können den Callback über
`ANSIBLE_CALLBACK_PLUGINS=tools/callbacks`,
`ANSIBLE_CALLBACKS_ENABLED=script_job_results`, `SCRIPT_JOBS_CALLBACK=1` und
`SCRIPT_JOBS_CONTROLLER_DB=/PFAD/controller.sqlite3` verwenden. Bestehende
Callback-Listen ergänzen.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "jobs-summary",
  "title": "Job-Zusammenfassung senden",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/jobs-summary.json",
    "bin/control.d/jobs-summary.sh",
    "scripts/job_summary.py",
    "playbooks/scripts/summary_jobs.yml"
  ],
  "source_hashes": {
    "bin/control.d/jobs-summary.json": "cd3547b41629df5f3397605610bdc437c8ccfd521afcd43539f9dc0def260705",
    "bin/control.d/jobs-summary.sh": "74416561b388b1d008581f335039243daff4241be88a850e9bcb26f2f974e853",
    "scripts/job_summary.py": "b5a50589306ad0445faa0faea158925da781e121b72dd8cd256525bfea9c601f",
    "playbooks/scripts/summary_jobs.yml": "d2b50212e653414f5d3feb028083114ed650d53ee3e855c8503b8659148e7063"
  }
}
```
