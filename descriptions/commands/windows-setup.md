# Prepare Windows HTTPS access

Run `bin/control windows-setup` for a preview, then `bin/control windows-setup --apply`.
The helper creates only a missing `group_vars/all_windows_systems/access.yml`, mode 0600.
It never opens password settings, changes an existing resolver, or contacts hosts.

Merge the neutral fields from `templates/windows/settings.example.yml` into the existing
private settings file. Enter `windows_access.user` and `.password` locally. Windows
inventory groups must include `all_windows_systems`; Linux keeps its existing SSH resolver.
HTTPS/5986, NTLM and certificate validation are defaults. Set a trusted CA bundle when
needed. Kerberos requires the corresponding controller dependencies and DNS setup.
After updating controller code, run `bin/setup-runtime` to install pywinrm before use.

<details>
<summary>Deutsch</summary>

# Windows-Zugang über HTTPS vorbereiten

`bin/control windows-setup` zeigt die Vorschau, `bin/control windows-setup --apply`
legt ausschließlich einen fehlenden Windows-Gruppenresolver mit Modus 0600 an.
Bestehende Resolver und Settings bleiben erhalten; der Helfer liest keine Passwortwerte.

Die neutralen Felder aus `templates/windows/settings.example.yml` in die vorhandenen
privaten Settings ergänzen und den Windows-Benutzer samt Passwort dort selbst eintragen.
Windows gehört in `all_windows_systems`. Die Linux-SSH-Auflösung bleibt bestehen.
Standard sind HTTPS/5986, NTLM und aktive Zertifikatsprüfung. Eine eigene CA bei Bedarf
über `ca_trust_path` angeben. Kerberos benötigt seine Controller-Abhängigkeiten und DNS.
Nach dem Codeupdate `bin/setup-runtime` für pywinrm ausführen. Kein Host wird hier verändert.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "windows-setup",
  "title": "Windows-Zugang über HTTPS vorbereiten",
  "documented": true,
  "fields": [
    {
      "id": "apply",
      "label": "apply",
      "description": "Create only the missing private Windows resolver.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--apply"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/windows-setup.json",
    "bin/control.d/windows-setup.sh",
    "templates/windows/access.yml.example",
    "templates/windows/settings.example.yml",
    "scripts/setup_windows.py"
  ],
  "source_hashes": {
    "bin/control.d/windows-setup.json": "ecb534a3939319fab5f34b2868056ca53e9ec3a5cd7b5f7095b61146ac7527f5",
    "bin/control.d/windows-setup.sh": "e836be47701c88a7ec783ac09c1886fc50234a89022cdfbfbb2102722fca3949",
    "templates/windows/access.yml.example": "1ac2489081cba24348ad5ba5050dd21da4d2ba255a42d118d9e40e9574bff264",
    "templates/windows/settings.example.yml": "5fb78cd68ace6c666611dafc1ce83c182de74b33a2b021df69112a7da4a7775d",
    "scripts/setup_windows.py": "57de0c8482ed5e1a1dc3cfcd7967ac07e0275a8e38f53b13da02e10878b48558"
  },
  "i18n": {
    "en": {
      "title": "Prepare Windows HTTPS access",
      "description": "# Prepare Windows HTTPS access\n\nRun `bin/control windows-setup` for a preview, then `bin/control windows-setup --apply`.\nThe helper creates only a missing `group_vars/all_windows_systems/access.yml`, mode 0600.\nIt never opens password settings, changes an existing resolver, or contacts hosts.\n\nMerge the neutral fields from `templates/windows/settings.example.yml` into the existing\nprivate settings file. Enter `windows_access.user` and `.password` locally. Windows\ninventory groups must include `all_windows_systems`; Linux keeps its existing SSH resolver.\nHTTPS/5986, NTLM and certificate validation are defaults. Set a trusted CA bundle when\nneeded. Kerberos requires the corresponding controller dependencies and DNS setup.\nAfter updating controller code, run `bin/setup-runtime` to install pywinrm before use.",
      "fields": {
        "apply": {
          "label": "apply",
          "description": "Create only the missing private Windows resolver."
        }
      }
    },
    "de": {
      "title": "Windows-Zugang über HTTPS vorbereiten",
      "description": "# Windows-Zugang über HTTPS vorbereiten\n\n`bin/control windows-setup` zeigt die Vorschau, `bin/control windows-setup --apply`\nlegt ausschließlich einen fehlenden Windows-Gruppenresolver mit Modus 0600 an.\nBestehende Resolver und Settings bleiben erhalten; der Helfer liest keine Passwortwerte.\n\nDie neutralen Felder aus `templates/windows/settings.example.yml` in die vorhandenen\nprivaten Settings ergänzen und den Windows-Benutzer samt Passwort dort selbst eintragen.\nWindows gehört in `all_windows_systems`. Die Linux-SSH-Auflösung bleibt bestehen.\nStandard sind HTTPS/5986, NTLM und aktive Zertifikatsprüfung. Eine eigene CA bei Bedarf\nüber `ca_trust_path` angeben. Kerberos benötigt seine Controller-Abhängigkeiten und DNS.\nNach dem Codeupdate `bin/setup-runtime` für pywinrm ausführen. Kein Host wird hier verändert.",
      "fields": {
        "apply": {
          "label": "apply",
          "description": "Create only the missing private Windows resolver."
        }
      }
    }
  }
}
```

</details>
