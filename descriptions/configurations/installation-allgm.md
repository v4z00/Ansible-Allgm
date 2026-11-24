# Ansible-Allgm auf Debian installieren

## Schnellinstallation

Für Debian 12 und 13. Für den ersten Abruf müssen `curl`, CA-Zertifikate und für die gezeigten Aufrufe `sudo` verfügbar sein. Fehlende Startwerkzeuge auf einem Minimalsystem als root mit `apt-get update && apt-get install -y ca-certificates curl sudo` installieren.

```bash
(set -o pipefail; curl -qfsSL --proto "=https" --proto-redir "=https" "https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/install.sh" | sudo bash)
```

Der Installer prüft die SHA-256-Manifeste vor der Installation, richtet `/root/ansible` ein und trägt die HTTPS-Origins in die lokale `versions.txt` ein.

## Installation aus einem Checkout

`bin/control update-check` prüft den Controller. Mit `--remote`, `--apply` und
`--auto` bezieht er den freigegebenen Code aus `main`.

Auf dem Controller Allgm anonym über HTTPS klonen, z. B. mit
`git clone --branch main https://github.com/v4z00/Ansible-Allgm.git`.
Der Installer übernimmt die HTTPS-Origin in die lokale `versions.txt`
(Modus 0600). Ihr Kommentar erklärt das Format
`Modul|Version|Repo-URL|Token-Dateipfad`. Bei Allgm bleibt das letzte Feld leer.
Der Update-Check erhält lokale Kommentare, weitere Module und eingetragene Pfade.

Auf einem frischen Debian 12/13 den Checkout außerhalb von `/root/ansible` ablegen. Aus diesem Repo als root starten. Der Installer ergänzt fehlende Debian-Pakete über APT, richtet die Ansible-Laufzeit ein und legt bei leerem Ziel lokale Startdateien an.

```sh
./bin/install-controller --target /root/ansible
```

## Bestehenden Controller übernehmen

Bei einem bestehenden `/root/ansible/bin/control` den Checkout getrennt ablegen. Aus diesem Repo zuerst die Vorschau aufrufen und die zum Ersetzen markierten lokalen Codeänderungen vergleichen. Den angezeigten Plan-Hash erst nach Prüfung einsetzen.

```sh
./bin/install-controller --target /root/ansible --update
./bin/install-controller --target /root/ansible --update --apply PLAN_SHA256
/root/ansible/bin/control update-check --remote
```

Inventory, lokale Gruppen- und Hostvariablen sowie eigene Dateien außerhalb der angezeigten Codepfade bleiben erhalten. Der Installer gibt eine Sicherungskennung aus. Der Rückweg vor dem nächsten Codewechsel lautet `./bin/install-controller --target /root/ansible --rollback SICHERUNGSKENNUNG`.

Für bestehende Namenskonventionen die Zuordnungen in `checkmk_tenant_prefixes` und gegebenenfalls `checkmk_folder_scopes` lokal pflegen. Vor Übernahme einer neu erzeugten Hostliste die Namen und Ordner mit dem bisherigen Inventory vergleichen. Für den Docker-Benutzerexport die lokale Quelle über `ANSIBLE_DOCKER_CONFIG_ROOT` setzen.

## Am Repo mitarbeiten

Aktiviere im Entwicklungs-Checkout einmalig die Git-Hooks mit `git config core.hooksPath .githooks`. Beim Commit aktualisieren sie das SHA-256-Manifest.

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "installation/allgm",
  "title": "Ansible-Allgm auf Debian installieren",
  "documented": true,
  "fields": [],
  "sources": [],
  "source_hashes": {}
}
```
