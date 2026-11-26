# Custom-systemd-Skripte rein lesend erfassen

`scripts/get_systemd_scripts.py` ist ein eigenständiger Sammler mit eingebettetem
Ansible-Playbook und Hostfilter. Bei Bedarf die einzelne Datei außerhalb des
Controllers als `GET_SYSTEMD_SCRIPTS.py` ablegen. Vorhandene Ansible-Konfiguration
und deren SSH-/Become-Einstellungen werden verwendet; es werden keine Pakete
installiert und keine Dienste, Timer oder Crons verändert.

```sh
python3 GET_SYSTEMD_SCRIPTS.py --project /root/ansible --limit all_linux_systems --list-hosts
python3 GET_SYSTEMD_SCRIPTS.py --project /root/ansible --limit all_linux_systems
```

`--limit` ist Pflicht, `--inventory` wählt ausdrücklich eine andere Inventoryquelle.
`--output` setzt einen neuen privaten Ausgabeordner; existierende Ausgabeordner
werden nicht überschrieben. Ohne diese Option entsteht ein neuer Zeitstempelordner
im Arbeitsverzeichnis. `--version` zeigt den Sammlerstand. Nur bestehende Linux-
Systemmanager werden abgefragt. Eine Controller-Inventarverbindung `local` führt
auch tatsächlich lokal aus; vom Mac aus dafür einen echten SSH-Zugang verwenden.

Pro Host entsteht `HOSTNAME/systemd.json` mit Modus 0600. Erfasst werden installierte
und geladene Services/Timer, lokale Unitfragmente/Drop-ins, Zustände und passende
Skriptpfade. Standardservices ohne lokale Anpassung oder passenden Skriptpfad
bleiben aus der Ergebnisliste. Bei Timern wird die auslösbare Unit ausgewiesen.
Lokale Benutzermanager-Unitdateien werden zunächst nur als Dateinamen aufgeführt;
solche Funde benötigen eine gesonderte Prüfung. Sie gelten nicht als vollständig
geprüfte Userdienste. Komplexe Startbefehle bleiben ebenfalls als Prüfung offen.

Die Abfrage fordert weder Environment/EnvironmentFiles noch Credential-Werte,
Beschreibungen oder Unit-Rohtexte an. Skript- und Konfigurationsdateien werden
nicht geöffnet. Exec-Eigenschaften werden separat ausschließlich auf dem Host
verarbeitet: Nur der ausführbare Skriptpfad oder der unmittelbare Skriptparameter
eines Shell-Aufrufs wird übernommen. Weitere Argumente werden nicht nach Pfaden
durchsucht und nicht ausgegeben; auch ein passwortartiger Wert mit .sh am Ende
bleibt verborgen. Ansible-Rohdiagnosen werden nicht ausgegeben oder gespeichert.

Die Ausgabe ist ein Bestandsbeleg zum Abfragezeitpunkt. Sie ändert keine
Startbedingungen und übernimmt keine Units automatisch. Erst nach bestätigter
Zuordnung lässt sich das bestehende Startmodell in die Skriptverwaltung
übernehmen. Ein Export von Timerdiensten allein belegt keine Boot-/Dauerdienste.

Fachreferenz: [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html),
[systemd.timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html).

```json
{
  "schema_version": 1,
  "kind": "configuration",
  "ref": "systemd-script-discovery",
  "title": "Custom-systemd-Skripte rein lesend erfassen",
  "documented": true,
  "fields": [],
  "sources": [
    "scripts/get_systemd_scripts.py"
  ],
  "source_hashes": {
    "scripts/get_systemd_scripts.py": "65d48b1c8525f1bf341668a5ebe415e11783142d6008c6d405aa1e2de860fb24"
  },
  "i18n": {
    "de": {
      "title": "Custom-systemd-Skripte rein lesend erfassen",
      "description": "# Custom-systemd-Skripte rein lesend erfassen\n\n`scripts/get_systemd_scripts.py` ist ein eigenständiger Sammler mit eingebettetem\nAnsible-Playbook und Hostfilter. Bei Bedarf die einzelne Datei außerhalb des\nControllers als `GET_SYSTEMD_SCRIPTS.py` ablegen. Vorhandene Ansible-Konfiguration\nund deren SSH-/Become-Einstellungen werden verwendet; es werden keine Pakete\ninstalliert und keine Dienste, Timer oder Crons verändert.\n\n```sh\npython3 GET_SYSTEMD_SCRIPTS.py --project /root/ansible --limit all_linux_systems --list-hosts\npython3 GET_SYSTEMD_SCRIPTS.py --project /root/ansible --limit all_linux_systems\n```\n\n`--limit` ist Pflicht, `--inventory` wählt ausdrücklich eine andere Inventoryquelle.\n`--output` setzt einen neuen privaten Ausgabeordner; existierende Ausgabeordner\nwerden nicht überschrieben. Ohne diese Option entsteht ein neuer Zeitstempelordner\nim Arbeitsverzeichnis. `--version` zeigt den Sammlerstand. Nur bestehende Linux-\nSystemmanager werden abgefragt. Eine Controller-Inventarverbindung `local` führt\nauch tatsächlich lokal aus; vom Mac aus dafür einen echten SSH-Zugang verwenden.\n\nPro Host entsteht `HOSTNAME/systemd.json` mit Modus 0600. Erfasst werden installierte\nund geladene Services/Timer, lokale Unitfragmente/Drop-ins, Zustände und passende\nSkriptpfade. Standardservices ohne lokale Anpassung oder passenden Skriptpfad\nbleiben aus der Ergebnisliste. Bei Timern wird die auslösbare Unit ausgewiesen.\nLokale Benutzermanager-Unitdateien werden zunächst nur als Dateinamen aufgeführt;\nsolche Funde benötigen eine gesonderte Prüfung. Sie gelten nicht als vollständig\ngeprüfte Userdienste. Komplexe Startbefehle bleiben ebenfalls als Prüfung offen.\n\nDie Abfrage fordert weder Environment/EnvironmentFiles noch Credential-Werte,\nBeschreibungen oder Unit-Rohtexte an. Skript- und Konfigurationsdateien werden\nnicht geöffnet. Exec-Eigenschaften werden separat ausschließlich auf dem Host\nverarbeitet: Nur der ausführbare Skriptpfad oder der unmittelbare Skriptparameter\neines Shell-Aufrufs wird übernommen. Weitere Argumente werden nicht nach Pfaden\ndurchsucht und nicht ausgegeben; auch ein passwortartiger Wert mit .sh am Ende\nbleibt verborgen. Ansible-Rohdiagnosen werden nicht ausgegeben oder gespeichert.\n\nDie Ausgabe ist ein Bestandsbeleg zum Abfragezeitpunkt. Sie ändert keine\nStartbedingungen und übernimmt keine Units automatisch. Erst nach bestätigter\nZuordnung lässt sich das bestehende Startmodell in die Skriptverwaltung\nübernehmen. Ein Export von Timerdiensten allein belegt keine Boot-/Dauerdienste.\n\nFachreferenz: [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html),\n[systemd.timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html).",
      "fields": []
    },
    "en": {
      "title": "Read custom systemd script bindings",
      "description": "# Read custom systemd script bindings\n\n`scripts/get_systemd_scripts.py` is a standalone, read-only Ansible collector.\nCopy the one file outside the controller if needed. Specify --project, an explicit\n--limit, optionally --inventory and a new --output directory. --list-hosts queries\ninventory selection only; --version identifies the collector. Existing SSH and\nbecome settings apply. A local inventory connection really executes locally.\n\nHost-filtered results are stored as HOSTNAME/systemd.json with mode 0600. No script\nor configuration contents, Environment/EnvironmentFiles, credentials, descriptions,\nraw units or command arguments are exported. Exec properties are filtered separately\non the host; only an executable script or an immediate shell script parameter is\nretained. Arbitrary arguments are never searched for path-looking values. Raw\nAnsible diagnostics are discarded.\n\nSystem-manager services/timers and custom drop-ins are identified. User-manager\nunit files are listed by filename only and require separate review. Complex starts\nremain unresolved. The collector never starts, stops, enables, disables or reloads\nunits, nor changes cron. An observation is not an automatic scheduler migration.",
      "fields": []
    }
  }
}
```
