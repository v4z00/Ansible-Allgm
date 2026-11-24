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
    "roles/script_jobs_controller/defaults/main.yml": "a89ca6f96c7a0be37719817eb0642b2c13a39e09cc8f7135f92223254cbeedd7",
    "roles/script_jobs_controller/tasks/main.yml": "a6d332177ed443ccae04bc2dcc87d18cb99a2424d3eca91a76c46b6377efc304"
  }
}
```
