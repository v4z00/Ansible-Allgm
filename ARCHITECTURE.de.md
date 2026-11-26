[English](ARCHITECTURE.md) | [Deutsch](ARCHITECTURE.de.md)

# Aufbau des Controllers

Jeder Controller beginnt mit Allgm. Ein Profil bündelt einen gemeinsamen Aufbau für mehrere Controller. Ein Git-Add-on ergänzt eine Funktion auf ausgewählten Controllern. Eine Aufgabe für genau eine Installation bekommt ein lokales Playbook.

```text
1  Allgm-Basis (Laufzeit, Registry, Rollen und Bibliothek) -+
                                                            +--> /root/ansible/
2  Optionales Profil und Git-Add-ons -----------------------+
                                                                   |
                                                               update-check
                                                                   |
3  /root/ansible-local/  lokaler Code und Belege <-----------------+

4  Private Eingaben: Inventory, Variablen, Secrets, Skriptquellen
```

## Wohin gehört eine Änderung?

**Basis.** `bin/control` lädt die Befehle aus `bin/control.d/`. Jeder Eintrag verweist auf das ausführende Skript. Die CLI liest die Befehlstitel aus `descriptions/`. Die optionale TUI verwendet auch die Eingabefelder und Hilfetexte. Die Beschreibungen verwenden Schema 1. Die optionalen Abschnitte `i18n.de` und `i18n.en` teilen sich Feld-IDs, Befehlsargumente und Quellhashes. Ältere Beschreibungen zeigen ihren vorhandenen Text. Für die Sprache gilt in dieser Reihenfolge `--lang`, `CONTROLLER_LANG`, dann `controller_lang` in den Controller-Einstellungen. Standard ist Deutsch.

**Profil und Git-Add-ons.** Ein Profil wie Homelab benennt sich und seine erlaubten Ersetzungen in `controller-overlay.json`. Ein Add-on legt seine Dateien in `controller-addon.json` fest. SSS wird zum Beispiel unter `playbooks/security/sss/` eingehängt, sein Befehl unter `bin/control.d/` und seine Hilfe unter `descriptions/commands/`. Jeder verwaltete Pfad gehört genau einem Modul. Ein belegter Add-on-Pfad blockiert die Installation.

**Lokale Erweiterungen.** Mit `tools/local_extension.py` gibst du eine Datei über ihren SHA-256 frei und installierst sie unter `/root/ansible-local/code/`. Die zugehörige `register.json` führt die freigegebene Revision. Ein lokales Playbook kann gemeinsame Rollen aufrufen. Eine Einmalaufgabe lässt sich nach erfolgreichem Lauf und ausdrücklicher Bestätigung des Hashes archivieren. Zum Archiv gehören Datei, Prüfsumme und Laufbeleg. Der Update-Checker prüft diese Ebene separat. Ausführung und Archivierung startest du selbst.

**Private Betriebsdaten.** `inventory/`, `group_vars/`, `host_vars/`, eine etwaige `secrets.yml` und die Skriptquellen unter `/root/skripte-config/` pflegst du lokal. Bei der Erstinstallation entstehen lokale Dateien aus Beispielen. Git-Updates verwalten den ausgelieferten Code. Sichere die Betriebsdaten separat.

## Vom Git-Stand zur Rücknahme

1. **Quellen wählen.** Die lokale `versions.txt` führt `Modul|Version|HTTPS-URL|Token-Dateipfad`. Bei öffentlichen Quellen bleibt das vierte Feld leer. Für einen geschützten Abruf enthält es den Pfad zu einer privaten Token-Datei. Ein Git-Add-on braucht neben der Modulzeile den Eintrag `# addon=NAME`. `bin/control module-versions` zeigt die installierten Versionen.
2. **Vorschau ansehen.** Im Controllerverzeichnis prüft `bin/control update-check --remote` den Branch `main`. Mit `--staging` prüfst du Staging. Die Auswahl gilt für diesen Aufruf und alle aktiven Git-Module. Der Checker vergleicht Dateien mit den SHA-256-Manifesten und prüft Einstellungen, Registry und Pfadkonflikte. Die Manifeste sind unsigniert. Für die Herkunft der Freigabe vertraut der Controller der eingetragenen Git-Quelle.
3. **Übernehmen.** `bin/control update-check --apply` übernimmt Main, mit zusätzlichem `--staging` den Teststand. Installierte Versionen heißen auf Main `X.Y.Z`, auf Staging `sX.Y.Z`. Der Installationsbeleg `.controller-install.json` verzeichnet Dateihashes, zuständige Module und deren Revisionen. Bei Codeänderungen entsteht eine Rücksicherung unter `.local/controller-updates/`. Ein eingerichteter Cronjob mit `--auto` wählt auch nach einem Staging-Lauf Main. Standardmäßig bewahrt er Sicherungen vier Tage auf. Die jüngste bleibt erhalten.
4. **Zurücksetzen.** Hast du das lokale Register migriert und benötigt der alte Checker Schema 1, stelle zuerst das Register wieder her. Verwende `python3 tools/migrate_local_extensions.py --rollback REGISTER_BACKUP` mit dem Sicherungspfad, den die Registermigration gemeldet hat. Für den Code folgt `bin/control update-check --rollback SNAPSHOT_ID` mit der Kennung aus dem Code-Update.

[Entwickleranleitung im Git-Repo](EXTENDING.de.md) · [Installation](descriptions/configurations/installation-allgm.md) · [Befehle für Update und Rücknahme](descriptions/commands/update-check.md)
