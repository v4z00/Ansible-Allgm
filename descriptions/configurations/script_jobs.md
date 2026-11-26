# Jobprotokoll und lokale Konfiguration

Protokollversion 1, Modulstand 0.3.0. Der SQLite-Runner und der Abfragehelfer sind
Teil der neutralen Library. Die Datenbank liegt lokal außerhalb von Code/Releases.
Sie enthält `runs`, `items`, `events`, `reports`, `report_runs`, `deliveries`,
`cursors`, `collection_health` und eigene Metadaten mit Datenbankgeneration.

Ein Lauf hat Hostherkunft, Generation, Lauf-ID, Jobnamen, Kategorie, Status,
UTC-Start/Aktivität/Ende, Exitcode und gegebenenfalls monotone Laufzeit.
Statuswerte: `running`, `success`, `failed`, `warning`, `skipped`. Ein Fehler-Exitcode
kann nicht als Erfolg abgeschlossen werden. Einzelobjekte tragen eigene IDs und
Status, beispielsweise VM-/LXC-IDs. Der Runner verhindert überlappende Aufrufe
über einen lokalen Lock und hält ihn auch im Kindprozess. Nach einem abgebrochenen
Vorgänger wird der nicht abgeschlossene Lauf nicht nachträglich zum Erfolg erklärt.

Die JSON-Abfrage `export` liefert Schema, Generation, Aufbewahrungsgrenze,
Lücken-/Neuanbindungsstatus, Ereignisse und nächsten Cursor. Ein Ereignis enthält
ID, Typ, Zeitpunkt und einen gefilterten Lauf-/Einzelobjekt-Schnappschuss.
`watch` liefert pro Ereignis eine NDJSON-Zeile und zusätzliche Heartbeats.
Ein Cursor ist nur innerhalb derselben Generation gültig. Der Controller schreibt
importierte Ergebnisse und Cursor in einer gemeinsamen Transaktion. Wiederholte
Übertragungen ändern die Historie nicht in doppelte Läufe.

Aufbewahrung: abgeschlossene Läufe 90 Tage ab Abschluss, samt zugehörigen Objekten,
Ereignissen und eigenen alten Joblogs. Laufende Vorgänge werden nicht durch die
Altersbereinigung entfernt. Ein verlorener Verlauf bleibt als Lücke sichtbar.
Private Rohlogs werden nicht in die Datenbank übernommen oder gestreamt. Auch
bekannte geheime Konfigurationswerte werden vor der Ereignisablage maskiert.
Die Library ist kein Ersatz für das Vermeiden von Secrets in eigenen Meldungen.

Ein verwaltetes Skript meldet Fortschritt über `hm_job_event MESSAGE` und
Einzelergebnisse über `hm_job_item ID STATUS MESSAGE`. Start/Abschluss übernimmt
der Runner. Alte Mail-/Telegram-Helfer senden innerhalb eines solchen verwalteten
Laufs keine Einzelmeldungen; der zugeordnete Bericht übernimmt den Versand.
Außerhalb eines verwalteten Laufs bleiben die Helfer direkt benutzbar.

Mail verwendet die feste ASCII-Tabelle für Betreff und Nachricht. Telegram bleibt
UTF-8 und hat Erfolg/Fehler/Warn-/Überspringsymbole. Standardmäßig werden
Zertifikate geprüft. Die allgemeine Ansible-Zusammenfassung übernimmt die vorhandene
Einstellung `tls_validate_certs.telegram_notification`; lokale Skriptkonfigurationen
können ausdrücklich `TELEGRAM_VALIDATE_CERTS` als JSON-Boolean setzen. Secrets
werden weder in Prozessargumente noch in den Ergebnisbericht eingebaut.

Für interaktive lokale Programme erhält der Runner ein kontrollierendes Terminal;
ein Cronlauf stellt dadurch keine interaktive Eingabe bereit. Fehlende reale
Konfigurationen, lokale Profile, Geräte oder Schlüsseldaten werden nicht erfunden.

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "artifacts/script-library/bin/script-jobs",
  "title": "Jobprotokoll und lokale Konfiguration",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "artifacts/script-library/bin/script-jobs",
    "artifacts/script-library/lib/python/job_store.py",
    "artifacts/script-library/lib/python/job_notify.py",
    "artifacts/script-library/lib/python/job_expectations.py"
  ],
  "source_hashes": {
    "artifacts/script-library/bin/script-jobs": "967bb307f3fadc4a63847353da4dc53a48ce551e263cae1eef04987726478598",
    "artifacts/script-library/lib/python/job_store.py": "c7d36eaebdc8544f9ace203839dd36002d15bd451ece8f26279269f0fac1db3f",
    "artifacts/script-library/lib/python/job_notify.py": "340b63932a5e0437a2d923b335aab2348f95784c589fb3e931622910c487e65b",
    "artifacts/script-library/lib/python/job_expectations.py": "659be323230c645a05e865e4545708755be5f4a40142570462a1f86ca5982791"
  },
  "i18n": {
    "de": {
      "title": "Jobprotokoll und lokale Konfiguration",
      "description": "# Jobprotokoll und lokale Konfiguration\n\nProtokollversion 1, Modulstand 0.3.0. Der SQLite-Runner und der Abfragehelfer sind\nTeil der neutralen Library. Die Datenbank liegt lokal außerhalb von Code/Releases.\nSie enthält \u0060runs\u0060, \u0060items\u0060, \u0060events\u0060, \u0060reports\u0060, \u0060report_runs\u0060, \u0060deliveries\u0060,\n\u0060cursors\u0060, \u0060collection_health\u0060 und eigene Metadaten mit Datenbankgeneration.\n\nEin Lauf hat Hostherkunft, Generation, Lauf-ID, Jobnamen, Kategorie, Status,\nUTC-Start/Aktivität/Ende, Exitcode und gegebenenfalls monotone Laufzeit.\nStatuswerte: \u0060running\u0060, \u0060success\u0060, \u0060failed\u0060, \u0060warning\u0060, \u0060skipped\u0060. Ein Fehler-Exitcode\nkann nicht als Erfolg abgeschlossen werden. Einzelobjekte tragen eigene IDs und\nStatus, beispielsweise VM-/LXC-IDs. Der Runner verhindert überlappende Aufrufe\nüber einen lokalen Lock und hält ihn auch im Kindprozess. Nach einem abgebrochenen\nVorgänger wird der nicht abgeschlossene Lauf nicht nachträglich zum Erfolg erklärt.\n\nDie JSON-Abfrage \u0060export\u0060 liefert Schema, Generation, Aufbewahrungsgrenze,\nLücken-/Neuanbindungsstatus, Ereignisse und nächsten Cursor. Ein Ereignis enthält\nID, Typ, Zeitpunkt und einen gefilterten Lauf-/Einzelobjekt-Schnappschuss.\n\u0060watch\u0060 liefert pro Ereignis eine NDJSON-Zeile und zusätzliche Heartbeats.\nEin Cursor ist nur innerhalb derselben Generation gültig. Der Controller schreibt\nimportierte Ergebnisse und Cursor in einer gemeinsamen Transaktion. Wiederholte\nÜbertragungen ändern die Historie nicht in doppelte Läufe.\n\nAufbewahrung: abgeschlossene Läufe 90 Tage ab Abschluss, samt zugehörigen Objekten,\nEreignissen und eigenen alten Joblogs. Laufende Vorgänge werden nicht durch die\nAltersbereinigung entfernt. Ein verlorener Verlauf bleibt als Lücke sichtbar.\nPrivate Rohlogs werden nicht in die Datenbank übernommen oder gestreamt. Auch\nbekannte geheime Konfigurationswerte werden vor der Ereignisablage maskiert.\nDie Library ist kein Ersatz für das Vermeiden von Secrets in eigenen Meldungen.\n\nEin verwaltetes Skript meldet Fortschritt über \u0060hm_job_event MESSAGE\u0060 und\nEinzelergebnisse über \u0060hm_job_item ID STATUS MESSAGE\u0060. Start/Abschluss übernimmt\nder Runner. Alte Mail-/Telegram-Helfer senden innerhalb eines solchen verwalteten\nLaufs keine Einzelmeldungen; der zugeordnete Bericht übernimmt den Versand.\nAußerhalb eines verwalteten Laufs bleiben die Helfer direkt benutzbar.\n\nMail verwendet die feste ASCII-Tabelle für Betreff und Nachricht. Telegram bleibt\nUTF-8 und hat Erfolg/Fehler/Warn-/Überspringsymbole. Standardmäßig werden\nZertifikate geprüft. Die allgemeine Ansible-Zusammenfassung übernimmt die vorhandene\nEinstellung \u0060tls_validate_certs.telegram_notification\u0060; lokale Skriptkonfigurationen\nkönnen ausdrücklich \u0060TELEGRAM_VALIDATE_CERTS\u0060 als JSON-Boolean setzen. Secrets\nwerden weder in Prozessargumente noch in den Ergebnisbericht eingebaut.\n\nFür interaktive lokale Programme erhält der Runner ein kontrollierendes Terminal;\nein Cronlauf stellt dadurch keine interaktive Eingabe bereit. Fehlende reale\nKonfigurationen, lokale Profile, Geräte oder Schlüsseldaten werden nicht erfunden.",
      "fields": {}
    },
    "en": {
      "title": "Job protocol and local configuration",
      "description": "# Job protocol and local configuration\n\nProtocol version 1, module version 0.3.0. The SQLite runner and query helper ship in the shared library. Keep the local database outside code and release directories. It contains \u0060runs\u0060, \u0060items\u0060, \u0060events\u0060, \u0060reports\u0060, \u0060report_runs\u0060, \u0060deliveries\u0060, \u0060cursors\u0060, \u0060collection_health\u0060 and metadata identifying the database generation.\n\nEach run records source host, generation, run ID, job, category, status, UTC start/activity/end, exit code and, when available, monotonic duration. Status values are \u0060running\u0060, \u0060success\u0060, \u0060failed\u0060, \u0060warning\u0060 and \u0060skipped\u0060. An error exit cannot be recorded as success. Individual items such as VM/LXC IDs carry their own IDs and status. The runner and child process hold a local lock against overlapping runs. An interrupted predecessor stays incomplete.\n\nThe \u0060export\u0060 JSON response contains the schema, generation, retention boundary, gap/rebind status, events and next cursor. Each event has an ID, type, timestamp and filtered run/item snapshot. \u0060watch\u0060 streams one NDJSON line per event plus heartbeats. Cursors are valid only for their generation. The controller stores imported results and cursor in a single transaction. Replays do not duplicate runs.\n\nCompleted runs, associated items and events, and the job’s own old logs are kept for 90 days after completion. Age cleanup preserves running jobs. Lost history shows as a gap. Private raw logs are neither imported nor streamed. Known secret configuration values are masked before an event is stored. Keep secrets out of your own messages.\n\nManaged scripts report progress with \u0060hm_job_event MESSAGE\u0060 and per-item results with \u0060hm_job_item ID STATUS MESSAGE\u0060. The runner records start and completion. During a managed run, legacy mail/Telegram helpers leave delivery to the assigned report. Outside managed runs the helpers can still send directly.\n\nMail uses the fixed ASCII mapping for subject and body. Telegram keeps UTF-8 and status symbols for success, error, warning and skipped items. Certificate verification defaults to enabled. The Ansible summary uses \u0060tls_validate_certs.telegram_notification\u0060. Local scripts can set \u0060TELEGRAM_VALIDATE_CERTS\u0060 as a JSON Boolean. Process arguments and result reports exclude secrets.\n\nFor interactive local programs the runner provides a controlling terminal. Cron cannot provide interactive input. Supply actual configurations, local profiles, devices and keys where required.",
      "fields": {}
    }
  }
}
```
