# Deploy local scripts with the shared library

Executable operational scripts stay in `/root/skripte-config/<inventory_hostname>/` on the controller. Keep these private sources, custom functions, host values and secrets outside Git. The shared library lives under `artifacts/script-library/`.

```sh
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --syntax-check
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --check
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host
```

Supply a verified local `deployment.json` with `files` entries specifying `path`, `sha256` and `kind`. Supported files include entry scripts, `programs/*.sh`, `config/*.json` and `lib/special/**/*.sh`. Local code cannot replace Git library files. Input hashes are verified before transfer. Rendered destination configurations are separate local files.

| Variable | Meaning and default |
|---|---|
| `script_jobs_source_root` | Local controller source, `/root/skripte-config` |
| `script_jobs_target_root` | Existing `script_path`, otherwise `/scripte` |
| `script_jobs_database_path` | Runtime data outside scripts, `/var/lib/script-jobs/jobs.sqlite3` |
| `script_jobs_owner`, `script_jobs_group` | Run and file owner/group, both `root` |
| `script_jobs_common_config` | Explicit shared JSON values, otherwise `script_library_common_config` or `{}` |
| `script_jobs_job_config` | Explicit per-script values, otherwise `script_library_job_config` or `{}` |
| `script_jobs` | Cron jobs to manage, `[]` |
| `script_jobs_sets` | Reusable local job lists, `{}` |
| `script_jobs_selected_sets` | Selected local sets, `[]` |
| `script_jobs_timezone` | Explicit IANA time zone for schedule checks |

Each job has `name`, `script`, optional list-valued `args` and `user`, a `category` (`general` or `vzdump`), a `cron` block and optionally `expected`. Cron accepts calendar fields or `special_time`. Vzdump requires explicit Monday (`1` or `mon`). `expected.deadline_minutes` and `expected.max_runtime_minutes` identify missing and overdue runs. Complex schedules need explicit `expected.start` and `expected.weekdays` (Monday=0). An incomplete expectation appears unconfigured. Schedule monitoring and execution are independent.

Private source configuration is followed by explicit host variables. At runtime the script-specific file overrides `common.json`, including explicitly empty values. `JOB_DATABASE_PATH` must match the Ansible database mapping. Conflicts fail before writes. Set `JOB_MAX_RUNTIME_SECONDS` to limit runner duration.

Every job in a local database uses the same configured owner. Files and the database use mode 0600, directories and executables 0700. The role follows existing become settings.

Cron management applies only to explicit entries. An unknown legacy invocation, a still-running script or a system-wide cron conflict blocks migration. After review, use the exact old command line as `legacy_command`. Unrelated jobs, unknown files and jobs removed from the selection are not silently deleted.

The role never starts backup scripts. Without a cron list it installs files and SQLite without creating schedules. There are no synthetic disable flags. Pilot the actual cron migration with the intended local configuration.

After merging configuration, the role removes mail/Telegram values and sets legacy delivery flags to false. Empty compatibility fields support older shell programs. Operational credentials such as the backup destination remain in place. All jobs, including Vzdump, record local results only. Managed cron scripts must be present in the verified source manifest.

The library installs `bin/job-status` on every host to read the latest job states without a controller, network access or starting jobs. On the controller, `bin/control jobs-last --limit TARGET` runs the same helper.

Map existing system services through reusable `script_jobs_systemd_profiles`
and the explicit host list `script_jobs_systemd_selected_profiles`. Profiles contain
unit names and `active`, `oneshot` or `observe` modes. Deployment uses the selected
profiles rather than inferring bindings from script or unit files. It writes fixed
status settings next to SQLite. The existing collector includes filtered service
observations in the same central summary. No units or cron schedules are changed
by these bindings. See [systemd status profiles](../configurations/systemd-job-status.md)
for point-in-time and shutdown-history limits.


Object profiles with source, target and services can also deploy private folders and explicit service units. List profiles remain status-only. See [deployment paths and lifecycle settings](../configurations/systemd-job-deployment.md).

`script_jobs_profile_config` holds rendered service-profile JSON settings and
overrides matching `script_jobs_job_config` defaults. This keeps service settings
separate from ordinary cron job configuration.

Status checks merge `script_jobs_expected_defaults`, per-job
`script_jobs_expected_overrides`, then `job.expected`. Both variables default to
empty and do not change execution. Minute/hour schedules support single values,
comma lists, `*`, and `*/N`; `expected.start` can also list explicit `HH:MM` times.
Timezone, start deadline and maximum observed runtime stay explicit local settings.
An older running job remains visible across the next scheduled slot.

<details>
<summary>Deutsch</summary>

# Lokale Skripte mit neutraler Library bereitstellen

Die ausführbaren Betriebsskripte liegen ausschließlich unter
`/root/skripte-config/<inventory_hostname>/` auf dem Controller. Diese privaten
Quellen, Spezialfunktionen, Hostwerte und Secrets gehören nicht in ein Git-Repo.
In `artifacts/script-library/` liegt nur die neutrale Grundbibliothek.

```sh
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --syntax-check
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --check
ansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host
```

Die Rolle verlangt ein geprüftes lokales `deployment.json` mit `files`-Einträgen
(`path`, `sha256`, `kind`). Erlaubt sind Einstiegsskripte, `programs/*.sh`,
`config/*.json` und `lib/special/**/*.sh`. Lokale Quellen dürfen die Git-Library
nicht überschreiben. Eingangs-SHA werden vor dem Übertragen geprüft; gerenderte
Zielkonfigurationen sind bewusst eigenständige lokale Dateien.

| Variable | Bedeutung / Standard |
|---|---|
| `script_jobs_source_root` | Lokale Controllerquelle, `/root/skripte-config` |
| `script_jobs_target_root` | Bestehendes `script_path`, sonst `/scripte` |
| `script_jobs_database_path` | Laufzeitdaten außerhalb der Skripte, `/var/lib/script-jobs/jobs.sqlite3` |
| `script_jobs_owner`, `script_jobs_group` | Ausführungs-/Dateibesitzer, jeweils `root` |
| `script_jobs_common_config` | Ausdrückliche gemeinsame JSON-Werte, sonst bestehendes `script_library_common_config` oder `{}` |
| `script_jobs_job_config` | Ausdrückliche Werte pro Skriptinstanz, sonst `script_library_job_config` oder `{}` |
| `script_jobs` | Ausdrückliche Liste zu verwaltender Cronjobs, `[]` |
| `script_jobs_sets` | Lokal definierte wiederverwendbare Joblisten, `{}` |
| `script_jobs_selected_sets` | Ausgewählte lokale Sets, `[]` |
| `script_jobs_timezone` | Explizite IANA-Zeitzone für Erwartungsprüfung |

Ein Job hat `name`, `script`, optional `args` als Liste und `user`, `category`
(`general`/`vzdump`), einen `cron`-Block und gegebenenfalls `expected`.
Cron kann Kalenderfelder oder `special_time` verwenden. Vzdump benötigt explizit
Montag (`1`/`mon`). `expected.deadline_minutes` und
`expected.max_runtime_minutes` bestimmen fehlende/überfällige Läufe. Komplexe
Zeitpläne benötigen explizite `expected.start`/`expected.weekdays` (Montag=0).
Ein nicht vollständig beschriebener Erwartungsplan wird als unkonfiguriert
angezeigt, niemals als bewiesener Erfolg. Kalenderüberwachung und tatsächliche
Ausführung sind getrennte Dinge.

Konfiguration: private Quelldaten, dann ausdrücklich gesetzte Hostvariablen.
Beim Lauf gilt `common.json`, danach die Skriptdatei. Explizit leere Skriptwerte
überschreiben gemeinsame Werte. `JOB_DATABASE_PATH` muss mit der
Ansible-Datenbankzuordnung übereinstimmen; Konflikte werden vor dem Schreiben
abgewiesen. `JOB_MAX_RUNTIME_SECONDS` kann das Laufzeitlimit des Runners setzen.

Alle Jobs einer lokalen Datenbank verwenden denselben konfigurierten Besitzer.
Die Dateien und Datenbank sind `0600`, Verzeichnisse `0700`, Programme `0700`.
Die Rolle wird unter den vorhandenen Become-Einstellungen ausgeführt.

Cron wird ausschließlich für die expliziten Einträge verwaltet. Ein unbekannter
Altaufruf, ein noch laufendes Skript oder ein systemweiter Cron-Konflikt blockiert
die Umstellung. Eine genaue alte Befehlszeile kann nach Prüfung als
`legacy_command` zugeordnet werden. Fremde Jobs werden nicht gelöscht. Unbekannte
Dateien oder aus der Auswahl entfernte frühere Jobs werden nicht still bereinigt.

Die Rolle startet keine Backupskripte. Ohne Cronliste werden Dateien und SQLite
bereitgestellt, aber kein Zeitplan erfunden. Es gibt keine künstlichen
Deaktivierungsschalter. Für die tatsächliche Cron-Übernahme ist ein Pilot mit der
konkreten lokalen Konfiguration erforderlich.



Bestehende systemd-Dienste werden ueber wiederverwendbare
`script_jobs_systemd_profiles` und die ausdrueckliche Hostauswahl
`script_jobs_systemd_selected_profiles` eingebunden. Die Profile enthalten
Dienstnamen und `active`/`oneshot`/`observe`; das Deployment erkennt diese nicht
aus Skript- oder Unitdateien. Es schreibt die feste Statuszuordnung neben SQLite.
Die zentrale Sammlung uebernimmt nur gefilterte Dienstzustaende in dieselbe Summary.
Details und Grenzen: [systemd-Statusprofile](../configurations/systemd-job-status.md).

Objektprofile mit `source`, `target` und `services` können zusätzlich private Ordner und explizite Units bereitstellen. Listenprofile behalten die reine Statusanbindung. [Pfadzuordnung, Voraussetzungen und Aktivierung](../configurations/systemd-job-deployment.md).

Nach dem Zusammenführen der Konfiguration entfernt die Rolle die Mail-/Telegramwerte
und setzt alte Versandflags auf `false`. Leere Kompatibilitätsfelder halten ältere
Shellprogramme lauffähig. Fachliche Zugangsdaten, etwa zum Backupziel, bleiben
bestehen. Alle Jobs einschließlich Vzdump erfassen ausschließlich lokale Ergebnisse.
Die zu verwaltenden Cron-Skripte müssen im geprüften Quellmanifest enthalten sein.

Die Library verteilt `bin/job-status` auf jeden Host. Es liest den letzten lokalen
Zustand je Job, ohne Controller, Netzwerk oder Jobstart. Der Controller verwendet
denselben Helfer über `bin/control jobs-last --limit ZIEL`.

`script_jobs_profile_config` enthält ausschließlich die gerenderten JSON-Werte
der Dienstprofile. Es überschreibt entsprechende `script_jobs_job_config`-Vorgaben
und hält die Dienstkonfiguration von den normalen Cronjob-Werten getrennt.

Für die Statusprüfung gelten `script_jobs_expected_defaults`, danach die
jobbezogenen `script_jobs_expected_overrides`, danach `job.expected`. Die beiden
Variablen sind standardmäßig leer und verändern keine Ausführung. Uhrzeiten
werden aus einzelnen Stunden/Minuten, Kommalisten, `*` und `*/N` abgeleitet.
Damit werden etwa zweimal tägliche Jobs und Fünf-Minuten-Checks korrekt getrennt.
`expected.start` kann auch eine ausdrückliche Liste von `HH:MM` enthalten.
Zeitzone, Startfrist und maximale Beobachtungsdauer bleiben explizite lokale Werte.
Ein noch laufender alter Job bleibt auch über das nächste Cronfenster sichtbar.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "role",
  "ref": "roles/script_jobs",
  "title": "Lokale Skripte mit neutraler Library bereitstellen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/script_jobs/defaults/main.yml",
    "roles/script_jobs/tasks/main.yml",
    "roles/script_jobs/templates/expectations.json.j2",
    "scripts/job_cron_guard.py",
    "roles/script_jobs/filter_plugins/local_config.py",
    "artifacts/script-library/lib/python/job_store.py"
  ],
  "source_hashes": {
    "roles/script_jobs/defaults/main.yml": "d43bab89763028a7311e916b459847d8db9ea428b4ff625273f5d4a0e427e618",
    "roles/script_jobs/tasks/main.yml": "38faf5577f57846d1cbc2773f7c16210270ef858382116bfc4787ed169dea324",
    "roles/script_jobs/templates/expectations.json.j2": "85e82b87971738ede16c51edd4b87b9bb2d002fa9f7a36e8adfb0870c4e99d07",
    "scripts/job_cron_guard.py": "c34ea1082b716021447fcff3869c73d9dfac808775118d3d38cde965543457d2",
    "roles/script_jobs/filter_plugins/local_config.py": "a040e1923a3678db9b1df20c6bdc659490a8f94cc400f5f03cf83ce54f2969e5",
    "artifacts/script-library/lib/python/job_store.py": "951a7e29be285a417dc61a1bebf97f1fd40f03998db793a85cdb64bf8abaab85"
  },
  "i18n": {
    "de": {
      "title": "Lokale Skripte mit neutraler Library bereitstellen",
      "description": "# Lokale Skripte mit neutraler Library bereitstellen\n\nDie ausführbaren Betriebsskripte liegen ausschließlich unter\n`/root/skripte-config/<inventory_hostname>/` auf dem Controller. Diese privaten\nQuellen, Spezialfunktionen, Hostwerte und Secrets gehören nicht in ein Git-Repo.\nIn `artifacts/script-library/` liegt nur die neutrale Grundbibliothek.\n\n```sh\nansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --syntax-check\nansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --check\nansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host\n```\n\nDie Rolle verlangt ein geprüftes lokales `deployment.json` mit `files`-Einträgen\n(`path`, `sha256`, `kind`). Erlaubt sind Einstiegsskripte, `programs/*.sh`,\n`config/*.json` und `lib/special/**/*.sh`. Lokale Quellen dürfen die Git-Library\nnicht überschreiben. Eingangs-SHA werden vor dem Übertragen geprüft; gerenderte\nZielkonfigurationen sind bewusst eigenständige lokale Dateien.\n\n| Variable | Bedeutung / Standard |\n|---|---|\n| `script_jobs_source_root` | Lokale Controllerquelle, `/root/skripte-config` |\n| `script_jobs_target_root` | Bestehendes `script_path`, sonst `/scripte` |\n| `script_jobs_database_path` | Laufzeitdaten außerhalb der Skripte, `/var/lib/script-jobs/jobs.sqlite3` |\n| `script_jobs_owner`, `script_jobs_group` | Ausführungs-/Dateibesitzer, jeweils `root` |\n| `script_jobs_common_config` | Ausdrückliche gemeinsame JSON-Werte, sonst bestehendes `script_library_common_config` oder `{}` |\n| `script_jobs_job_config` | Ausdrückliche Werte pro Skriptinstanz, sonst `script_library_job_config` oder `{}` |\n| `script_jobs` | Ausdrückliche Liste zu verwaltender Cronjobs, `[]` |\n| `script_jobs_sets` | Lokal definierte wiederverwendbare Joblisten, `{}` |\n| `script_jobs_selected_sets` | Ausgewählte lokale Sets, `[]` |\n| `script_jobs_timezone` | Explizite IANA-Zeitzone für Erwartungsprüfung |\n\nEin Job hat `name`, `script`, optional `args` als Liste und `user`, `category`\n(`general`/`vzdump`), einen `cron`-Block und gegebenenfalls `expected`.\nCron kann Kalenderfelder oder `special_time` verwenden. Vzdump benötigt explizit\nMontag (`1`/`mon`). `expected.deadline_minutes` und\n`expected.max_runtime_minutes` bestimmen fehlende/überfällige Läufe. Komplexe\nZeitpläne benötigen explizite `expected.start`/`expected.weekdays` (Montag=0).\nEin nicht vollständig beschriebener Erwartungsplan wird als unkonfiguriert\nangezeigt, niemals als bewiesener Erfolg. Kalenderüberwachung und tatsächliche\nAusführung sind getrennte Dinge.\n\nKonfiguration: private Quelldaten, dann ausdrücklich gesetzte Hostvariablen.\nBeim Lauf gilt `common.json`, danach die Skriptdatei. Explizit leere Skriptwerte\nüberschreiben gemeinsame Werte. `JOB_DATABASE_PATH` muss mit der\nAnsible-Datenbankzuordnung übereinstimmen; Konflikte werden vor dem Schreiben\nabgewiesen. `JOB_MAX_RUNTIME_SECONDS` kann das Laufzeitlimit des Runners setzen.\n\nAlle Jobs einer lokalen Datenbank verwenden denselben konfigurierten Besitzer.\nDie Dateien und Datenbank sind `0600`, Verzeichnisse `0700`, Programme `0700`.\nDie Rolle wird unter den vorhandenen Become-Einstellungen ausgeführt.\n\nCron wird ausschließlich für die expliziten Einträge verwaltet. Ein unbekannter\nAltaufruf, ein noch laufendes Skript oder ein systemweiter Cron-Konflikt blockiert\ndie Umstellung. Eine genaue alte Befehlszeile kann nach Prüfung als\n`legacy_command` zugeordnet werden. Fremde Jobs werden nicht gelöscht. Unbekannte\nDateien oder aus der Auswahl entfernte frühere Jobs werden nicht still bereinigt.\n\nDie Rolle startet keine Backupskripte. Ohne Cronliste werden Dateien und SQLite\nbereitgestellt, aber kein Zeitplan erfunden. Es gibt keine künstlichen\nDeaktivierungsschalter. Für die tatsächliche Cron-Übernahme ist ein Pilot mit der\nkonkreten lokalen Konfiguration erforderlich.\n\n\n\nBestehende systemd-Dienste werden ueber wiederverwendbare\n`script_jobs_systemd_profiles` und die ausdrueckliche Hostauswahl\n`script_jobs_systemd_selected_profiles` eingebunden. Die Profile enthalten\nDienstnamen und `active`/`oneshot`/`observe`; das Deployment erkennt diese nicht\naus Skript- oder Unitdateien. Es schreibt die feste Statuszuordnung neben SQLite.\nDie zentrale Sammlung uebernimmt nur gefilterte Dienstzustaende in dieselbe Summary.\nDetails und Grenzen: [systemd-Statusprofile](../configurations/systemd-job-status.md).\n\nObjektprofile mit `source`, `target` und `services` können zusätzlich private Ordner und explizite Units bereitstellen. Listenprofile behalten die reine Statusanbindung. [Pfadzuordnung, Voraussetzungen und Aktivierung](../configurations/systemd-job-deployment.md).\n\nNach dem Zusammenführen der Konfiguration entfernt die Rolle die Mail-/Telegramwerte\nund setzt alte Versandflags auf `false`. Leere Kompatibilitätsfelder halten ältere\nShellprogramme lauffähig. Fachliche Zugangsdaten, etwa zum Backupziel, bleiben\nbestehen. Alle Jobs einschließlich Vzdump erfassen ausschließlich lokale Ergebnisse.\nDie zu verwaltenden Cron-Skripte müssen im geprüften Quellmanifest enthalten sein.\n\nDie Library verteilt `bin/job-status` auf jeden Host. Es liest den letzten lokalen\nZustand je Job, ohne Controller, Netzwerk oder Jobstart. Der Controller verwendet\ndenselben Helfer über `bin/control jobs-last --limit ZIEL`.\n\n`script_jobs_profile_config` enthält ausschließlich die gerenderten JSON-Werte\nder Dienstprofile. Es überschreibt entsprechende `script_jobs_job_config`-Vorgaben\nund hält die Dienstkonfiguration von den normalen Cronjob-Werten getrennt.\n\nFür die Statusprüfung gelten `script_jobs_expected_defaults`, danach die\njobbezogenen `script_jobs_expected_overrides`, danach `job.expected`. Die beiden\nVariablen sind standardmäßig leer und verändern keine Ausführung. Uhrzeiten\nwerden aus einzelnen Stunden/Minuten, Kommalisten, `*` und `*/N` abgeleitet.\nDamit werden etwa zweimal tägliche Jobs und Fünf-Minuten-Checks korrekt getrennt.\n`expected.start` kann auch eine ausdrückliche Liste von `HH:MM` enthalten.\nZeitzone, Startfrist und maximale Beobachtungsdauer bleiben explizite lokale Werte.\nEin noch laufender alter Job bleibt auch über das nächste Cronfenster sichtbar.\n",
      "fields": {}
    },
    "en": {
      "title": "Deploy local scripts with the shared library",
      "description": "# Deploy local scripts with the shared library\n\nExecutable operational scripts stay in `/root/skripte-config/<inventory_hostname>/` on the controller. Keep these private sources, custom functions, host values and secrets outside Git. The shared library lives under `artifacts/script-library/`.\n\n```sh\nansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --syntax-check\nansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host --check\nansible-playbook playbooks/scripts/deploy_jobs.yml --limit example-host\n```\n\nSupply a verified local `deployment.json` with `files` entries specifying `path`, `sha256` and `kind`. Supported files include entry scripts, `programs/*.sh`, `config/*.json` and `lib/special/**/*.sh`. Local code cannot replace Git library files. Input hashes are verified before transfer. Rendered destination configurations are separate local files.\n\n| Variable | Meaning and default |\n|---|---|\n| `script_jobs_source_root` | Local controller source, `/root/skripte-config` |\n| `script_jobs_target_root` | Existing `script_path`, otherwise `/scripte` |\n| `script_jobs_database_path` | Runtime data outside scripts, `/var/lib/script-jobs/jobs.sqlite3` |\n| `script_jobs_owner`, `script_jobs_group` | Run and file owner/group, both `root` |\n| `script_jobs_common_config` | Explicit shared JSON values, otherwise `script_library_common_config` or `{}` |\n| `script_jobs_job_config` | Explicit per-script values, otherwise `script_library_job_config` or `{}` |\n| `script_jobs` | Cron jobs to manage, `[]` |\n| `script_jobs_sets` | Reusable local job lists, `{}` |\n| `script_jobs_selected_sets` | Selected local sets, `[]` |\n| `script_jobs_timezone` | Explicit IANA time zone for schedule checks |\n\nEach job has `name`, `script`, optional list-valued `args` and `user`, a `category` (`general` or `vzdump`), a `cron` block and optionally `expected`. Cron accepts calendar fields or `special_time`. Vzdump requires explicit Monday (`1` or `mon`). `expected.deadline_minutes` and `expected.max_runtime_minutes` identify missing and overdue runs. Complex schedules need explicit `expected.start` and `expected.weekdays` (Monday=0). An incomplete expectation appears unconfigured. Schedule monitoring and execution are independent.\n\nPrivate source configuration is followed by explicit host variables. At runtime the script-specific file overrides `common.json`, including explicitly empty values. `JOB_DATABASE_PATH` must match the Ansible database mapping. Conflicts fail before writes. Set `JOB_MAX_RUNTIME_SECONDS` to limit runner duration.\n\nEvery job in a local database uses the same configured owner. Files and the database use mode 0600, directories and executables 0700. The role follows existing become settings.\n\nCron management applies only to explicit entries. An unknown legacy invocation, a still-running script or a system-wide cron conflict blocks migration. After review, use the exact old command line as `legacy_command`. Unrelated jobs, unknown files and jobs removed from the selection are not silently deleted.\n\nThe role never starts backup scripts. Without a cron list it installs files and SQLite without creating schedules. There are no synthetic disable flags. Pilot the actual cron migration with the intended local configuration.\n\nAfter merging configuration, the role removes mail/Telegram values and sets legacy delivery flags to false. Empty compatibility fields support older shell programs. Operational credentials such as the backup destination remain in place. All jobs, including Vzdump, record local results only. Managed cron scripts must be present in the verified source manifest.\n\nThe library installs `bin/job-status` on every host to read the latest job states without a controller, network access or starting jobs. On the controller, `bin/control jobs-last --limit TARGET` runs the same helper.\n\nMap existing system services through reusable `script_jobs_systemd_profiles`\nand the explicit host list `script_jobs_systemd_selected_profiles`. Profiles contain\nunit names and `active`, `oneshot` or `observe` modes. Deployment uses the selected\nprofiles rather than inferring bindings from script or unit files. It writes fixed\nstatus settings next to SQLite. The existing collector includes filtered service\nobservations in the same central summary. No units or cron schedules are changed\nby these bindings. See [systemd status profiles](../configurations/systemd-job-status.md)\nfor point-in-time and shutdown-history limits.\n\n\nObject profiles with source, target and services can also deploy private folders and explicit service units. List profiles remain status-only. See [deployment paths and lifecycle settings](../configurations/systemd-job-deployment.md).\n\n`script_jobs_profile_config` holds rendered service-profile JSON settings and\noverrides matching `script_jobs_job_config` defaults. This keeps service settings\nseparate from ordinary cron job configuration.\n\nStatus checks merge `script_jobs_expected_defaults`, per-job\n`script_jobs_expected_overrides`, then `job.expected`. Both variables default to\nempty and do not change execution. Minute/hour schedules support single values,\ncomma lists, `*`, and `*/N`; `expected.start` can also list explicit `HH:MM` times.\nTimezone, start deadline and maximum observed runtime stay explicit local settings.\nAn older running job remains visible across the next scheduled slot.\n",
      "fields": {}
    }
  }
}
```

</details>
