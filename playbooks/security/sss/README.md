# SSS – persönlicher Notfall-Stack

**HTML-Wiederherstellung auf Windows, macOS und Linux:** [START-HIER.md](START-HIER.md). Windows: `start-html.bat` (WSL/Ubuntu); Mac: `start-html.command` (Homebrew); Linux: `bash start-html.sh`. Alle Dateien zusammen entpacken. Die zentrale Ansible-Einrichtung bleibt auf Debian/Ubuntu.

Die ausführliche [Bedienungsanleitung für Vertrauenspersonen](BEDIENUNGSANLEITUNG.md)
erklärt beide Zugangsarten, Dokumentations- und Tresorablagen, Verschwiegenheit,
Wiederherstellung und KI-Hilfe. Das Playbook legt sie auch im Verzeichnis `offline/`
ab. Platzhalter für konkrete Kontakte und Ablageorte vor der Verteilung ausfüllen.

**Master (3 von 10) rekonstruiert das Vaultwarden-Master-Passwort.** Infra (2 von 6) bleibt der getrennte Infrastruktur-Zugang. Die KDBX ist die zusätzliche Offline-Notfallvariante. Ob sie dasselbe Passwort nutzt, muss separat eingerichtet, dokumentiert und getestet werden. Der Stack erstellt oder synchronisiert weder Vaultwarden-Daten noch KDBX-Dateien.

Dieser Ordner gehört nach `~/ansible/playbooks/SSS/` auf deinen **separaten Ansible-Host**.
Zielplattform: Debian/Ubuntu mit Ansible und Python 3. Keine Änderungen an deinem
normalen Inventory oder anderen Hosts. Kein Docker und kein dauerhaft laufender Dienst.

## Schnellstart

1. In `treuhaender.yml` die zehn Beispielpersonen durch echte Personen ersetzen.
   Jede Master-ID 1–10 und jede Infra-ID 1–6 muss genau einmal vergeben sein.
   `false` bedeutet „kein Teil“. Zusätzliche Personen nur für Infra sind möglich.
2. In `config.yml` Kontakt und konkrete Datenorte eintragen. Erst danach
   `konfiguration_bestaetigt: true` setzen. Die voreingestellten Regeln sind
   **Master: 3 von 10**, **Infra: 2 von 6**.
3. Auf dem Ansible-Host vorbereiten:

   ```bash
   cd ~/ansible/playbooks/SSS
   bash run.sh
   # Fehlende Pakete und nötige Admin-Rechte werden automatisch angefordert.
   ```

4. Konfiguration prüfen und interaktiv erzeugen:

   ```bash
   bash start-generator.sh --validate
   bash start-generator.sh
   ```

   `GENERIEREN` eingeben und das **bestehende Vaultwarden-Master-Passwort** sowie das vereinbarte **Infra-Passwort**
   jeweils zweimal verdeckt eingeben. Anschließend wählen: `1` = TOTP-Einrichtungsschlüssel, `2` = 2FA-Wiederherstellungscode, `0` = bisher nur Passwort. Den zweiten Zugangsschlüssel ebenfalls zweimal verdeckt eingeben. Keine Passwörter als CLI-Argumente,
   Ansible-Variablen, YAML-Werte oder Umgebungsvariablen verwenden.

5. Unter `/root/rescue/SSS/ausgaben/<satz-id>/` liegt pro Person eine HTML-Datei
   zum lokalen Öffnen und Drucken sowie dieselbe Unterlage als TXT. Die
   HTML-Dateien haben A4-Druckformat und benötigen keine externen Ressourcen.
   Lange Passwörter oder Beschreibungen können mehrere Seiten ergeben: in der
   Druckvorschau prüfen und alle Seiten gemeinsam versiegeln.

## Speicherorte und Sicherung

```text
~/ansible/playbooks/SSS/             # Code und nicht geheime Konfiguration
├── setup.yml
├── run.sh
├── config.yml
├── treuhaender.yml
├── files/
│   ├── generate.py
│   ├── recover.py
│   ├── start-html.sh
│   ├── install-voraussetzungen.sh
│   └── notfall_entschluesselung.html
└── tests/test_sss.py

/root/rescue/SSS/                    # nur auf dem Ansible-Host
├── config.json                     # Namen, Zuordnung, Kontakte; keine Schlüssel
├── bin/generate.py
├── offline/
│   ├── recover.py
│   ├── start-html.sh
│   ├── install-voraussetzungen.sh
│   └── notfall_entschluesselung.html
└── ausgaben/<satz-id>/              # enthält zusammen ALLE Schlüsselteile
    ├── person01.html / person01.txt
    ├── ...
    └── manifest.json               # Zuordnung und Prüfstatus; keine Passwörter
```

**Alle erzeugten Dateien bleiben unter `/root/rescue`**, außerhalb des gesicherten
Ansible-Verzeichnisses. Verzeichnisse haben 0700, erzeugte Dateien 0600; Eigentümer
ist root. Passwörter gelangen nicht in Ansible: Ansible installiert nur das
Werkzeug. Der Generator verarbeitet die Geheimnisse anschließend separat im RAM
und über stdin an `ssss`, ohne Shell. Core-Dumps werden für diese Prozesse deaktiviert.
Python garantiert keine vollständige RAM-Löschung; Swap und Terminalaufzeichnungen
müssen beim gewählten Generierungsrechner berücksichtigt werden.

Der Pfad allein ist **kein Backup-Ausschluss**: Wenn dein Host, `/root` oder die
gesamte VM gesichert bzw. gesnapshottet wird, kann `/root/rescue` trotzdem enthalten
sein. In diesen Jobs `/root/rescue` explizit ausschließen bzw. die Aufbewahrung
entsprechend planen. Bestehende Backup-Jobs werden durch diesen Stack nicht verändert.

`ausgaben/` enthält gemeinsam genug Material zum Öffnen beider Tresore. Diese
Unterlagen nicht gesammelt nach BookStack, GPO oder auf allgemeine Notfall-PCs
kopieren. Dort gehören ausschließlich die vorgesehenen verschlüsselten KDBX-Dateien,
die allgemeine Anleitung und das Werkzeug hin. Auch Druckspooler, PDF-Exporte und
Kopien auf einem Druckrechner berücksichtigen. Nach erfolgreicher Probe und Übergabe
die zentrale Aufbewahrung bzw. Entfernung der Druckdateien bewusst entscheiden;
der Stack löscht sie nicht automatisch.

## Voraussetzungen und automatische Admin-Abfrage

- `bash run.sh`: prüft und installiert bei Bedarf Python 3, ssss und ansible-core. Fordert auch für das Ansible-Deployment die nötigen Admin-Rechte an.
- `bash start-generator.sh`: prüft Voraussetzungen und startet den installierten Generator mit sudo beziehungsweise su, damit `/root/rescue` erreichbar ist. Zuerst `run.sh` ausführen.
- `bash start-html.sh`: installiert bei Bedarf Python 3 und ssss, danach Start der HTML-Wiederherstellung mit dem ursprünglichen Benutzer.
- `bash install-voraussetzungen.sh`: nur Voraussetzungen installieren; mit `--ansible` zusätzlich Ansible berücksichtigen. Im Quellstack liegt dieses Skript unter `files/`.
- `python3 recover.py`: kann fehlendes ssss über die mitgelieferte Installationshilfe nachinstallieren. Falls Python selbst fehlt, zuerst das Bash-Startskript verwenden.

Automatische Linux-Installation: **Debian/Ubuntu**, über die bereits konfigurierten Paketquellen. Unter macOS verwendet die Wiederherstellung Homebrew; unter Windows bereitet PowerShell WSL/Ubuntu vor (Einzelheiten und Admin-Abfragen in START-HIER.md). Erfordert Zugriff auf diese Quellen (normalerweise Internet) und ein berechtigtes Konto. Fehlende Berechtigungen, verweigerte Anmeldung oder Paketfehler führen zum Abbruch. Keine Passwörter in Dateien oder Kommandozeilenargumente eintragen; die Abfrage übernimmt sudo, su oder Ansible. Bei bereits gültiger sudo-Anmeldung beziehungsweise root kann eine erneute Passwortabfrage entfallen.

Für den echten Offline-Notfall alle Voraussetzungen vorher installieren und testen. Der Windows-Starter installiert bei Bedarf Ubuntu in WSL. Eine grafische Desktopumgebung oder ein Browser werden nicht automatisch installiert; die HTML-Nutzung setzt einen vorhandenen lokalen Browser voraus.

## HTML-Wiederherstellung – offline

Auf einem unabhängigen Debian/Ubuntu-Notfallrechner **vor dem Notfall** vorbereiten:

```bash
sudo apt-get update
sudo apt-get install python3 ssss
```

Alle Werkzeugdateien und Plattform-Starter aus `offline/` zusammen mit START-HIER.md und der Bedienungsanleitung auf das Offline-Medium kopieren.
Sie enthalten keine Geheimnisse. Zum Start auf diesem Rechner:

```bash
bash start-html.sh
```

Das Startskript prüft Python, ssss und die Werkzeugdateien. Es startet den lokalen Dienst und öffnet in einer grafischen Sitzung nach Möglichkeit den Browser. Fehlende Voraussetzungen werden auf Debian/Ubuntu automatisch nachinstalliert. Dafür fragt die Installationshilfe bei Bedarf per sudo nach dem Admin-Passwort; ohne sudo verwendet sie su und fragt nach dem root-Passwort. Sind alle Pakete vorhanden, erfolgt keine Rechteabfrage. Nach der Installation läuft die Wiederherstellung als der Benutzer, der das Startskript aufgerufen hat; starte es auf dem Desktop ohne sudo. Der Ordner muss für die ausführende Person lesbar sein. Das Terminal bis zum Ende geöffnet lassen.

Ohne automatischen Browserstart: `bash start-html.sh --no-browser`. Ohne Startskript: `python3 recover.py --web`.

Auf dem Ansible-Host liegt das Skript unter `/root/rescue/SSS/offline/start-html.sh`; dort gelten die root-Zugriffsrechte. Auf einem Server ohne grafische Sitzung öffnet sich kein Browser. Für die HTML-Bedienung die Werkzeugkopie auf dem vorbereiteten lokalen Linux-Desktop verwenden.

Die angezeigte Adresse `http://127.0.0.1:<port>/<zufallstoken>/` im Browser
**desselben Rechners** öffnen. Der Dienst lauscht ausschließlich auf Loopback,
nutzt einen zufälligen Port und Sitzungspfad und schreibt keine Zugriffslogs.
Keine Portfreigabe und keinen Reverse Proxy davor setzen. Mit Strg+C beenden.

Die HTML-Oberfläche läuft ohne Internet, CDN, Telemetrie oder Browser-Speicherung.
Oben wird die Zugangsart ausgewählt: **Infrastruktur – 2 Personen** oder
**Master – 3 Personen**. Es erscheinen genau zwei bzw. drei Eingabefelder.
Beim Wechsel werden Eingaben und Ergebnisse geleert. Browser und lokaler Dienst
prüfen, dass Bereich und Schwellenwert der Teile zur Auswahl passen. Diese beiden
HTML-Modi sind auf 2 bzw. 3 Personen festgelegt; andere konfigurierte Schwellenwerte
lassen sich nur über die Terminal-Variante wiederherstellen.
Sie sendet die Teile nur an das lokale `ssss-combine`. Ein Doppelklick auf die
HTML-Datei zeigt die Startanleitung; die Berechnung benötigt den lokalen Dienst.
**Es ist keine eigenständig rechnende HTML-Datei.** Unter Windows startet die BAT/PowerShell Ubuntu in WSL und öffnet die Oberfläche im Windows-Browser. Auf macOS startet die COMMAND-Datei den lokalen Dienst direkt. Die jeweilige Erstinstallation muss vor einem Offline-Notfall abgeschlossen sein; siehe START-HIER.md.

Alternativ ohne Browser:

```bash
python3 recover.py
```

Die Teile werden im Terminal verdeckt eingegeben; das Passwort wird erst nach
`ANZEIGEN` sichtbar. In beiden Varianten Satz und Bereich prüfen und exakt die
erforderliche Anzahl verschiedener Teile verwenden. Im Browser wird das Ergebnis
nach 60 Sekunden geleert. Master dient dem Vaultwarden-Zugang mit dokumentierter Serveradresse, Konto und gegebenenfalls 2FA. Infra dient dem dokumentierten Infrastruktur-Zugang. Für die KDBX-Offline-Variante Passwortzuordnung und Zusatzfaktoren separat prüfen; SSS ersetzt diese nicht.

## Master-Passwort und zweiter Zugangsschlüssel

Beim Erzeugen wird für Master zusätzlich nach der Art des zweiten Zugangsschlüssels gefragt. Unterstützt werden **TOTP-Einrichtungsschlüssel** oder **2FA-Wiederherstellungscode**. Ein aktueller sechsstelliger Code und ein API-client_secret sind dafür nicht vorgesehen. `0` lässt den bisherigen Passwort-only-Weg bestehen.

Die drei Master-Personen erhalten mit neuen **SSS2-Teilen** gemeinsam Zugriff auf beide Angaben. Der Generator verpackt sie strukturiert; Schrägstriche und Sonderzeichen im Passwort sind kein Trennzeichen. HTML und Terminal zeigen Passwort und zweiten Zugangsschlüssel getrennt an. Das TOTP-Secret wird lokal in einen vertrauenswürdigen Authenticator übernommen, der Wiederherstellungscode im vorgesehenen 2FA-Notfallverfahren verwendet. Beide werden nach 60 Sekunden aus der HTML-Anzeige geleert.

**Aktualisierung:** `bash run.sh` installiert die neue Version. Danach mit `bash start-generator.sh` neue Briefe erzeugen und alle neu erzeugten Sätze kontrolliert verteilen. Ein Generatorlauf erstellt sowohl Master- als auch Infra-Teile neu. Vorhandene Ausgaben werden nicht geändert. Alte SSS1-Teile bleiben mit dem neuen Werkzeug lesbar, enthalten aber weiterhin ausschließlich das ursprünglich gesicherte Passwort. Alte Werkzeugkopien erkennen SSS2 nicht; das komplette aktuelle Offline-Paket verteilen. Alte und neue Teile niemals mischen.

Master-Passwort: maximal 127 UTF-8-Bytes. Zweiter Zugangsschlüssel: maximal 128 UTF-8-Bytes. Das strukturierte Gesamtpaket wird in unabhängig mit ssss geteilte Blöcke zerlegt und pro Person zu einem vollständigen SSS2-Teil verbunden. Kein gemeinsames 127-Byte-Limit mehr. Intern maximal 1024 Paket-Bytes / 9 Blöcke. Alle Blöcke eines persönlichen Teils müssen übernommen werden. Infra bleibt unverändert SSS1.

## Format, Prüfung und neue Sätze

- Krypto-Operationen übernimmt `ssss`, keine eigene Shamir-Implementierung.
- UTF-8-Passwörter mit 1–127 Bytes werden unterstützt, einschließlich Leerzeichen,
  Anführungszeichen und Umlauten; Steuerzeichen sind ausgeschlossen. Master und
  Infra müssen unterschiedlich sein.
- `SSS1|satz|bereich|schwelle|anzahl|ssss-teil|prüfsumme` sichert ein Passwort. `SSS2|satz|master|schwelle|anzahl|block1~block2~…|prüfsumme` sichert die strukturierten Master-Zugangsdaten. Beide enthalten Metadaten und eine
  Tippfehler-Prüfsumme. Diese ist keine Signatur und schützt nicht vor absichtlicher
  Manipulation. Originalität der Umschläge separat sicherstellen.
- Der Generator prüft vor dem Schreiben **alle** Quoren gegen das eingegebene
  Passwort: standardmäßig 120 Master- und 15 Infra-Kombinationen.
- Jede Erzeugung hat eine neue zufällige Satz-ID; kein Überschreiben. Teile aus
  verschiedenen Sätzen werden abgelehnt. Ein abgebrochener Schreibvorgang wird
  mit `UNVOLLSTAENDIG` markiert und darf nicht verteilt werden.
- Ein neuer Satz widerruft alte Teile nicht. Bei unverändertem Passwort kann ein
  alter vollständiger Satz weiterhin den Tresor öffnen. Für einen echten Widerruf
  zuerst das betroffene Tresorpasswort ändern, danach neue Teile erzeugen und
  die Verteilung sowie alte Tresorkopien berücksichtigen.
- Das rohe ssss-Feld allein liefert bei manueller Wiederherstellung eine
  Hex-Kodierung. Das mitgelieferte Werkzeug dekodiert den `01`-Präfix und UTF-8.
  Fremde SSS-Browser-Tools sind nicht automatisch kompatibel. Diffusion bleibt aktiv.

## Abnahme vor der Verteilung

1. Einen vollständigen neuen Satz erstellen; kein `UNVOLLSTAENDIG` im Ausgabeordner.
2. Drei Master-Briefe auf dem vorbereiteten unabhängigen Notfallrechner kombinieren.
3. Mit dem Ergebnis den **realen Vaultwarden-Zugang** prüfen, einschließlich Konto und des gewählten zweiten Zugangsschlüssels. Wiederherstellungscodes nur gemäß dem dokumentierten Verfahren einsetzen und nach einem verbrauchenden Test den aktuellen Code neu sichern.
4. Zwei Infra-Briefe ebenso prüfen und den dokumentierten Infra-Zugang testen. Zusätzlich die KDBX-Offline-Variante unabhängig von Vaultwarden testen und ihre Passwortzuordnung dokumentieren.
5. Persönliche HTML-Dateien in der Druckvorschau prüfen, drucken und versiegeln.
   Übergabe und Satz-ID dokumentieren, ohne Schlüssel in die Übergabeliste zu kopieren.
6. KDBX-Dateien, Offline-Werkzeug und nötige Zusatzfaktoren vom Ansible-Host unabhängig
   verfügbar halten. GPO- und BookStack-Verteilung ist nicht Bestandteil dieses Stacks,
   weil dazu keine Zielpfade oder Zugangsdaten vorliegen.

## Entwicklertests

```bash
ansible-playbook -i localhost, setup.yml --syntax-check
python3 -m unittest discover -s tests -v
```

Die Integrationstests benötigen `ssss-split` und `ssss-combine` im PATH und verwenden
ausschließlich Testpasswörter. Fehlende ssss-Binaries führen zu expliziten Skips.
Ein Test startet kurz einen ausschließlich lokalen HTTP-Dienst.

Referenz für Hex-Modus und CLI-Optionen:
[Debian ssss-Handbuch](https://manpages.debian.org/bookworm/ssss/ssss.1.en.html).
