# Playbook playbooks/bootstrap/root_access.yml

Playbook: `playbooks/bootstrap/root_access.yml`.

Play and task names as written in the playbook:

- Prepare root access
- Require configured bootstrap profiles
- Require the selected bootstrap profile
- Check the controller key
- Require the controller key
- Validate selected bootstrap profiles
- Prepare root key access or individual bootstrap credentials
- Establish root access with sudo or su
- Test the initial connection
- Test sudo access to root
- Test su access to root
- Select a working privilege escalation method
- Stop if privilege escalation to root fails
- Configure root key access
- Create the root SSH directory
- Install the controller key for root
- Enable SSH key authentication for root
- Validate the SSH configuration
- Reload SSH
- Report the privilege escalation method
- Confirm existing root key access
- Test the root key connection with Ansible
- Report existing root key access

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/bootstrap/root_access.yml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/bootstrap/root_access.yml

Vorhandener Einstieg: `playbooks/bootstrap/root_access.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Prepare root access
- Require configured bootstrap profiles
- Require the selected bootstrap profile
- Check the controller key
- Require the controller key
- Validate selected bootstrap profiles
- Prepare root key access or individual bootstrap credentials
- Establish root access with sudo or su
- Test the initial connection
- Test sudo access to root
- Test su access to root
- Select a working privilege escalation method
- Stop if privilege escalation to root fails
- Configure root key access
- Create the root SSH directory
- Install the controller key for root
- Enable SSH key authentication for root
- Validate the SSH configuration
- Reload SSH
- Report the privilege escalation method
- Confirm existing root key access
- Test the root key connection with Ansible
- Report existing root key access

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/bootstrap/root_access.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/bootstrap/root_access.yml",
  "title": "Playbook playbooks/bootstrap/root_access.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/bootstrap/root_access.yml"
  ],
  "source_hashes": {
    "playbooks/bootstrap/root_access.yml": "2849bfd465ea29572683a29bc70404d43f28ece511b70498de3cea98fdbe435a"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/bootstrap/root_access.yml",
      "description": "# Playbook playbooks/bootstrap/root_access.yml\n\nVorhandener Einstieg: `playbooks/bootstrap/root_access.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Prepare root access\n- Require configured bootstrap profiles\n- Require the selected bootstrap profile\n- Check the controller key\n- Require the controller key\n- Validate selected bootstrap profiles\n- Prepare root key access or individual bootstrap credentials\n- Establish root access with sudo or su\n- Test the initial connection\n- Test sudo access to root\n- Test su access to root\n- Select a working privilege escalation method\n- Stop if privilege escalation to root fails\n- Configure root key access\n- Create the root SSH directory\n- Install the controller key for root\n- Enable SSH key authentication for root\n- Validate the SSH configuration\n- Reload SSH\n- Report the privilege escalation method\n- Confirm existing root key access\n- Test the root key connection with Ansible\n- Report existing root key access\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/bootstrap/root_access.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/bootstrap/root_access.yml",
      "description": "# Playbook playbooks/bootstrap/root_access.yml\n\nPlaybook: `playbooks/bootstrap/root_access.yml`.\n\nPlay and task names as written in the playbook:\n\n- Prepare root access\n- Require configured bootstrap profiles\n- Require the selected bootstrap profile\n- Check the controller key\n- Require the controller key\n- Validate selected bootstrap profiles\n- Prepare root key access or individual bootstrap credentials\n- Establish root access with sudo or su\n- Test the initial connection\n- Test sudo access to root\n- Test su access to root\n- Select a working privilege escalation method\n- Stop if privilege escalation to root fails\n- Configure root key access\n- Create the root SSH directory\n- Install the controller key for root\n- Enable SSH key authentication for root\n- Validate the SSH configuration\n- Reload SSH\n- Report the privilege escalation method\n- Confirm existing root key access\n- Test the root key connection with Ansible\n- Report existing root key access\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/bootstrap/root_access.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
