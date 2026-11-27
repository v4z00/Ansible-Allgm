# Check Windows remoting and identity

Run `bin/control windows-check --limit example-windows-host`. An explicit limit is required.
The read-only playbook checks authenticated WinRM HTTPS and returns only hostname,
OS/PowerShell versions, domain membership, DC role, effective execution policy and the
number of machine-store code-signing certificates with private keys. It does not export
certificate keys, passwords, settings contents or task arguments.

For AllSigned, enable the configured [central signing pipeline](../configurations/windows-code-signing.md) before library deployment. Windows policy is not disabled. This check changes no services, tasks, firewall or GPOs.

<details>
<summary>Deutsch</summary>

# Windows-Verbindung und Identität prüfen

`bin/control windows-check --limit example-windows-host` prüft den bestehenden
WinRM-HTTPS-Zugang lesend. Die ausdrückliche Zielauswahl ist Pflicht. Zurück kommen
nur Rechner-/OS-/PowerShell-Daten, Domänenzuordnung, DC-Rolle, Ausführungsrichtlinie
und die Anzahl verfügbarer Codesignatur-Zertifikate im Maschinenstore.
Passwörter, private Schlüssel, Konfigurationsinhalte und Aufgabenargumente werden nicht exportiert.

Bei AllSigned zuerst die [zentrale Signierstrecke](../configurations/windows-code-signing.md) konfigurieren. Die Windows-Richtlinie wird nicht abgeschaltet. Der Check verändert keine Dienste, Aufgaben,
Firewallregeln oder GPOs.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "windows-check",
  "title": "Windows-Verbindung und Identität prüfen",
  "documented": true,
  "fields": [
    {
      "id": "limit",
      "label": "limit",
      "description": "Explicit Windows inventory host/group.",
      "type": "string",
      "required": true,
      "sensitive": false,
      "binding": {
        "kind": "option",
        "name": "--limit"
      }
    }
  ],
  "constraints": [],
  "sources": [
    "bin/control.d/windows-check.json",
    "bin/control.d/windows-check.sh",
    "playbooks/windows/check.yml"
  ],
  "source_hashes": {
    "bin/control.d/windows-check.json": "bda7e4cc2266c2d5faddc366a29050469cbbbdb34c3cd73eae71b09296e6aea7",
    "bin/control.d/windows-check.sh": "6ee135270ec378cfad418d3eba806d41a9df322be10b8ef48cc2a7e2375e3aae",
    "playbooks/windows/check.yml": "0850b7e1c9fe01c8166186e5ba42d1372c34b32fa8cd7001cbe805da42a3056b"
  },
  "i18n": {
    "en": {
      "title": "Check Windows remoting and identity",
      "description": "# Check Windows remoting and identity\n\nRun `bin/control windows-check --limit example-windows-host`. An explicit limit is required.\nThe read-only playbook checks authenticated WinRM HTTPS and returns only hostname,\nOS/PowerShell versions, domain membership, DC role, effective execution policy and the\nnumber of machine-store code-signing certificates with private keys. It does not export\ncertificate keys, passwords, settings contents or task arguments.\n\nFor AllSigned, enable the configured [central signing pipeline](../configurations/windows-code-signing.md) before library deployment. Windows policy is not disabled. This check changes no services, tasks, firewall or GPOs.",
      "fields": {
        "limit": {
          "label": "limit",
          "description": "Explicit Windows inventory host/group."
        }
      }
    },
    "de": {
      "title": "Windows-Verbindung und Identität prüfen",
      "description": "# Windows-Verbindung und Identität prüfen\n\n`bin/control windows-check --limit example-windows-host` prüft den bestehenden\nWinRM-HTTPS-Zugang lesend. Die ausdrückliche Zielauswahl ist Pflicht. Zurück kommen\nnur Rechner-/OS-/PowerShell-Daten, Domänenzuordnung, DC-Rolle, Ausführungsrichtlinie\nund die Anzahl verfügbarer Codesignatur-Zertifikate im Maschinenstore.\nPasswörter, private Schlüssel, Konfigurationsinhalte und Aufgabenargumente werden nicht exportiert.\n\nBei AllSigned zuerst die [zentrale Signierstrecke](../configurations/windows-code-signing.md) konfigurieren. Die Windows-Richtlinie wird nicht abgeschaltet. Der Check verändert keine Dienste, Aufgaben,\nFirewallregeln oder GPOs.",
      "fields": {
        "limit": {
          "label": "limit",
          "description": "Explicit Windows inventory host/group."
        }
      }
    }
  }
}
```

</details>
