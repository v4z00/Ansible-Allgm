# Changelog

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
