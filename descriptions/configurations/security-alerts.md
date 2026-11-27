# Immediate security alerts on Linux and Windows

Ordinary job successes/failures stay in the controller summary. Explicit security events
use the local host outbox and send immediately without the controller. Enable
`script_security_enabled: true`, select `script_security_channels: [mail, telegram]`, and
run `playbooks/scripts/security_alerts.yml --limit example-host`. The selected channels
alone are rendered into a protected host config; no secrets belong in SYSVOL or drop-ins.
Existing group-wide Telegram/mail variables supply defaults; normal host_vars override them.

The caller supplies a stable event key and structured job/summary/details. Linux accepts
JSON on stdin through `script-jobs security-alert --event-id KEY --config PRIVATE_FILE`
or `hm_security_alert KEY`. Windows uses `Send-SecurityAlert` and a private config.
An atomic transaction persists the event and channel intents before delivery. Retrying
an event key does not create another alert. Delivery ACKs are per channel. Retry schedules
run locally every minute; the Checkmk outbox check flags undelivered notifications.
A crash after remote acceptance but before the ACK can still cause a duplicate: transport
is at-least-once, not exactly-once. Pending notification reports survive retention.

`script_jobs_smtp` supports host, port, sender, tls, auth, username and password. Set
`auth: none` for the intended internal relay. TLS is independent: `starttls` is default;
`none` must be explicit. Windows supports none/starttls; Python additionally supports
implicit tls. Missing STARTTLS fails without plaintext fallback. Without SMTP_HOST,
Linux/controller may retain the existing mail/mailx transport. German mail text uses the
shared fixed transliteration table; Telegram retains Unicode/emoji. Do not send raw logs.
Deployment creates transports/retries only. Each security detector must call the API;
this preview is not a claim that every existing detector has already been migrated.

<details>
<summary>Deutsch</summary>

# Sicherheitsalarme unmittelbar auf Linux und Windows

Normale Jobs bleiben im zentralen Bericht. Ausdrückliche Sicherheitsereignisse werden
lokal gespeichert und sofort auch ohne Controller gesendet. `script_security_enabled`
aktivieren, die Kanäle in `script_security_channels` wählen und das Sicherheitsplaybook
mit `--limit` ausführen. Nur benötigte Kanalwerte kommen in eine geschützte Hostdatei.
Bestehende Telegram-/Mailwerte aus All bleiben Standard; Hostvariablen können überschreiben.
Keine Zugangsdaten in SYSVOL oder lesbaren Drop-ins ablegen.

Ein stabiler Ereignisschlüssel verhindert doppelte Erfassung. Linux erhält strukturierte
JSON-Daten über stdin, Windows verwendet `Send-SecurityAlert`. Vor dem Netzwerkzugriff
werden Ereignis und beabsichtigte Kanäle atomar gespeichert. Erfolgreiche Kanäle werden
bestätigt und bei Wiederholungen ausgelassen. Ein lokaler Zeitplan versucht offene
Zustellungen minütlich erneut; Checkmk kann den Rückstau anzeigen. Ein Absturz zwischen
Annahme durch den Empfänger und lokaler Bestätigung kann dennoch eine doppelte Nachricht
erzeugen. Offene Alarmberichte werden bei der Aufbewahrungsbereinigung erhalten.

`script_jobs_smtp` enthält host, port, sender, tls, auth sowie optional username/password.
Für das interne Relay `auth: none` setzen. TLS ist getrennt: Standard starttls, Klartext
nur ausdrücklich mit none. Windows unterstützt none/starttls, Python zusätzlich tls.
Fehlendes STARTTLS führt zum Fehler, nicht zur unverschlüsselten Ersatzsendung. Ohne
SMTP bleibt unter Linux der bisherige mail/mailx-Weg möglich. Deutsche Mailzeichen
verwenden die gemeinsame feste Tabelle, Telegram behält Unicode/Smileys.

Die Rolle richtet Versand und Wiederholung ein. Jeder Sicherheitsdetektor muss die
Alarm-API ausdrücklich aufrufen; die vorhandenen Detektoren sind noch nicht vollständig
umgebaut. Keine Rohlogs als Alarmtext übernehmen.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "playbooks/scripts/security_alerts.yml",
  "title": "Sicherheitsalarme unmittelbar auf Linux und Windows",
  "documented": true,
  "fields": [],
  "constraints": [],
  "sources": [
    "artifacts/script-library/lib/common/hm_security_alert.sh",
    "artifacts/script-library/lib/python/job_notify.py",
    "artifacts/script-library/lib/python/job_security.py",
    "playbooks/scripts/security_alerts.yml",
    "roles/script_security_alerts/defaults/main.yml",
    "roles/script_security_alerts/filter_plugins/security_config.py",
    "roles/script_security_alerts/tasks/linux.yml",
    "roles/script_security_alerts/tasks/main.yml",
    "roles/script_security_alerts/tasks/windows.yml"
  ],
  "source_hashes": {
    "artifacts/script-library/lib/common/hm_security_alert.sh": "c49632199db5fd4fda2acd123108aa926d024fc525683c538b982bdc33dd8579",
    "artifacts/script-library/lib/python/job_notify.py": "193b7dd2684f9f4bba059032328be8c6dfd2020a72b62807c481b30268558f96",
    "artifacts/script-library/lib/python/job_security.py": "c46d4a7fe0fa1c3c3452472b829a6d1df5c6a142cc5a450d2e3c400bbd1fdc40",
    "playbooks/scripts/security_alerts.yml": "6a4826a77dbb4f8c6b05997f9ae8c44b5da14b65f30afba5a0451b8059f65a08",
    "roles/script_security_alerts/defaults/main.yml": "8afb61f1708df82384b6c9f1f3983cc96fd663684e3fb65c435c6e2433bf27b0",
    "roles/script_security_alerts/filter_plugins/security_config.py": "ad19715118643aca33470cd58855c440708b59e7c50a672e0e3e34d2659613d7",
    "roles/script_security_alerts/tasks/linux.yml": "16befe4c45e6d877e1572bf249f47442a19172df900cb1fe8b662bed0804ee97",
    "roles/script_security_alerts/tasks/main.yml": "f2e652061739bc5bee61a9c77228f7bb2fa33eb04b196799cf4c2be07dbc0add",
    "roles/script_security_alerts/tasks/windows.yml": "7ee74697d6cbd47da24531b808afdb60d418a110897005794024afa15c33a62e"
  },
  "i18n": {
    "en": {
      "title": "Immediate security alerts on Linux and Windows",
      "description": "# Immediate security alerts on Linux and Windows\n\nOrdinary job successes/failures stay in the controller summary. Explicit security events\nuse the local host outbox and send immediately without the controller. Enable\n`script_security_enabled: true`, select `script_security_channels: [mail, telegram]`, and\nrun `playbooks/scripts/security_alerts.yml --limit example-host`. The selected channels\nalone are rendered into a protected host config; no secrets belong in SYSVOL or drop-ins.\nExisting group-wide Telegram/mail variables supply defaults; normal host_vars override them.\n\nThe caller supplies a stable event key and structured job/summary/details. Linux accepts\nJSON on stdin through `script-jobs security-alert --event-id KEY --config PRIVATE_FILE`\nor `hm_security_alert KEY`. Windows uses `Send-SecurityAlert` and a private config.\nAn atomic transaction persists the event and channel intents before delivery. Retrying\nan event key does not create another alert. Delivery ACKs are per channel. Retry schedules\nrun locally every minute; the Checkmk outbox check flags undelivered notifications.\nA crash after remote acceptance but before the ACK can still cause a duplicate: transport\nis at-least-once, not exactly-once. Pending notification reports survive retention.\n\n`script_jobs_smtp` supports host, port, sender, tls, auth, username and password. Set\n`auth: none` for the intended internal relay. TLS is independent: `starttls` is default;\n`none` must be explicit. Windows supports none/starttls; Python additionally supports\nimplicit tls. Missing STARTTLS fails without plaintext fallback. Without SMTP_HOST,\nLinux/controller may retain the existing mail/mailx transport. German mail text uses the\nshared fixed transliteration table; Telegram retains Unicode/emoji. Do not send raw logs.\nDeployment creates transports/retries only. Each security detector must call the API;\nthis preview is not a claim that every existing detector has already been migrated.",
      "fields": {}
    },
    "de": {
      "title": "Sicherheitsalarme unmittelbar auf Linux und Windows",
      "description": "# Sicherheitsalarme unmittelbar auf Linux und Windows\n\nNormale Jobs bleiben im zentralen Bericht. Ausdrückliche Sicherheitsereignisse werden\nlokal gespeichert und sofort auch ohne Controller gesendet. `script_security_enabled`\naktivieren, die Kanäle in `script_security_channels` wählen und das Sicherheitsplaybook\nmit `--limit` ausführen. Nur benötigte Kanalwerte kommen in eine geschützte Hostdatei.\nBestehende Telegram-/Mailwerte aus All bleiben Standard; Hostvariablen können überschreiben.\nKeine Zugangsdaten in SYSVOL oder lesbaren Drop-ins ablegen.\n\nEin stabiler Ereignisschlüssel verhindert doppelte Erfassung. Linux erhält strukturierte\nJSON-Daten über stdin, Windows verwendet `Send-SecurityAlert`. Vor dem Netzwerkzugriff\nwerden Ereignis und beabsichtigte Kanäle atomar gespeichert. Erfolgreiche Kanäle werden\nbestätigt und bei Wiederholungen ausgelassen. Ein lokaler Zeitplan versucht offene\nZustellungen minütlich erneut; Checkmk kann den Rückstau anzeigen. Ein Absturz zwischen\nAnnahme durch den Empfänger und lokaler Bestätigung kann dennoch eine doppelte Nachricht\nerzeugen. Offene Alarmberichte werden bei der Aufbewahrungsbereinigung erhalten.\n\n`script_jobs_smtp` enthält host, port, sender, tls, auth sowie optional username/password.\nFür das interne Relay `auth: none` setzen. TLS ist getrennt: Standard starttls, Klartext\nnur ausdrücklich mit none. Windows unterstützt none/starttls, Python zusätzlich tls.\nFehlendes STARTTLS führt zum Fehler, nicht zur unverschlüsselten Ersatzsendung. Ohne\nSMTP bleibt unter Linux der bisherige mail/mailx-Weg möglich. Deutsche Mailzeichen\nverwenden die gemeinsame feste Tabelle, Telegram behält Unicode/Smileys.\n\nDie Rolle richtet Versand und Wiederholung ein. Jeder Sicherheitsdetektor muss die\nAlarm-API ausdrücklich aufrufen; die vorhandenen Detektoren sind noch nicht vollständig\numgebaut. Keine Rohlogs als Alarmtext übernehmen.",
      "fields": {}
    }
  }
}
```

</details>
