# Playbook playbooks/docker/deploy_docker_stacks.yml

Vorhandener Einstieg: `playbooks/docker/deploy_docker_stacks.yml`.

Im Quelltext benannte Plays/Aufgaben:

- PLAY 1: Vorbereitung
- TASK 1.1: Ergebnislisten initialisieren
- TASK 1.2: Basisvariablen prüfen
- PLAY 2: Nicht mehr verwaltete Docker Stacks erkennen
- TASK 2.1: Verwaltete Compose-Dateien für diesen Host auf Management-Host finden
- TASK 2.2: Liste verwalteter Compose-Projektnamen erstellen
- TASK 2.3: Laufende Compose-Projekte auf Host abrufen
- TASK 2.4: Laufende Compose-Projekte parsen
- TASK 2.5: Waisen-Stack-Kandidatenliste initialisieren
- TASK 2.6: Waisen-Stacks per Projektname sammeln
- TASK 2.7: Gefundene Waisen-Stacks anzeigen
- PLAY 2.5: Lokale Bestätigung für Waisen-Stack-Bereinigung
- TASK 2.5.1: Globale Waisen-Stack-Anzahl berechnen
- TASK 2.5.2: Waisen-Stacks lokal auf Management-Host bestätigen
- TASK 2.5.3: Globale Prune-Bestätigung speichern
- PLAY 2.6: Bestätigte Waisen-Stacks entfernen
- TASK 2.6.1: Waisen-Stacks entfernen
- TASK 2.6.2: Bereinigungsergebnis speichern
- TASK 2.6.3: Bereinigte Stacks anzeigen
- PLAY 3: Konfiguration synchronisieren
- TASK 3.1: Sicherstellen, dass das Zielverzeichnis existiert
- TASK 3.2: Projektverzeichnisse synchronisieren
- TASK 3.3: Compose-Projekte auf Zielsystem finden
- TASK 3.4: Prüfen, ob Compose-Projekte gefunden wurden
- PLAY 4: Dateirechte aus host_vars vor Deployment setzen
- TASK 4.1: Dateiregeln validieren
- TASK 4.2: Zielpfade pruefen
- TASK 4.3: Konfigurierte Dateirechte anwenden
- PLAY 6: Docker Stacks deployen
- TASK 6.1: Kritische Compose-Projekte bestimmen
- TASK 6.2: Standard Compose-Projekte bestimmen
- TASK 6.3: Kritische Stacks deployen
- TASK 6.4: Warte kurz auf Basisdienste
- TASK 6.5: Standard-Stacks deployen
- TASK 6.6: Deployment-Ergebnisse zusammenführen
- PLAY 7: Intelligenter Health Check
- TASK 7.1: Compose-Dateien einlesen
- TASK 7.2: Erwartete Container-Namen ermitteln
- TASK 7.3: Hinweis, falls keine container_name-Werte gefunden wurden
- TASK 7.4: Auf Start aller explizit benannten Container warten
- TASK 7.5: Containerstatus speichern
- TASK 7.6: Problematische Container anzeigen
- PLAY 8: Globale Ergebnisse aggregieren
- TASK 8.1: Deployment-Ergebnisse von allen Hosts sammeln
- PLAY 9: Zusammenfassung & Log-Datei erstellen
- TASK 9.1: Log-Verzeichnis anlegen
- TASK 9.2: Zusammenfassung generieren
- TASK 9.3: Zusammenfassung im Terminal anzeigen und auf Bestätigung warten

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/docker/deploy_docker_stacks.yml",
  "title": "Playbook playbooks/docker/deploy_docker_stacks.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/docker/deploy_docker_stacks.yml"
  ],
  "source_hashes": {
    "playbooks/docker/deploy_docker_stacks.yml": "ca74ef6d5d83e9d2c87a8014a3e275d7f0db3e9fe61c90075d67f2a9d1ec29f4"
  }
}
```

## Quellen und Pflege

- `playbooks/docker/deploy_docker_stacks.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
