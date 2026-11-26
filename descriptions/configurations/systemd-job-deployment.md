# Private Ordner und systemd-Dienste per Profil bereitstellen

Die gemeinsame Library und die Deploymentlogik liegen in Git. Dienstprogramme,
Spezialfunktionen und feste Konfiguration bleiben privat auf dem Controller unter
`/root/skripte-config/<inventory_hostname>/`. Profile definieren ausdrücklich,
welcher relative Quellordner in welchen absoluten Zielordner kommt. Unterordner
bleiben erhalten. Es gibt keine Erkennung aus Skript- oder Unitdateien.

```yaml
# Beispiel in lokalen group_vars/all; keine produktiven Werte in Git
script_jobs_systemd_profiles:
  watcher:
    source: services/watcher
    target: /opt/example-watcher
    owner: root
    group: root
    services:
      - unit: example-watcher.service
        mode: active
        type: simple
        exec_start: ["{target}/bin/watcher.sh"]
        working_directory: "{target}"
        user: root
        group: root
        restart: on-failure
        wanted_by: [multi-user.target]
        # Nur bei gewollter Aktivierung ausdruecklich ergaenzen:
        # enabled: true
        # state: started

# Lokale host_vars/<host>/script_logic.yml
script_jobs_systemd_selected_profiles: [watcher]
```

Damit wird `services/watcher/bin/watcher.sh` aus dem privaten Hostordner nach
`/opt/example-watcher/bin/watcher.sh` kopiert. `{target}` und `{library_root}`
werden ausschließlich in Profilwerten ersetzt. Der Inhalt der Programme wird
nicht umgeschrieben. Eigene absolute Pfade innerhalb eines Programms müssen vor
der Umstellung angepasst oder als lokale Konfiguration herausgezogen werden.
Ansible ersetzt ein Dictionary beim Hostoverride als Ganzes; eine abweichende
Profildefinition daher vollständig angeben oder verschiedene Profilnamen nutzen.

Der Quellordner benötigt ein separat geprüftes `deployment.json`:

```text
{"files": [{"path": "bin/watcher.sh", "kind": "script", "sha256": "SHA256_DES_GEPRUEFTEN_INHALTS"}]}
```

`path` ist relativ zum Profilquellordner. Optional benennt `dest` einen anderen
relativen Zielpfad. `kind` erlaubt `script` (0700), `config`, `library` und `data`
(jeweils 0600). Quellen und Manifest dürfen keine Symlinks enthalten; jede SHA-256
muss vor dem Übertragen stimmen. `review_required` oder `sanitized_import` im
Manifest blockiert ein ungeprüftes Importpaket. Pfadwechsel, kollidierende Dateien,
Libraryüberschreibungen und ein Überschreiben der Beobachtungsdatenbank werden
abgewiesen. Unbekannte vorhandene Dateien bleiben erhalten.

```sh
ansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host --check
ansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host
```

Das eigenständige Playbook benötigt nur die ausgewählten Profilmanifeste; kein
zusätzliches altes Hostmanifest. Es liefert die gesamte neutrale Library aus und
schreibt Units aus den Profilwerten. `deploy_jobs.yml` kann dieselben Profile
zusätzlich zu seinen bisherigen Skript-/Cronquellen bereitstellen. Vorhandene
Listenprofile bleiben reine Statusanbindungen ohne Dateikopie oder Unitwechsel.

Bei geänderten Unitdefinitionen folgt `daemon-reload`. Ohne `enabled` und `state`
wird weder ein Dienst gestartet/gestoppt noch dessen Bootaktivierung geändert.
`state` erlaubt `started`, `stopped`, `restarted`, `reloaded`; `enabled` ist boolesch.
Ein bewusster Neustart benötigt `state: restarted`. Maskierte Units werden nicht
automatisch entsperrt. Entfernte Profile löschen oder stoppen keine Altdienste.
Kopien und Units erhalten Ansible-Sicherungen, die Quelldatenbank bleibt erhalten.
Die Vorschau führt keine systemd-Aktionen aus.

Weitere Servicefelder: `description`, `type` (simple, exec, oneshot, notify,
forking, idle), `exec_stop` als Argumentliste, `exec_start_pre`, `exec_start_post`
und `exec_stop_post` als Listen von Argumentlisten, `restart_sec`,
`remain_after_exit`, `timeout_start_sec`, `timeout_stop_sec`, `pid_file`, `kill_mode`,
`after`, `before`, `wants`, `requires`, `conflicts`, `wanted_by`,
`default_dependencies` und `environment_files` als Liste absoluter Pfade.
Abhängigkeiten sind Listen konkreter Unitnamen. `mode` ist active, oneshot oder
observe; eine Oneshot-Ausführung muss `type: oneshot` und `mode: oneshot` verwenden.
Unbekannte Felder, mehrzeilige Werte und implizite Shellbefehle werden abgewiesen.
Argumente werden als Literale gequotet; Secrets gehören in private 0600-Dateien,
nicht in öffentlich lesbare Units oder Argumente. Benutzer, Pakete und externe
Environment-Dateien müssen zuvor vorhanden sein. Private Dateiowner und
Dienstbenutzer müssen zu den benötigten Zugriffsrechten passen.

Die Unitablage ist standardmäßig `/etc/systemd/system`
(`script_jobs_systemd_unit_dir`, Owner/Group jeweils root). Librarypfad und
Datenbank verwenden die vorhandenen `script_jobs_*`-Variablen. Die Beobachtung
fordert ausschließlich freigegebene Statusfelder an, niemals Environment oder
Exec-Argumente. Das gilt auch für den kleinen Helfer zur expliziten Aktivierung.

Die fachliche Migration bestehender Dienste braucht geprüfte private Quellen,
Konfigurationswerte und einen eigenen Pilot. Ein gültiges Profil beweist weder
Anwendungsfunktion noch einen Live-Rollout. [Statusauswertung und Grenzen](systemd-job-status.md).

## Dienstbenutzer und gerenderte Konfiguration

`library: true` im Objektprofil installiert die vollständige gemeinsame Library
zusätzlich im Profilziel, mit dessen Owner und Group. `{library_root}` zeigt dann
auf dieses Ziel. Verwende getrennte, nicht ineinander verschachtelte Ziele für
verschiedene Benutzer. Ein Dienst als root benötigt root-eigene Programme und
Konfiguration; ein unprivilegierter Dienst erhält einen eigenen privaten Ordner.
Die Rolle erweitert keine Zugriffsrechte auf das gemeinsame root-Verzeichnis.

Ein Manifest-Eintrag `{"path": "config/watcher.json", "kind": "config",
"config_key": "watcher", "sha256": "SHA256"}` wird aus geprüftem JSON plus
`script_jobs_job_config.watcher` gerendert. Hostwerte überschreiben Quelldefaults.
Das Ergebnis ist 0600 mit dem Profilowner; Mail- und Telegramzugangsdaten werden
wie bei normalen Jobs entfernt. Die Quell-SHA wird vor dem Rendern geprüft,
der gerenderte Inhalt hat anschließend bewusst eine andere SHA. Ohne
`config_key` bleibt die bisherige unveränderte Dateikopie erhalten.

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "systemd-job-deployment",
  "title": "Private Ordner und systemd-Dienste per Profil bereitstellen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "roles/script_jobs/filter_plugins/profile_deployment.py",
    "roles/script_jobs/tasks/systemd_plan.yml",
    "roles/script_jobs/tasks/systemd_deploy.yml",
    "roles/script_jobs/templates/profile.service.j2",
    "roles/script_jobs/defaults/main.yml",
    "scripts/job_profile_guard.py",
    "scripts/job_profile_apply.py",
    "playbooks/scripts/deploy_systemd.yml"
  ],
  "source_hashes": {
    "roles/script_jobs/filter_plugins/profile_deployment.py": "be1e0495ada4b1abba720b77b464582c30c94cd56688eb8b5d30058cc9fabcfb",
    "roles/script_jobs/tasks/systemd_plan.yml": "5bfd472b58b2515655a1fb0fd88bd960cdc1760f3f0a8e803dc91fc579f9440e",
    "roles/script_jobs/tasks/systemd_deploy.yml": "f04257ab784c902131dd5bea6adf4aac8db0f61ffc0e407e3a5e0d309f678453",
    "roles/script_jobs/templates/profile.service.j2": "d1b8a0089c4c4d1cefbf09a7511bc12861353c4b7e66be0fe2a2f3f27d571b8c",
    "roles/script_jobs/defaults/main.yml": "d78878e22bb6c06993b645a8a692a4a1ecf03edbc9caea857df1d4f2c28088f6",
    "scripts/job_profile_guard.py": "09c3db8f5bdb0d35ffdcea1f62aebe2e2050b23d31650aa6c57099efae14bd76",
    "scripts/job_profile_apply.py": "e3a395bc8fb887e1c0bcab45d496e7aa86f3bba084d41e298b1b534f8fe3b429",
    "playbooks/scripts/deploy_systemd.yml": "d119b7890da6f392f8e47599c735a223bfa7eb1879f29eeb20a5546aa157f101"
  },
  "i18n": {
    "de": {
      "title": "Private Ordner und systemd-Dienste per Profil bereitstellen",
      "description": "# Private Ordner und systemd-Dienste per Profil bereitstellen\n\nDie gemeinsame Library und die Deploymentlogik liegen in Git. Dienstprogramme,\nSpezialfunktionen und feste Konfiguration bleiben privat auf dem Controller unter\n`/root/skripte-config/<inventory_hostname>/`. Profile definieren ausdrücklich,\nwelcher relative Quellordner in welchen absoluten Zielordner kommt. Unterordner\nbleiben erhalten. Es gibt keine Erkennung aus Skript- oder Unitdateien.\n\n```yaml\n# Beispiel in lokalen group_vars/all; keine produktiven Werte in Git\nscript_jobs_systemd_profiles:\n  watcher:\n    source: services/watcher\n    target: /opt/example-watcher\n    owner: root\n    group: root\n    services:\n      - unit: example-watcher.service\n        mode: active\n        type: simple\n        exec_start: [\"{target}/bin/watcher.sh\"]\n        working_directory: \"{target}\"\n        user: root\n        group: root\n        restart: on-failure\n        wanted_by: [multi-user.target]\n        # Nur bei gewollter Aktivierung ausdruecklich ergaenzen:\n        # enabled: true\n        # state: started\n\n# Lokale host_vars/<host>/script_logic.yml\nscript_jobs_systemd_selected_profiles: [watcher]\n```\n\nDamit wird `services/watcher/bin/watcher.sh` aus dem privaten Hostordner nach\n`/opt/example-watcher/bin/watcher.sh` kopiert. `{target}` und `{library_root}`\nwerden ausschließlich in Profilwerten ersetzt. Der Inhalt der Programme wird\nnicht umgeschrieben. Eigene absolute Pfade innerhalb eines Programms müssen vor\nder Umstellung angepasst oder als lokale Konfiguration herausgezogen werden.\nAnsible ersetzt ein Dictionary beim Hostoverride als Ganzes; eine abweichende\nProfildefinition daher vollständig angeben oder verschiedene Profilnamen nutzen.\n\nDer Quellordner benötigt ein separat geprüftes `deployment.json`:\n\n```text\n{\"files\": [{\"path\": \"bin/watcher.sh\", \"kind\": \"script\", \"sha256\": \"SHA256_DES_GEPRUEFTEN_INHALTS\"}]}\n```\n\n`path` ist relativ zum Profilquellordner. Optional benennt `dest` einen anderen\nrelativen Zielpfad. `kind` erlaubt `script` (0700), `config`, `library` und `data`\n(jeweils 0600). Quellen und Manifest dürfen keine Symlinks enthalten; jede SHA-256\nmuss vor dem Übertragen stimmen. `review_required` oder `sanitized_import` im\nManifest blockiert ein ungeprüftes Importpaket. Pfadwechsel, kollidierende Dateien,\nLibraryüberschreibungen und ein Überschreiben der Beobachtungsdatenbank werden\nabgewiesen. Unbekannte vorhandene Dateien bleiben erhalten.\n\n```sh\nansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host --check\nansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host\n```\n\nDas eigenständige Playbook benötigt nur die ausgewählten Profilmanifeste; kein\nzusätzliches altes Hostmanifest. Es liefert die gesamte neutrale Library aus und\nschreibt Units aus den Profilwerten. `deploy_jobs.yml` kann dieselben Profile\nzusätzlich zu seinen bisherigen Skript-/Cronquellen bereitstellen. Vorhandene\nListenprofile bleiben reine Statusanbindungen ohne Dateikopie oder Unitwechsel.\n\nBei geänderten Unitdefinitionen folgt `daemon-reload`. Ohne `enabled` und `state`\nwird weder ein Dienst gestartet/gestoppt noch dessen Bootaktivierung geändert.\n`state` erlaubt `started`, `stopped`, `restarted`, `reloaded`; `enabled` ist boolesch.\nEin bewusster Neustart benötigt `state: restarted`. Maskierte Units werden nicht\nautomatisch entsperrt. Entfernte Profile löschen oder stoppen keine Altdienste.\nKopien und Units erhalten Ansible-Sicherungen, die Quelldatenbank bleibt erhalten.\nDie Vorschau führt keine systemd-Aktionen aus.\n\nWeitere Servicefelder: `description`, `type` (simple, exec, oneshot, notify,\nforking, idle), `exec_stop` als Argumentliste, `exec_start_pre`, `exec_start_post`\nund `exec_stop_post` als Listen von Argumentlisten, `restart_sec`,\n`remain_after_exit`, `timeout_start_sec`, `timeout_stop_sec`, `pid_file`, `kill_mode`,\n`after`, `before`, `wants`, `requires`, `conflicts`, `wanted_by`,\n`default_dependencies` und `environment_files` als Liste absoluter Pfade.\nAbhängigkeiten sind Listen konkreter Unitnamen. `mode` ist active, oneshot oder\nobserve; eine Oneshot-Ausführung muss `type: oneshot` und `mode: oneshot` verwenden.\nUnbekannte Felder, mehrzeilige Werte und implizite Shellbefehle werden abgewiesen.\nArgumente werden als Literale gequotet; Secrets gehören in private 0600-Dateien,\nnicht in öffentlich lesbare Units oder Argumente. Benutzer, Pakete und externe\nEnvironment-Dateien müssen zuvor vorhanden sein. Private Dateiowner und\nDienstbenutzer müssen zu den benötigten Zugriffsrechten passen.\n\nDie Unitablage ist standardmäßig `/etc/systemd/system`\n(`script_jobs_systemd_unit_dir`, Owner/Group jeweils root). Librarypfad und\nDatenbank verwenden die vorhandenen `script_jobs_*`-Variablen. Die Beobachtung\nfordert ausschließlich freigegebene Statusfelder an, niemals Environment oder\nExec-Argumente. Das gilt auch für den kleinen Helfer zur expliziten Aktivierung.\n\nDie fachliche Migration bestehender Dienste braucht geprüfte private Quellen,\nKonfigurationswerte und einen eigenen Pilot. Ein gültiges Profil beweist weder\nAnwendungsfunktion noch einen Live-Rollout. [Statusauswertung und Grenzen](systemd-job-status.md).\n\n## Dienstbenutzer und gerenderte Konfiguration\n\n`library: true` im Objektprofil installiert die vollständige gemeinsame Library\nzusätzlich im Profilziel, mit dessen Owner und Group. `{library_root}` zeigt dann\nauf dieses Ziel. Verwende getrennte, nicht ineinander verschachtelte Ziele für\nverschiedene Benutzer. Ein Dienst als root benötigt root-eigene Programme und\nKonfiguration; ein unprivilegierter Dienst erhält einen eigenen privaten Ordner.\nDie Rolle erweitert keine Zugriffsrechte auf das gemeinsame root-Verzeichnis.\n\nEin Manifest-Eintrag `{\"path\": \"config/watcher.json\", \"kind\": \"config\",\n\"config_key\": \"watcher\", \"sha256\": \"SHA256\"}` wird aus geprüftem JSON plus\n`script_jobs_job_config.watcher` gerendert. Hostwerte überschreiben Quelldefaults.\nDas Ergebnis ist 0600 mit dem Profilowner; Mail- und Telegramzugangsdaten werden\nwie bei normalen Jobs entfernt. Die Quell-SHA wird vor dem Rendern geprüft,\nder gerenderte Inhalt hat anschließend bewusst eine andere SHA. Ohne\n`config_key` bleibt die bisherige unveränderte Dateikopie erhalten.\n",
      "fields": {}
    },
    "en": {
      "title": "Deploy private folders and system services through explicit profiles",
      "description": "# Deploy private folders and system services through explicit profiles\n\nThe shared library and deployment logic belong in Git. Keep actual service programs,\nspecial functions and fixed configuration in the private controller source folder\n`/root/skripte-config/<inventory_hostname>/`. Select named profiles with\n`script_jobs_systemd_selected_profiles`; define reusable profiles in local\n`script_jobs_systemd_profiles`. No source or unit inspection infers deployment.\n\nA deployment profile is an object with `source` (relative private host folder),\n`target` (dedicated absolute destination), optional `owner`/`group`, and `services`.\nFor example, source `services/watcher`, target `/opt/example-watcher`, and manifest\npath `bin/watcher.sh` deploy that exact relative file under the target. Each source\nfolder needs `deployment.json` with `files`: each entry has `path`, `kind`, `sha256`\nand optional relative `dest`. Kinds are script (0700), config/library/data (0600).\nReviewed source hashes are required. Links, path traversal, collisions, shared\nlibrary replacement and observation database overwrites fail before deployment.\n`review_required` or `sanitized_import` prevents unreviewed imports from deploying.\nUnknown existing files remain. Existing directory ownership is preserved.\n\nEach service requires `unit`, `mode` (active/oneshot/observe), and `exec_start` as\nan explicit argument list, e.g. `[\"{target}/bin/watcher.sh\"]`. Optional fields:\n`name`, `description`, `type` (simple/exec/oneshot/notify/forking/idle), `user`, `group`,\n`working_directory`, `exec_stop` (argument list), `exec_start_pre`, `exec_start_post`,\n`exec_stop_post` (lists of argument lists), `restart`, `restart_sec`,\n`remain_after_exit`, `timeout_start_sec`, `timeout_stop_sec`, `pid_file`, `kill_mode`,\n`after`, `before`, `wants`, `requires`, `conflicts`, `wanted_by`,\n`default_dependencies`, `environment_files`, `enabled`, and `state`.\nDependency fields are unit-name lists; environment files are explicit absolute\npaths. Oneshot execution and observation modes must agree. Unknown fields, multiline\nvalues and implicit shell commands fail. Arguments are quoted literally. Keep\nsecrets in private mode-0600 configuration, not unit text or command arguments.\nExisting users, packages and external configuration are prerequisites.\n\n`{target}` and `{library_root}` are expanded only in profile values. Program text\nis never rewritten: move hardcoded internal paths into private configuration before\nchanging its destination. Ansible replaces a host dictionary override as a whole;\nprovide a full replacement profile or distinct profile names.\n\nRun `ansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host\n--check` first, then the same explicit command without `--check`. This standalone\nplaybook deploys the shared library, selected folders, generated units and fixed\nstatus bindings, without requiring an old root host manifest. `deploy_jobs.yml`\nalso supports the profiles alongside its existing private script/Cron manifest.\nLegacy list profiles remain status-only and do not copy files or replace units.\n\nChanged units trigger daemon-reload. No lifecycle setting is inferred: only explicit\nboolean `enabled` and `state` (started/stopped/restarted/reloaded) alter service\nactivation. A running service needs explicit `state: restarted` to load new code.\nMasked units are not unmasked; removing a profile does not delete or stop anything.\nCheck mode performs no systemd actions. File and unit backups preserve prior files.\nThe existing database is initialized without resetting history or running programs.\n\nThe unit directory defaults to `/etc/systemd/system` via\n`script_jobs_systemd_unit_dir` with root owner/group; library and database paths use\nthe existing script_jobs variables. Only approved status properties are queried,\nincluding during explicit lifecycle management. No Environment or Exec values are\nrequested. A working profile is not a live application test; review private sources,\nconfiguration and permissions, then run an explicit pilot before migration.\nSee [observation behavior and limits](systemd-job-status.md).\n\n## Service users and rendered settings\n\nSet `library: true` on an object profile to install a complete additional shared\nlibrary inside its target, owned by that profile. `{library_root}` then resolves\nto that target. Use separate, nonoverlapping roots for different service users.\nRoot services need root-owned programs and settings; unprivileged services get\ntheir own private folder. No access to the root library is widened.\n\nA manifest JSON entry with `kind: config` and `config_key: watcher` is rendered\nfrom its hash-verified source object plus `script_jobs_job_config.watcher`. Host\nsettings override defaults. The result is mode 0600 with the profile owner and\nnotification credentials removed. Its digest intentionally differs from source.\nEntries without `config_key` retain byte-for-byte copying.\n",
      "fields": {}
    }
  }
}
```
