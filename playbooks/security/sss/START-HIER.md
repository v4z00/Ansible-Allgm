# SSS-Wiederherstellung starten

Lege das vollständige Werkzeugpaket in einem Ordner auf dem vorbereiteten Notfallrechner ab. Öffne die Dateien dort zusammen.

| System | Start | Voraussetzung |
| --- | --- | --- |
| Windows | `start-html.bat`, bei Bedarf `start-html.ps1` | Ubuntu in WSL |
| macOS | `start-html.command` | Python 3 und ssss, bei Bedarf über Homebrew |
| Linux | `bash start-html.sh` | Python 3 und ssss, auf Debian/Ubuntu über die Installationshilfe |

Installiere und teste die Voraussetzungen vor dem Offline-Einsatz. Lass das Startterminal offen und öffne die dort angezeigte lokale Adresse im Browser desselben Rechners. Beende den Dienst mit Strg+C.

Die HTML-Oberfläche unterstützt zwei Infra- oder drei Master-Teile. Verwende für andere Schwellenwerte, etwa zwei Master-Teile aus der Beispielkonfiguration, `python3 recover.py` im passenden Terminal. Starte den Befehl im Werkzeugordner. Unter Windows nutzt du das vorbereitete WSL-Terminal.

Zur [Anleitung für Vertrauenspersonen](BEDIENUNGSANLEITUNG.md).
