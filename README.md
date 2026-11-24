Hallöchen, das ist mein Repo für Ansible auf Debian. Hier findest du die Rollen, den Update-Check und die Bash-Funktionen, auf denen meine weiteren Ansible-Projekte aufbauen.

Ich programmiere selbst nur selten. Die Ideen und Anforderungen kommen von mir. Beim Schreiben und Testen des Codes hilft mir KI. Welche Änderungen ich übernehme, entscheide ich selbst.

Bitte probier die Playbooks zuerst mit Testdaten aus und prüfe vor dem Ausführen die Zielhosts. Wenn dir ein Fehler auffällt oder du eine einfachere Lösung kennst, schreib mir gern ein Issue oder schick einen Pull Request. Ich schaue mir die Vorschläge an und übernehme, was zum Projekt passt.

## Installation per Pipe

Für Debian 12 und 13. Für den ersten Abruf müssen `curl`, CA-Zertifikate und für die gezeigten Aufrufe `sudo` verfügbar sein. Fehlende Startwerkzeuge auf einem Minimalsystem als root mit `apt-get update && apt-get install -y ca-certificates curl sudo` installieren.

```bash
(set -o pipefail; curl -qfsSL --proto "=https" --proto-redir "=https" "https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/install.sh" | sudo bash)
```

Der Installer prüft die SHA-256-Manifeste vor der Installation, richtet `/root/ansible` ein und trägt die HTTPS-Origins in die lokale `versions.txt` ein. Die Repo-Adressen gehören zum GitHub-Konto `v4z00`.

## Arbeit mit einem Checkout

Commits aktualisieren das SHA-256-Manifest über `.githooks`. Nach dem Klonen
für die Entwicklung `git config core.hooksPath .githooks` ausführen.

Gemeinsame Basis. Einstieg auf Debian: `bin/install-controller --target PFAD`.
`bin/control update-check` prüft den Controller. Mit `--remote`, `--apply` und
`--auto` bezieht er den freigegebenen Code aus `main`.

Auf dem Controller Allgm anonym über HTTPS klonen, z. B. mit
`git clone --branch main https://github.com/v4z00/Ansible-Allgm.git`.
Der Installer übernimmt die HTTPS-Origin in die lokale `versions.txt`
(Modus 0600). Ihr Kommentar erklärt das Format
`Modul|Version|Repo-URL|Token-Dateipfad`. Bei Allgm bleibt das letzte Feld leer.
Der Update-Check erhält lokale Kommentare, weitere Module und eingetragene Pfade.

## Erstinstallation auf Debian

Auf einem frischen Debian 12/13 den Checkout außerhalb von `/root/ansible` ablegen. Aus diesem Repo als root starten. Der Installer ergänzt fehlende Debian-Pakete über APT, richtet die Ansible-Laufzeit ein und legt bei leerem Ziel lokale Startdateien an.

```sh
./bin/install-controller --target /root/ansible
```

## Bestehenden Controller migrieren

Bei einem bestehenden `/root/ansible/bin/control` den Checkout getrennt ablegen. Aus diesem Repo zuerst die Vorschau aufrufen und die zum Ersetzen markierten lokalen Codeänderungen vergleichen. Den angezeigten Plan-Hash erst nach Prüfung einsetzen.

```sh
./bin/install-controller --target /root/ansible --update
./bin/install-controller --target /root/ansible --update --apply PLAN_SHA256
/root/ansible/bin/control update-check --remote
```

Inventory, lokale Gruppen- und Hostvariablen sowie eigene Dateien außerhalb der angezeigten Codepfade bleiben erhalten. Der Installer gibt eine Sicherungskennung aus. Der Rückweg vor dem nächsten Codewechsel lautet `./bin/install-controller --target /root/ansible --rollback SICHERUNGSKENNUNG`.

Für bestehende Namenskonventionen die Zuordnungen in `checkmk_tenant_prefixes` und gegebenenfalls `checkmk_folder_scopes` lokal pflegen. Vor Übernahme einer neu erzeugten Hostliste die Namen und Ordner mit dem bisherigen Inventory vergleichen. Für den Docker-Benutzerexport die lokale Quelle über `ANSIBLE_DOCKER_CONFIG_ROOT` setzen.

## Bash-Bibliothek

Die öffentlichen Artefakte aus der gemeinsamen Bibliothek 0.2.0 liegen unter
`artifacts/script-library/lib/`. Der Loader stellt die Funktionen aus `common/`
bereit. Die Mailfunktionen nutzen zusätzlich `data/mail-translations.json`.
Für den Rollout auf den ausgewählten Host im installierten Controller:

```sh
cd /root/ansible
.venv/bin/ansible-playbook playbooks/scripts/stage_library.yml --limit ZIELHOST
```

Auf dem Zielhost lädt ein eigenes Bash-Skript die Bibliothek mit
`source /root/script-config/lib/load.sh`. Eine unabhängige Funktion wie
`hm_log` lässt sich nach der Veröffentlichung auch einzeln beziehen:

```sh
curl -fsSLo hm_log.sh https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/artifacts/script-library/lib/common/hm_log.sh
```

Die SHA-256-Werte jeder Datei stehen in `SHA256SUMS.json`.

## Aufbau und lokale Erweiterungen

| Pfad | Zweck |
|---|---|
| `bin/control` | Einstieg für Betrieb und Update-Check |
| `playbooks/`, `roles/` | Gemeinsame, über Git aktualisierte Abläufe |
| `tools/local_extension.py` | Lokale Dateien freigeben, installieren, ausführen und archivieren |
| `/root/ansible-local/code/` | Separat installierte Rollen, Playbooks, Skripte und lokale Variablendateien |
| `/root/ansible-local/register.json` | Freigegebene Pfade und SHA-256 |
| `/root/ansible-local/runs/`, `archiv/` | Lokale Ausführungs- und Archivbelege |

Nach der oben beschriebenen Basisinstallation kann ein eigenes Erweiterungspaket hinzukommen. Lege es außerhalb eines Git-Checkouts an. Für ein erstes Beispiel auf einem Debian-Controller als root:

```bash
mkdir -p /root/mein-paket/code/scripts
cat > /root/mein-paket/code/scripts/beispiel.sh <<'SH'
#!/bin/bash
# manuell-integriert: ja
# bereinigung: nach-erfolg-archivieren
echo 'Lokale Beispielaufgabe abgeschlossen.'
SH
cd /root/ansible
datei=scripts/beispiel.sh
sha=$(sha256sum "/root/mein-paket/code/$datei" | cut -d ' ' -f 1)
python3 tools/local_extension.py approve /root/mein-paket "$datei" "$sha"
python3 tools/local_extension.py install /root/mein-paket
bin/control update-check --only local
python3 tools/local_extension.py run "$datei"
python3 tools/local_extension.py archive "$datei"
```

Der letzte Befehl zeigt die Vorschau. Nach Prüfung der Aufrufer archiviert `python3 tools/local_extension.py archive "$datei" --confirm-sha "$sha"` diese Dateiversion. Im ausgegebenen Archivordner liegen die Datei, `BELEG.json` mit freigegebenem SHA-256, gemessenem Archiv-SHA und Laufnachweis sowie `SHA256SUMS`. Dort prüft `sha256sum -c SHA256SUMS` die archivierten Bytes.

Für dauerhafte Dateien verwende `# bereinigung: behalten`. In YAML stehen beide Kommentarzeilen direkt unter `---`, in ausführbaren Skripten unter der Shebang. Lokale Playbooks liegen unter `code/playbooks/` und laufen mit `python3 tools/local_extension.py run playbooks/beispiel.yml --limit ZIELGRUPPE`. Jede Änderung zuerst in der privaten Pflegequelle prüfen, mit ihrer neuen SHA freigeben und das Paket erneut installieren. Eine unveränderte archivierte Revision bleibt archiviert.

`bin/control update-check` meldet lokale Erweiterungen in einem eigenen Abschnitt. `--json` enthält dafür `local_extensions`. Der bestehende Cron-Aufruf mit `--auto` prüft die lokalen SHA-256 vor dem Git-Abruf. Fehlende, zusätzliche oder veränderte Dateien blockieren den Wechsel. Ein Controller ohne eingerichtete Erweiterungen arbeitet wie bisher. Cron führt lokale Aufgaben und Archivierungen niemals selbst aus.

## Ein Zusatzplaybook zu einem vorhandenen Standort liefern

Die gemeinsamen Playbooks und Rollen unter `/root/ansible` beziehen ihre Updates aus Git. Für eine standortspezifische Aufgabe ein eigenes Playbook mit eindeutigem Namen schreiben. Es darf die regulären Basisrollen aufrufen. Ein lokales Zusatzpaket trägt dieselbe Standortkennung wie das vorhandene Standortpaket und einen eigenen Namen. Beide können getrennt gepflegt werden.

Im privaten Arbeitsverzeichnis das vorhandene Standortpaket als ersten Parameter angeben. Der zweite Parameter ist ein neuer Ordner. Beispiel für Debian:

```bash
werkzeug=/root/ansible/tools/local_extension.py
python3 "$werkzeug" new-supplement ./standort ./zusatz dienstpruefung
mkdir -p ./zusatz/code/playbooks
cp ./local_dienst_pruefen.yml ./zusatz/code/playbooks/
datei=playbooks/local_dienst_pruefen.yml
sha=$(sha256sum "./zusatz/code/$datei" | cut -d ' ' -f 1)
python3 "$werkzeug" approve ./zusatz "$datei" "$sha"
```

Das oben beschriebene Kommentarformat gilt auch für den Zusatz. Das Standortpaket muss auf dem Ziel bereits registriert sein. Den Ordner `zusatz` auf diesen Controller kopieren. Dort als root registrieren und überprüfen:

```bash
cd /root/ansible
python3 tools/local_extension.py install /root/eingang/zusatz
bin/control update-check --only local
```

Der Checker meldet den Zusatznamen und prüft die Dateien auch beim Cronlauf. Fehlt eine lokale Datei in einer späteren Standortlieferung, bleibt die registrierte Revision erhalten. Nur eine bewusste Lieferung desselben lokalen Pakets kann dessen Datei aktualisieren. Ein fremder Paketpfad oder eine gleichnamige Controllerrolle blockiert die Übernahme. Den fachlichen Lauf separat und mit konkreter Zielauswahl starten, etwa mit `python3 tools/local_extension.py run playbooks/local_dienst_pruefen.yml --limit ZIELHOST`.

## Docker-Update und Portainer

`bin/control docker-update --limit ZIELHOST` wartet bei jedem aktualisierten Compose-Stack auf laufende Dienste oder deren erfolgreichen Healthcheck (bis zu 180 Sekunden je Stack). Danach prüft es die Compose-Quellen und Docker-Netze. Ein Fehler lässt den Lauf fehlschlagen.

Nur der zusätzliche TCP-Test für Portainer ist schaltbar. In den **lokalen Hostvariablen** des betreffenden Docker-Hosts `portainer_check_enabled: true` setzen. Mit `false` oder ohne Eintrag entfällt der Verbindungsversuch. Standardmäßig prüft der Controller die Ansible-Adresse des Hosts auf Port 9443 mit fünf Sekunden Wartezeit. Ein abweichendes Ziel ist über `portainer_check_host`, `portainer_check_port` und `portainer_check_timeout` konfigurierbar. Der Einzelaufruf lautet `.venv/bin/ansible-playbook playbooks/docker/check_portainer.yml --limit ZIELHOST`.
