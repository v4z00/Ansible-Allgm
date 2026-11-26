# Ergebnis-Controller einrichten

`playbooks/scripts/setup_controller.yml` richtet ausschließlich den lokalen
Controller ein. Die vorhandene Ansible-Umgebung wird weiterverwendet.

Pflichtwerte: `script_jobs_targets`, `script_jobs_summary_cron` mit Minute/Stunde/
Wochentag und mindestens ein vollständiger Versandkanal (`script_jobs_mail_to`
oder vorhandene `telegram_bot_token`/`telegram_chat_id`). Werte bleiben lokal.

`script_jobs_controller_db` ist standardmäßig
`/var/lib/script-jobs/controller.sqlite3`, `script_jobs_controller_root`
standardmäßig `/root/ansible`. Die private
`config/script_jobs_controller.json` verbindet Control-Helfer, Callback,
Abfrage und Zusammenfassung mit derselben Datenbank. Der eigene Cronname lautet
`script-jobs-summary`. Ein anderer lokaler Cron mit ähnlicher Aufgabe wird nicht
automatisch entfernt; vorhandene Controllerzeitpläne vorher prüfen.

Der Callback erfasst ausschließlich aggregierte Hoststatus, keine Taskargumente,
Nachrichtentexte oder Hostvars. Allgemeine Ergebnisse und eigene Ansible-Läufe
werden gemeinsam konsolidiert, der Vzdump-Bericht bleibt getrennt.

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/script_jobs_controller",
  "title": "Ergebnis-Controller einrichten",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/script_jobs_controller/defaults/main.yml",
    "roles/script_jobs_controller/tasks/main.yml"
  ],
  "source_hashes": {
    "roles/script_jobs_controller/defaults/main.yml": "6ed7c2a5fc02ca90ca0f0b3a36e81ec81ec5f3edd50952c8f170ef57db040cba",
    "roles/script_jobs_controller/tasks/main.yml": "72f1e99feb83af463a9515a92c6eccba4452395d5dcf9ffc5e0e047e6c5cbe67"
  },
  "i18n": {
    "de": {
      "title": "Ergebnis-Controller einrichten",
      "description": "# Ergebnis-Controller einrichten\n\n`playbooks/scripts/setup_controller.yml` richtet ausschließlich den lokalen\nController ein. Die vorhandene Ansible-Umgebung wird weiterverwendet.\n\nPflichtwerte: `script_jobs_targets`, `script_jobs_summary_cron` mit Minute/Stunde/\nWochentag und mindestens ein vollständiger Versandkanal (`script_jobs_mail_to`\noder vorhandene `telegram_bot_token`/`telegram_chat_id`). Werte bleiben lokal.\n\n`script_jobs_controller_db` ist standardmäßig\n`/var/lib/script-jobs/controller.sqlite3`, `script_jobs_controller_root`\nstandardmäßig `/root/ansible`. Die private\n`config/script_jobs_controller.json` verbindet Control-Helfer, Callback,\nAbfrage und Zusammenfassung mit derselben Datenbank. Der eigene Cronname lautet\n`script-jobs-summary`. Ein anderer lokaler Cron mit ähnlicher Aufgabe wird nicht\nautomatisch entfernt; vorhandene Controllerzeitpläne vorher prüfen.\n\nDer Callback erfasst ausschließlich aggregierte Hoststatus, keine Taskargumente,\nNachrichtentexte oder Hostvars. Allgemeine Ergebnisse und eigene Ansible-Läufe\nwerden gemeinsam konsolidiert, der Vzdump-Bericht bleibt getrennt.\n\nTelegram und Mail werden ausschließlich vom Controller versendet. Die Hostrolle\nverteilt keine Versandzugangsdaten. Die bestehenden Variablen aus `group_vars/all`\nund ihre lokalen Überschreibungen gelten weiter. Bei einem Controllerausfall\narbeiten die Hosts selbstständig weiter; Nachrichten werden nachgeholt.\n\n`script_jobs_report_labels` setzt optionale sprechende Namen über die Mappings\n`hosts: {example-host: ServerA}` und `jobs: {backup: Backup}`. Der Jobschlüssel\n`example-host/backup` gilt nur für diesen Host. Die lokale JSON-Datei speichert\ndiese Vorgaben als `labels`.\n`script_jobs_source_overrides` erlaubt je Inventory-Host absolute `root`- und\n`database`-Pfade für getrennte Testablagen; SSH-/Become-Konfiguration bleibt erhalten.\n\nDie Control-Einstiege zeichnen eigene Wartungs-, Docker-Update- und mit passendem\nHomelab-Stand Backup-Ergebnisse auf. Auch Fehler bei der Zielauswahl werden erfasst.\nReine Status- und Summary-Playbooks erzeugen keinen eigenen Berichtsinhalt.\nDie Einrichtung aktiviert nur den ausdrücklich angegebenen Summary-Zeitplan.\nEine spätere Überwachung des Collectors mit Checkmk ist hier nicht enthalten.",
      "fields": {}
    },
    "en": {
      "title": "Set up the results controller",
      "description": "# Set up the results controller\n\n`playbooks/scripts/setup_controller.yml` configures only the local controller and reuses its Ansible environment.\n\nRequired values are `script_jobs_targets`, `script_jobs_summary_cron` with minute/hour/weekday, and at least one complete delivery channel (`script_jobs_mail_to` or existing `telegram_bot_token` and `telegram_chat_id`). Keep values local.\n\n`script_jobs_controller_db` defaults to `/var/lib/script-jobs/controller.sqlite3` and `script_jobs_controller_root` to `/root/ansible`. Private `config/script_jobs_controller.json` points the Control helpers, callback, queries and summary to the same database. The cron entry is named `script-jobs-summary`. Check existing controller schedules first. Similar local cron jobs are not automatically removed.\n\nThe callback stores aggregated host statuses, excluding task arguments, messages and host variables. General results and the controller’s own Ansible runs share a summary. Vzdump uses a separate report.\n\nOnly the controller sends Telegram and email. The host role never distributes delivery credentials. Existing variables under `group_vars/all` and their local overrides continue to apply. During controller downtime, hosts work independently and queued notifications can be delivered later.\n\nConfigure display names with `script_jobs_report_labels` and mappings such as `hosts: {example-host: ServerA}` and `jobs: {backup: Backup}`. A key such as `example-host/backup` applies to that host only. The private JSON stores them as `labels`. `script_jobs_source_overrides` accepts absolute `root` and `database` paths per inventory host for isolated test storage and retains existing SSH/become settings.\n\nControl commands record their maintenance and Docker update results and, with the matching Homelab version, backup results. Target selection failures are included. Status and summary playbooks add no recursive report content. Setup enables only the explicitly supplied summary schedule. Collector monitoring through Checkmk is outside this role.",
      "fields": {}
    }
  }
}
```

Telegram und Mail werden ausschließlich vom Controller versendet. Die Hostrolle
verteilt keine Versandzugangsdaten. Die bestehenden Variablen aus `group_vars/all`
und ihre lokalen Überschreibungen gelten weiter. Bei einem Controllerausfall
arbeiten die Hosts selbstständig weiter; Nachrichten werden nachgeholt.

`script_jobs_report_labels` setzt optionale sprechende Namen über die Mappings
`hosts: {example-host: ServerA}` und `jobs: {backup: Backup}`. Der Jobschlüssel
`example-host/backup` gilt nur für diesen Host. Die lokale JSON-Datei speichert
diese Vorgaben als `labels`.
`script_jobs_source_overrides` erlaubt je Inventory-Host absolute `root`- und
`database`-Pfade für getrennte Testablagen; SSH-/Become-Konfiguration bleibt erhalten.

Die Control-Einstiege zeichnen eigene Wartungs-, Docker-Update- und mit passendem
Homelab-Stand Backup-Ergebnisse auf. Auch Fehler bei der Zielauswahl werden erfasst.
Reine Status- und Summary-Playbooks erzeugen keinen eigenen Berichtsinhalt.
Die Einrichtung aktiviert nur den ausdrücklich angegebenen Summary-Zeitplan.
Eine spätere Überwachung des Collectors mit Checkmk ist hier nicht enthalten.
