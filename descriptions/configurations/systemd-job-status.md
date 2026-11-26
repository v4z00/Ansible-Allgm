# Bestehende systemd-Dienste in Jobberichte aufnehmen

Das bestehende Skript-Deployment verarbeitet zentrale `script_jobs_systemd_profiles` und
die ausdrückliche Hostauswahl `script_jobs_systemd_selected_profiles`. Die Profile
enthalten feste Dienstnamen und deren erwartete Betriebsart; Skript- oder
Unitdateien werden nicht zur Erkennung ausgelesen. Die Rolle legt die feste Zuordnung als
`systemd.json` neben der Hostdatenbank ab, mit Modus 0600.

```yaml
# group_vars/all: wiederverwendbare Profile
script_jobs_systemd_profiles:
  watcher:
    - unit: example-watcher.service
      mode: active
  lifecycle:
    - unit: example-startup.service
      mode: oneshot
    - unit: example-optional.service
      mode: observe

# host_vars/<host>/script_logic.yml: ausdrueckliche Auswahl
script_jobs_systemd_selected_profiles: [watcher, lifecycle]
```

`active` erwartet einen dauerhaft aktiven Dienst. Ein inaktiver Dienst gilt als
Fehler. `oneshot` akzeptiert einen erfolgreichen, von systemd gespeicherten
Prozessabschluss; ein noch nie ausgeführter Einmalaufruf wird übersprungen.
`observe` meldet aktive Dienste erfolgreich und inaktive neutral übersprungen,
ohne eine Dauerlaufpflicht zu erfinden. Fehler bleiben in jedem Modus Fehler.
Zustandswechsel erscheinen als Warnung. Optional benennt `name` den Job;
standardmäßig heißt er `systemd:<unit-ohne-.service>`. Vorlagen benötigen eine
konkrete Instanz. Unbekannte Profile sowie doppelte ausgewählte Profile, Units oder Jobnamen werden
abgewiesen. Ohne Hostauswahl wird kein Profil aktiviert.

Beim zentralen Sammellauf fragt der installierte Helfer nur feste
systemd-Statusfelder ab. Er schreibt je Dienst eine atomare Momentaufnahme in
die lokale SQLite. Wiederholte Seiten desselben Abrufs erzeugen keine doppelten
Beobachtungen. Import, 90-Tage-Aufbewahrung und zentrale Mail-/Telegram-Summary
verwenden denselben Weg wie andere Jobs. Abweichende oder fehlende installierte
Zuordnungen blockieren die Übernahme veralteter grüner Ergebnisse.

```text
Example-host Dienst example watcher ✅
Example-host Dienst example startup ⏭️
```

Frisch und rein lesend auf dem Host:

```sh
PFAD/bin/script-jobs systemd-status --config /var/lib/script-jobs/systemd.json
```

Dieser Aufruf benötigt keine SQLite. `bin/job-status` zeigt dagegen den letzten
gespeicherten Abfragestand. Der Sammler fordert weder ExecStart noch Environment,
Credentials, Beschreibungen oder Journalinhalte an. Unbekannte Felder und rohe
Fehlertexte werden nicht gespeichert oder übertragen.

Die Ausführung bleibt vollständig bei systemd. Das Deployment erstellt für diese
Liste keine Cronjobs, ersetzt keine Units und startet oder aktiviert keine Dienste.
Es erhält damit MainPID, Benutzer, Neustartverhalten sowie Boot-/Shutdown-Reihenfolge.
Vorhandene Dienstprogramme und deren bisheriger Versand werden durch diese reine
Statusanbindung noch nicht umgeschrieben. Deren spätere Migration braucht die
separat geprüften privaten Quellen und eine bewusste Freigabe.

Eine aktive Unit beweist lediglich den beobachteten Dienstzustand. Fachliche
Gesundheit und alle Ausführungen zwischen zwei Abfragen sind damit nicht belegt.
systemd hält insbesondere Oneshot-Ergebnisse nicht als vollständige Historie über
Neustarts vor. Ein Shutdown-Ereignis kann nach dem nächsten Boot ohne zusätzliche
lokale Ereignisaufzeichnung fehlen. Gespeicherte Beobachtungen bleiben 90 Tage
abfragbar; die Anbindung rekonstruiert keine fehlende Vergangenheit.

Statussemantik: [systemd-D-Bus-Schnittstelle](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.systemd1.html)
und [Diensttypen](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html).

Objektprofile mit `source`, `target` und `services` können zusätzlich private Ordner und explizite Units bereitstellen. Listenprofile behalten die reine Statusanbindung. [Pfadzuordnung, Voraussetzungen und Aktivierung](systemd-job-deployment.md).

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "systemd-job-status",
  "title": "Bestehende systemd-Dienste in Jobberichte aufnehmen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/script_jobs/defaults/main.yml",
    "roles/script_jobs/tasks/main.yml",
    "roles/script_jobs/filter_plugins/local_config.py",
    "artifacts/script-library/lib/python/job_store.py",
    "artifacts/script-library/bin/script-jobs",
    "scripts/job_console.py"
  ],
  "source_hashes": {
    "roles/script_jobs/defaults/main.yml": "d78878e22bb6c06993b645a8a692a4a1ecf03edbc9caea857df1d4f2c28088f6",
    "roles/script_jobs/tasks/main.yml": "38faf5577f57846d1cbc2773f7c16210270ef858382116bfc4787ed169dea324",
    "roles/script_jobs/filter_plugins/local_config.py": "a040e1923a3678db9b1df20c6bdc659490a8f94cc400f5f03cf83ce54f2969e5",
    "artifacts/script-library/bin/script-jobs": "77dd5d1c4a4dd0184fe01edfc9d3b1b4d9ec41ea5e5f0fd64ece86bc361933b4",
    "scripts/job_console.py": "03c27d3957d2f9df811175ca3bf5fc22434554585471379d9ae249cef46e513d",
    "artifacts/script-library/lib/python/job_store.py": "951a7e29be285a417dc61a1bebf97f1fd40f03998db793a85cdb64bf8abaab85"
  },
  "i18n": {
    "de": {
      "title": "Bestehende systemd-Dienste in Jobberichte aufnehmen",
      "description": "# Bestehende systemd-Dienste in Jobberichte aufnehmen\n\nDas bestehende Skript-Deployment verarbeitet zentrale `script_jobs_systemd_profiles` und\ndie ausdrückliche Hostauswahl `script_jobs_systemd_selected_profiles`. Die Profile\nenthalten feste Dienstnamen und deren erwartete Betriebsart; Skript- oder\nUnitdateien werden nicht zur Erkennung ausgelesen. Die Rolle legt die feste Zuordnung als\n`systemd.json` neben der Hostdatenbank ab, mit Modus 0600.\n\n```yaml\n# group_vars/all: wiederverwendbare Profile\nscript_jobs_systemd_profiles:\n  watcher:\n    - unit: example-watcher.service\n      mode: active\n  lifecycle:\n    - unit: example-startup.service\n      mode: oneshot\n    - unit: example-optional.service\n      mode: observe\n\n# host_vars/<host>/script_logic.yml: ausdrueckliche Auswahl\nscript_jobs_systemd_selected_profiles: [watcher, lifecycle]\n```\n\n`active` erwartet einen dauerhaft aktiven Dienst. Ein inaktiver Dienst gilt als\nFehler. `oneshot` akzeptiert einen erfolgreichen, von systemd gespeicherten\nProzessabschluss; ein noch nie ausgeführter Einmalaufruf wird übersprungen.\n`observe` meldet aktive Dienste erfolgreich und inaktive neutral übersprungen,\nohne eine Dauerlaufpflicht zu erfinden. Fehler bleiben in jedem Modus Fehler.\nZustandswechsel erscheinen als Warnung. Optional benennt `name` den Job;\nstandardmäßig heißt er `systemd:<unit-ohne-.service>`. Vorlagen benötigen eine\nkonkrete Instanz. Unbekannte Profile sowie doppelte ausgewählte Profile, Units oder Jobnamen werden\nabgewiesen. Ohne Hostauswahl wird kein Profil aktiviert.\n\nBeim zentralen Sammellauf fragt der installierte Helfer nur feste\nsystemd-Statusfelder ab. Er schreibt je Dienst eine atomare Momentaufnahme in\ndie lokale SQLite. Wiederholte Seiten desselben Abrufs erzeugen keine doppelten\nBeobachtungen. Import, 90-Tage-Aufbewahrung und zentrale Mail-/Telegram-Summary\nverwenden denselben Weg wie andere Jobs. Abweichende oder fehlende installierte\nZuordnungen blockieren die Übernahme veralteter grüner Ergebnisse.\n\n```text\nExample-host Dienst example watcher ✅\nExample-host Dienst example startup ⏭️\n```\n\nFrisch und rein lesend auf dem Host:\n\n```sh\nPFAD/bin/script-jobs systemd-status --config /var/lib/script-jobs/systemd.json\n```\n\nDieser Aufruf benötigt keine SQLite. `bin/job-status` zeigt dagegen den letzten\ngespeicherten Abfragestand. Der Sammler fordert weder ExecStart noch Environment,\nCredentials, Beschreibungen oder Journalinhalte an. Unbekannte Felder und rohe\nFehlertexte werden nicht gespeichert oder übertragen.\n\nDie Ausführung bleibt vollständig bei systemd. Das Deployment erstellt für diese\nListe keine Cronjobs, ersetzt keine Units und startet oder aktiviert keine Dienste.\nEs erhält damit MainPID, Benutzer, Neustartverhalten sowie Boot-/Shutdown-Reihenfolge.\nVorhandene Dienstprogramme und deren bisheriger Versand werden durch diese reine\nStatusanbindung noch nicht umgeschrieben. Deren spätere Migration braucht die\nseparat geprüften privaten Quellen und eine bewusste Freigabe.\n\nEine aktive Unit beweist lediglich den beobachteten Dienstzustand. Fachliche\nGesundheit und alle Ausführungen zwischen zwei Abfragen sind damit nicht belegt.\nsystemd hält insbesondere Oneshot-Ergebnisse nicht als vollständige Historie über\nNeustarts vor. Ein Shutdown-Ereignis kann nach dem nächsten Boot ohne zusätzliche\nlokale Ereignisaufzeichnung fehlen. Gespeicherte Beobachtungen bleiben 90 Tage\nabfragbar; die Anbindung rekonstruiert keine fehlende Vergangenheit.\n\nStatussemantik: [systemd-D-Bus-Schnittstelle](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.systemd1.html)\nund [Diensttypen](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html).\n\nObjektprofile mit `source`, `target` und `services` können zusätzlich private Ordner und explizite Units bereitstellen. Listenprofile behalten die reine Statusanbindung. [Pfadzuordnung, Voraussetzungen und Aktivierung](systemd-job-deployment.md).\n",
      "fields": {}
    },
    "en": {
      "title": "Include existing system services in job reports",
      "description": "# Include existing system services in job reports\n\nDefine reusable `script_jobs_systemd_profiles` in private group variables and select\nnames through `script_jobs_systemd_selected_profiles` in each host's script logic.\nThe existing script deployment writes the resolved fixed bindings as mode-0600\n`systemd.json` beside the host database. No script or unit-file inspection is used\nto infer the selection. Unknown profiles, duplicate selections, overlapping units\nand duplicate job names fail validation. An empty selection activates nothing.\n\nEach profile is a list of objects with `unit`, `mode` and optional `name`. Use\n`active` for a continuously required service, `oneshot` for an actual recorded\nsuccessful process exit, and `observe` when inactivity is acceptable. Inactive\nrequired daemons fail; inactive optional services and never-run oneshots are skipped.\nFailures always remain failures and transition states produce warnings.\n\nDuring central collection, the host helper queries only fixed systemd status\nproperties and stores an atomic observation in local SQLite. Repeated pages share\none sample identifier and do not duplicate observations. The existing event import,\n90-day retention and controller-only notification process include these jobs.\nInventory/profile drift blocks stale green results. Service execution, restart\npolicy, MainPID and boot/shutdown ordering stay under the existing system manager.\n\nRun `PATH/bin/script-jobs systemd-status --config /var/lib/script-jobs/systemd.json`\nfor a fresh read-only local observation without creating a database. `bin/job-status`\nshows the last stored observation. Exec commands, environment values, credentials,\ndescriptions, journals and raw diagnostics are never requested or exported.\n\nAn active service is a state observation, not a functional application test. Polling\ncannot reconstruct executions between queries or retain all oneshot outcomes across\nreboots. Shutdown results may be absent after reboot without separate local event\nrecording. This integration does not rewrite the existing private service programs\nor their old notification behavior. That migration needs separately reviewed sources.\n\n\nObject profiles with source, target and services can also deploy private folders and explicit service units. List profiles remain status-only. See [deployment paths and lifecycle settings](systemd-job-deployment.md).\n",
      "fields": {}
    }
  }
}
```
