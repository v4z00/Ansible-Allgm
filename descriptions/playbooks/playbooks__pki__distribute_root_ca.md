# Playbook playbooks/pki/distribute_root_ca.yml

Vorhandener Einstieg: `playbooks/pki/distribute_root_ca.yml`.

Im Quelltext benannte Plays/Aufgaben:

- Distribute the internal root CA
- Require an explicit target
- Configure the local CA source
- Copy the CA certificate
- Update the trust store

Ausfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.


## Parameter und maschinenlesbarer Vertrag

Die Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind
als solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.
Vertrauliche Werte werden nicht dokumentiert.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/pki/distribute_root_ca.yml",
  "title": "Playbook playbooks/pki/distribute_root_ca.yml",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/pki/distribute_root_ca.yml"
  ],
  "source_hashes": {
    "playbooks/pki/distribute_root_ca.yml": "debe0193430719d2b622e0eaedda0935de2699030f3f2ebe3b40989fd835d00e"
  },
  "i18n": {
    "de": {
      "title": "Playbook playbooks/pki/distribute_root_ca.yml",
      "description": "# Playbook playbooks/pki/distribute_root_ca.yml\n\nVorhandener Einstieg: `playbooks/pki/distribute_root_ca.yml`.\n\nIm Quelltext benannte Plays/Aufgaben:\n\n- Distribute the internal root CA\n- Require an explicit target\n- Configure the local CA source\n- Copy the CA certificate\n- Update the trust store\n\nAusfuehrung bevorzugt ueber den passenden Control-Befehl. Die Datei allein beschreibt nicht alle effektiven Variablen: Rollen, Inventar und lokale Standortkonfiguration wirken weiterhin. Keine allgemeinen --check-/Limit-Garantien daraus ableiten.\n\n\n## Parameter und maschinenlesbarer Vertrag\n\nDie Angaben stammen aus den aufgefuehrten Quellen. Fehlende Erklaerungen sind\nals solche markiert. Defaults sind Hinweise und werden nicht automatisch gesetzt.\nVertrauliche Werte werden nicht dokumentiert.\n\n## Quellen und Pflege\n\n- `playbooks/pki/distribute_root_ca.yml`\n\nDiese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen\nBeschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.",
      "fields": {}
    },
    "en": {
      "title": "Playbook playbooks/pki/distribute_root_ca.yml",
      "description": "# Playbook playbooks/pki/distribute_root_ca.yml\n\nPlaybook: `playbooks/pki/distribute_root_ca.yml`.\n\nPlay and task names as written in the playbook:\n\n- Distribute the internal root CA\n- Require an explicit target\n- Configure the local CA source\n- Copy the CA certificate\n- Update the trust store\n\nRun the corresponding Control command. Roles, inventory and site settings also affect this playbook. Check support for --limit and check mode before use.\n\n## Parameters\n\nThe listed sources define these parameters. Missing documentation is indicated. Defaults are informational. Credentials are omitted.\n\n## Sources and maintenance\n\n- `playbooks/pki/distribute_root_ca.yml`\n\nMaintain this description and its source hashes together when the code changes. The database stores a cache.",
      "fields": {}
    }
  }
}
```

## Quellen und Pflege

- `playbooks/pki/distribute_root_ca.yml`

Diese Datei ist die Pflegequelle fuer Mensch und Add-on. Bei Codeaenderungen
Beschreibung und Quellhashs gemeinsam pruefen. Die Datenbank ist nur Cache.
