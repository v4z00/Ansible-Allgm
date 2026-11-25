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
    "roles/script_jobs_controller/defaults/main.yml": "a70274f7c9a6cd64e44b4dbb8bd54c130188545f5622d4f480c41151dd1aa16a",
    "roles/script_jobs_controller/tasks/main.yml": "83ce948b66200e7a329a47a4cd8cb7f7109b860eeb9b45d483070094f89566e5"
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
