# Private Dienstprofile bereitstellen

`ansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host --check` prüft die Vorschau. Ohne `--check` werden ausgewählte private Ordner und daraus explizit definierte Units bereitgestellt. Voraussetzungen, Pfadzuordnung und Aktivierung stehen in [Dienstprofile](../configurations/systemd-job-deployment.md). Bestehende Programme werden nicht automatisch gestartet.

```json
{
  "schema_version": 1,
  "kind": "playbook",
  "ref": "playbooks/scripts/deploy_systemd.yml",
  "title": "Private Dienstprofile bereitstellen",
  "documented": false,
  "fields": [],
  "constraints": [],
  "sources": [
    "playbooks/scripts/deploy_systemd.yml"
  ],
  "source_hashes": {
    "playbooks/scripts/deploy_systemd.yml": "d119b7890da6f392f8e47599c735a223bfa7eb1879f29eeb20a5546aa157f101"
  },
  "i18n": {
    "de": {
      "title": "Private Dienstprofile bereitstellen",
      "description": "# Private Dienstprofile bereitstellen\n\n`ansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host --check` prüft die Vorschau. Ohne `--check` werden ausgewählte private Ordner und daraus explizit definierte Units bereitgestellt. Voraussetzungen, Pfadzuordnung und Aktivierung stehen in [Dienstprofile](../configurations/systemd-job-deployment.md). Bestehende Programme werden nicht automatisch gestartet.\n",
      "fields": {}
    },
    "en": {
      "title": "Deploy private service profiles",
      "description": "# Deploy private service profiles\n\nRun `ansible-playbook playbooks/scripts/deploy_systemd.yml --limit example-host --check` for a preview, then omit `--check` for the selected private folders and explicitly defined units. See [service profiles](../configurations/systemd-job-deployment.md) for prerequisites, paths and lifecycle settings. Programs are not started implicitly.\n",
      "fields": {}
    }
  }
}
```
