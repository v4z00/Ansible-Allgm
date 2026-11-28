# Prepare Windows HTTPS access

Run `bin/control windows-setup` for a preview and add `--apply` to create the
missing Windows-group resolver (0600). Use `--upgrade-known-resolver` to preview
an upgrade of a byte-identical previous resolver. With `--apply`, the helper
backs up that resolver under `x/backups/windows-access` before replacing it.
Custom resolvers need a manual review of the differences.

Keep `windows_access.user` and `windows_access.password` together in the existing
private `group_vars/all/secrets.yml`. The helper uses only the public resolver
template. Optional connection settings are in `templates/windows/settings.example.yml`.
Windows inventory hosts belong to `all_windows_systems`. Use a DNS name matching
the server certificate and Kerberos service principal. Set
`windows_connection.dns_suffix` to qualify short inventory names for WinRM.
Set a complete `inventory_dns_name` in static inventory or in the inventory
generator's `host_overrides` to replace the derived name.
`windows_host_connection.<host>.dns_name` takes precedence and an empty name uses
`ansible_host`. These settings resolve the WinRM endpoint and leave the inventory
address available for the other integrations.

With `features.kerberos: true`, WinRM requires Kerberos over HTTPS/5986. Set a UPN
such as `automation@EXAMPLE.INVALID`. Managed kinit obtains a ticket with the
configured account. Manual kinit uses an existing ticket cache. Prepare the
Debian controller with `bin/setup-runtime --windows-kerberos` and configure DNS,
time synchronization, the realm and CA trust. Without the Kerberos feature, the
resolver defaults to NTLM unless Kerberos is selected explicitly.
Run `bin/control windows-check --limit HOST` to verify the connection.

<details>
<summary>Deutsch</summary>

# Windows-Zugang über HTTPS vorbereiten

`bin/control windows-setup` zeigt die Vorschau. Mit `--apply` wird der fehlende
Windows-Gruppenresolver mit Modus 0600 angelegt. `--upgrade-known-resolver` zeigt
die Aktualisierung eines exakt bekannten Altstands. Mit `--apply` sichert der
Helfer diesen Resolver unter `x/backups/windows-access` und aktualisiert ihn.
Bei einem selbst bearbeiteten Resolver die Unterschiede manuell prüfen.

`windows_access.user` und `windows_access.password` bleiben zusammen in der
bestehenden privaten `group_vars/all/secrets.yml`. Der Helfer verwendet die
öffentliche Resolver-Vorlage. Optionale Verbindungseinstellungen stehen in
`templates/windows/settings.example.yml`. Windows-Ziele gehören in
`all_windows_systems`. Der DNS-Name muss zu Zertifikat und Kerberos-SPN passen.
`windows_connection.dns_suffix` ergänzt kurze Inventarnamen für WinRM.
Ein vollständiges `inventory_dns_name` aus dem statischen Inventar oder
aus `host_overrides` im Inventar-Update ersetzt den abgeleiteten Namen.
`windows_host_connection.<host>.dns_name` hat Vorrang. Bei einem ausdrücklich
leeren Wert verwendet WinRM `ansible_host`. Die Inventar-IP bleibt für andere
Integrationen verfügbar.

Bei `features.kerberos: true` ist Kerberos über HTTPS/5986 verpflichtend. Den
Benutzer als UPN eintragen, beispielsweise `automation@EXAMPLE.INVALID`.
Managed kinit bezieht das Ticket mit dem konfigurierten Konto. Manual kinit
verwendet einen vorhandenen Ticketcache. Auf Debian
`bin/setup-runtime --windows-kerberos` ausführen. DNS, Zeitsynchronisation, Realm
und CA-Vertrauen müssen passen. Bei ausgeschaltetem Kerberos-Feature gilt NTLM
als Vorgabe, sofern nicht ausdrücklich Kerberos gewählt wird.
`bin/control windows-check --limit HOST` prüft die Verbindung.

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
      "description": "Create a missing resolver or apply an explicitly selected upgrade.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--apply"
      }
    },
    {
      "id": "upgrade_known_resolver",
      "label": "Upgrade the known resolver",
      "description": "Preview and optionally upgrade a byte-identical old resolver with backup.",
      "type": "boolean",
      "required": false,
      "sensitive": false,
      "binding": {
        "kind": "flag",
        "name": "--upgrade-known-resolver"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/windows-setup.json",
    "bin/control.d/windows-setup.sh",
    "bin/setup-runtime",
    "scripts/setup_windows.py",
    "templates/windows/access.yml.example",
    "templates/windows/requirements-kerberos.txt",
    "templates/windows/secrets.yml.example",
    "templates/windows/settings.example.yml"
  ],
  "source_hashes": {
    "bin/control.d/windows-setup.json": "cb3df6fe981ebf693ecbe77a6e47d1f3b778bdbc4b49dae1f854e9736a56235d",
    "bin/control.d/windows-setup.sh": "e836be47701c88a7ec783ac09c1886fc50234a89022cdfbfbb2102722fca3949",
    "bin/setup-runtime": "24f88f27c7103dc52203585a16f5223540a8ceddb270c7f27914f14e43ca902c",
    "scripts/setup_windows.py": "78480395f32b0ef7d2c445f50b6d192fd292138e8a8d21f4e2c81e2c88e205a2",
    "templates/windows/access.yml.example": "0e9db5160d2796c76ce605d70b87e3296b72f51f66c6f99d14d60cb9591fb823",
    "templates/windows/requirements-kerberos.txt": "c4dd61709f3d0676371b1d9e09b688fe993e598a522d07acacf2a3681bd68171",
    "templates/windows/secrets.yml.example": "db8877b6d3ae05c1960d336cc4de380f1811f400a4d58453fa1d6f257f3b3478",
    "templates/windows/settings.example.yml": "b6c034e14124ac5cebabd7744adfc2d51d36c6819f557a8ff0941e140a2ef262"
  },
  "i18n": {
    "en": {
      "title": "Prepare Windows HTTPS access",
      "description": "# Prepare Windows HTTPS access\n\nRun `bin/control windows-setup` for a preview and add `--apply` to create the\nmissing Windows-group resolver (0600). Use `--upgrade-known-resolver` to preview\nan upgrade of a byte-identical previous resolver. With `--apply`, the helper\nbacks up that resolver under `x/backups/windows-access` before replacing it.\nCustom resolvers need a manual review of the differences.\n\nKeep `windows_access.user` and `windows_access.password` together in the existing\nprivate `group_vars/all/secrets.yml`. The helper uses only the public resolver\ntemplate. Optional connection settings are in `templates/windows/settings.example.yml`.\nWindows inventory hosts belong to `all_windows_systems`. Use a DNS name matching\nthe server certificate and Kerberos service principal.\n\nWith `features.kerberos: true`, WinRM requires Kerberos over HTTPS/5986. Set a UPN\nsuch as `automation@EXAMPLE.INVALID`. Managed kinit obtains a ticket with the\nconfigured account. Manual kinit uses an existing ticket cache. Prepare the\nDebian controller with `bin/setup-runtime --windows-kerberos` and configure DNS,\ntime synchronization, the realm and CA trust. Without the Kerberos feature, the\nresolver defaults to NTLM unless Kerberos is selected explicitly.\nRun `bin/control windows-check --limit HOST` to verify the connection.\n",
      "fields": {
        "apply": {
          "label": "apply",
          "description": "Create a missing resolver or apply an explicitly selected upgrade."
        },
        "upgrade_known_resolver": {
          "label": "Upgrade the known resolver",
          "description": "Preview and optionally upgrade a byte-identical old resolver with backup."
        }
      }
    },
    "de": {
      "title": "Windows-Zugang über HTTPS vorbereiten",
      "description": "# Windows-Zugang über HTTPS vorbereiten\n\n`bin/control windows-setup` zeigt die Vorschau. Mit `--apply` wird der fehlende\nWindows-Gruppenresolver mit Modus 0600 angelegt. `--upgrade-known-resolver` zeigt\ndie Aktualisierung eines exakt bekannten Altstands. Mit `--apply` sichert der\nHelfer diesen Resolver unter `x/backups/windows-access` und aktualisiert ihn.\nBei einem selbst bearbeiteten Resolver die Unterschiede manuell prüfen.\n\n`windows_access.user` und `windows_access.password` bleiben zusammen in der\nbestehenden privaten `group_vars/all/secrets.yml`. Der Helfer verwendet die\nöffentliche Resolver-Vorlage. Optionale Verbindungseinstellungen stehen in\n`templates/windows/settings.example.yml`. Windows-Ziele gehören in\n`all_windows_systems`. Der DNS-Name muss zu Zertifikat und Kerberos-SPN passen.\n\nBei `features.kerberos: true` ist Kerberos über HTTPS/5986 verpflichtend. Den\nBenutzer als UPN eintragen, beispielsweise `automation@EXAMPLE.INVALID`.\nManaged kinit bezieht das Ticket mit dem konfigurierten Konto. Manual kinit\nverwendet einen vorhandenen Ticketcache. Auf Debian\n`bin/setup-runtime --windows-kerberos` ausführen. DNS, Zeitsynchronisation, Realm\nund CA-Vertrauen müssen passen. Bei ausgeschaltetem Kerberos-Feature gilt NTLM\nals Vorgabe, sofern nicht ausdrücklich Kerberos gewählt wird.\n`bin/control windows-check --limit HOST` prüft die Verbindung.\n",
      "fields": {
        "apply": {
          "label": "apply",
          "description": "Fehlenden Resolver anlegen oder ausdrücklich gewählte Aktualisierung anwenden."
        },
        "upgrade_known_resolver": {
          "label": "Bekannten Resolver aktualisieren",
          "description": "Unveränderten Altstand prüfen und optional mit Sicherung aktualisieren."
        }
      }
    }
  }
}
```

</details>
