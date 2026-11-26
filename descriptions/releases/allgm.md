# Changelog

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
