# Windows GPO hardening / GPO-Basishardening

`bin/control windows-gpo --limit INVENTORY_HOST --check` reads the selected domain
and previews grouped, unlinked policy objects. Remove `--check` to apply the
reviewed settings. Configure exactly one `windows_gpo_management_host`, explicitly
set `windows_gpo_enabled: true` and supply `windows_gpo_profiles` in private host or
group variables. The example is `examples/windows/gpo.yml.example`. Install the
GroupPolicy and ActiveDirectory PowerShell modules on that host first. The role
uses the configured account via Windows runas to obtain a network logon; this
needs valid `ansible_user`/`ansible_password` and the required AD/GPO permissions.
Credentials are consumed by Ansible and never included in source or output.

Names default to `Ansible: Security`, `Ansible: Windows` or `Ansible: Tasks` as
selected by the operator. Prefix and topic names are variables. Group by purpose:
a task that escrows BitLocker keys belongs to Security, even though it uses Task
Scheduler. Use separate profiles only where target scopes/precedence differ.
No profile is automatically attached to an OU, domain or site. Links and policy
application remain manual in GPMC. Newly created objects are unlinked; an existing
object's links are preserved, so changing a linked object can affect its clients
on their next policy refresh.

The first catalog covers WinRM Basic/unencrypted transport, SMB client/server
signature requirements and outgoing NTLM allow/audit/deny. Missing/null values
mean unmanaged; false explicitly writes 0. Removing a switch retains the last
policy value. NTLM deny is rejected while this management path uses NTLM/CredSSP.
These are selected registry policies, not a complete Microsoft security baseline.
Other security templates, per-task GPP merging and ADMX rollout remain separate
work. No private SYSVOL exports, binaries, domains or host settings are shipped.

Existing GPO names require the matching creation marker or explicit
`windows_gpo_adopt_existing: true`. Adoption allows only the listed values to be
updated and does not rename/delete the object or mark all its contents as owned.
Unrelated values, manual settings and files remain. Before changing an existing
object, `Backup-GPO` creates a protected local recovery backup. No full import is
used for merging. A failure may leave a partially updated object; review the
backup and changed values before retry. A full restore would also replace manual
settings, so recovery is a separate deliberate operation. Concurrent MMC edits
cannot be locked by this role; schedule a common maintenance window.

Registry.pol is read structurally for comparison; string/password contents are
not decoded or printed. Native GroupPolicy cmdlets perform updates and version
bookkeeping. Offline fixtures verify parsing, check mode and preservation of
unmanaged content; real domain execution remains a required pilot.

Deutsch: Generische Bausteine bleiben in Allgm, Umgebungswerte privat. Pro Thema
eine GPO mit Schaltern, keine GPO pro Kleinstfunktion. Verknuepfungen ausschliesslich
in der GUI. Vorschau und Sicherung sind vorhanden; noch kein bestaetigter AD-Rollout.

References: [New-GPO](https://learn.microsoft.com/en-us/powershell/module/grouppolicy/new-gpo),
[Set-GPRegistryValue](https://learn.microsoft.com/en-us/powershell/module/grouppolicy/set-gpregistryvalue),
[SMB signing](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/overview-server-message-block-signing),
[WinRM policy](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-remotemanagement),
[NTLM modes](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-outgoing-ntlm-traffic-to-remote-servers).

<details>
<summary>Catalog metadata (JSON)</summary>

```json
{
  "schema_version": 1,
  "kind": "command",
  "ref": "windows-gpo",
  "title": "GPO-Basishardening verwalten",
  "documented": true,
  "fields": [],
  "constraints": [
    "Explicit single management host; no automatic policy links."
  ],
  "sources": [
    "bin/control.d/windows-gpo.json",
    "bin/control.d/windows-gpo.sh",
    "playbooks/windows/gpo.yml",
    "roles/windows_gpo/defaults/main.yml",
    "roles/windows_gpo/files/Get-GpoRegistrySnapshot.ps1",
    "roles/windows_gpo/files/Read-GpoPolicyString.ps1",
    "roles/windows_gpo/files/Read-GpoRegistryPolicy.ps1",
    "roles/windows_gpo/filter_plugins/gpo_plan.py",
    "roles/windows_gpo/tasks/main.yml",
    "roles/windows_gpo/templates/manage.ps1.j2"
  ],
  "source_hashes": {
    "bin/control.d/windows-gpo.json": "44b49d43fb875fe8d27c6121313c62cfb59c2fa75d2da39a3294c68657b5a2bd",
    "bin/control.d/windows-gpo.sh": "421ce77a02e8414f37c00887a9e708d7c49c99295c28369ba36f30c897aa6200",
    "playbooks/windows/gpo.yml": "9dceb81219751dc0f58e542cd03a5ea3b98ffd2d68a22116c587e00d5c4e22e1",
    "roles/windows_gpo/defaults/main.yml": "959e9af437de883ff792b95f0e7b88c01f93e2244289d9a94f240f1062726748",
    "roles/windows_gpo/files/Get-GpoRegistrySnapshot.ps1": "e878e71709a985b0aa2cf4d6bb9138d87403206f75c57726b372c9a68ce5e518",
    "roles/windows_gpo/files/Read-GpoPolicyString.ps1": "040111e1c864b8b31385d10444fac4e38eb3d2eb0ce140c6376e37f6ebcb2905",
    "roles/windows_gpo/files/Read-GpoRegistryPolicy.ps1": "18039c42061fa0df67c0909214ba486dbad3500d77222f9c3e271ac1075bae2a",
    "roles/windows_gpo/filter_plugins/gpo_plan.py": "13a5d1c6c73144c236245254c6a8615d2a54279ba40bffb51afc506537b9d6f1",
    "roles/windows_gpo/tasks/main.yml": "3297962ae4c1dfba6d558a60cfa51491aaedba30b9c88ebf65a66d850e0c0495",
    "roles/windows_gpo/templates/manage.ps1.j2": "cc921f320ebd1586ea6859ab1e5a9a6de50cfd70c0af0debc826e17bd88dd0f8"
  },
  "i18n": {
    "en": {
      "title": "Manage grouped GPO hardening",
      "description": "# Windows GPO hardening / GPO-Basishardening\n\n`bin/control windows-gpo --limit INVENTORY_HOST --check` reads the selected domain\nand previews grouped, unlinked policy objects. Remove `--check` to apply the\nreviewed settings. Configure exactly one `windows_gpo_management_host`, explicitly\nset `windows_gpo_enabled: true` and supply `windows_gpo_profiles` in private host or\ngroup variables. The example is `examples/windows/gpo.yml.example`. Install the\nGroupPolicy and ActiveDirectory PowerShell modules on that host first. The role\nuses the configured account via Windows runas to obtain a network logon; this\nneeds valid `ansible_user`/`ansible_password` and the required AD/GPO permissions.\nCredentials are consumed by Ansible and never included in source or output.\n\nNames default to `Ansible: Security`, `Ansible: Windows` or `Ansible: Tasks` as\nselected by the operator. Prefix and topic names are variables. Group by purpose:\na task that escrows BitLocker keys belongs to Security, even though it uses Task\nScheduler. Use separate profiles only where target scopes/precedence differ.\nNo profile is automatically attached to an OU, domain or site. Links and policy\napplication remain manual in GPMC. Newly created objects are unlinked; an existing\nobject's links are preserved, so changing a linked object can affect its clients\non their next policy refresh.\n\nThe first catalog covers WinRM Basic/unencrypted transport, SMB client/server\nsignature requirements and outgoing NTLM allow/audit/deny. Missing/null values\nmean unmanaged; false explicitly writes 0. Removing a switch retains the last\npolicy value. NTLM deny is rejected while this management path uses NTLM/CredSSP.\nThese are selected registry policies, not a complete Microsoft security baseline.\nOther security templates, per-task GPP merging and ADMX rollout remain separate\nwork. No private SYSVOL exports, binaries, domains or host settings are shipped.\n\nExisting GPO names require the matching creation marker or explicit\n`windows_gpo_adopt_existing: true`. Adoption allows only the listed values to be\nupdated and does not rename/delete the object or mark all its contents as owned.\nUnrelated values, manual settings and files remain. Before changing an existing\nobject, `Backup-GPO` creates a protected local recovery backup. No full import is\nused for merging. A failure may leave a partially updated object; review the\nbackup and changed values before retry. A full restore would also replace manual\nsettings, so recovery is a separate deliberate operation. Concurrent MMC edits\ncannot be locked by this role; schedule a common maintenance window.\n\nRegistry.pol is read structurally for comparison; string/password contents are\nnot decoded or printed. Native GroupPolicy cmdlets perform updates and version\nbookkeeping. Offline fixtures verify parsing, check mode and preservation of\nunmanaged content; real domain execution remains a required pilot.\n\nDeutsch: Generische Bausteine bleiben in Allgm, Umgebungswerte privat. Pro Thema\neine GPO mit Schaltern, keine GPO pro Kleinstfunktion. Verknuepfungen ausschliesslich\nin der GUI. Vorschau und Sicherung sind vorhanden; noch kein bestaetigter AD-Rollout.\n\nReferences: [New-GPO](https://learn.microsoft.com/en-us/powershell/module/grouppolicy/new-gpo),\n[Set-GPRegistryValue](https://learn.microsoft.com/en-us/powershell/module/grouppolicy/set-gpregistryvalue),\n[SMB signing](https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/overview-server-message-block-signing),\n[WinRM policy](https://learn.microsoft.com/en-us/windows/client-management/mdm/policy-csp-remotemanagement),\n[NTLM modes](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-outgoing-ntlm-traffic-to-remote-servers).\n",
      "fields": {}
    },
    "de": {
      "title": "GPO-Basishardening verwalten",
      "description": "Generische Themen-GPOs mit expliziten Schaltern. Vorhandene manuelle Inhalte erhalten, vor Aenderung sichern und nie automatisch verknuepfen. Echter Windows-/AD-Pilot steht aus.",
      "fields": {}
    }
  }
}
```

</details>
