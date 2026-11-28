"""Compile a scoped, stable Active Directory firewall plan."""
from collections.abc import Mapping
from ipaddress import ip_network
import re

from ansible.errors import AnsibleFilterError


CATALOG = {
    "directory": (
        ("dns-tcp", "DNS", "TCP", 53),
        ("dns-udp", "DNS", "UDP", 53),
        ("kerberos-tcp", "Kerberos", "TCP", 88),
        ("kerberos-udp", "Kerberos", "UDP", 88),
        ("ldap-tcp", "LDAP", "TCP", 389),
        ("ldap-udp", "LDAP", "UDP", 389),
        ("ldaps-tcp", "LDAPS", "TCP", 636),
        ("gc-tcp", "Global Catalog", "TCP", 3268),
    ),
    "rpc": (
        ("rpc-mapper", "RPC Endpoint Mapper", "TCP", 135),
        ("rpc-dynamic", "Dynamic RPC", "TCP", None),
    ),
    "domain-members": (
        ("smb", "SMB", "TCP", 445),
        ("kpasswd-tcp", "Kerberos password change", "TCP", 464),
        ("kpasswd-udp", "Kerberos password change", "UDP", 464),
        ("time", "Windows Time", "UDP", 123),
        ("gc-ssl", "Global Catalog TLS", "TCP", 3269),
    ),
    "administration": (("adws", "AD Web Services", "TCP", 9389),),
}


def ad_firewall_plan(stages, networks, rpc_ports):
    if not isinstance(stages, Mapping) or not isinstance(networks, Mapping):
        raise AnsibleFilterError("AD firewall stages and networks must be mappings.")
    ports = re.fullmatch(r"([1-9][0-9]{0,4})(?:-([1-9][0-9]{0,4}))?", str(rpc_ports))
    if not ports or not 1 <= int(ports[1]) <= int(ports[2] or ports[1]) <= 65535:
        raise AnsibleFilterError("Invalid AD RPC port or range.")

    result = []
    for stage, names in stages.items():
        if (stage not in CATALOG or not isinstance(names, list) or not names or
                any(not isinstance(name, str) or name not in networks for name in names)):
            raise AnsibleFilterError("Each selected stage needs known named network scopes.")
        addresses = set()
        for name in names:
            entries = networks[name]
            if not isinstance(entries, list) or not entries:
                raise AnsibleFilterError("A network scope requires a list of addresses or CIDRs.")
            for entry in entries:
                try:
                    if not isinstance(entry, str) or "%" in entry or entry != entry.strip():
                        raise ValueError
                    address = ip_network(entry)
                    if address.prefixlen == 0:
                        raise ValueError
                except ValueError as exc:
                    raise AnsibleFilterError("AD firewall scope must be a specific IP network or address.") from exc
                addresses.add(str(address))
        for identifier, caption, protocol, port in CATALOG[stage]:
            result.append({
                "name": f"Ansible-AD-{identifier}",
                "display_name": f"Ansible: AD {caption} ({protocol})",
                "stage": stage,
                "protocol": protocol,
                "port": str(port if port is not None else rpc_ports),
                "addresses": sorted(addresses),
            })
    return result


class FilterModule:
    def filters(self):
        return {"windows_ad_firewall_plan": ad_firewall_plan}
