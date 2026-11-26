# Changelog

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

## s0.8.2 – Controller-Prüfer 1.5.3

Die Prüfungen für Updates, Bereinigung und Feature-Schalter sind leichter zu pflegen. Befehle, Exitcodes und die Struktur der JSON-Berichte bleiben kompatibel. Eine Konfigurationsmigration ist für diesen Patch nicht nötig.

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
