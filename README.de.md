[English](README.md) | [Deutsch](README.de.md)

# Ansible-Allgm

Hallöchen! Hier liegt meine gehärtete Ansible-Controller-Basis für Debian 12 und 13. Sie erzeugt Inventories aus Proxmox, verwaltet Docker-Stacks, bindet Checkmk an und erfasst Jobs lokal in SQLite. Ein optionales Standortprofil und weitere Add-ons nutzen dieselbe SHA-256-Prüfung und denselben Rollback.

## Für wen lohnt sich das?

Ich nutze die Basis für wiederkehrende Wartung auf mehreren Hosts. Sie passt zu IT-Dienstleistern, internen IT-Teams und größeren Proxmox- oder Docker-Homelabs, wenn man wissen will, welcher Stand läuft, was ein Job gemacht hat und wie man ein Update zurücknimmt. Für drei Raspberry Pis ist der ganze Controller meist zu groß. Einzelne Rollen, die Bash-Bibliothek und der SSS-Notfallkoffer lassen sich auch für sich nutzen. [Rollen](roles/) · [Skriptbibliothek](artifacts/script-library/) · [SSS-Notfallkoffer](https://github.com/v4z00/Ansible-SSS)

## Ein erster Blick auf den Controller

Angenommen, du willst eine Gruppe Debian-Gäste warten. Im Controller-Verzeichnis kannst du zuerst nachsehen, was installiert ist und welche Befehle bereitstehen:

```sh
bin/control module-versions
bin/control list
bin/control --lang de help
```

Das Inventory liefert die Ziele. Die Befehlsregistrierung verbindet eine Aktion mit dem passenden Skript oder Playbook. Der Katalog beschreibt die Parameter, damit dieselbe Aktion auch in der TUI funktioniert. Beim Baseline-Lauf wählst du zum Beispiel gezielt eine Inventory-Gruppe oder ausdrücklich alle Hosts. [Baseline und Zielauswahl](descriptions/commands/base.md)

| Verzeichnis | Was du dort findest |
| --- | --- |
| [playbooks/](playbooks/) und [roles/](roles/) | Wartung, Zertifikatsverteilung und Updates von Docker-Stacks. |
| [bin/control.d/](bin/control.d/) und [descriptions/](descriptions/) | Registrierte Befehle und die dazugehörigen Bedienhinweise. |
| [examples/first_run/](examples/first_run/) | Vorlagen für ein neues Inventory und die lokalen Einstellungen. Die echten Host- und Gruppenvariablen liegen auf dem Controller. |
| [artifacts/script-library/](artifacts/script-library/) | Funktionen und Jobberichte für eigene Skripte. |

Vor einem Update vergleichst du den installierten Stand mit der stabilen Version über `bin/control update-check --remote`. Nach Prüfung des Ergebnisses kannst du den Wechsel mit `--apply` auslösen.

## Einstieg

Für einen frischen Controller gibt es den Debian-Installer. Bei einer bestehenden Installation zuerst die Hinweise zur Übernahme lesen. Im installierten Verzeichnis zeigt `bin/control list` die verfügbaren Befehle, `bin/control module-versions` die installierten Module. Bestehende Controller ohne Sprachvorgabe starten weiter auf Deutsch. Bei einer Erstinstallation kannst du Deutsch oder Englisch wählen. [Installation](descriptions/configurations/installation-allgm.md#schnellinstallation) · [Updates und Rollback](ARCHITECTURE.de.md)

Entwickelt und getestet wird auf `staging`. Der Installer und geplante Updates beziehen `main`. [Architektur](ARCHITECTURE.de.md) · [Eigene Erweiterungen](EXTENDING.de.md) · [Changelog](descriptions/releases/allgm.md) · [GitHub-Releases](https://github.com/v4z00/Ansible-Allgm/releases)

## Sprache im Bestand

Ohne Sprachvorgabe verwendet der Controller weiter Deutsch. Für einen einzelnen Aufruf reicht zum Beispiel `bin/control --lang en help`. Um Deutsch ausdrücklich zu speichern, gibt es den [Sprachhelfer](tools/set-controller-language.py). Er zeigt auf Wunsch eine Vorschau und sichert die vorhandene Datei vor der Änderung.

```sh
.venv/bin/python tools/set-controller-language.py --check
.venv/bin/python tools/set-controller-language.py
```

## Weitere Projekte

- [Ansible-Homelab](https://github.com/v4z00/Ansible-Homelab) ergänzt die Basis um ein Standortprofil mit Backups, Storage und OpenWrt.
- [Ansible-TUI](https://github.com/v4z00/Ansible-TUI) zeigt die installierten Befehle und ihre Beschreibungen im Terminal.
- [Ansible-SSS](https://github.com/v4z00/Ansible-SSS) verteilt Wiederherstellungsdaten auf mehrere Anteile und läuft eigenständig oder als Controller-Add-on.

Ich programmiere nur selten selbst und entwickle das Projekt mit KI-Unterstützung. Wenn etwas bei dir anders läuft, schreib mir gern ein Issue mit Befehl, Version und erwartetem Ergebnis. Damit kann ich den Fehler nachstellen. [Issues](https://github.com/v4z00/Ansible-Allgm/issues) · [MIT-Lizenz](LICENSE)
