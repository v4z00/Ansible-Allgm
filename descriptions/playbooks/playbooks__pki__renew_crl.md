# Playbook playbooks/pki/renew_crl.yml

Vorhandener Einstieg: `playbooks/pki/renew_crl.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Step 1: Renew and Convert Root CRL (on the controller)
- Require a locally configured CA password
- Generate new CRL (PEM format)
- Convert CRL to DER format (Required for Windows!)
- Display generation status
- Step 2: Deploy CRL to Docker Server
- Ensure destination directory exists
- Copy new Root CRL (DER) with permissions 0774
- Restart Webserver Container

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/pki/renew_crl.yml",
  "title": "Playbook playbooks/pki/renew_crl.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/pki/renew_crl.yml"
  ],
  "source_hashes": {
    "playbooks/pki/renew_crl.yml": "8a6c90060a7f40717a71af79c7e89805fca2d59400cc6bddcc76bd02173d34fa"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/pki/renew_crl.yml",
      "description": "# Playbook playbooks/pki/renew_crl.yml\n\nVorhandener Einstieg: `playbooks/pki/renew_crl.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Step 1: Renew and Convert Root CRL (on the controller)\n- Require a locally configured CA password\n- Generate new CRL (PEM format)\n- Convert CRL to DER format (Required for Windows!)\n- Display generation status\n- Step 2: Deploy CRL to Docker Server\n- Ensure destination directory exists\n- Copy new Root CRL (DER) with permissions 0774\n- Restart Webserver Container\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/pki/renew_crl.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/pki/renew_crl.yml",
      "description": "# Playbook playbooks/pki/renew_crl.yml\n\nPlaybook: `playbooks/pki/renew_crl.yml`.\n\nPlay and task names as written in the playbook:\n\n- Step 1: Renew and Convert Root CRL (on the controller)\n- Require a locally configured CA password\n- Generate new CRL (PEM format)\n- Convert CRL to DER format (Required for Windows!)\n- Display generation status\n- Step 2: Deploy CRL to Docker Server\n- Ensure destination directory exists\n- Copy new Root CRL (DER) with permissions 0774\n- Restart Webserver Container\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/pki/renew_crl.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/pki/renew_crl.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
