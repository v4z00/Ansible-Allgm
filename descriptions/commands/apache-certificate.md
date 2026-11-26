# Apache-Zertifikat austauschen

Als root auf dem Controller `APACHE_CERTIFICATE_ROOT` auf das Verzeichnis mit den Zertifikatssätzen setzen. `bin/control apache-certificate` zeigt die vollständigen Sätze nach Änderungszeit des Serverzertifikats an. Für einen bestimmten Satz kann `APACHE_CERTIFICATE_SOURCE_DIRECTORY` direkt auf dessen Ordner zeigen. Ein verschlüsselter Schlüssel erfordert beim ersten Entschlüsseln die Passphrase am Terminal.

Das Playbook `playbooks/pki/deploy_apache_certificate.yml` verwendet die Gruppe `checkmk_webserver_hosts`. Die folgenden Ansible-Variablen können im privaten Inventory stehen. Für die Auswahl im Shell-Aufruf setzt du abweichende Dateinamen vor dem Aufruf in der gleichnamigen Umgebungsvariablen in Großbuchstaben.

| Datei | Variable | Standard |
| --- | --- | --- |
| Serverzertifikat | `apache_certificate_filename` | `certificate.crt` |
| PEM-Zertifikatskette | `apache_intermediate_filename` | `intermediate1.crt` |
| Verschlüsselter Quellschlüssel (Shell) | `apache_encrypted_key_filename` | `wildcard_example_org.key` |
| Entschlüsselter Quellschlüssel | `apache_private_key_filename` | `wildcard_example_org_unencrypted.key` |
| Zertifikat mit Kette auf dem Webserver | `apache_certificate_target_filename` | `cert.cert` |
| Privater Schlüssel auf dem Webserver | `apache_private_key_target_filename` | `key.key` |

Der Quellordner ist `apache_certificate_source_directory`, standardmäßig `apache_certificate_root/apache_certificate_year`. Einzelne absolute Quellpfade heißen `apache_certificate_source`, `apache_intermediate_source` und `apache_private_key_source`. Die Shell kennt zusätzlich `APACHE_ENCRYPTED_KEY_SOURCE`. Das Zielverzeichnis `apache_certificate_directory` ist anfangs `/cert`. Die absoluten Einzelziele `apache_certificate_target` und `apache_private_key_target` haben Vorrang. Verwende eindeutige Pfade ohne Verknüpfungen. Die Zielverzeichnisse dürfen für fremde Konten nicht beschreibbar sein.

Zum Prüfen des ausgewählten Satzes und der geplanten Änderungen:

```bash
APACHE_CERTIFICATE_ROOT=/srv/pki bin/control apache-certificate --check --limit web
```

`--limit web` auf das eigene Inventory anpassen. Der Shell-Einstieg bereitet den entschlüsselten Schlüssel mit Modus `0600` auch für die Vorschau vor. Auf dem Ziel prüft Ansible Zertifikat, Kette und zugehörigen Schlüssel. Beim Austausch sichert es vorhandene geänderte Dateien unter `.<Dateiname>.previous-*` mit Modus `0600`. Nach erfolgreichem `apache2ctl configtest` startet Apache neu. Schlägt die Prüfung oder der Neustart fehl, setzt der Helfer die Dateien auf den vorigen Stand. Bei fehlgeschlagenem Neustart mit vorhandenem altem Paar versucht er anschließend, Apache mit diesem Paar wieder zu starten.

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
    "bin/control.d/apache-certificate.sh",
    "playbooks/pki/deploy_apache_certificate.yml",
    "scripts/deploy_apache_certificate.sh",
    "scripts/apache_certificate_files.py"
  ],
  "source_hashes": {
    "bin/control.d/apache-certificate.json": "4751636b59997d25283ef316dc6174ed7526550b80799910e67b569e1b44bcaf",
    "bin/control.d/apache-certificate.sh": "ff5df678a25307b590e22a037358cb6294e1a57a6cff219580d67664f94aa397",
    "playbooks/pki/deploy_apache_certificate.yml": "4f7d78bcfac9d8d1b70c875941645b57943a6b4dd6a3424171086e3df88137a9",
    "scripts/deploy_apache_certificate.sh": "e94115ec8e07b758a6a6b4b72cd9fac5ce5c6c308b9b8f98f9e1bcc360e17b6f",
    "scripts/apache_certificate_files.py": "7e7c684282c654f0531d17617103cf33b421b4e64326d70ff1ac618ea53eb8b6"
  },
  "i18n": {
    "de": {
      "title": "Apache-Zertifikate kontrolliert austauschen",
      "description": "# Apache-Zertifikat austauschen\n\nAls root auf dem Controller `APACHE_CERTIFICATE_ROOT` auf das Verzeichnis mit den Zertifikatssätzen setzen. `bin/control apache-certificate` zeigt die vollständigen Sätze nach Änderungszeit des Serverzertifikats an. Für einen bestimmten Satz kann `APACHE_CERTIFICATE_SOURCE_DIRECTORY` direkt auf dessen Ordner zeigen. Ein verschlüsselter Schlüssel erfordert beim ersten Entschlüsseln die Passphrase am Terminal.\n\nDas Playbook `playbooks/pki/deploy_apache_certificate.yml` verwendet die Gruppe `checkmk_webserver_hosts`. Die folgenden Ansible-Variablen können im privaten Inventory stehen. Für die Auswahl im Shell-Aufruf setzt du abweichende Dateinamen vor dem Aufruf in der gleichnamigen Umgebungsvariablen in Großbuchstaben.\n\n| Datei | Variable | Standard |\n| --- | --- | --- |\n| Serverzertifikat | `apache_certificate_filename` | `certificate.crt` |\n| PEM-Zertifikatskette | `apache_intermediate_filename` | `intermediate1.crt` |\n| Verschlüsselter Quellschlüssel (Shell) | `apache_encrypted_key_filename` | `wildcard_example_org.key` |\n| Entschlüsselter Quellschlüssel | `apache_private_key_filename` | `wildcard_example_org_unencrypted.key` |\n| Zertifikat mit Kette auf dem Webserver | `apache_certificate_target_filename` | `cert.cert` |\n| Privater Schlüssel auf dem Webserver | `apache_private_key_target_filename` | `key.key` |\n\nDer Quellordner ist `apache_certificate_source_directory`, standardmäßig `apache_certificate_root/apache_certificate_year`. Einzelne absolute Quellpfade heißen `apache_certificate_source`, `apache_intermediate_source` und `apache_private_key_source`. Die Shell kennt zusätzlich `APACHE_ENCRYPTED_KEY_SOURCE`. Das Zielverzeichnis `apache_certificate_directory` ist anfangs `/cert`. Die absoluten Einzelziele `apache_certificate_target` und `apache_private_key_target` haben Vorrang. Verwende eindeutige Pfade ohne Verknüpfungen. Die Zielverzeichnisse dürfen für fremde Konten nicht beschreibbar sein.\n\nZum Prüfen des ausgewählten Satzes und der geplanten Änderungen:\n\n```bash\nAPACHE_CERTIFICATE_ROOT=/srv/pki bin/control apache-certificate --check --limit web\n```\n\n`--limit web` auf das eigene Inventory anpassen. Der Shell-Einstieg bereitet den entschlüsselten Schlüssel mit Modus `0600` auch für die Vorschau vor. Auf dem Ziel prüft Ansible Zertifikat, Kette und zugehörigen Schlüssel. Beim Austausch sichert es vorhandene geänderte Dateien unter `.<Dateiname>.previous-*` mit Modus `0600`. Nach erfolgreichem `apache2ctl configtest` startet Apache neu. Schlägt die Prüfung oder der Neustart fehl, setzt der Helfer die Dateien auf den vorigen Stand. Bei fehlgeschlagenem Neustart mit vorhandenem altem Paar versucht er anschließend, Apache mit diesem Paar wieder zu starten.",
      "fields": {}
    },
    "en": {
      "title": "Replace Apache certificates",
      "description": "# Replace an Apache certificate\n\nAs root on the controller, set `APACHE_CERTIFICATE_ROOT` to the directory containing your certificate sets. `bin/control apache-certificate` lists complete sets, newest leaf certificate first. Set `APACHE_CERTIFICATE_SOURCE_DIRECTORY` to select a set directly. An encrypted source key requires its passphrase at the terminal the first time it is decrypted.\n\nThe playbook `playbooks/pki/deploy_apache_certificate.yml` runs on the `checkmk_webserver_hosts` group. Set the following Ansible variables in your private inventory. For source selection in the shell wrapper, set the corresponding uppercase environment variables before running it.\n\n| File | Variable | Default |\n| --- | --- | --- |\n| Leaf certificate | `apache_certificate_filename` | `certificate.crt` |\n| PEM certificate chain | `apache_intermediate_filename` | `intermediate1.crt` |\n| Encrypted source key (shell) | `apache_encrypted_key_filename` | `wildcard_example_org.key` |\n| Decrypted source key | `apache_private_key_filename` | `wildcard_example_org_unencrypted.key` |\n| Certificate and chain on the server | `apache_certificate_target_filename` | `cert.cert` |\n| Private key on the server | `apache_private_key_target_filename` | `key.key` |\n\nThe source directory is `apache_certificate_source_directory`, defaulting to `apache_certificate_root/apache_certificate_year`. Individual absolute source paths are `apache_certificate_source`, `apache_intermediate_source` and `apache_private_key_source`. The wrapper also supports `APACHE_ENCRYPTED_KEY_SOURCE`. The target directory `apache_certificate_directory` defaults to `/cert`. Individual absolute paths `apache_certificate_target` and `apache_private_key_target` take precedence. Use distinct paths without links. Other users must not have write access to destination directories.\n\nPreview the selected set and the proposed changes:\n\n```bash\nAPACHE_CERTIFICATE_ROOT=/srv/pki bin/control apache-certificate --check --limit web\n```\n\nAdjust `--limit web` to your inventory. The wrapper prepares a mode-`0600` decrypted key on the controller even for preview. On the target, Ansible checks the certificate, chain and matching key. When replacing files it saves previous versions as mode-`0600` files named `.<filename>.previous-*`. Apache restarts after `apache2ctl configtest` succeeds. On a failed test or restart the helper restores the previous files. If a restart failed and the old pair exists, it also attempts a restart using the restored files.",
      "fields": {}
    }
  }
}
```
