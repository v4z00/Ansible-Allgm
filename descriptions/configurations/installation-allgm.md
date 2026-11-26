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
  "source_hashes": {},
  "i18n": {
    "de": {
      "title": "Ansible-Allgm auf Debian installieren",
      "description": "# Ansible-Allgm auf Debian installieren\n\n## Schnellinstallation\n\nFür Debian 12 und 13. Für den ersten Abruf müssen `curl`, CA-Zertifikate und für die gezeigten Aufrufe `sudo` verfügbar sein. Fehlende Startwerkzeuge auf einem Minimalsystem als root mit `apt-get update && apt-get install -y ca-certificates curl sudo` installieren.\n\n\u0060\u0060\u0060bash\n(set -o pipefail; curl -qfsSL --proto \"=https\" --proto-redir \"=https\" \"https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/install.sh\" | sudo bash)\n\u0060\u0060\u0060\n\nDer Installer prüft die SHA-256-Manifeste vor der Installation, richtet `/root/ansible` ein und trägt die HTTPS-Origins in die lokale `versions.txt` ein.\n\n## Installation aus einem Checkout\n\n`bin/control update-check` prüft den Controller. Mit `--remote`, `--apply` und\n`--auto` bezieht er den freigegebenen Code aus `main`.\n\nAuf dem Controller Allgm anonym über HTTPS klonen, z. B. mit\n`git clone --branch main https://github.com/v4z00/Ansible-Allgm.git`.\nDer Installer übernimmt die HTTPS-Origin in die lokale `versions.txt`\n(Modus 0600). Ihr Kommentar erklärt das Format\n`Modul|Version|Repo-URL|Token-Dateipfad`. Bei Allgm bleibt das letzte Feld leer.\nDer Update-Check erhält lokale Kommentare, weitere Module und eingetragene Pfade.\n\nAuf einem frischen Debian 12/13 den Checkout außerhalb von `/root/ansible` ablegen. Aus diesem Repo als root starten. Der Installer ergänzt fehlende Debian-Pakete über APT, richtet die Ansible-Laufzeit ein und legt bei leerem Ziel lokale Startdateien an.\n\n\u0060\u0060\u0060sh\n./bin/install-controller --target /root/ansible\n\u0060\u0060\u0060\n\n## Bestehenden Controller übernehmen\n\nBei einem bestehenden `/root/ansible/bin/control` den Checkout getrennt ablegen. Aus diesem Repo zuerst die Vorschau aufrufen und die zum Ersetzen markierten lokalen Codeänderungen vergleichen. Den angezeigten Plan-Hash erst nach Prüfung einsetzen.\n\n\u0060\u0060\u0060sh\n./bin/install-controller --target /root/ansible --update\n./bin/install-controller --target /root/ansible --update --apply PLAN_SHA256\n/root/ansible/bin/control update-check --remote\n\u0060\u0060\u0060\n\nInventory, lokale Gruppen- und Hostvariablen sowie eigene Dateien außerhalb der angezeigten Codepfade bleiben erhalten. Der Installer gibt eine Sicherungskennung aus. Der Rückweg vor dem nächsten Codewechsel lautet `./bin/install-controller --target /root/ansible --rollback SICHERUNGSKENNUNG`.\n\nFür bestehende Namenskonventionen die Zuordnungen in `checkmk_tenant_prefixes` und gegebenenfalls `checkmk_folder_scopes` lokal pflegen. Vor Übernahme einer neu erzeugten Hostliste die Namen und Ordner mit dem bisherigen Inventory vergleichen. Für den Docker-Benutzerexport die lokale Quelle über `ANSIBLE_DOCKER_CONFIG_ROOT` setzen.\n\n## Am Repo mitarbeiten\n\nAktiviere im Entwicklungs-Checkout einmalig die Git-Hooks mit `git config core.hooksPath .githooks`. Beim Commit aktualisieren sie das SHA-256-Manifest.",
      "fields": {}
    },
    "en": {
      "title": "Install Ansible-Allgm on Debian",
      "description": "# Install Ansible-Allgm on Debian\n\n## Quick install\n\nFor Debian 12 and 13. The initial fetch needs `curl`, CA certificates and, for the commands below, `sudo`. On a minimal system, run `apt-get update && apt-get install -y ca-certificates curl sudo` as root first.\n\n\u0060\u0060\u0060bash\n(set -o pipefail; curl -qfsSL --proto \"=https\" --proto-redir \"=https\" \"https://raw.githubusercontent.com/v4z00/Ansible-Allgm/main/install.sh\" | sudo bash)\n\u0060\u0060\u0060\n\nThe installer verifies the SHA-256 manifests, prepares `/root/ansible` and records the HTTPS origins in local `versions.txt`.\n\n## Install from a checkout\n\n`bin/control update-check` checks the controller. With `--remote`, `--apply` or `--auto` it fetches released code from main.\n\nClone Allgm anonymously over HTTPS, for example with `git clone --branch main https://github.com/v4z00/Ansible-Allgm.git`. The installer records the HTTPS origin in local `versions.txt` (0600). Its comment describes the four fields: module, version, repository URL and token-file path. The last field is empty for Allgm. Updates preserve local comments, additional modules and configured paths.\n\nOn fresh Debian 12/13, keep the checkout outside `/root/ansible`. Start from this repository as root. The installer uses APT for missing Debian packages, configures Ansible and initializes local files only on an empty target.\n\n\u0060\u0060\u0060sh\n./bin/install-controller --target /root/ansible\n\u0060\u0060\u0060\n\n## Adopt an existing controller\n\nIf `/root/ansible/bin/control` exists, keep the checkout separate. Preview from this repository first and compare local code changes marked for replacement. Use the displayed plan hash only after review.\n\n\u0060\u0060\u0060sh\n./bin/install-controller --target /root/ansible --update\n./bin/install-controller --target /root/ansible --update --apply PLAN_SHA256\n/root/ansible/bin/control update-check --remote\n\u0060\u0060\u0060\n\nInventory, local host and group variables and files outside the listed code paths are retained. The installer reports a backup ID. Before the next code change, roll back with `./bin/install-controller --target /root/ansible --rollback BACKUP_ID`.\n\nPreserve naming conventions with local `checkmk_tenant_prefixes` and, if needed, `checkmk_folder_scopes`. Compare generated names and folders against the previous inventory before accepting a new host list. Set `ANSIBLE_DOCKER_CONFIG_ROOT` to the local export source for Docker users.\n\n## Contribute\n\nIn the development checkout, enable Git hooks once with `git config core.hooksPath .githooks`. Commits refresh the SHA-256 manifest.",
      "fields": {}
    }
  }
}
```
