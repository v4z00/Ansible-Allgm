# Job-Zusammenfassung senden

`bin/control jobs-summary` sammelt Ergebnisse der in der privaten
Controllerkonfiguration festgelegten Zielgruppe und sendet noch offene Berichte.
`--limit example-host` überschreibt die Auswahl für diesen Lauf, ohne den lokalen
Summary-Play aus dem Ansible-Limit auszuschließen.

Die Einrichtung erfolgt ausdrücklich über
`ansible-playbook playbooks/scripts/setup_controller.yml` mit lokalen Variablen
wie im reservierten Beispiel `examples/script_jobs/controller.yml.example`.
Zeitplan, Zielgruppe und mindestens ein vollständiger Nachrichtenkanal sind
Pflichtwerte der Einrichtung. Bestehende gültige lokale Werte werden nicht erraten.

Nach der Einrichtung werden durch die Control-Helfer gestartete Ansible-Läufe
und freigegebene lokale Erweiterungs-Playbooks erfasst. Die bisherigen sofortigen
Control-Betriebsnachrichten werden dann durch die Zusammenfassung ersetzt.
Direkte manuelle `ansible-playbook`-Aufrufe außerhalb dieser Einstiege können den
Callback ausdrücklich über `ANSIBLE_CALLBACK_PLUGINS=tools/callbacks`,
`ANSIBLE_CALLBACKS_ENABLED=script_job_results`, `SCRIPT_JOBS_CALLBACK=1` und
`SCRIPT_JOBS_CONTROLLER_DB=/PFAD/controller.sqlite3` verwenden. Existierende
Callback-Listen dabei ergänzen, nicht verdrängen.

Mail und Telegram werden getrennt bestätigt. Ein fehlgeschlagener Kanal bleibt
offen. Der Sender beansprucht einen Bericht kurzzeitig; Netzwerkversand hält
keine Datenbanktransaktion offen. Nach einem Abbruch zwischen Versand und
Bestätigung ist eine Dublette möglich; die Bericht-ID macht sie erkennbar.
Pro Aufruf werden höchstens drei Berichte mit jeweils maximal 200 Läufen
verarbeitet, damit ein aufgestauter Verlauf keinen unbegrenzten Nachrichtenstrom
verursacht. Weitere Ergebnisse bleiben gespeichert und werden später berücksichtigt.

Vzdump-Berichte sind getrennt und erscheinen nicht zusätzlich in der allgemeinen
Zusammenfassung. Fehlende oder überfällige geplante Läufe können als separate
Controllerwarnung erscheinen. Es gibt keine Meldung „wieder erfolgreich“.

Bei unvollständiger Hostabfrage wird der Fehlerzustand gemeldet; der Sammellauf
endet trotzdem ungleich null. Interne Sammelläufe erzeugen keine rekursive
Zusammenfassung ihrer eigenen Zusammenfassung.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "jobs-summary",
  "title": "Job-Zusammenfassung senden",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/jobs-summary.json",
    "bin/control.d/jobs-summary.sh",
    "scripts/job_summary.py",
    "playbooks/scripts/summary_jobs.yml"
  ],
  "source_hashes": {
    "bin/control.d/jobs-summary.json": "cd3547b41629df5f3397605610bdc437c8ccfd521afcd43539f9dc0def260705",
    "bin/control.d/jobs-summary.sh": "74416561b388b1d008581f335039243daff4241be88a850e9bcb26f2f974e853",
    "scripts/job_summary.py": "a42193ce6ef16e3e709e9671a6a7a8527873d524ce3b20131c198633691d640b",
    "playbooks/scripts/summary_jobs.yml": "63df8610672f470476cb863d493e145d8040bb0d4ea5f54ec573fbca86c2f150"
  }
}
```
