# Active Directory firewall rules

Choose named IPv4 and IPv6 networks in private inventory. Assign each stage only
to its required source networks in group or host vars. The play targets selected
domain controllers, one at a time.

| Stage | Services |
| --- | --- |
| directory | DNS, Kerberos, LDAP/LDAPS and Global Catalog |
| rpc | Endpoint Mapper and configurable dynamic RPC |
| domain-members | SMB, Kerberos password change, Windows Time and GC TLS |
| administration | AD Web Services |

Preview with `ansible-playbook playbooks/windows/ad_firewall.yml --limit INVENTORY_HOST`.
The default invocation only reads the firewall. Use the same command with
`-e '{"windows_ad_firewall_apply":true}'` to write and read back the active rules.
Check mode remains read-only. Inspect DNS, Kerberos, LDAP and replication from
the actual service networks before retiring prior rules.

Only explicit stable IDs under `Ansible-AD-` with the expected ownership marker
can be reconciled. Rules live in the Windows local policy store and only apply
to the Domain profile. Missing stages leave existing rules accessible for a
separately reviewed migration. This play does not create or link GPOs.

[Port requirements for AD](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/config-firewall-for-ad-domains-and-trusts)
