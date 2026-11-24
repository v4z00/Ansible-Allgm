Hallöchen, das ist mein Repo für Ansible auf Debian. Hier findest du die Rollen, den Update-Check und die Bash-Funktionen, auf denen meine weiteren Ansible-Projekte aufbauen.

Ich entwickle dieses Projekt mit KI-Unterstützung. Ich programmiere selbst. Für die vielen Details zwischen einer Idee und einem getesteten Update fehlt mir im Alltag oft die Zeit. Die KI hilft mir beim Schreiben und Testen. Welche Änderungen ich übernehme, entscheide ich selbst.

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
