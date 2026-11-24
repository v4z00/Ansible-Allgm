# Playbook playbooks/security/sss/setup.yml

Vorhandener Einstieg: `playbooks/security/sss/setup.yml`.

Im Quelltext benannte Plays/Aufgaben:

- SSS auf dem Ansible-Host vorbereiten
- Unterstützte Plattform prüfen
- Offline-Werkzeuge installieren
- Geschützte Verzeichnisse außerhalb des Ansible-Baums anlegen
- Generator installieren
- Offline-Wiederherstellung installieren
- Startskript für die HTML-Oberfläche installieren
- Installationshilfe für Voraussetzungen ablegen
- Windows- und macOS-Starter ablegen
- Nicht geheime Konfiguration bereitstellen
- HTML-Oberfläche für die Offline-Wiederherstellung installieren
- Bedienungsanleitung ablegen
- Ausführliche Anleitung für Vertrauenspersonen ablegen
- Plattform-Startanleitung ablegen
- Nächster Schritt

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/security/sss/setup.yml",
  "title": "Playbook playbooks/security/sss/setup.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/security/sss/setup.yml"
  ],
  "source_hashes": {
    "playbooks/security/sss/setup.yml": "34f482f96aa7063a1a923713f363bc96802d605a022728bcbf0d0351c0e772ec"
  }
}
```

## Quellen und Pflege

- `playbooks/security/sss/setup.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
