# Apache-Zertifikate kontrolliert austauschen

Apache-Zertifikate kontrolliert austauschen

Aufruf: `bin/control apache-certificate [Optionen]`.

Vorhandene Kurzformen: `apache-certificate`.

Feature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.

Keine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.

Voraussetzungen laut Registry:
- `lib/control/helpers.sh`
- `scripts/deploy_apache_certificate.sh`
- `playbooks/pki/deploy_apache_certificate.yml`

Für den Aufruf über `bin/control` zuerst `APACHE_CERTIFICATE_ROOT` auf das lokale Quellverzeichnis setzen. Beim direkten Playbook-Aufruf `apache_certificate_root` und `apache_certificate_year` mitgeben.

## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "apache-certificate",
  "title": "Apache-Zertifikate kontrolliert austauschen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "bin/control.d/apache-certificate.json",
    "bin/control.d/apache-certificate.sh"
  ],
  "source_hashes": {
    "bin/control.d/apache-certificate.json": "e22750d73244a2894a08c6749c068421ff49cfa35c92e785c36f22659b3a278d",
    "bin/control.d/apache-certificate.sh": "ff5df678a25307b590e22a037358cb6294e1a57a6cff219580d67664f94aa397"
  },
  "i18n": {
    "de": {
      "title": "Apache-Zertifikate kontrolliert austauschen",
      "description": "# Apache-Zertifikate kontrolliert austauschen\n\nApache-Zertifikate kontrolliert austauschen\n\nAufruf: `bin/control apache-certificate [Optionen]`.\n\nVorhandene Kurzformen: `apache-certificate`.\n\nFeature: kein zusaetzlicher Feature-Schalter. Die aktuelle Aktivierung prueft weiterhin Control.\n\nKeine vollstaendige strukturierte Parameterbeschreibung im Bestand. Den bestehenden Terminalablauf und dessen Hilfe verwenden; keine Optionen erfinden.\n\nVoraussetzungen laut Registry:\n- `lib/control/helpers.sh`\n- `scripts/deploy_apache_certificate.sh`\n- `playbooks/pki/deploy_apache_certificate.yml`\n\nFür den Aufruf über `bin/control` zuerst `APACHE_CERTIFICATE_ROOT` auf das lokale Quellverzeichnis setzen. Beim direkten Playbook-Aufruf `apache_certificate_root` und `apache_certificate_year` mitgeben.\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `bin/control.d/apache-certificate.json`\n- `bin/control.d/apache-certificate.sh`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Replace Apache certificates",
      "description": "# Replace Apache certificates\n\nReplace Apache certificates\n\nRun: `bin/control apache-certificate [options]`.\n\nAliases: `apache-certificate`.\n\nAvailable without a separate feature switch. Control checks availability at runtime.\n\nNo structured parameter list is available. Use the existing terminal workflow and its help.\n\nRegistry prerequisites:\n- `lib/control/helpers.sh`\n- `scripts/deploy_apache_certificate.sh`\n- `playbooks/pki/deploy_apache_certificate.yml`\n\nWhen running through `bin/control`, set `APACHE_CERTIFICATE_ROOT` to the local source directory first. For a direct playbook run, set `apache_certificate_root` and `apache_certificate_year`.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `bin/control.d/apache-certificate.json`\n- `bin/control.d/apache-certificate.sh`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `bin/control.d/apache-certificate.json`
- `bin/control.d/apache-certificate.sh`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
