# Playbook playbooks/maintenance/mount_all.yaml

Playbook: `playbooks/maintenance/mount_all.yaml`.

Play and task names as written in the playbook:

- Refresh Mount Points
- Execute mount -a to remount filesystems defined in fstab
- Debug output (optional)

Run the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.

## Parameters

The listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.

## Sources and maintenance

- `playbooks/maintenance/mount_all.yaml`

Maintain this description and its source hashes together when the code changes. The database stores a cache.

<details>
<summary>Deutsch</summary>

# Playbook playbooks/maintenance/mount_all.yaml

Vorhandener Einstieg: `playbooks/maintenance/mount_all.yaml`.

Im Quelltext benannte Plays/Aufgaben:

- Refresh Mount Points
- Execute mount -a to remount filesystems defined in fstab
- Debug output (optional)

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

## Quellen und Pflege

- `playbooks/maintenance/mount_all.yaml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.

</details>

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/maintenance/mount_all.yaml",
  "title": "Playbook playbooks/maintenance/mount_all.yaml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/maintenance/mount_all.yaml"
  ],
  "source_hashes": {
    "playbooks/maintenance/mount_all.yaml": "c8d51609933fbb3e8c0f6cdde5085e83aee33e7e1f150d31c446d463e2564fb6"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/maintenance/mount_all.yaml",
      "description": "# Playbook playbooks/maintenance/mount_all.yaml\n\nVorhandener Einstieg: `playbooks/maintenance/mount_all.yaml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Refresh Mount Points\n- Execute mount -a to remount filesystems defined in fstab\n- Debug output (optional)\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/maintenance/mount_all.yaml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/maintenance/mount_all.yaml",
      "description": "# Playbook playbooks/maintenance/mount_all.yaml\n\nPlaybook: `playbooks/maintenance/mount_all.yaml`.\n\nPlay and task names as written in the playbook:\n\n- Refresh Mount Points\n- Execute mount -a to remount filesystems defined in fstab\n- Debug output (optional)\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/maintenance/mount_all.yaml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

</details>
