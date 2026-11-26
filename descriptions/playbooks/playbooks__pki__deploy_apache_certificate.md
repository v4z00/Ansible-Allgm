# Playbook playbooks/pki/deploy_apache_certificate.yml

Vorhandener Einstieg: `playbooks/pki/deploy_apache_certificate.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Deploy the wildcard certificate to Apache web servers
- Check source files on the controller
- Show the selected certificate path
- Require all certificate source files
- Validate the decrypted private key
- Get the public key fingerprint from the private key
- Get the public key fingerprint from the certificate
- Require the certificate and private key to match
- Create the Apache certificate directory
- Deploy the certificate and intermediate chain
- Deploy the decrypted private key
- Validate the Apache configuration
- Restart Apache

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
    "playbooks/pki/deploy_apache_certificate.yml": "4f7d78bcfac9d8d1b70c875941645b57943a6b4dd6a3424171086e3df88137a9"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/pki/deploy_apache_certificate.yml",
      "description": "# Playbook playbooks/pki/deploy_apache_certificate.yml\n\nVorhandener Einstieg: `playbooks/pki/deploy_apache_certificate.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Deploy the wildcard certificate to Apache web servers\n- Check source files on the controller\n- Show the selected certificate path\n- Require all certificate source files\n- Validate the decrypted private key\n- Get the public key fingerprint from the private key\n- Get the public key fingerprint from the certificate\n- Require the certificate and private key to match\n- Create the Apache certificate directory\n- Deploy the certificate and intermediate chain\n- Deploy the decrypted private key\n- Validate the Apache configuration\n- Restart Apache\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/pki/deploy_apache_certificate.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/pki/deploy_apache_certificate.yml",
      "description": "# Playbook playbooks/pki/deploy_apache_certificate.yml\n\nPlaybook: `playbooks/pki/deploy_apache_certificate.yml`.\n\nPlay and task names as written in the playbook:\n\n- Deploy the wildcard certificate to Apache web servers\n- Check source files on the controller\n- Show the selected certificate path\n- Require all certificate source files\n- Validate the decrypted private key\n- Get the public key fingerprint from the private key\n- Get the public key fingerprint from the certificate\n- Require the certificate and private key to match\n- Create the Apache certificate directory\n- Deploy the certificate and intermediate chain\n- Deploy the decrypted private key\n- Validate the Apache configuration\n- Restart Apache\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/pki/deploy_apache_certificate.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/pki/deploy_apache_certificate.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
