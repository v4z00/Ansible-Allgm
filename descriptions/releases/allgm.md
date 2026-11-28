# Changelog

## s0.9.4 – Windows profiles and separate job failure delivery

The preflight accepts the Kerberos backend provided by the installed pywinrm
and still requires `kinit`. The pinned runtime can use pywinrm's bundled
authentication module without a separate requests-kerberos installation.

Approved Windows profiles can use the existing job database and a named
scheduled account. A scheduled task can run several profiles in a fixed order,
with a separate job result for each step. SYSVOL shares receive only
manifest-listed PowerShell code.
Selected jobs can send individual failures with per-channel receipts. Their
successful runs remain in the daily summary. The additional schedule starts
only when configured. The job module is 0.6.2.

## s0.9.3 – Separate WinRM DNS names from inventory addresses

WinRM accepts an environment DNS suffix, an explicit inventory name and a
complete host override. The DNS name is used for HTTPS and Kerberos while
Proxmox continues to refresh the inventory IP. Existing controllers can update
the byte-identical resolver via `windows-setup --upgrade-known-resolver --apply`.
With no DNS settings, the existing address is used.

## s0.9.2 – Scoped AD firewall and job monitoring

Active Directory firewall rules use explicit directory, RPC, member and
administration stages with named private network scopes. The standard invocation
previews changes on one domain controller at a time. Managed IDs are distinct
from existing local and GPO rules. Windows Checkmk queries go through the common
PowerShell entry point and support the configured Authenticode workflow.

## s0.9.1 – Windows Kerberos access

Keep the Windows account in the private secrets file. Enabled Kerberos requires
Kerberos for WinRM. Existing controllers can upgrade the known Windows resolver
with `bin/control windows-setup --upgrade-known-resolver` and `--apply`, then
prepare the Debian runtime with `bin/setup-runtime --windows-kerberos`.
See the [Windows access guide](../commands/windows-setup.md).

## s0.9.0 – Windows foundation and immediate host security alerts

The Windows foundation now also includes grouped, unlinked GPO registry hardening
with explicit switches, check-mode comparison and protected recovery backups. The
central signing pipeline accepts independent code bundles for add-ons; CoreDC is
maintained in its own repository and update module. No private host scripts or
SYSVOL exports are published. Native Windows/AD/logon pilots remain outstanding.

Staging source preview: WinRM HTTPS access preparation, separate Windows bootstrap,
portable PowerShell/SQLite APIs, shared schema/mail mapping, Windows event collection,
read-only job/Checkmk views and optional Windows Checkmk MSI rollout. Existing Linux
SSH and job workflows remain available. Job module 0.6.0; checker 1.5.5.

Security events can use a durable local mail/Telegram outbox with per-channel retry.
Ordinary jobs keep the central summary. SMTP authentication and TLS are separate;
an intended internal relay can use authentication none. Enable explicit host security
profiles and migrate each detector to the alarm API before relying on delivery.

Run bin/setup-runtime for pywinrm. Prepare the pinned SQLite executable separately;
it is not shipped in Git. First authenticated Windows/ACL/MSI/signing pilots are pending.
Optional central signing keeps private keys on a configured Windows signer and validates artifacts before execution. AllSigned cannot be bypassed by disabling the integration. Private
business-script migration, Task Scheduler profiles, SYSVOL background/Blackbox integration
and grouped GPO managed-content modules are not complete in this foundation checkpoint. GPO links stay manual.

Older updater allowlists reject the new SQL/PowerShell artifact paths. Use the current
staging checkout installer and its preview/backup/plan-hash flow for the first update;
a Homelab controller uses the matching Homelab installer with this Allgm checkout.
Do not install an Allgm-only profile over an existing Homelab controller. No automatic
host migration, cron replacement or promotion to main is included.

## 0.8.13 – Quiet service observations and Compose builds

Job module 0.5.5 keeps healthy and intentionally inactive systemd snapshots out of new job summaries while retaining status/history and all service problems. Observation provenance is stored additively on import; host configurations and running services do not need changes.

Docker deployment builds local Compose images by default (boolean `docker_compose_build`, optional false). Docker updates pull registry images with bounded retries before building local images and waiting for healthy/running containers. Failed preparation prevents container changes. Existing mandatory checks remain. Private build output is hidden.

## 0.8.12 – English documentation and language selection

The English README now walks through a maintenance run. Catalog pages open in English and include the German text. New installations suggest a language from the locale and accept an explicit choice. Existing controllers without a language preference still use German. The optional `tools/set-controller-language.py` changes just the local language setting and saves a backup.

## Previous releases

### 0.8.11

Fix systemd WorkingDirectory and PIDFile syntax. This release includes job module 0.5.4 and checker 1.5.4, resumable report delivery, recurring cron windows and explicitly selected service profiles. Preview new profiles with `--check`. Migrate a local approval register separately if required.

### s0.8.10

Job module 0.5.3 supports multiple cron windows and per-host or per-job tolerances. Running jobs are reported without being stopped. The service deployment passes role defaults to the library step.

### s0.8.9

Accept numeric time values from Ansible variables when validating service profiles.

### s0.8.8

Job module 0.5.1 can render private JSON from host variables and install a complete library in the service user’s directory. Select the new profile fields explicitly after a pilot.

### s0.8.7

Checker 1.5.4 supports an internal `.local/extensions` register and the established sibling location. Using both blocks migration. Older checkers need the sibling path before rollback.

### s0.8.6

Job module 0.5.0 can deploy private source directories and systemd units by profile. Preview with `--check`; enable, start and restart only through explicit profile fields.

### s0.8.5

Explicitly selected services can report snapshots to SQLite and central summaries. Long-running services, one-shots and optional services are evaluated separately. Units, processes and cron stay under their existing management.

### s0.8.4

Read-only discovery of custom services and timers leaves environment values, configuration bodies and command arguments on each host. Review user services and complex launch commands separately.

### s0.8.3

Pending report channels survive interruptions. An incomplete Ansible query retains the previous cursors so partial results are not treated as complete. No database or scheduling changes are required.

### 0.8.2

Checker 1.5.3 simplifies update, cleanup and feature checks while retaining the CLI, exit codes and JSON format.

### s0.8.2

Checker 1.5.3 previews the same compatible changes to update, cleanup and feature checks.

### 0.8.1

Install, validate and roll back one profile and multiple Git add-ons together. English and German CLI, descriptions and developer guides are available. Checkmk supports native OMD backups. Review the [migration guide](../commands/update-check.md) when upgrading an older controller.

### s0.8.1

English and German architecture and extension guides cover commands, profiles, Git add-ons and local packages. Add-on hooks can use `addon-index` and `addon-verify`.

### s0.8.0

Checkmk migration supports Docker or native OMD backups. Apache source and target paths are configurable, and Docker can skip its final summary pause. Removing obsolete stacks still requires confirmation.

### s0.7.0

Preview a local register migration with `tools/migrate_local_extensions.py --check`. Migration creates a private backup and retains approved hashes. [Register migration](../commands/update-check.md)

### s0.6.0

Select German or English with `--lang` or `controller_lang`. Both languages share sources and checksums. JSON reports add machine-readable status codes.

### s0.5.0

SSS moves into a separate optional add-on. Register an active SSS installation before changing controller versions. [Migration and rollback](../commands/update-check.md)

### s0.4.1

Git add-ons are checked with the base and site profile. The install receipt tracks file ownership and rollback restores it alongside files and module versions.

### s0.4.0

The controller sends email and Telegram reports while hosts keep their local SQLite records and cron. Use `jobs-last --limit TARGET` or `bin/job-status` to inspect results. Pilot the library and explicitly choose a summary schedule. Homelab backups require Homelab 0.3.0.

### 0.3.1

Use `module-versions` or `bin/control update-check --versions` to inspect installed modules. Open a new shell or run `reload` after updating.

### 0.3.0

My first GitHub release. The controller records script job results, handles the first Compose file when stopping stacks and requests privilege escalation for maintenance and root CA distribution.

<details>
<summary>Deutsch · frühere Versionshinweise</summary>

## 0.8.11 – Gültige systemd-Pfadangaben

Diese Freigabe bündelt die Änderungen seit 0.8.2: zentrale Jobberichte setzen offene Versandkanäle nach Abbrüchen fort, bewerten wiederkehrende Cronfenster und können ausdrücklich ausgewählte systemd-Profile samt privaten Dienstordnern verwalten. Enthalten sind Jobmodul 0.5.4 und Controller-Prüfer 1.5.4.

Für bestehende Controller ist keine automatische Host-/Cronumstellung vorgesehen. Neue Dienstprofile zuerst mit privaten Quellen und `--check` prüfen. Ein lokales Freigaberegister bleibt an seinem vorhandenen Ort; eine gewünschte Schema- oder Pfadmigration erfolgt separat mit Vorschau und Sicherung. Siehe [Update und lokale Register](../commands/update-check.md) und [Dienstdeployment](../configurations/systemd-job-deployment.md).

Jobmodul 0.5.4 erzeugt WorkingDirectory und PIDFile ohne Anführungszeichen.
Die erzeugten Dienstdefinitionen werden dadurch von systemd korrekt geladen.
Bestehende Profile behalten ihre Pfade und ausdrücklichen Aktivierungseinstellungen.

## s0.8.10 – Cronfenster und Standardwerte im Dienstdeployment

Jobmodul 0.5.3 wertet mehrere tägliche und häufige Cronfenster korrekt aus.
Fristen lassen sich zentral vorgeben und pro Host, Job oder Eintrag überschreiben.
Lange laufende Jobs bleiben beim nächsten Termin sichtbar. Die Prüfung beendet
keine Prozesse und verändert keine Zeitpläne. Bestehende unvollständige Fenster
bleiben als unkonfiguriert erkennbar.

Das eigenständige Dienstdeployment stellt seine Rollen-Standardwerte auch dem
nachfolgenden Library-Schritt bereit. Root-Owner und -Group müssen nicht zusätzlich
in host_vars wiederholt werden. Vorhandene explizite Benutzer haben weiter Vorrang.

## s0.8.9 – Numerische Zeitwerte in Dienstprofilen

Jobmodul 0.5.2 akzeptiert Ansible-markierte Zahlen für Start-/Stop- und
Neustartzeiten. Boolesche Werte, unendliche und ungültige Zahlen bleiben gesperrt.
Zuvor konnte eine korrekte lokale JSON-/YAML-Profilkonfiguration bei der Vorprüfung
stoppen; vor diesem Fehler wurden keine Dateien oder Dienste verändert.

## s0.8.8 – Private Dienstkonfiguration nach Benutzer

Jobmodul 0.5.1 rendert optionale JSON-Einträge aus Hostvariablen und kann je
Systemd-Profil eine vollständige Library im privaten Benutzerordner installieren.
Dienste benötigen dadurch keine erweiterten Rechte am root-Skriptordner. Bestehende
Profile bleiben unverändert; neue Felder nur nach explizitem Pilot auswählen.

## s0.8.7 – Lokales Zusatzregister im Controllerzustand

Prüfer 1.5.4 erkennt auf ausdrückliche Einrichtung auch `.local/extensions`
innerhalb des Controllers. Der bisherige Nachbarordner bleibt unterstützt.
Schemawechsel, Rücknahme und weitere lokale Paketupdates funktionieren mit beiden
Ablagen; zwei gleichzeitige Register blockieren. Dateiinhalte und Freigabe-SHA
bleiben erhalten. Kein automatisches Verschieben beim Update. Für ältere Prüfer
den Registerordner vor dem Code-Rollback an den Nachbarpfad zurücklegen.

## s0.8.6 – Private Dienstordner und Units per Profil

Jobmodul 0.5.0 ergänzt explizite Quell-/Zielordner mit erhaltenen relativen Pfaden.
Geprüfte private Dateien bleiben außerhalb von Git; systemd-Units entstehen aus
Profilwerten. Das eigenständige Playbook `playbooks/scripts/deploy_systemd.yml`
benötigt kein altes Hostmanifest. Bestehende Listenprofile bleiben status-only.

Für die Nutzung private Profilmanifeste prüfen und zuerst mit `--check` planen.
Aktivieren, Starten oder Neustarten erfolgt ausschließlich durch explizite
Profilfelder. Kein automatischer Altbestandabbau, keine Konfigurationsmigration.
Die bestehende SQLite-Historie und zentralen Berichte bleiben erhalten.

## s0.8.5 – Systemd-Statusprofile im Skript-Deployment

Bestehende Dienste lassen sich ueber zentrale Profile und eine ausdrueckliche
Hostauswahl in lokale SQLite und die zentrale Summary einbinden. Das bestehende
Skript-Deployment verteilt die feste Statuskonfiguration; Zuordnungen werden
nicht aus Skript- oder Unitdateien erraten. Units, MainPID, Starts und Cron bleiben
bei dieser Statusanbindung unveraendert. Dauerlaeufer, Oneshots und optionale
Dienste werden getrennt bewertet; es handelt sich um Momentaufnahmen.

Fuer die Nutzung erst Library und ausgewaehlte Profile bereitstellen. Ohne
Profilauswahl bleibt das bisherige Verhalten erhalten. Bestandsabfrage 0.1.1
behandelt uninstanziierte Vorlagen separat statt als fehlgeschlagene Units.

## s0.8.4 – Custom-systemd-Bestand ohne Secret-Export

Ein eigenständiger lesender Ansible-Sammler findet Custom-/Skriptservices und
zugehörige Timer. Umgebungswerte, Konfigurationsinhalte und Befehlsargumente
bleiben auf dem Host. Ergebnisse liegen ungepackt pro Host vor; komplexe Starts
und Userdienste benötigen weitere Prüfung. Der Sammler ändert keine Units oder
Crons und übernimmt noch keine Schedulerzuordnung automatisch.

## s0.8.3 – Jobberichte nach Abbrüchen fortsetzen

Alle konfigurierten Versandkanäle werden zusammen mit dem Bericht vorgemerkt.
Nach einem Abbruch direkt nach der Mailbestätigung bleibt Telegram offen.
Ein fehlgeschlagener Ansible-Abfragelauf gilt auch bei einzelnen vorhandenen
Antworten als unvollständig; seine Teildaten werden nicht als vollständige
Sammlung übernommen. Der nächste Abruf setzt an den bisherigen Cursorn fort.

Keine Konfigurations- oder Datenbankmigration nötig. Hostjobs und Cron bleiben
unverändert. Zusätzliche Tests decken Abbrüche, Parallelversand, veraltete Abfragen
und die Übernahme vorhandener SQLite-Datenbanken ab.

## 0.8.2 – Controller-Prüfer 1.5.3

Die Prüfungen für Updates, Bereinigung und Feature-Schalter sind leichter zu pflegen. Befehle, Exitcodes und die Struktur der JSON-Berichte bleiben kompatibel. Eine Konfigurationsmigration ist für diesen Patch nicht nötig.

## s0.8.2 – Controller-Prüfer 1.5.3

Die Prüfungen für Updates, Bereinigung und Feature-Schalter sind leichter zu pflegen. Befehle, Exitcodes und die Struktur der JSON-Berichte bleiben kompatibel. Eine Konfigurationsmigration ist für diesen Patch nicht nötig.

## 0.8.1 – Profile, Add-ons und zweisprachige Bedienung

Ein Controller kann ein Standortprofil und mehrere Git-Add-ons gemeinsam installieren, prüfen und zurückrollen. CLI, Beschreibungen und Entwicklerleitfäden gibt es auf Deutsch und Englisch. Checkmk unterstützt native OMD-Backups. Für vorhandene Controller mit dem älteren Checker oder lokalen Freigaben zuerst den [Migrationsweg](https://github.com/v4z00/Ansible-Allgm/blob/main/descriptions/commands/update-check.md#sss-aus-einem-älteren-controller-übernehmen) mit Vorschau und Sicherung verwenden. Der erste Wechsel ist ein manueller Wartungsschritt.

## s0.8.1 – Developer guides / Entwicklerleitfäden

English and German guides cover the controller architecture, custom commands, profiles, Git add-ons and local packages. Add-on authors can create and verify their Git manifests with `addon-index` and `addon-verify`.

Die zweisprachigen Leitfäden zeigen die Architektur und den Weg vom ersten eigenen Befehl bis zum geprüften Zusatzpaket. Die neuen Manifestbefehle lassen sich direkt in Git-Hooks verwenden. Der Cleaner unterscheidet das Einlesen eines Git-Checkouts von einem tatsächlichen Aufrufer lokaler Skripte.

## s0.8.0 – Wählbare Betriebspfade und Backup-Modi

Checkmk sichert vor einer Migration wahlweise im Docker-Container oder direkt mit OMD auf dem Zielhost. Bei Apache sind Quellen, Dateinamen und Ziele einstellbar. Das Docker-Deployment kann die Abschlussanzeige ohne Pause schreiben. Verwaiste Stacks brauchen weiterhin eine bestätigte Löschfreigabe.

Alternative Controllerverzeichnisse werden von Shell, Job-Sammlung und Berichten berücksichtigt. Die bisherigen Befehlsnamen und Playbookpfade, darunter `postfix-queue-clear` und `clear_postfix_que.yaml`, bleiben für vorhandene Cronjobs und direkte Playbook-Aufrufe gültig.

## s0.7.0 – Lokale Freigaben migrieren

Neue Standortpakete verstehen deutsche und englische Dateiköpfe. Für einen
bestehenden Controller zeigt `tools/migrate_local_extensions.py --check` die
anstehende Registermigration an. Beim Übernehmen entsteht eine private
Sicherung. Die freigegebenen Skripte und Archivbelege behalten ihre SHA-256.
Die [Anleitung](../commands/update-check.md#lokales-register-migrieren)
beschreibt Vorschau, Wechsel und Rücknahme.

## s0.6.0 – Deutsch und Englisch auf einem Controller

`bin/control --lang en help` zeigt die englische Hilfe. Dauerhaft lässt sich
die Sprache über `controller_lang` einstellen. Beschreibungen teilen sich in
beiden Sprachen dieselben Quellen und SHA-Prüfsummen. Technische Tasknamen
stehen auf Englisch. JSON-Berichte ergänzen maschinenlesbare Statuscodes.

## s0.5.0 – SSS als eigenes Git-Add-on

Die Basis liefert den SSS-Notfallkoffer jetzt über das optionale Add-on.
Bestehende Installationen mit aktivem SSS brauchen dessen Registrierung vor
dem Wechsel. Der [Migrationsweg](../commands/update-check.md#sss-aus-einem-%C3%A4lteren-controller-%C3%BCbernehmen)
erhält lokale Anpassungen und beschreibt die Rücknahme.

## s0.4.1 – Gemeinsame Updates für Profile und Add-ons

Der Checker prüft registrierte Git-Add-ons zusammen mit der Basis und dem Standortprofil.
Die lokale Installationsquittung hält je Datei fest, welches Modul sie geliefert hat.
Bei einem Rollback werden die Dateien, die Modulversionen und die vorherige Quittung gemeinsam wiederhergestellt.

## s0.4.0 – Zentrale Jobberichte und lokale Statusabfrage

26. November 2026

Telegram und Mail zeigen eine kompakte Zeile je Host/Job mit passendem Symbol;
Details stehen nur unter Fehlern und Warnungen. Allgemeine und getrennte
Vzdump-Berichte sendet der Controller. Hosts arbeiten mit lokaler SQLite und Cron
weiter und erhalten keine Versandzugangsdaten. `jobs-last --limit ZIEL` und der
lokale Helfer `bin/job-status` zeigen den neuesten Zustand je Job. Eigene
Ansible-Ergebnisse und Vorabfehler werden zentral erfasst.

Zum Umstieg zuerst die Hostlibrary in einem Testpfad aktualisieren und anschließend
den Controller mit den bestehenden Kanalwerten und einem ausdrücklichen
Summary-Zeitplan einrichten. Git-Update allein ändert keine Host-Crons.
Homelab-Backups benötigen dazu Homelab 0.3.0.

## 0.3.1 – Versionsanzeige für Controller-Module

`module-versions` zeigt die installierten Controller-Module an. In Skripten funktioniert auch `bin/control update-check --versions`. Nach dem Update eine neue Shell öffnen oder `reload` aufrufen.

## 0.3.0 – Mein Start mit GitHub

24. November 2026

Mit diesem Release fange ich an, die Änderungen an meiner Ansible-Basis auf GitHub festzuhalten. Hier steht künftig, was sich für den Controller ändert.

- Skript-Jobs lassen sich auf dem Controller auswerten. Die Übersicht zeigt Läufe und Ergebnisse.
- Beim Stoppen eines Compose-Projekts verwendet Ansible die erste gemeldete Compose-Datei. Das funktioniert auch bei mehreren Dateien und bei Sonderzeichen im Pfad.
- Die Wartungsplaybooks und die Verteilung der Root-CA fordern die nötigen Rechte an. Der Update-Checker berücksichtigt getrennt installierte Erweiterungen.

</details>
