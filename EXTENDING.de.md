[English](EXTENDING.md) | [Deutsch](EXTENDING.de.md)

# Den Controller erweitern

Ein Registry-Befehl eignet sich für eine Bedienfunktion, ein Add-on für separat versionierte Playbooks oder Rollen und ein lokales Paket für Aufgaben auf einem einzelnen Controller. Die Beispiele bauen einen Befehl, installieren ein kleines Add-on und führen ein lokales Skript mit anschließender Archivierung aus.

Starte **in einem bereits committeten Checkout dieser Version von Ansible-Allgm**. Führe alle Blöcke der Reihe nach in derselben Bash-Sitzung als normaler Benutzer aus. Auf dem `PATH` werden Git, Ansible und Python 3.11–3.13 mit PyYAML benötigt. Das Beispiel arbeitet mit lokalen Klonen und einer Installation ohne Systempakete. Der einzige Push geht in ein temporäres Bare-Repository auf der Festplatte. Den ausgegebenen Laborpfad brauchst du zum Nachsehen.

<!-- example: setup -->
```bash
set -euo pipefail
umask 077
SOURCE=$(git rev-parse --show-toplevel)
LAB=$(mktemp -d)
LAB=$(cd "$LAB" && pwd -P)
export LAB BASE="$LAB/base" TARGET="$LAB/controller" ADDON="$LAB/heartbeat"
export BUNDLE="$LAB/site" SUPPLEMENT="$LAB/site-once"
export PYTHONDONTWRITEBYTECODE=1 CONTROLLER_PYTHON="$(command -v python3)"
git clone --quiet --no-local "$SOURCE" "$BASE"
cd "$BASE"
git switch -C staging
git config core.hooksPath .githooks
sha_file() { python3 -c 'import hashlib,pathlib,sys; print(hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest())' "$1"; }
printf 'Lab: %s\n' "$LAB"
```

## A · Einen Befehl mit Funktionsschalter registrieren

`demo-hello` liest `features.demo_hello` aus der lokalen `group_vars/all/settings.yml`. Fehlt der Schalter, bleibt der Befehl deaktiviert. Die Registry-Datei heißt wie der Befehl und enthält genau einen Eintrag. Der Handler liest den Gruß aus dem gewählten Sprachkatalog. Die Markdown-Beschreibung liefert Control den Titel und der TUI den Hilfetext. Ihre Quellhashes beziehen sich auf Registry, Handler und beide Übersetzungen.

Der Block schreibt Testeinstellungen **im frischen Klon**, um den Schalter auszuprobieren. Prüfe die neuen Quellen vor dem Release-Build. Das Werkzeug berechnet die Komponentenhashes aus diesem Offline-Baum. Beim Commit versiegelt der Git-Hook den vorgemerkten auslieferbaren Code.

<!-- example: A -->
```bash
cd "$BASE"
cat > bin/control.d/demo-hello.json <<'JSON'
{"schema":1,"commands":[{"name":"demo-hello","description":"Demo greeting","handler":"bin/control.d/demo-hello.sh","feature":"demo_hello","requires":["lib/control/i18n.sh"],"aliases":[]}]}
JSON
cat > bin/control.d/demo-hello.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=${CONTROL_PROJECT_ROOT:?}
source "$ROOT_DIR/lib/control/i18n.sh"
controller_tr demo.hello
SH
chmod +x bin/control.d/demo-hello.sh
printf '%s\n' '{"demo.hello":"Hello!"}' > lib/i18n/en/demo.json
printf '%s\n' '{"demo.hello":"Hallo!"}' > lib/i18n/de/demo.json

python3 - <<'PY'
from pathlib import Path
import hashlib, json

def read(name):
    return json.loads(Path(name).read_text())
def write(name, data):
    Path(name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
def sha(name):
    return hashlib.sha256(Path(name).read_bytes()).hexdigest()

registry = "bin/control.d/demo-hello.json"
handler = "bin/control.d/demo-hello.sh"
help_file = "descriptions/commands/demo-hello.md"
messages = ["lib/i18n/en/demo.json", "lib/i18n/de/demo.json"]
sources = [registry, handler, *messages]
languages = {"en": {"title": "Demo greeting", "description": "Print a greeting.", "fields": {}},
             "de": {"title": "Demogruß", "description": "Gibt einen Gruß aus.", "fields": {}}}
document = {"schema_version": 1, "kind": "command", "ref": "demo-hello", "title": "Demo greeting",
            "documented": True, "fields": [], "constraints": [], "sources": sources,
            "source_hashes": {p: sha(p) for p in sources}, "i18n": languages}
Path(help_file).write_text("# Demo greeting\n\n```json\n" + json.dumps(document, ensure_ascii=False, indent=2) + "\n```\n")

catalog = "scripts/feature_catalog.json"
features = read(catalog)
features["features"]["demo_hello"] = {"sources": ["group_vars/all/settings.yml", registry]}
write(catalog, features)
manifest = "update_check/manifests/controller_basis.json"
component = read(manifest)
for path in [*sources, help_file]:
    component["files"][path] = sha(path)
write(manifest, component)
PY
mkdir -p group_vars/all
printf 'features:\n  demo_hello: false\n' > group_vars/all/settings.yml
if bin/control demo-hello; then exit 1; fi
printf 'features:\n  demo_hello: true\n' > group_vars/all/settings.yml
bin/control --lang en demo-hello
bin/control --lang de demo-hello
python3 scripts/feature_audit.py --project-root "$BASE" --json > "$LAB/features.json"
python3 -c 'import json,sys; rows=json.load(open(sys.argv[1]))["features"]; assert any(r["key"]=="features.demo_hello" and r["status_code"]=="enabled" for r in rows)' "$LAB/features.json"
python3 tools/update_check/build_release.py --release-root "$BASE" --check-dir update_check --write --release-source-reviewed
git add -- bin/control.d/demo-hello.* descriptions/commands/demo-hello.md lib/i18n/{en,de}/demo.json scripts/feature_catalog.json update_check/manifests update_check/integrity.json
git -c user.name=Example -c user.email=example@example.invalid commit -qm 'Add a demo command'
```

Soll der Konfigurationsassistent diesen Schalter anbieten, ergänze ihn als optionalen Boolean in `update_check/settings_contract.json`, als Feld in `update_check/settings_catalog.json` und in beiden Sprachen der Settings-Beschreibung. Gib ihm in der Erstinstallations- und Referenzvorlage den neutralen Wert `false` und aktualisiere die Quellhashes der Beispiele. Bestehende Controller behalten ihre privaten Einstellungen. Einen reinen Registry-Schalter wie in diesem Beispiel kannst du direkt in den lokalen Einstellungen aktivieren.

## B · Ein Playbook als Add-on verpacken

`Heartbeat` erhält einen eigenen Zielordner unter `playbooks/`. Die Pfade in `payload` gelten relativ zur Wurzel des kleinen Quellrepos. Über `exports` lassen sich auch Registry-Handler und Beschreibungen an den Controller anbinden. Die leere Liste `replaces` hält die Zuständigkeiten eindeutig. Pro Installation gibt es höchstens ein exklusives Profil und beliebig viele Add-ons mit eigenen Namen und Pfaden.

Führe den Block in derselben Sitzung aus. Der Hook verwendet den Add-on-Modus des aus der geprüften Basis kopierten Werkzeugs. Er versiegelt alle getrackten Add-on-Dateien einschließlich der Hooks. Der Hashkatalog selbst ist ausgenommen. Jeder Entwickler setzt `core.hooksPath` in seinem eigenen Klon. In der Versionsdatei steht schlicht `0.1.0`. Bei einem Checkout auf `staging` setzt der Installer das `s` davor.

<!-- example: B -->
```bash
mkdir -p "$ADDON/.githooks"
cd "$ADDON"
git init --quiet -b staging
git config core.hooksPath .githooks
printf '0.1.0\n' > VERSION.txt
cat > controller-addon.json <<'JSON'
{"schema":1,"kind":"addon","name":"Heartbeat","mount_prefix":"playbooks/heartbeat","payload":["check.yml"],"exports":{},"replaces":[]}
JSON
cat > check.yml <<'YAML'
---
- name: Show the local heartbeat
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Print a heartbeat
      ansible.builtin.debug:
        msg: heartbeat
YAML
cp "$BASE/update_check/staging_manifest.py" .githooks/
cat > .githooks/pre-commit <<'SH'
#!/bin/sh
set -eu
exec python3 .githooks/staging_manifest.py addon-index Heartbeat
SH
cat > .githooks/pre-push <<'SH'
#!/bin/sh
set -eu
while read -r local_ref local_oid remote_ref remote_oid; do
    case "$local_oid" in
        *[!0]*) python3 .githooks/staging_manifest.py addon-verify Heartbeat "$local_oid" ;;
    esac
done
SH
chmod +x .githooks/pre-commit .githooks/pre-push
git add -- .githooks VERSION.txt controller-addon.json check.yml
git -c user.name=Example -c user.email=example@example.invalid commit -qm 'Add heartbeat playbook'
python3 .githooks/staging_manifest.py addon-verify Heartbeat HEAD
git init --quiet --bare "$LAB/heartbeat.git"
git push --quiet "$LAB/heartbeat.git" staging

cd "$BASE"
bin/install-controller --skip-runtime --target "$TARGET" --addon "$ADDON" \
  --addon-url Heartbeat=https://github.com/example/Ansible-Heartbeat.git
grep -Fx '# addon=Heartbeat' "$TARGET/versions.txt"
grep -Fx 'Heartbeat|s0.1.0|https://github.com/example/Ansible-Heartbeat.git|' "$TARGET/versions.txt"
cmp "$ADDON/check.yml" "$TARGET/playbooks/heartbeat/check.yml"
```

Die GitHub-URL des Beispiels wird als lokale Quellenangabe gespeichert. Gib für ein ausrollbares Add-on die HTTPS-URL deines veröffentlichten Repos an. Der Installer pflegt die vier Felder (`Modul|Version|HTTPS-URL|Token-Dateipfad`) und die Registrierung `# addon=Heartbeat` in der privaten `versions.txt` des Controllers. Bei einem öffentlichen Add-on bleibt das vierte Feld leer. Ein privates Add-on deklariert `"authentication":"token-file"`. Sein Installerargument `--addon-token-file Heartbeat=/absoluter/pfad` verweist auf eine Datei mit Modus `0600` außerhalb von Controller und Checkout. Weitere Add-ons lassen sich mit zusätzlichen `--addon`- und `--addon-url`-Argumenten registrieren. Sind alle registrierten Quellen veröffentlicht, prüft `bin/control update-check --remote --staging` den Testzweig und `--remote` den Hauptzweig.

## C · Ein lokales Paket mit einmaliger Ergänzung installieren

Standortspezifischer Code liegt neben dem Controller, etwa in `/root/ansible-local` neben `/root/ansible`. Pflege die Paketquelle separat und prüfe den Dateiinhalt, bevor du seine SHA freigibst. Die Installation kontrolliert, ob Dateien oder Rollen bereits zum verwalteten Bestand gehören. Eine Ergänzung übernimmt die Kennung ihres Stammpakets.

Die beiden Header im Beispiel sind gleichwertig. Direkt unter dem Shebang oder dem YAML-Start `---` stehen zwei Kommentarzeilen. Die deutschen Optionen heißen `behalten` und `nach-erfolg-archivieren`, die englischen `keep` und `archive-after-success`. Verwende je Header dieselbe Sprache.

<!-- example: C -->
```bash
cd "$LAB"
local_tool() { python3 "$TARGET/tools/local_extension.py" --controller "$TARGET" "$@"; }
mkdir -p "$BUNDLE/code/scripts"
cat > "$BUNDLE/code/scripts/site-check.sh" <<'SH'
#!/bin/sh
# manuell-integriert: ja
# bereinigung: behalten
printf 'site check OK\n'
SH
local_tool approve "$BUNDLE" scripts/site-check.sh "$(sha_file "$BUNDLE/code/scripts/site-check.sh")"
local_tool install "$BUNDLE"
local_tool run scripts/site-check.sh

local_tool new-supplement "$BUNDLE" "$SUPPLEMENT" once
mkdir -p "$SUPPLEMENT/code/scripts"
cat > "$SUPPLEMENT/code/scripts/once.sh" <<'SH'
#!/bin/sh
# manually-integrated: yes
# cleanup: archive-after-success
printf 'one-time check OK\n'
SH
digest=$(sha_file "$SUPPLEMENT/code/scripts/once.sh")
local_tool approve "$SUPPLEMENT" scripts/once.sh "$digest"
local_tool install "$SUPPLEMENT"
local_tool run scripts/once.sh
local_tool archive scripts/once.sh
local_tool archive scripts/once.sh --confirm-sha "$digest"
```

Der erste Archivaufruf zeigt die Vorschau. Der zweite verlangt die freigegebene SHA und einen erfolgreichen Lauf genau dieser Revision. Er legt die ursprüngliche Datei, `SHA256SUMS` und `BELEG.json` unter `$TARGET-local/archiv/` ab. Das dauerhaft freigegebene Skript bleibt ausführbar. Für ein YAML-Playbook verwendest du auf einem Controller mit installierter Ansible-Laufzeit `local_tool run playbooks/name.yml --limit GRUPPE`.

## D · Installation und Commit-Siegel prüfen

Die Tests vergleichen Schlüssel und Platzhalter der Sprachkataloge, beide Sprachfassungen der Beschreibungen und die hinterlegten Quellhashes. Der Release-Builder prüft Komponentenmanifeste und Integrität des Checkers. Die Git-Verifier vergleichen beide Commits mit ihrem jeweiligen Siegel. Zuletzt vergleicht der installierte Update-Checker die lokalen Add-on-Dateien mit ihren hinterlegten SHA-256-Werten. Diese Prüfung läuft ohne Netzwerkzugriff.

<!-- example: D -->
```bash
cd "$BASE"
python3 -m unittest discover -s update_check/tests -p test_i18n.py
python3 -m unittest discover -s update_check/tests -p test_description_languages.py
python3 tools/update_check/build_release.py --release-root "$BASE" --check-dir update_check
python3 update_check/staging_manifest.py verify Allgm HEAD
(cd "$ADDON" && python3 .githooks/staging_manifest.py addon-verify Heartbeat HEAD)
"$TARGET/bin/control" --lang en update-check --only addon-heartbeat --json > "$LAB/heartbeat-audit.json"
```

Beide Sprachfassungen kannst du in einem sauberen, bereits committeten Checkout mit `CONTROLLER_TEST_EXTENDING_EXAMPLES=1 python3 -m unittest discover -s update_check/tests -p test_extending_examples.py` in frischen lokalen Klonen durchspielen.

Die vollständige Projektsuite läuft in einem unveränderten Checkout mit `python3 -m unittest discover -s update_check/tests`. Tests mit fehlenden Voraussetzungen wie Schwester-Repos oder Ansible werden als übersprungen gemeldet. Private Inventories, Zugangsdaten, aktive Einstellungen und lokale Pakete gehören nicht in den Commit. Die [Architektur](ARCHITECTURE.de.md) erklärt die Zuständigkeiten. Das [Update-Handbuch](descriptions/commands/update-check.md) beschreibt Ausrollen und Rücknahme.
