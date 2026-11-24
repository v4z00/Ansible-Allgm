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

Mit `ansible-Version` siehst du die installierte Version jedes Moduls. Ist Ansible TUI für das aktuelle Konto installiert, wird auch ihre Version angezeigt. In einer neuen Controller-Shell steht der Alias bereit. Direkt geht es mit `bin/control ansible-Version`. In der lokalen `versions.txt` steht zum Beispiel `s1.2.3` für Staging und `1.2.3` für Main. Beide leiten sich aus derselben numerischen Basis in `VERSION.txt` ab. Die Vorschau zeigt die Zielversionen. Erst das Übernehmen ändert die installierten Versionen.

Beim Wechsel werden verwaltete Dateien, die nur zum bisherigen Stand gehören, mitgesichert und entfernt. Eigene Änderungen an solchen Dateien blockieren den Wechsel. Über `--rollback SICHERUNGSKENNUNG` lässt sich der gesicherte Stand wiederherstellen.

### Einen älteren Controller testen

Kennt der installierte Checker `--staging` noch nicht, kannst du den neuen Checker aus einem separaten Checkout starten. Als root auf dem Debian-Testcontroller:

```bash
(
  set -eu
  testcode=$(mktemp -d)
  trap 'rm -rf -- "$testcode"' EXIT
  git clone --quiet --single-branch --branch staging https://github.com/v4z00/Ansible-Allgm.git "$testcode/Allgm"
  cd "$testcode/Allgm"
  /root/ansible/.venv/bin/python /root/ansible/update_check/staging_manifest.py verify Allgm HEAD
  /root/ansible/.venv/bin/python update_check/check.py --root /root/ansible --staging
)
```

Das zeigt die Vorschau. Für die Übernahme hänge beim letzten Python-Aufruf `--apply` an. Der Checker bezieht die registrierten Module aus ihren geprüften Quellen. Nach der Rückkehr zu einer älteren Freigabe funktioniert der separate Checkout auf dieselbe Weise.

## Lokale SHA-Prüfung

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
    "tools/install_controller.py"
  ],
  "source_hashes": {
    "bin/control.d/update-check.json": "168ea20754ab69374245ba47cc97f1938fc4a53c3269a94d7108bec1101dfd7b",
    "bin/control.d/update-check.sh": "7cc1fc9287cff92e352ad038519366d7dfd04d4efe99d1c70d980de0c62ac807",
    "update_check/check.py": "639c47fa2eec26fa81a6e81e0b9f531c4794d894fc3480237b75bed553c941e1",
    "update_check/configure.py": "c6c675198f99121dbd1d6f550481b2a9190bdb25a4c19d5ec45e7da4fb1340d3",
    "update_check/probes.py": "22dbb65098b7adfce12c0dc0a39df14440748bbf3926416c432f2a7fbf69c75a",
    "update_check/cleanup.py": "b075547b1bfbfc3483563c2d3e79ff5ec2a5b9901a879b352ed45635228b2a36",
    "update_check/rollout.py": "d1f87001f346785631356491d1fb4afb168e075af10967f69aed49408c560601",
    "tools/github_https.py": "4939726758123ce18c3558bd22a668052a0bb028b62a1c71534b92ccb89e5bd5",
    "tools/install_controller.py": "af369a6a3d1824eba91c71ba5453ff7cdef61368ec8f6f28eff40932ea046302"
  }
}
```
