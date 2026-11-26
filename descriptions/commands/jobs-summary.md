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
    "playbooks/scripts/summary_jobs.yml": "ac6fbab4e7add7ba5625df407c92492db49d0e068359539fb34ba8f7eba4ab7f"
  },
  "i18n": {
    "de": {
      "title": "Job-Zusammenfassung senden",
      "description": "# Job-Zusammenfassung senden\n\n`bin/control jobs-summary` sammelt gespeicherte Ergebnisse der privaten\nControllerzielgruppe. `--limit example-host` begrenzt die Abfrage für diesen Lauf.\nEs werden keine Jobs gestartet. Telegram und Mail versendet ausschließlich der\nController, mit `telegram_bot_token`, `telegram_chat_id` und `script_jobs_mail_to`.\nNeue Bots, Topics oder Versandzugangsdaten auf den Hosts sind nicht erforderlich.\n\n\u0060\u0060\u0060text\nJob-Zusammenfassung\n\nServerA Backup ✅\nServerB Backup ❌\n  Quelldatei fehlt.\n\u0060\u0060\u0060\n\nPro Host/Job erscheint eine Zeile mit automatisch gewähltem Symbol. Erfolge\nbenötigen keine Details. Fehler und Warnungen erhalten kurze Erläuterungen.\nInterne Bericht- und Lauf-IDs, Erfolgszähler und technische Statuscodes bleiben\nin SQLite und der Detailabfrage. Mehrere ungemeldete Läufe werden zusammengefasst;\nein Fehler bleibt sichtbar, auch wenn danach ein Lauf erfolgreich war.\nErfolgreiche Einzelobjekte bleiben in SQLite. Telegram bleibt UTF-8; Mail verwendet\ndie feste ASCII-Tabelle einschließlich ae/oe/ue/ss.\n\nVzdump wird getrennt zusammengefasst und ebenfalls zentral gesendet. Fehlende\noder überfällige geplante Läufe erscheinen in ihrer jeweiligen Kategorie.\nEs gibt keine Meldung „wieder erfolgreich“ und keine Sofortmeldungen der Hosts.\nBei einem Controllerausfall laufen Skripte und Cron lokal weiter. Gespeicherte\nErgebnisse werden beim nächsten Sammellauf innerhalb der Aufbewahrung nachgeholt.\n\nMail und Telegram werden getrennt bestätigt. Scheitert ein Kanal, bleibt nur\ndessen Versand offen. Netzwerkversand hält keine SQLite-Transaktion offen.\nNach einem Abbruch zwischen Versand und Bestätigung ist eine Dublette möglich.\nPro Aufruf wird je Kategorie höchstens ein Bericht aus maximal 2000 Läufen\nverarbeitet. Ein größerer Rückstand wird sichtbar gemeldet und später abgearbeitet.\n\nDie Einrichtung erfolgt ausdrücklich über `playbooks/scripts/setup_controller.yml`.\nZeitplan, Zielgruppe und mindestens ein vollständiger Nachrichtenkanal sind Pflicht.\nGit-Aktualisierung allein aktiviert keinen Summary-Cron. Nach der Einrichtung\nerfassen die Control-Einstiege auch eigene Ansible-Ergebnisse; Homelab-Backups\nbenötigen dazu den passenden Homelab-Stand. Alte sofortige Control-Meldungen\nwerden dann durch die Summary ersetzt.\n\n`--config /ABSOLUT/controller-test.json` wählt eine eigene private Konfiguration\nmit `database`, `targets`, optional `labels` und `source_overrides`. Damit können\nbestehende Testdatenbanken abgefragt werden. `source_overrides` erlaubt je\nInventory-Host nur absolute `root`- und `database`-Pfade. Das vorhandene Inventory\nund seine SSH-/Become-Einstellungen werden verwendet.\n\nEine unvollständige Hostabfrage erscheint als Abfragefehler, nicht als erfolgreicher\nBackupjob; der Sammellauf endet dann ungleich null. Interne Abfrage-/Summary-Läufe\nerzeugen keinen rekursiven Berichtsinhalt.\n\nDirekte manuelle Ansible-Aufrufe können den Callback über\n`ANSIBLE_CALLBACK_PLUGINS=tools/callbacks`,\n`ANSIBLE_CALLBACKS_ENABLED=script_job_results`, `SCRIPT_JOBS_CALLBACK=1` und\n`SCRIPT_JOBS_CONTROLLER_DB=/PFAD/controller.sqlite3` verwenden. Bestehende\nCallback-Listen ergänzen.",
      "fields": {}
    },
    "en": {
      "title": "Send a job summary",
      "description": "# Send a job summary\n\n`bin/control jobs-summary` collects stored results for the private controller target group. Narrow collection with `--limit example-host`. Collection starts no jobs. Only the controller sends Telegram and email, using `telegram_bot_token`, `telegram_chat_id` and `script_jobs_mail_to`. Hosts need no new bots, topics or delivery credentials.\n\n\u0060\u0060\u0060text\nJob-Zusammenfassung\n\nServerA Backup ✅\nServerB Backup ❌\n  Quelldatei fehlt.\n\u0060\u0060\u0060\n\nEach host/job gets one line and a status symbol. Errors and warnings include a short explanation. SQLite and detailed queries retain report/run IDs, success counts, status codes and successful individual items. A later success does not hide an unreported failure. Telegram uses UTF-8 and email uses the fixed ASCII mapping, including ae/oe/ue/ss.\n\nThe controller sends a separate Vzdump summary. Missing or overdue scheduled runs appear in their category. Hosts send no immediate notifications, and no recovery notification follows a failure. Jobs and cron continue locally during controller outages. The next collection picks up stored results within their retention period.\n\nEmail and Telegram are acknowledged independently. If one channel fails, only that delivery remains pending. No SQLite transaction stays open during network delivery. Interruption between delivery and acknowledgement can cause duplicates. Each call processes at most one report per category with up to 2,000 runs. Larger backlogs are reported and processed later.\n\nConfigure this explicitly with `playbooks/scripts/setup_controller.yml`. It requires a schedule, targets and at least one complete notification channel. Updating Git alone does not enable summary cron. Configured Control commands also record their Ansible results. Homelab backups require the matching Homelab version. The summary replaces older immediate Control notifications.\n\nSelect a private configuration with `--config /ABSOLUTE/controller-test.json`. It contains `database`, `targets` and optional `labels` and `source_overrides`. This can query existing test databases. Host-specific `source_overrides` accepts only absolute `root` and `database` paths, using the existing inventory and SSH/become settings.\n\nIncomplete host collection is a collection error. It does not count as a successful backup, and collection exits nonzero. Internal queries and summaries do not recursively generate reports.\n\nFor direct Ansible runs, append the callback to existing lists using `ANSIBLE_CALLBACK_PLUGINS=tools/callbacks`, `ANSIBLE_CALLBACKS_ENABLED=script_job_results`, `SCRIPT_JOBS_CALLBACK=1` and `SCRIPT_JOBS_CONTROLLER_DB=/PATH/controller.sqlite3`.",
      "fields": {}
    }
  }
}
```
