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
    "artifacts/script-library/bin/script-jobs": "55b0630be42fac925e6133ba43c3b2b3538f61b798a08ab82f717105ba5d605c",
    "artifacts/script-library/lib/python/job_store.py": "c99bb49bd0792f2a7091c46000dd65592a60f99070c4743a7349b708bbbca811",
    "artifacts/script-library/lib/python/job_notify.py": "340b63932a5e0437a2d923b335aab2348f95784c589fb3e931622910c487e65b",
    "artifacts/script-library/lib/python/job_expectations.py": "659be323230c645a05e865e4545708755be5f4a40142570462a1f86ca5982791"
  }
}
```
