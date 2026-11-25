# Changelog

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
