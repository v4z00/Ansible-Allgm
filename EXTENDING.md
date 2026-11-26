[English](EXTENDING.md) | [Deutsch](EXTENDING.de.md)

# Extend the controller

Use a registry command for a shared operator action, an add-on for independently versioned playbooks or roles, and a local package for work that belongs to one controller. The examples build a command, install a small add-on, then run and archive a local script.

Start **in a committed checkout of this version of Ansible-Allgm**. Run the blocks in order in the same Bash session as an ordinary user. Use Python 3.11–3.13 with PyYAML, Git and Ansible available on `PATH`. The lab uses local clones and a code-only installation. The only push goes to a temporary bare repository on disk. Keep the printed lab path until you have finished reviewing the results.

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

## A · Register a command with a feature switch

`demo-hello` reads `features.demo_hello` from the controller's local `group_vars/all/settings.yml`. An absent switch leaves the command disabled. The registry file has one command and shares its name with the command. Its handler retrieves the greeting from the active language catalog. The Markdown description supplies titles for Control and help for the TUI. Its source hashes cover the registry, handler and both translations.

The block creates synthetic settings **in the fresh clone** to exercise the switch. Review the new sources before running the release builder. It refreshes the component hashes from this offline tree. The Git hook seals the staged deployment code on commit.

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

If the configuration assistant should also offer this switch, declare it as an optional boolean in `update_check/settings_contract.json`, add the matching field in `update_check/settings_catalog.json` and both language entries in the settings description. Give it a neutral `false` in the first-run and reference examples, and refresh the example source hashes. Existing controllers keep their private settings. A registry-only switch such as this example can be enabled directly by its operator.

## B · Package a playbook as an add-on

`Heartbeat` owns a dedicated mount under `playbooks/`. The source repo stays small. Paths in `payload` are relative to the repository root. Explicit `exports` can connect a registry handler and a description to the controller. A replacement list of `[]` keeps ownership unambiguous. An installation can have one exclusive profile and several add-ons with distinct names and paths.

Run this block in the same session. The hook uses the add-on variant of the verifier copied from the checked base. It seals all tracked add-on files, including hook files, except the seal itself. Each contributor must set `core.hooksPath` in their own clone. The version file holds plain `0.1.0`. The installer adds the `s` when the checkout is on `staging`.

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

The example GitHub URL is stored as metadata. For a deployable add-on, supply the HTTPS URL of your published repository. The installer maintains both the module's four-field row (`module|version|HTTPS URL|token file`) and its `# addon=Heartbeat` registration in the controller's private `versions.txt`. A public add-on leaves the fourth field empty. A private add-on declares `"authentication":"token-file"` and takes `--addon-token-file Heartbeat=/absolute/path` pointing to a mode-`0600` file outside the controller and checkout. Register further add-ons with additional `--addon` and `--addon-url` arguments. Once all registered sources have been published, `bin/control update-check --remote --staging` previews staging and `--remote` previews main.

## C · Install a local package and a one-time supplement

Case-specific code lives in a sibling of the controller, such as `/root/ansible-local` next to `/root/ansible`. Maintain the source package separately and review its bytes before approving the SHA. The installer checks for collisions with managed files and roles. A supplement inherits the parent package's identifier.

Both header spellings below are valid. Place the two comment lines directly after the shebang or YAML `---`. The German alternatives are `behalten` and `nach-erfolg-archivieren`, the English ones are `keep` and `archive-after-success`. Keep each pair in one language.

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

The first archive call shows the preview. The second requires the approved SHA and a successful run of the same revision. It archives the original bytes, `SHA256SUMS` and `BELEG.json` under `$TARGET-local/archiv/`. The persistent script remains runnable. For a YAML playbook use `local_tool run playbooks/name.yml --limit GROUP` on a controller with its Ansible runtime installed.

## D · Check the installed result and the committed seals

These tests compare catalog keys and placeholders, the two translations of descriptions, and their recorded source hashes. The release builder checks component manifests and checker integrity. The Git verifiers compare the two committed trees against their respective seals. Finally, run the installed checker's offline audit for the add-on.

<!-- example: D -->
```bash
cd "$BASE"
python3 -m unittest discover -s update_check/tests -p test_i18n.py
python3 -m unittest discover -s update_check/tests -p test_description_languages.py
python3 tools/update_check/build_release.py --release-root "$BASE" --check-dir update_check
python3 update_check/staging_manifest.py verify Allgm HEAD
(cd "$ADDON" && python3 .githooks/staging_manifest.py addon-verify Heartbeat HEAD)
"$TARGET/bin/control" --lang en update-check --offline --only addon-heartbeat --json > "$LAB/heartbeat-audit.json"
```

To replay both language editions in fresh local clones, run `CONTROLLER_TEST_EXTENDING_EXAMPLES=1 python3 -m unittest discover -s update_check/tests -p test_extending_examples.py` from a clean, committed checkout.

For a full project run from an unmodified checkout, use `python3 -m unittest discover -s update_check/tests`. Tests that need sibling repos or an Ansible executable report a skip when those prerequisites are absent. Keep private inventory, credentials, live settings and local packages outside the commit. See the [architecture](ARCHITECTURE.md) for ownership and the [update guide](descriptions/commands/update-check.md) for deployment and rollback.
