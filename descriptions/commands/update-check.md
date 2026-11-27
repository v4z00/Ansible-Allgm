Check controller profiles, file hashes and optional cleanup. `--remote` previews the released main branch over HTTPS. `--apply` installs it. Cron uses the same credentials with `--auto`. Local `versions.txt` records version, HTTPS origin and an optional token-file path for each module. Public modules are anonymous. A private module’s external token file must be owned by the executing user and have mode `0600`.

## Switch between main and staging

| Branch | Preview | Apply |
| --- | --- | --- |
| Release (`main`) | `bin/control update-check --remote` | `bin/control update-check --apply` |
| Test (`staging`) | `bin/control update-check --staging` | `bin/control update-check --apply --staging` |

The selection applies to this invocation and all installed controller modules. Cron always uses main with `--auto`, so the next scheduled update can return a test controller to the release. Both branches must support the flag for switching in both directions.

`ansible --version` shows the Ansible CLI version. `module-versions`, or directly `bin/control module-versions`, lists installed module versions and the current user’s installed TUI. The alias is available in a new controller shell. Local `versions.txt` uses `s1.2.3` for staging and `1.2.3` for main, both derived from the numeric `VERSION.txt`. Preview shows target versions. Apply changes installed versions.

A branch change backs up and removes managed files exclusive to the previous version. Local edits to those files block the change. Restore the saved state with `--rollback BACKUP_ID`.

### Test an older controller

For an older checker, use the verified migration through the intermediate commits below.

## Check local SHA-256 hashes

### Migrate SSS from an older controller

Back up the local `versions.txt` before switching. If SSS is in use, add the registration below. Modifications in the old SSS directory are reported as conflicts. Migrate personal settings privately as described in the [SSS guide](https://github.com/v4z00/Ansible-SSS/blob/main/README.md) and review each hash conflict before updating.

Run the first block in a root Bash shell on a Debian controller with its existing Python environment. It creates a private checkout under `/root` and verifies the job-report path update, the SSS bridge commit, its successor and the current main revision with the previously verified checker at each step. Record the printed directory path.

```bash
bridge_dir=$(mktemp -d /root/ansible-bridge.XXXXXXXX) && (
  set -eu
  umask 077
  printf 'Bridge directory: %s\n' "$bridge_dir"
  git clone --quiet --branch main https://github.com/v4z00/Ansible-Allgm.git "$bridge_dir/base"
  cd "$bridge_dir/base"
  git checkout --quiet --detach 5fd77a75b6d089f063dccc675f50d07b074925c8
  /root/ansible/.venv/bin/python /root/ansible/update_check/staging_manifest.py verify Allgm HEAD
  cp update_check/staging_manifest.py "$bridge_dir/jobs-verifier.py"
  git checkout --quiet --detach c7d2d7cbd881a7387d2fa424c10dfabc48a3fd41
  /root/ansible/.venv/bin/python "$bridge_dir/jobs-verifier.py" verify Allgm HEAD
  cp update_check/staging_manifest.py "$bridge_dir/bridge-verifier.py"
  git checkout --quiet --detach 760166ebd9fd0b933b17307c6ace6855719c0652
  /root/ansible/.venv/bin/python "$bridge_dir/bridge-verifier.py" verify Allgm HEAD
  cp update_check/staging_manifest.py "$bridge_dir/current-verifier.py"
  git checkout --quiet --detach origin/main
  /root/ansible/.venv/bin/python "$bridge_dir/current-verifier.py" verify Allgm HEAD
  git rev-parse --verify HEAD > "$bridge_dir/VERIFIED"
)
```

The `VERIFIED` file contains the commit ID only after verification succeeds. If a check fails, stop, resolve the error and repeat the first block in a new directory. The checkout survives logout. In the original shell `bridge_dir` is already set. After reconnecting, list the verification records and enter **the directory for this operation without `/VERIFIED`**:

```bash
printf '%s\n' /root/ansible-bridge.*/VERIFIED
read -r -p 'Bridge directory: ' bridge_dir
```

**Preview.** Inspect the planned switch to main without applying changes:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote
)
```

When `MIGRATION_REQUIRED` is the only blocker and local files are intact, exit status 1 is expected in this preview. Review the register migration plan first. Investigate other failures before proceeding. If there is no legacy register, skip both register steps.

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --check
)
```

**Migrate the register.** Apply after reviewing the plan and record the printed path to the private schema-1 backup. This block then runs a fresh code preview:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --apply
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote
)
```

**Apply the code update.** Run only after a successful preview and review of its changes. Record the printed controller backup ID for rollback:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --apply
)
```

**Rollback.** If switching fails before the new code is installed, restore the migrated register using the retained checkout. Enter the recorded **register backup path**:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  read -r -p 'Register backup: ' backup
  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --rollback "$backup"
)
```

If the new code was installed and you need the older checker again, restore the register first as above. Then enter the **controller backup ID**. Code rollback also restores the previous receipt and `versions.txt`:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  read -r -p 'Controller backup ID: ' backup_id
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --rollback "$backup_id"
)
```

If the register was never migrated, only code rollback is needed. Keep the checkout until you have confirmed the final controller and register state. Then manually remove the specific bridge directory you recorded.

### Git add-ons

A controller can have one site profile and multiple Git add-ons. Keep all four fields in each module row. A separate comment registers each add-on. Example for the local `versions.txt`:

```text
# addon=SSS
SSS|0.0.0|https://github.com/v4z00/Ansible-SSS.git|
```

Use `0.0.0` for initial registration. Preview shows the offered version, and apply records the installed version. Rows without registration remain passive. For a private add-on the fourth field holds the token-file path. All registered modules must offer the chosen branch.

Preview the plan with `bin/control update-check --remote` before `bin/control update-check --apply`. To revert, pass the printed backup ID to `bin/control update-check --rollback BACKUP_ID`. Keep both row and registration for installed add-ons. Missing sources, changed managed add-on files or occupied destinations stop the checker before replacement.

`--only local` shows the separate file report. Cron reports this status before fetching from Git with `--auto`. Unknown, missing or modified local files and damaged archives block apply. Supplements are reported by package name. Conflicts with a base playbook or role are reported as `BASIS_KONFLIKT`.

## Create a local extension package

| Path | Purpose |
|---|---|
| `bin/control` | Controller commands and update checks |
| `playbooks/`, `roles/` | Shared workflows managed through Git |
| `tools/local_extension.py` | Approve, install, run and archive local files |
| `/root/ansible-local/code/` | Separately installed roles, playbooks, scripts and local variables |
| `/root/ansible-local/register.json` | Approved paths and SHA-256 values |
| `/root/ansible-local/runs/`, `archiv/` | Local run and archive receipts |

After [installing the base](../configurations/installation-allgm.md), create a local extension package outside any Git checkout. Example as root on a Debian controller:

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

The last command previews the operation. Check callers, then archive this specific revision with `python3 tools/local_extension.py archive "$datei" --confirm-sha "$sha"`. The reported archive contains the file, `BELEG.json` with approved and measured hashes and the run receipt, and `SHA256SUMS`. Run `sha256sum -c SHA256SUMS` there to verify the archived bytes.

For permanent files, use `# bereinigung: behalten`. Place both marker comments directly under `---` in YAML or after the shebang in scripts. Put playbooks under `code/playbooks/` and run them with `python3 tools/local_extension.py run playbooks/beispiel.yml --limit TARGET_GROUP`. Verify each change in the private source, approve its new hash and reinstall the package. An unchanged archived revision stays archived.

`bin/control update-check` reports extensions in a separate section. JSON reports use `local_extensions`. Cron with `--auto` verifies local SHA-256 before fetching from Git. Missing, extra or modified files block the switch. Controllers without local extensions continue to work as before. Cron does not run or archive local tasks.

## Extend an existing site package

Shared playbooks and roles under `/root/ansible` receive updates from Git. Give site-specific playbooks unique names. They may call shared base roles. Give a supplement the same site ID as its parent package and a unique package name. Maintain them independently.

In the private workspace, pass the existing site package first, followed by a new directory. On Debian:

```bash
werkzeug=/root/ansible/tools/local_extension.py
python3 "$werkzeug" new-supplement ./standort ./zusatz dienstpruefung
mkdir -p ./zusatz/code/playbooks
cp ./local_dienst_pruefen.yml ./zusatz/code/playbooks/
datei=playbooks/local_dienst_pruefen.yml
sha=$(sha256sum "./zusatz/code/$datei" | cut -d ' ' -f 1)
python3 "$werkzeug" approve ./zusatz "$datei" "$sha"
```

Use the same marker comments for the supplement. The target must already have the site package registered. Copy the `zusatz` directory to the controller. Register and check it as root:

```bash
cd /root/ansible
python3 tools/local_extension.py install /root/eingang/zusatz
bin/control update-check --only local
```

The checker reports the supplement by name and verifies its files during cron. A later site package that omits a registered file leaves that revision in place. Only a deliberate update from the same local package can replace it. Paths owned by another package or matching a controller role block installation. Run the operation separately with an explicit target, for example `python3 tools/local_extension.py run playbooks/local_dienst_pruefen.yml --limit TARGET_HOST`.

## Migrate a local register

If the checker reports `MIGRATION_REQUIRED`, review the existing approvals. Run these commands from the controller directory:

```sh
python3 tools/migrate_local_extensions.py --check
python3 tools/migrate_local_extensions.py --apply
bin/control update-check --only local
```

The second command prints the path to the private schema-1 backup (mode `0600`). Migration changes only `register.json`. Scripts, playbooks and run receipts keep their original bytes and checksums. The archive names `archiv/<id>/datei`, `BELEG.json` and `SHA256SUMS` are stable so older receipts remain verifiable.

German headers remain valid. For English headers, put `# manually-integrated: yes` and either `# cleanup: keep` or `# cleanup: archive-after-success` directly after the shebang or YAML document start. Before rolling the controller back to an older checker, restore the register with `python3 tools/migrate_local_extensions.py --rollback "$BACKUP"`. Set `BACKUP` to the path printed during migration. The restore refuses to overwrite later register edits.

For a first migration from an older checker, use the private bridge checkout above. Follow its separate preview, register migration, code update and recovery steps.

## Keep the local extension register in controller state

The checker supports both the existing sibling `<controller>-local` and
`<controller>/.local/extensions`. Keep the register, private code, run receipts and
archives together; the site pin remains `.local/local-extension-id`. The internal
layout is selected only when its folder already exists. Existing installations
and new installations retain the sibling default. Two simultaneous locations
fail explicitly instead of choosing one silently.

For a deliberate move, back up the register and site pin privately, then check
and apply any schema migration with `tools/migrate_local_extensions.py`. With no
concurrent update/register writer, move the complete folder into `.local/extensions`
and run `bin/control update-check --only local`. Before rolling back to an older
checker, move it back to its sibling position and restore the schema-1 backup with
the current migrator if required. Moving does not change private code or approved
hashes. Schema migration and rollback work in either location.

An update or rollback target without declared internal-layout support is blocked, including automatic main updates. Move the complete register to the sibling location before switching.

<details>
<summary>Deutsch</summary>

Controllerprüfung für Profile, Datei-SHA und optionale Bereinigung.
Mit `--remote` den freigegebenen Branch `main` über HTTPS prüfen, mit `--apply`
übernehmen. `--auto` nutzt dieselben Zugangsdaten im Cronlauf. Die lokale
`versions.txt` enthält pro Modul Version, HTTPS-Origin und optional den Pfad
zur Token-Datei. Öffentliche Module verwenden anonymen Zugriff. Bei einem
privaten Modul muss die externe Token-Datei dem ausführenden Benutzer gehören
und Modus `0600` haben.

## Zwischen main und staging wechseln

| Ziel | Vorschau | Übernehmen |
| --- | --- | --- |
| Freigabe (`main`) | `bin/control update-check --remote` | `bin/control update-check --apply` |
| Teststand (`staging`) | `bin/control update-check --staging` | `bin/control update-check --apply --staging` |

Die Auswahl gilt für diesen Aufruf und alle installierten Controller-Module. Der Cronlauf mit `--auto` verwendet immer `main`. Ein laufender Testcontroller kann dadurch beim nächsten automatischen Update auf die Freigabe zurückkehren. Beide Branches müssen den Schalter unterstützen, damit du beliebig hin- und herwechseln kannst.

Die Ansible-CLI meldet ihre Version mit `ansible --version`. Mit `module-versions` siehst du die installierte Version jedes Moduls. Ist Ansible TUI für das aktuelle Konto installiert, wird auch ihre Version angezeigt. In einer neuen Controller-Shell steht der Alias bereit. Direkt geht es mit `bin/control module-versions`. In der lokalen `versions.txt` steht zum Beispiel `s1.2.3` für Staging und `1.2.3` für Main. Beide leiten sich aus derselben numerischen Basis in `VERSION.txt` ab. Die Vorschau zeigt die Zielversionen. Erst das Übernehmen ändert die installierten Versionen.

Beim Wechsel werden verwaltete Dateien, die nur zum bisherigen Stand gehören, mitgesichert und entfernt. Eigene Änderungen an solchen Dateien blockieren den Wechsel. Über `--rollback SICHERUNGSKENNUNG` lässt sich der gesicherte Stand wiederherstellen.

### Einen älteren Controller testen

Bei einem älteren Prüfprogramm den unten dokumentierten, verifizierten Übergang über die Brückenstände verwenden.

## Lokale SHA-Prüfung

### SSS aus einem älteren Controller übernehmen

Vor dem ersten Wechsel die eigene `versions.txt` sichern. Wer SSS bereits
nutzt, ergänzt den unten gezeigten Eintrag. Veränderte Dateien aus dem alten
SSS-Verzeichnis werden als Konflikt gemeldet. Eigene Konfiguration zuerst nach
der [SSS-Anleitung](https://github.com/v4z00/Ansible-SSS/blob/main/README.de.md)
privat übernehmen. Den SHA-Konflikt vor dem Update einzeln prüfen.

Führe den ersten Block als root in Bash auf einem Debian-Controller mit vorhandener Python-Umgebung aus. Er legt unter `/root` einen privaten Checkout an und prüft zuerst die Dateiliste für die Jobberichte, dann den SSS-Brückenstand, seinen Nachfolger und den aktuellen Main-Stand mit dem jeweils zuvor verifizierten Prüfer. Notiere den ausgegebenen Verzeichnispfad.

```bash
bridge_dir=$(mktemp -d /root/ansible-bridge.XXXXXXXX) && (
  set -eu
  umask 077
  printf 'Bridge directory: %s\n' "$bridge_dir"
  git clone --quiet --branch main https://github.com/v4z00/Ansible-Allgm.git "$bridge_dir/base"
  cd "$bridge_dir/base"
  git checkout --quiet --detach 5fd77a75b6d089f063dccc675f50d07b074925c8
  /root/ansible/.venv/bin/python /root/ansible/update_check/staging_manifest.py verify Allgm HEAD
  cp update_check/staging_manifest.py "$bridge_dir/jobs-verifier.py"
  git checkout --quiet --detach c7d2d7cbd881a7387d2fa424c10dfabc48a3fd41
  /root/ansible/.venv/bin/python "$bridge_dir/jobs-verifier.py" verify Allgm HEAD
  cp update_check/staging_manifest.py "$bridge_dir/bridge-verifier.py"
  git checkout --quiet --detach 760166ebd9fd0b933b17307c6ace6855719c0652
  /root/ansible/.venv/bin/python "$bridge_dir/bridge-verifier.py" verify Allgm HEAD
  cp update_check/staging_manifest.py "$bridge_dir/current-verifier.py"
  git checkout --quiet --detach origin/main
  /root/ansible/.venv/bin/python "$bridge_dir/current-verifier.py" verify Allgm HEAD
  git rev-parse --verify HEAD > "$bridge_dir/VERIFIED"
)
```

Erst nach erfolgreicher Verifikation steht die Commit-ID in `VERIFIED`. Bei einem Fehler hier aufhören, die Ursache klären und den ersten Block in einem neuen Verzeichnis wiederholen. Der Checkout bleibt auch nach dem Abmelden erhalten. In derselben Shell gilt `bridge_dir` weiter. Nach dem erneuten Anmelden die vorhandenen Nachweise anzeigen und den **Verzeichnispfad des eigenen Vorgangs ohne `/VERIFIED`** eingeben:

```bash
printf '%s\n' /root/ansible-bridge.*/VERIFIED
read -r -p 'Bridge directory: ' bridge_dir
```

**Vorschau.** Prüfe den geplanten Wechsel auf Main ohne Übernahme:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote
)
```

Bei `MIGRATION_REQUIRED` und intakten lokalen Dateien ist Exitcode 1 in dieser Vorschau zu erwarten. Prüfe zunächst den Migrationsplan. Bei anderen Fehlern den gemeldeten Befund klären. Ohne altes Lokalregister die beiden Registerschritte überspringen.

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --check
)
```

**Register migrieren.** Nach Prüfung des Plans übernehmen und den ausgegebenen Pfad der privaten Schema-1-Sicherung notieren. Danach folgt erneut die reine Codevorschau:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --apply
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote
)
```

**Code übernehmen.** Erst nach erfolgreicher Vorschau und Prüfung der Änderungen ausführen. Die ausgegebene Controller-Sicherungskennung für den Rückweg notieren:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --apply
)
```

**Rückweg.** Scheitert der Wechsel vor der Installation des neuen Codes, lässt sich das migrierte Register im erhaltenen Checkout wiederherstellen. Den zuvor notierten **Register-Sicherungspfad** eingeben:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  read -r -p 'Register backup: ' backup
  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --rollback "$backup"
)
```

Wurde der neue Code bereits installiert und soll der ältere Checker wieder laufen, wie oben zuerst das Register zurücksetzen. Danach die **Controller-Sicherungskennung** verwenden. Der Code-Rollback stellt auch die vorherige Quittung und `versions.txt` wieder her:

```bash
(
  set -eu
  cd "${bridge_dir:?}/base"
  test -s ../VERIFIED
  test "$(git rev-parse --verify HEAD)" = "$(cat ../VERIFIED)"
  read -r -p 'Controller backup ID: ' backup_id
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --rollback "$backup_id"
)
```

Wenn kein Register migriert wurde, genügt der Code-Rollback. Behalte den Checkout bis zur Kontrolle des endgültigen Controller- und Registerstands. Anschließend kannst du genau das notierte Brückenverzeichnis manuell entfernen.

### Git-Add-ons

Ein Controller kann ein Standortprofil und mehrere Git-Add-ons verwenden. Die
vier Felder jeder Zeile bleiben erhalten. Ein eigener Kommentar registriert
das jeweilige Add-on. Beispiel für die lokale `versions.txt`:

```text
# addon=SSS
SSS|0.0.0|https://github.com/v4z00/Ansible-SSS.git|
```

Bei der ersten Registrierung dient `0.0.0` als Startwert. Die Vorschau zeigt
die angebotene Version. Die Übernahme schreibt die installierte Version in
die Datei. Andere Modulzeilen ohne Registrierung bleiben passive Einträge.
Ein privates Git-Add-on verwendet das vierte Feld für den Pfad seiner
Token-Datei. Für die Vorschau müssen alle registrierten Module den gewählten
Branch anbieten.

Mit `bin/control update-check --remote` zuerst den Plan prüfen, danach
`bin/control update-check --apply` ausführen. Für die Rücknahme
die ausgegebene Sicherungskennung mit `bin/control update-check --rollback KENNUNG`
angeben. Zu einem bereits installierten Add-on müssen Eintrag und Registrierung
vorhanden bleiben. Der Checker bricht bei fehlenden Modulquellen, geänderten
verwalteten Add-on-Dateien oder belegten Zielpfaden vor dem Austausch ab.

`--only local` zeigt den getrennten Dateibericht. Der Cronlauf mit `--auto` meldet den Status vor dem Git-Abruf. Unbekannte, fehlende oder geänderte lokale Dateien sowie beschädigte Archive blockieren die Übernahme. Der Bericht nennt bei einzeln gelieferten Zusätzen den Paketnamen. Ein Namenskonflikt mit einem Basisplaybook oder einer Basisrolle wird als `BASIS_KONFLIKT` gemeldet.

## Lokales Erweiterungspaket anlegen

| Pfad | Zweck |
|---|---|
| `bin/control` | Einstieg für Betrieb und Update-Check |
| `playbooks/`, `roles/` | Gemeinsame, über Git aktualisierte Abläufe |
| `tools/local_extension.py` | Lokale Dateien freigeben, installieren, ausführen und archivieren |
| `/root/ansible-local/code/` | Separat installierte Rollen, Playbooks, Skripte und lokale Variablendateien |
| `/root/ansible-local/register.json` | Freigegebene Pfade und SHA-256 |
| `/root/ansible-local/runs/`, `archiv/` | Lokale Ausführungs- und Archivbelege |

Nach der [Basisinstallation](../configurations/installation-allgm.md) kann ein eigenes Erweiterungspaket hinzukommen. Lege es außerhalb eines Git-Checkouts an. Für ein erstes Beispiel auf einem Debian-Controller als root:

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

## Vorhandenes Standortpaket ergänzen

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

## Lokales Register migrieren

Bei `MIGRATION_REQUIRED` zuerst die bestehende Freigabe prüfen. Im Controller-Verzeichnis:

```sh
python3 tools/migrate_local_extensions.py --check
python3 tools/migrate_local_extensions.py --apply
bin/control update-check --only local
```

Der zweite Befehl meldet den Pfad der privaten Schema-1-Sicherung (Modus `0600`). Die Migration ändert ausschließlich `register.json`. Skripte, YAML-Dateien und Laufbelege behalten ihre Bytes und Prüfsummen. Auch `archiv/<id>/datei`, `BELEG.json` und `SHA256SUMS` behalten ihre Namen, damit alte Belege weiter prüfbar sind.

Deutsche Dateiköpfe bleiben gültig. Auf Englisch stehen direkt unter dem Shebang oder YAML-Dokumentanfang `# manually-integrated: yes` und `# cleanup: keep` oder `# cleanup: archive-after-success`. Vor dem Controller-Rollback auf einen älteren Prüfer zuerst das Register mit `python3 tools/migrate_local_extensions.py --rollback "$BACKUP"` zurücksetzen. Für `BACKUP` den vom Migrationsbefehl ausgegebenen Sicherungspfad einsetzen. Spätere Registeränderungen sperren diese Rücknahme.

Für die Erstmigration mit einem älteren Checker steht der private Brücken-Checkout oben bereit. Dort sind die einzelnen Schritte für Vorschau, Registermigration, Codeübernahme und Wiederherstellung nach Unterbrechungen aufgeführt.

## Lokales Zusatzregister im Controllerzustand

Neben dem bisherigen Nachbarordner `<controller>-local` unterstützt der Prüfer
auch `<controller>/.local/extensions`. Das vorhandene Register, der private Code,
Laufbelege und Archive bleiben dabei zusammen; die Standortkennung bleibt in
`.local/local-extension-id`. Das neue Layout wird nur verwendet, wenn sein Ordner
bereits vorhanden ist. Neue Installationen und bestehende Nachbarordner bleiben
beim bisherigen Verhalten. Zwei gleichzeitige Ablagen werden als Konflikt gemeldet.

Für eine bewusste Umstellung zuerst das Register und die Kennung privat sichern,
den Schemawechsel mit `tools/migrate_local_extensions.py` prüfen und übernehmen.
Während kein Update- oder Registerschreibprozess läuft, den vollständigen Ordner
in `.local/extensions` verschieben. Danach `bin/control update-check --only local`
prüfen. Für einen Rückwechsel auf einen älteren Prüfer den Ordner vorher an die
bisherige Nachbarposition zurückschieben und gegebenenfalls das Schema-1-Backup
mit dem noch aktuellen Migrator wiederherstellen. Die Dateiinhalte und freigegebenen
SHA-Werte ändern sich durch den Pfadwechsel nicht. Schema-Migration und deren
Rücknahme funktionieren mit beiden Ablagen.

Ein Ziel ohne deklarierte Unterstützung der internen Ablage wird bei Update und Rollback blockiert. Das gilt auch für automatische main-Updates; zuerst die komplette Ablage an den Nachbarpfad zurücklegen.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "update-check",
  "title": "Versionen, Settings und Initialkonfiguration",
  "documented": true,
  "fields": [
    {
      "id": "check",
      "label": "check",
      "description": "Erweiterte lokale Konfigurations-/GET-API-Pruefung, keine Schreib-API.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--check"
      }
    },
    {
      "id": "offline",
      "label": "offline",
      "description": "Mit --check keine Netzwerkaufrufe.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--offline"
      }
    },
    {
      "id": "configure",
      "label": "configure",
      "description": "Interaktive Einrichtung mit Vorschau/YES; Terminal erforderlich, nicht mit --json.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--configure"
      }
    },
    {
      "id": "sort_settings",
      "label": "sort-settings",
      "description": "Nur Settings ordnen mit Vorschau/YES; Terminal erforderlich.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--sort-settings"
      }
    },
    {
      "id": "details",
      "label": "details",
      "description": "Auch passende/optionale Feldbefunde anzeigen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--details"
      }
    },
    {
      "id": "json",
      "label": "json",
      "description": "Strukturierter Nur-Lese-Bericht ohne Credentialwerte.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--json"
      }
    },
    {
      "id": "only",
      "label": "only",
      "description": "Eine Komponente, settings, registry oder eine installierte Erweiterung prüfen.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--only"
      }
    },
    {
      "id": "field",
      "label": "field",
      "description": "Mit --configure gezielt bekannten Schluessel abfragen; im Terminal wiederholbar.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--field"
      }
    },
    {
      "id": "find_usage",
      "label": "find-usage",
      "description": "Statische Fundstellen einer Variable, keine automatische Loeschung.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--find-usage"
      }
    },
    {
      "id": "timeout",
      "label": "timeout",
      "description": "API-Timeout 1 bis 30 Sekunden, Standard 8.",
      "type": "integer",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--timeout"
      }
    },
    {
      "id": "color",
      "label": "Farbausgabe",
      "description": "auto: nur Terminal; always: erzwingen; never: ausschalten. JSON immer farbfrei.",
      "type": "string",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--color"
      }
    },
    {
      "id": "cleanup",
      "label": "cleanup",
      "description": "Freigegebene Altdateien nach Projekt-/Cron-/Systemd-Pruefung, Vorschau und YES archivieren; keine aktiven Dateien loeschen.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--cleanup"
      }
    },
    {
      "id": "no-prompt",
      "label": "no-prompt",
      "description": "Keine optionale Bereinigungsfrage im normalen Terminalprueflauf.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--no-prompt"
      }
    },
    {
      "id": "remote",
      "label": "remote",
      "description": "Änderungen aus main anzeigen (mit --staging aus staging).",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--remote"
      }
    },
    {
      "id": "staging",
      "label": "staging",
      "description": "Staging für diesen manuellen Abruf wählen. Ohne --apply nur Vorschau.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--staging"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/update-check.json",
    "bin/control.d/update-check.sh",
    "update_check/check.py",
    "update_check/configure.py",
    "update_check/probes.py",
    "update_check/cleanup.py",
    "update_check/rollout.py",
    "tools/github_https.py",
    "tools/install_controller.py",
    "tools/migrate_local_extensions.py",
    "tools/local_extension.py",
    "update_check/local_extensions.py"
  ],
  "source_hashes": {
    "bin/control.d/update-check.json": "adb0a79c424f87249ca66e73d2256bc2f477017e3ce4ebc906364678a95b3177",
    "bin/control.d/update-check.sh": "7cc1fc9287cff92e352ad038519366d7dfd04d4efe99d1c70d980de0c62ac807",
    "update_check/check.py": "890f0b01367f27d240f86dfbdbed7cd40bac372997a40d4c8a80c00b293c7d53",
    "update_check/configure.py": "2c7e913b78c703326eb4116bbb2f6a3ea7402903357eb12ba977bb988e2e22b7",
    "update_check/probes.py": "3ef5592956d6f9e7072310b39b3a9cdf5e38057b194faa4790a30ea38c01fa70",
    "update_check/cleanup.py": "ef0fd75326697b291b075104c0d4408030aa89fad020193671758a4759121738",
    "update_check/rollout.py": "5fee32129a8d78b1dc85e55e734ebc5845d5fbcde4a5cd92024fa83fd78e45f9",
    "tools/github_https.py": "4939726758123ce18c3558bd22a668052a0bb028b62a1c71534b92ccb89e5bd5",
    "tools/install_controller.py": "ba99175981bf232f640cea854b3c26ab5d9f02a7e7f2c9a885603c1098277e8e",
    "tools/migrate_local_extensions.py": "7043675fffecee75166ef62bebe1859a90b27e5ebca38ee4bd6d085003ea43ba",
    "tools/local_extension.py": "7039aef7502b9793aa8105b0ff44b467268cfc3a49b5c05d3c2d721752dc6fe0",
    "update_check/local_extensions.py": "ea5afc8741f12bd72e9b011465f3a4e7c06dbf3f84c4434742582c5fa2827a60"
  },
  "i18n": {
    "de": {
      "title": "Versionen, Settings und Initialkonfiguration",
      "description": "Controllerprüfung für Profile, Datei-SHA und optionale Bereinigung.\nMit `--remote` den freigegebenen Branch `main` über HTTPS prüfen, mit `--apply`\nübernehmen. `--auto` nutzt dieselben Zugangsdaten im Cronlauf. Die lokale\n`versions.txt` enthält pro Modul Version, HTTPS-Origin und optional den Pfad\nzur Token-Datei. Öffentliche Module verwenden anonymen Zugriff. Bei einem\nprivaten Modul muss die externe Token-Datei dem ausführenden Benutzer gehören\nund Modus `0600` haben.\n\n## Zwischen main und staging wechseln\n\n| Ziel | Vorschau | Übernehmen |\n| --- | --- | --- |\n| Freigabe (`main`) | `bin/control update-check --remote` | `bin/control update-check --apply` |\n| Teststand (`staging`) | `bin/control update-check --staging` | `bin/control update-check --apply --staging` |\n\nDie Auswahl gilt für diesen Aufruf und alle installierten Controller-Module. Der Cronlauf mit `--auto` verwendet immer `main`. Ein laufender Testcontroller kann dadurch beim nächsten automatischen Update auf die Freigabe zurückkehren. Beide Branches müssen den Schalter unterstützen, damit du beliebig hin- und herwechseln kannst.\n\nDie Ansible-CLI meldet ihre Version mit `ansible --version`. Mit `module-versions` siehst du die installierte Version jedes Moduls. Ist Ansible TUI für das aktuelle Konto installiert, wird auch ihre Version angezeigt. In einer neuen Controller-Shell steht der Alias bereit. Direkt geht es mit `bin/control module-versions`. In der lokalen `versions.txt` steht zum Beispiel `s1.2.3` für Staging und `1.2.3` für Main. Beide leiten sich aus derselben numerischen Basis in `VERSION.txt` ab. Die Vorschau zeigt die Zielversionen. Erst das Übernehmen ändert die installierten Versionen.\n\nBeim Wechsel werden verwaltete Dateien, die nur zum bisherigen Stand gehören, mitgesichert und entfernt. Eigene Änderungen an solchen Dateien blockieren den Wechsel. Über `--rollback SICHERUNGSKENNUNG` lässt sich der gesicherte Stand wiederherstellen.\n\n### Einen älteren Controller testen\n\nBei einem älteren Prüfprogramm den unten dokumentierten, verifizierten Übergang über die Brückenstände verwenden.\n\n## Lokale SHA-Prüfung\n\n### SSS aus einem älteren Controller übernehmen\n\nVor dem ersten Wechsel die eigene `versions.txt` sichern. Wer SSS bereits\nnutzt, ergänzt den unten gezeigten Eintrag. Veränderte Dateien aus dem alten\nSSS-Verzeichnis werden als Konflikt gemeldet. Eigene Konfiguration zuerst nach\nder [SSS-Anleitung](https://github.com/v4z00/Ansible-SSS/blob/main/README.de.md)\nprivat übernehmen. Den SHA-Konflikt vor dem Update einzeln prüfen.\n\nFühre den ersten Block als root in Bash auf einem Debian-Controller mit vorhandener Python-Umgebung aus. Er legt unter `/root` einen privaten Checkout an und prüft zuerst die Dateiliste für die Jobberichte, dann den SSS-Brückenstand, seinen Nachfolger und den aktuellen Main-Stand mit dem jeweils zuvor verifizierten Prüfer. Notiere den ausgegebenen Verzeichnispfad.\n\n```bash\nbridge_dir=$(mktemp -d /root/ansible-bridge.XXXXXXXX) && (\n  set -eu\n  umask 077\n  printf 'Bridge directory: %s\\n' \"$bridge_dir\"\n  git clone --quiet --branch main https://github.com/v4z00/Ansible-Allgm.git \"$bridge_dir/base\"\n  cd \"$bridge_dir/base\"\n  git checkout --quiet --detach 5fd77a75b6d089f063dccc675f50d07b074925c8\n  /root/ansible/.venv/bin/python /root/ansible/update_check/staging_manifest.py verify Allgm HEAD\n  cp update_check/staging_manifest.py \"$bridge_dir/jobs-verifier.py\"\n  git checkout --quiet --detach c7d2d7cbd881a7387d2fa424c10dfabc48a3fd41\n  /root/ansible/.venv/bin/python \"$bridge_dir/jobs-verifier.py\" verify Allgm HEAD\n  cp update_check/staging_manifest.py \"$bridge_dir/bridge-verifier.py\"\n  git checkout --quiet --detach 760166ebd9fd0b933b17307c6ace6855719c0652\n  /root/ansible/.venv/bin/python \"$bridge_dir/bridge-verifier.py\" verify Allgm HEAD\n  cp update_check/staging_manifest.py \"$bridge_dir/current-verifier.py\"\n  git checkout --quiet --detach origin/main\n  /root/ansible/.venv/bin/python \"$bridge_dir/current-verifier.py\" verify Allgm HEAD\n  git rev-parse --verify HEAD > \"$bridge_dir/VERIFIED\"\n)\n```\n\nErst nach erfolgreicher Verifikation steht die Commit-ID in `VERIFIED`. Bei einem Fehler hier aufhören, die Ursache klären und den ersten Block in einem neuen Verzeichnis wiederholen. Der Checkout bleibt auch nach dem Abmelden erhalten. In derselben Shell gilt `bridge_dir` weiter. Nach dem erneuten Anmelden die vorhandenen Nachweise anzeigen und den **Verzeichnispfad des eigenen Vorgangs ohne `/VERIFIED`** eingeben:\n\n```bash\nprintf '%s\\n' /root/ansible-bridge.*/VERIFIED\nread -r -p 'Bridge directory: ' bridge_dir\n```\n\n**Vorschau.** Prüfe den geplanten Wechsel auf Main ohne Übernahme:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote\n)\n```\n\nBei `MIGRATION_REQUIRED` und intakten lokalen Dateien ist Exitcode 1 in dieser Vorschau zu erwarten. Prüfe zunächst den Migrationsplan. Bei anderen Fehlern den gemeldeten Befund klären. Ohne altes Lokalregister die beiden Registerschritte überspringen.\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --check\n)\n```\n\n**Register migrieren.** Nach Prüfung des Plans übernehmen und den ausgegebenen Pfad der privaten Schema-1-Sicherung notieren. Danach folgt erneut die reine Codevorschau:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --apply\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote\n)\n```\n\n**Code übernehmen.** Erst nach erfolgreicher Vorschau und Prüfung der Änderungen ausführen. Die ausgegebene Controller-Sicherungskennung für den Rückweg notieren:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --apply\n)\n```\n\n**Rückweg.** Scheitert der Wechsel vor der Installation des neuen Codes, lässt sich das migrierte Register im erhaltenen Checkout wiederherstellen. Den zuvor notierten **Register-Sicherungspfad** eingeben:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  read -r -p 'Register backup: ' backup\n  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --rollback \"$backup\"\n)\n```\n\nWurde der neue Code bereits installiert und soll der ältere Checker wieder laufen, wie oben zuerst das Register zurücksetzen. Danach die **Controller-Sicherungskennung** verwenden. Der Code-Rollback stellt auch die vorherige Quittung und `versions.txt` wieder her:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  read -r -p 'Controller backup ID: ' backup_id\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --rollback \"$backup_id\"\n)\n```\n\nWenn kein Register migriert wurde, genügt der Code-Rollback. Behalte den Checkout bis zur Kontrolle des endgültigen Controller- und Registerstands. Anschließend kannst du genau das notierte Brückenverzeichnis manuell entfernen.\n\n### Git-Add-ons\n\nEin Controller kann ein Standortprofil und mehrere Git-Add-ons verwenden. Die\nvier Felder jeder Zeile bleiben erhalten. Ein eigener Kommentar registriert\ndas jeweilige Add-on. Beispiel für die lokale `versions.txt`:\n\n```text\n# addon=SSS\nSSS|0.0.0|https://github.com/v4z00/Ansible-SSS.git|\n```\n\nBei der ersten Registrierung dient `0.0.0` als Startwert. Die Vorschau zeigt\ndie angebotene Version. Die Übernahme schreibt die installierte Version in\ndie Datei. Andere Modulzeilen ohne Registrierung bleiben passive Einträge.\nEin privates Git-Add-on verwendet das vierte Feld für den Pfad seiner\nToken-Datei. Für die Vorschau müssen alle registrierten Module den gewählten\nBranch anbieten.\n\nMit `bin/control update-check --remote` zuerst den Plan prüfen, danach\n`bin/control update-check --apply` ausführen. Für die Rücknahme\ndie ausgegebene Sicherungskennung mit `bin/control update-check --rollback KENNUNG`\nangeben. Zu einem bereits installierten Add-on müssen Eintrag und Registrierung\nvorhanden bleiben. Der Checker bricht bei fehlenden Modulquellen, geänderten\nverwalteten Add-on-Dateien oder belegten Zielpfaden vor dem Austausch ab.\n\n`--only local` zeigt den getrennten Dateibericht. Der Cronlauf mit `--auto` meldet den Status vor dem Git-Abruf. Unbekannte, fehlende oder geänderte lokale Dateien sowie beschädigte Archive blockieren die Übernahme. Der Bericht nennt bei einzeln gelieferten Zusätzen den Paketnamen. Ein Namenskonflikt mit einem Basisplaybook oder einer Basisrolle wird als `BASIS_KONFLIKT` gemeldet.\n\n## Lokales Erweiterungspaket anlegen\n\n| Pfad | Zweck |\n|---|---|\n| `bin/control` | Einstieg für Betrieb und Update-Check |\n| `playbooks/`, `roles/` | Gemeinsame, über Git aktualisierte Abläufe |\n| `tools/local_extension.py` | Lokale Dateien freigeben, installieren, ausführen und archivieren |\n| `/root/ansible-local/code/` | Separat installierte Rollen, Playbooks, Skripte und lokale Variablendateien |\n| `/root/ansible-local/register.json` | Freigegebene Pfade und SHA-256 |\n| `/root/ansible-local/runs/`, `archiv/` | Lokale Ausführungs- und Archivbelege |\n\nNach der [Basisinstallation](../configurations/installation-allgm.md) kann ein eigenes Erweiterungspaket hinzukommen. Lege es außerhalb eines Git-Checkouts an. Für ein erstes Beispiel auf einem Debian-Controller als root:\n\n```bash\nmkdir -p /root/mein-paket/code/scripts\ncat > /root/mein-paket/code/scripts/beispiel.sh <<'SH'\n#!/bin/bash\n# manuell-integriert: ja\n# bereinigung: nach-erfolg-archivieren\necho 'Lokale Beispielaufgabe abgeschlossen.'\nSH\ncd /root/ansible\ndatei=scripts/beispiel.sh\nsha=$(sha256sum \"/root/mein-paket/code/$datei\" | cut -d ' ' -f 1)\npython3 tools/local_extension.py approve /root/mein-paket \"$datei\" \"$sha\"\npython3 tools/local_extension.py install /root/mein-paket\nbin/control update-check --only local\npython3 tools/local_extension.py run \"$datei\"\npython3 tools/local_extension.py archive \"$datei\"\n```\n\nDer letzte Befehl zeigt die Vorschau. Nach Prüfung der Aufrufer archiviert `python3 tools/local_extension.py archive \"$datei\" --confirm-sha \"$sha\"` diese Dateiversion. Im ausgegebenen Archivordner liegen die Datei, `BELEG.json` mit freigegebenem SHA-256, gemessenem Archiv-SHA und Laufnachweis sowie `SHA256SUMS`. Dort prüft `sha256sum -c SHA256SUMS` die archivierten Bytes.\n\nFür dauerhafte Dateien verwende `# bereinigung: behalten`. In YAML stehen beide Kommentarzeilen direkt unter `---`, in ausführbaren Skripten unter der Shebang. Lokale Playbooks liegen unter `code/playbooks/` und laufen mit `python3 tools/local_extension.py run playbooks/beispiel.yml --limit ZIELGRUPPE`. Jede Änderung zuerst in der privaten Pflegequelle prüfen, mit ihrer neuen SHA freigeben und das Paket erneut installieren. Eine unveränderte archivierte Revision bleibt archiviert.\n\n`bin/control update-check` meldet lokale Erweiterungen in einem eigenen Abschnitt. `--json` enthält dafür `local_extensions`. Der bestehende Cron-Aufruf mit `--auto` prüft die lokalen SHA-256 vor dem Git-Abruf. Fehlende, zusätzliche oder veränderte Dateien blockieren den Wechsel. Ein Controller ohne eingerichtete Erweiterungen arbeitet wie bisher. Cron führt lokale Aufgaben und Archivierungen niemals selbst aus.\n\n## Vorhandenes Standortpaket ergänzen\n\nDie gemeinsamen Playbooks und Rollen unter `/root/ansible` beziehen ihre Updates aus Git. Für eine standortspezifische Aufgabe ein eigenes Playbook mit eindeutigem Namen schreiben. Es darf die regulären Basisrollen aufrufen. Ein lokales Zusatzpaket trägt dieselbe Standortkennung wie das vorhandene Standortpaket und einen eigenen Namen. Beide können getrennt gepflegt werden.\n\nIm privaten Arbeitsverzeichnis das vorhandene Standortpaket als ersten Parameter angeben. Der zweite Parameter ist ein neuer Ordner. Beispiel für Debian:\n\n```bash\nwerkzeug=/root/ansible/tools/local_extension.py\npython3 \"$werkzeug\" new-supplement ./standort ./zusatz dienstpruefung\nmkdir -p ./zusatz/code/playbooks\ncp ./local_dienst_pruefen.yml ./zusatz/code/playbooks/\ndatei=playbooks/local_dienst_pruefen.yml\nsha=$(sha256sum \"./zusatz/code/$datei\" | cut -d ' ' -f 1)\npython3 \"$werkzeug\" approve ./zusatz \"$datei\" \"$sha\"\n```\n\nDas oben beschriebene Kommentarformat gilt auch für den Zusatz. Das Standortpaket muss auf dem Ziel bereits registriert sein. Den Ordner `zusatz` auf diesen Controller kopieren. Dort als root registrieren und überprüfen:\n\n```bash\ncd /root/ansible\npython3 tools/local_extension.py install /root/eingang/zusatz\nbin/control update-check --only local\n```\n\nDer Checker meldet den Zusatznamen und prüft die Dateien auch beim Cronlauf. Fehlt eine lokale Datei in einer späteren Standortlieferung, bleibt die registrierte Revision erhalten. Nur eine bewusste Lieferung desselben lokalen Pakets kann dessen Datei aktualisieren. Ein fremder Paketpfad oder eine gleichnamige Controllerrolle blockiert die Übernahme. Den fachlichen Lauf separat und mit konkreter Zielauswahl starten, etwa mit `python3 tools/local_extension.py run playbooks/local_dienst_pruefen.yml --limit ZIELHOST`.\n\n## Lokales Register migrieren\n\nBei `MIGRATION_REQUIRED` zuerst die bestehende Freigabe prüfen. Im Controller-Verzeichnis:\n\n```sh\npython3 tools/migrate_local_extensions.py --check\npython3 tools/migrate_local_extensions.py --apply\nbin/control update-check --only local\n```\n\nDer zweite Befehl meldet den Pfad der privaten Schema-1-Sicherung (Modus `0600`). Die Migration ändert ausschließlich `register.json`. Skripte, YAML-Dateien und Laufbelege behalten ihre Bytes und Prüfsummen. Auch `archiv/<id>/datei`, `BELEG.json` und `SHA256SUMS` behalten ihre Namen, damit alte Belege weiter prüfbar sind.\n\nDeutsche Dateiköpfe bleiben gültig. Auf Englisch stehen direkt unter dem Shebang oder YAML-Dokumentanfang `# manually-integrated: yes` und `# cleanup: keep` oder `# cleanup: archive-after-success`. Vor dem Controller-Rollback auf einen älteren Prüfer zuerst das Register mit `python3 tools/migrate_local_extensions.py --rollback \"$BACKUP\"` zurücksetzen. Für `BACKUP` den vom Migrationsbefehl ausgegebenen Sicherungspfad einsetzen. Spätere Registeränderungen sperren diese Rücknahme.\n\nFür die Erstmigration mit einem älteren Checker steht der private Brücken-Checkout oben bereit. Dort sind die einzelnen Schritte für Vorschau, Registermigration, Codeübernahme und Wiederherstellung nach Unterbrechungen aufgeführt.\n\n## Lokales Zusatzregister im Controllerzustand\n\nNeben dem bisherigen Nachbarordner `<controller>-local` unterstützt der Prüfer\nauch `<controller>/.local/extensions`. Das vorhandene Register, der private Code,\nLaufbelege und Archive bleiben dabei zusammen; die Standortkennung bleibt in\n`.local/local-extension-id`. Das neue Layout wird nur verwendet, wenn sein Ordner\nbereits vorhanden ist. Neue Installationen und bestehende Nachbarordner bleiben\nbeim bisherigen Verhalten. Zwei gleichzeitige Ablagen werden als Konflikt gemeldet.\n\nFür eine bewusste Umstellung zuerst das Register und die Kennung privat sichern,\nden Schemawechsel mit `tools/migrate_local_extensions.py` prüfen und übernehmen.\nWährend kein Update- oder Registerschreibprozess läuft, den vollständigen Ordner\nin `.local/extensions` verschieben. Danach `bin/control update-check --only local`\nprüfen. Für einen Rückwechsel auf einen älteren Prüfer den Ordner vorher an die\nbisherige Nachbarposition zurückschieben und gegebenenfalls das Schema-1-Backup\nmit dem noch aktuellen Migrator wiederherstellen. Die Dateiinhalte und freigegebenen\nSHA-Werte ändern sich durch den Pfadwechsel nicht. Schema-Migration und deren\nRücknahme funktionieren mit beiden Ablagen.\n\nEin Ziel ohne deklarierte Unterstützung der internen Ablage wird bei Update und Rollback blockiert. Das gilt auch für automatische main-Updates; zuerst die komplette Ablage an den Nachbarpfad zurücklegen.\n",
      "fields": {
        "check": {
          "label": "check",
          "description": "Erweiterte lokale Konfigurations-/GET-API-Pruefung, keine Schreib-API."
        },
        "offline": {
          "label": "offline",
          "description": "Mit --check keine Netzwerkaufrufe."
        },
        "configure": {
          "label": "configure",
          "description": "Interaktive Einrichtung mit Vorschau/YES; Terminal erforderlich, nicht mit --json."
        },
        "sort_settings": {
          "label": "sort-settings",
          "description": "Nur Settings ordnen mit Vorschau/YES; Terminal erforderlich."
        },
        "details": {
          "label": "details",
          "description": "Auch passende/optionale Feldbefunde anzeigen."
        },
        "json": {
          "label": "json",
          "description": "Strukturierter Nur-Lese-Bericht ohne Credentialwerte."
        },
        "only": {
          "label": "only",
          "description": "Eine Komponente, settings, registry oder eine installierte Erweiterung prüfen."
        },
        "field": {
          "label": "field",
          "description": "Mit --configure gezielt bekannten Schluessel abfragen; im Terminal wiederholbar."
        },
        "find_usage": {
          "label": "find-usage",
          "description": "Statische Fundstellen einer Variable, keine automatische Loeschung."
        },
        "timeout": {
          "label": "timeout",
          "description": "API-Timeout 1 bis 30 Sekunden, Standard 8."
        },
        "color": {
          "label": "Farbausgabe",
          "description": "auto: nur Terminal; always: erzwingen; never: ausschalten. JSON immer farbfrei."
        },
        "cleanup": {
          "label": "cleanup",
          "description": "Freigegebene Altdateien nach Projekt-/Cron-/Systemd-Pruefung, Vorschau und YES archivieren; keine aktiven Dateien loeschen."
        },
        "no-prompt": {
          "label": "no-prompt",
          "description": "Keine optionale Bereinigungsfrage im normalen Terminalprueflauf."
        },
        "remote": {
          "label": "remote",
          "description": "Änderungen aus main anzeigen (mit --staging aus staging)."
        },
        "staging": {
          "label": "staging",
          "description": "Staging für diesen manuellen Abruf wählen. Ohne --apply nur Vorschau."
        }
      }
    },
    "en": {
      "title": "Check versions and settings or configure a new controller",
      "description": "Check controller profiles, file hashes and optional cleanup. `--remote` previews the released main branch over HTTPS. `--apply` installs it. Cron uses the same credentials with `--auto`. Local `versions.txt` records version, HTTPS origin and an optional token-file path for each module. Public modules are anonymous. A private module’s external token file must be owned by the executing user and have mode `0600`.\n\n## Switch between main and staging\n\n| Branch | Preview | Apply |\n| --- | --- | --- |\n| Release (`main`) | `bin/control update-check --remote` | `bin/control update-check --apply` |\n| Test (`staging`) | `bin/control update-check --staging` | `bin/control update-check --apply --staging` |\n\nThe selection applies to this invocation and all installed controller modules. Cron always uses main with `--auto`, so the next scheduled update can return a test controller to the release. Both branches must support the flag for switching in both directions.\n\n`ansible --version` shows the Ansible CLI version. `module-versions`, or directly `bin/control module-versions`, lists installed module versions and the current user’s installed TUI. The alias is available in a new controller shell. Local `versions.txt` uses `s1.2.3` for staging and `1.2.3` for main, both derived from the numeric `VERSION.txt`. Preview shows target versions. Apply changes installed versions.\n\nA branch change backs up and removes managed files exclusive to the previous version. Local edits to those files block the change. Restore the saved state with `--rollback BACKUP_ID`.\n\n### Test an older controller\n\nFor an older checker, use the verified migration through the intermediate commits below.\n\n## Check local SHA-256 hashes\n\n### Migrate SSS from an older controller\n\nBack up the local `versions.txt` before switching. If SSS is in use, add the registration below. Modifications in the old SSS directory are reported as conflicts. Migrate personal settings privately as described in the [SSS guide](https://github.com/v4z00/Ansible-SSS/blob/main/README.md) and review each hash conflict before updating.\n\nRun the first block in a root Bash shell on a Debian controller with its existing Python environment. It creates a private checkout under `/root` and verifies the job-report path update, the SSS bridge commit, its successor and the current main revision with the previously verified checker at each step. Record the printed directory path.\n\n```bash\nbridge_dir=$(mktemp -d /root/ansible-bridge.XXXXXXXX) && (\n  set -eu\n  umask 077\n  printf 'Bridge directory: %s\\n' \"$bridge_dir\"\n  git clone --quiet --branch main https://github.com/v4z00/Ansible-Allgm.git \"$bridge_dir/base\"\n  cd \"$bridge_dir/base\"\n  git checkout --quiet --detach 5fd77a75b6d089f063dccc675f50d07b074925c8\n  /root/ansible/.venv/bin/python /root/ansible/update_check/staging_manifest.py verify Allgm HEAD\n  cp update_check/staging_manifest.py \"$bridge_dir/jobs-verifier.py\"\n  git checkout --quiet --detach c7d2d7cbd881a7387d2fa424c10dfabc48a3fd41\n  /root/ansible/.venv/bin/python \"$bridge_dir/jobs-verifier.py\" verify Allgm HEAD\n  cp update_check/staging_manifest.py \"$bridge_dir/bridge-verifier.py\"\n  git checkout --quiet --detach 760166ebd9fd0b933b17307c6ace6855719c0652\n  /root/ansible/.venv/bin/python \"$bridge_dir/bridge-verifier.py\" verify Allgm HEAD\n  cp update_check/staging_manifest.py \"$bridge_dir/current-verifier.py\"\n  git checkout --quiet --detach origin/main\n  /root/ansible/.venv/bin/python \"$bridge_dir/current-verifier.py\" verify Allgm HEAD\n  git rev-parse --verify HEAD > \"$bridge_dir/VERIFIED\"\n)\n```\n\nThe `VERIFIED` file contains the commit ID only after verification succeeds. If a check fails, stop, resolve the error and repeat the first block in a new directory. The checkout survives logout. In the original shell `bridge_dir` is already set. After reconnecting, list the verification records and enter **the directory for this operation without `/VERIFIED`**:\n\n```bash\nprintf '%s\\n' /root/ansible-bridge.*/VERIFIED\nread -r -p 'Bridge directory: ' bridge_dir\n```\n\n**Preview.** Inspect the planned switch to main without applying changes:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote\n)\n```\n\nWhen `MIGRATION_REQUIRED` is the only blocker and local files are intact, exit status 1 is expected in this preview. Review the register migration plan first. Investigate other failures before proceeding. If there is no legacy register, skip both register steps.\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --check\n)\n```\n\n**Migrate the register.** Apply after reviewing the plan and record the printed path to the private schema-1 backup. This block then runs a fresh code preview:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --apply\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --remote\n)\n```\n\n**Apply the code update.** Run only after a successful preview and review of its changes. Record the printed controller backup ID for rollback:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --apply\n)\n```\n\n**Rollback.** If switching fails before the new code is installed, restore the migrated register using the retained checkout. Enter the recorded **register backup path**:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  read -r -p 'Register backup: ' backup\n  /root/ansible/.venv/bin/python tools/migrate_local_extensions.py --controller /root/ansible --rollback \"$backup\"\n)\n```\n\nIf the new code was installed and you need the older checker again, restore the register first as above. Then enter the **controller backup ID**. Code rollback also restores the previous receipt and `versions.txt`:\n\n```bash\n(\n  set -eu\n  cd \"${bridge_dir:?}/base\"\n  test -s ../VERIFIED\n  test \"$(git rev-parse --verify HEAD)\" = \"$(cat ../VERIFIED)\"\n  read -r -p 'Controller backup ID: ' backup_id\n  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --rollback \"$backup_id\"\n)\n```\n\nIf the register was never migrated, only code rollback is needed. Keep the checkout until you have confirmed the final controller and register state. Then manually remove the specific bridge directory you recorded.\n\n### Git add-ons\n\nA controller can have one site profile and multiple Git add-ons. Keep all four fields in each module row. A separate comment registers each add-on. Example for the local `versions.txt`:\n\n```text\n# addon=SSS\nSSS|0.0.0|https://github.com/v4z00/Ansible-SSS.git|\n```\n\nUse `0.0.0` for initial registration. Preview shows the offered version, and apply records the installed version. Rows without registration remain passive. For a private add-on the fourth field holds the token-file path. All registered modules must offer the chosen branch.\n\nPreview the plan with `bin/control update-check --remote` before `bin/control update-check --apply`. To revert, pass the printed backup ID to `bin/control update-check --rollback BACKUP_ID`. Keep both row and registration for installed add-ons. Missing sources, changed managed add-on files or occupied destinations stop the checker before replacement.\n\n`--only local` shows the separate file report. Cron reports this status before fetching from Git with `--auto`. Unknown, missing or modified local files and damaged archives block apply. Supplements are reported by package name. Conflicts with a base playbook or role are reported as `BASIS_KONFLIKT`.\n\n## Create a local extension package\n\n| Path | Purpose |\n|---|---|\n| `bin/control` | Controller commands and update checks |\n| `playbooks/`, `roles/` | Shared workflows managed through Git |\n| `tools/local_extension.py` | Approve, install, run and archive local files |\n| `/root/ansible-local/code/` | Separately installed roles, playbooks, scripts and local variables |\n| `/root/ansible-local/register.json` | Approved paths and SHA-256 values |\n| `/root/ansible-local/runs/`, `archiv/` | Local run and archive receipts |\n\nAfter [installing the base](../configurations/installation-allgm.md), create a local extension package outside any Git checkout. Example as root on a Debian controller:\n\n```bash\nmkdir -p /root/mein-paket/code/scripts\ncat > /root/mein-paket/code/scripts/beispiel.sh <<'SH'\n#!/bin/bash\n# manuell-integriert: ja\n# bereinigung: nach-erfolg-archivieren\necho 'Lokale Beispielaufgabe abgeschlossen.'\nSH\ncd /root/ansible\ndatei=scripts/beispiel.sh\nsha=$(sha256sum \"/root/mein-paket/code/$datei\" | cut -d ' ' -f 1)\npython3 tools/local_extension.py approve /root/mein-paket \"$datei\" \"$sha\"\npython3 tools/local_extension.py install /root/mein-paket\nbin/control update-check --only local\npython3 tools/local_extension.py run \"$datei\"\npython3 tools/local_extension.py archive \"$datei\"\n```\n\nThe last command previews the operation. Check callers, then archive this specific revision with `python3 tools/local_extension.py archive \"$datei\" --confirm-sha \"$sha\"`. The reported archive contains the file, `BELEG.json` with approved and measured hashes and the run receipt, and `SHA256SUMS`. Run `sha256sum -c SHA256SUMS` there to verify the archived bytes.\n\nFor permanent files, use `# bereinigung: behalten`. Place both marker comments directly under `---` in YAML or after the shebang in scripts. Put playbooks under `code/playbooks/` and run them with `python3 tools/local_extension.py run playbooks/beispiel.yml --limit TARGET_GROUP`. Verify each change in the private source, approve its new hash and reinstall the package. An unchanged archived revision stays archived.\n\n`bin/control update-check` reports extensions in a separate section. JSON reports use `local_extensions`. Cron with `--auto` verifies local SHA-256 before fetching from Git. Missing, extra or modified files block the switch. Controllers without local extensions continue to work as before. Cron does not run or archive local tasks.\n\n## Extend an existing site package\n\nShared playbooks and roles under `/root/ansible` receive updates from Git. Give site-specific playbooks unique names. They may call shared base roles. Give a supplement the same site ID as its parent package and a unique package name. Maintain them independently.\n\nIn the private workspace, pass the existing site package first, followed by a new directory. On Debian:\n\n```bash\nwerkzeug=/root/ansible/tools/local_extension.py\npython3 \"$werkzeug\" new-supplement ./standort ./zusatz dienstpruefung\nmkdir -p ./zusatz/code/playbooks\ncp ./local_dienst_pruefen.yml ./zusatz/code/playbooks/\ndatei=playbooks/local_dienst_pruefen.yml\nsha=$(sha256sum \"./zusatz/code/$datei\" | cut -d ' ' -f 1)\npython3 \"$werkzeug\" approve ./zusatz \"$datei\" \"$sha\"\n```\n\nUse the same marker comments for the supplement. The target must already have the site package registered. Copy the `zusatz` directory to the controller. Register and check it as root:\n\n```bash\ncd /root/ansible\npython3 tools/local_extension.py install /root/eingang/zusatz\nbin/control update-check --only local\n```\n\nThe checker reports the supplement by name and verifies its files during cron. A later site package that omits a registered file leaves that revision in place. Only a deliberate update from the same local package can replace it. Paths owned by another package or matching a controller role block installation. Run the operation separately with an explicit target, for example `python3 tools/local_extension.py run playbooks/local_dienst_pruefen.yml --limit TARGET_HOST`.\n\n## Migrate a local register\n\nIf the checker reports `MIGRATION_REQUIRED`, review the existing approvals. Run these commands from the controller directory:\n\n```sh\npython3 tools/migrate_local_extensions.py --check\npython3 tools/migrate_local_extensions.py --apply\nbin/control update-check --only local\n```\n\nThe second command prints the path to the private schema-1 backup (mode `0600`). Migration changes only `register.json`. Scripts, playbooks and run receipts keep their original bytes and checksums. The archive names `archiv/<id>/datei`, `BELEG.json` and `SHA256SUMS` are stable so older receipts remain verifiable.\n\nGerman headers remain valid. For English headers, put `# manually-integrated: yes` and either `# cleanup: keep` or `# cleanup: archive-after-success` directly after the shebang or YAML document start. Before rolling the controller back to an older checker, restore the register with `python3 tools/migrate_local_extensions.py --rollback \"$BACKUP\"`. Set `BACKUP` to the path printed during migration. The restore refuses to overwrite later register edits.\n\nFor a first migration from an older checker, use the private bridge checkout above. Follow its separate preview, register migration, code update and recovery steps.\n\n## Keep the local extension register in controller state\n\nThe checker supports both the existing sibling `<controller>-local` and\n`<controller>/.local/extensions`. Keep the register, private code, run receipts and\narchives together; the site pin remains `.local/local-extension-id`. The internal\nlayout is selected only when its folder already exists. Existing installations\nand new installations retain the sibling default. Two simultaneous locations\nfail explicitly instead of choosing one silently.\n\nFor a deliberate move, back up the register and site pin privately, then check\nand apply any schema migration with `tools/migrate_local_extensions.py`. With no\nconcurrent update/register writer, move the complete folder into `.local/extensions`\nand run `bin/control update-check --only local`. Before rolling back to an older\nchecker, move it back to its sibling position and restore the schema-1 backup with\nthe current migrator if required. Moving does not change private code or approved\nhashes. Schema migration and rollback work in either location.\n\nAn update or rollback target without declared internal-layout support is blocked, including automatic main updates. Move the complete register to the sibling location before switching.\n",
      "fields": {
        "check": {
          "label": "Check mode",
          "description": "Run the extended local configuration and read-only GET API checks."
        },
        "offline": {
          "label": "Offline",
          "description": "With --check, skip network calls."
        },
        "configure": {
          "label": "configure",
          "description": "Configure interactively with a preview and YES confirmation. Requires a terminal and cannot be combined with --json."
        },
        "sort_settings": {
          "label": "sort-settings",
          "description": "Reorder settings only. Requires a terminal, a preview and YES confirmation."
        },
        "details": {
          "label": "details",
          "description": "Also show matching and optional field results."
        },
        "json": {
          "label": "JSON output",
          "description": "Produce a structured read-only report without credential values."
        },
        "only": {
          "label": "Component",
          "description": "Check one component, settings, the registry or an installed extension."
        },
        "field": {
          "label": "field",
          "description": "With --configure, prompt for a specific known key. Repeat this option for multiple keys."
        },
        "find_usage": {
          "label": "find-usage",
          "description": "List static references to a variable for review. No files are removed."
        },
        "timeout": {
          "label": "Timeout",
          "description": "API timeout in seconds, from 1 to 30. Defaults to 8."
        },
        "color": {
          "label": "Color output",
          "description": "auto: terminal only. always: force color. never: disable color. JSON is always plain text."
        },
        "cleanup": {
          "label": "cleanup",
          "description": "Preview and archive approved obsolete files after checking project, cron and systemd references. Type YES to confirm. Active files are preserved."
        },
        "no-prompt": {
          "label": "Skip cleanup prompt",
          "description": "Skip the optional cleanup prompt during a regular terminal check."
        },
        "remote": {
          "label": "Preview remote changes",
          "description": "Show changes from main, or from staging when --staging is set."
        },
        "staging": {
          "label": "Staging branch",
          "description": "Select staging for this manual fetch. Preview unless --apply is present."
        }
      }
    }
  }
}
```

</details>
