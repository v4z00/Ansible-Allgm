# Playbook playbooks/pki/deploy_apache_certificate.yml

Vorhandener Einstieg: `playbooks/pki/deploy_apache_certificate.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Wildcard-Zertifikat auf Apache-Webserver verteilen
- Quelldateien auf dem Controller pruefen
- Ausgewaehlten Zertifikatspfad anzeigen
- Vollstaendige Quelldateien verlangen
- Entschluesselten privaten Schluessel pruefen
- Public-Key-Fingerabdruck des privaten Schluessels ermitteln
- Public-Key-Fingerabdruck des Zertifikats ermitteln
- Zusammengehoerendes Zertifikat und Schluessel verlangen
- Zielverzeichnis fuer Apache-Zertifikat anlegen
- Zertifikat mit Intermediate-Zertifikat verteilen
- Entschluesselten privaten Schluessel verteilen
- Apache-Konfiguration pruefen
- Apache neu starten
- apache2

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/pki/deploy_apache_certificate.yml",
  "title": "Playbook playbooks/pki/deploy_apache_certificate.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/pki/deploy_apache_certificate.yml"
  ],
  "source_hashes": {
    "playbooks/pki/deploy_apache_certificate.yml": "1554b6670bba4baf512de2ec5191ae1a01d23d784eef0a9ea3d767ebd172f468"
  }
}
```

## Quellen und Pflege

- `playbooks/pki/deploy_apache_certificate.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
