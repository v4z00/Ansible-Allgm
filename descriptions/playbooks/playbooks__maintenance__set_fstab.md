# Playbook playbooks/maintenance/set_fstab.yaml

Playbook: `playbooks/maintenance/set_fstab.yaml`.

Play and task names as written in the playbook:

- Manage centrally defined mounts
- Find the storage definition for this host
- Load the storage definition for this host
- Set the managed mounts
- Require unique mount names and mount points
- Validate mount definitions
- Identify required mount types
- Install the CIFS client
- Install the NFS client
- Install bindfs
- Detect active mount points
- Create mount points
- Write fstab entries and optionally mount filesystems
- Manage the optional mount health check cron job
- Manage the optional Kerberos refresh cron job
- Run fstab handlers now
- Validate fstab
- Reload systemd after fstab changes

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/maintenance/set_fstab.yaml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/maintenance/set_fstab.yaml

Vorhandener Einstieg: `playbooks/maintenance/set_fstab.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Manage centrally defined mounts
- Find the storage definition for this host
- Load the storage definition for this host
- Set the managed mounts
- Require unique mount names and mount points
- Validate mount definitions
- Identify required mount types
- Install the CIFS client
- Install the NFS client
- Install bindfs
- Detect active mount points
- Create mount points
- Write fstab entries and optionally mount filesystems
- Manage the optional mount health check cron job
- Manage the optional Kerberos refresh cron job
- Run fstab handlers now
- Validate fstab
- Reload systemd after fstab changes

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/maintenance/set_fstab.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/set_fstab.yaml",
  "title": "Playbook playbooks/maintenance/set_fstab.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/set_fstab.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/set_fstab.yaml": "51479cf10e35e639396518456487e04b15f41e01ee9b1e19b3b032dc0eab6bf1"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/maintenance/set_fstab.yaml",
      "description": "# Playbook playbooks/maintenance/set_fstab.yaml\n\nVorhandener Einstieg: `playbooks/maintenance/set_fstab.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Manage centrally defined mounts\n- Find the storage definition for this host\n- Load the storage definition for this host\n- Set the managed mounts\n- Require unique mount names and mount points\n- Validate mount definitions\n- Identify required mount types\n- Install the CIFS client\n- Install the NFS client\n- Install bindfs\n- Detect active mount points\n- Create mount points\n- Write fstab entries and optionally mount filesystems\n- Manage the optional mount health check cron job\n- Manage the optional Kerberos refresh cron job\n- Run fstab handlers now\n- Validate fstab\n- Reload systemd after fstab changes\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/maintenance/set_fstab.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/maintenance/set_fstab.yaml",
      "description": "# Playbook playbooks/maintenance/set_fstab.yaml\n\nPlaybook: `playbooks/maintenance/set_fstab.yaml`.\n\nPlay and task names as written in the playbook:\n\n- Manage centrally defined mounts\n- Find the storage definition for this host\n- Load the storage definition for this host\n- Set the managed mounts\n- Require unique mount names and mount points\n- Validate mount definitions\n- Identify required mount types\n- Install the CIFS client\n- Install the NFS client\n- Install bindfs\n- Detect active mount points\n- Create mount points\n- Write fstab entries and optionally mount filesystems\n- Manage the optional mount health check cron job\n- Manage the optional Kerberos refresh cron job\n- Run fstab handlers now\n- Validate fstab\n- Reload systemd after fstab changes\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/maintenance/set_fstab.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
