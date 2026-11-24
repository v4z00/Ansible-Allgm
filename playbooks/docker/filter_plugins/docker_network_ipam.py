"""Validate network definitions and build explicit dual-stack Docker IPAM."""
from ipaddress import ip_address, ip_network

from ansible.errors import AnsibleFilterError


def flag(value):
    if isinstance(value, bool):
        return value
    if str(value).lower() in ('true', 'yes', '1', 'on'):
        return True
    if str(value).lower() in ('false', 'no', '0', 'off'):
        return False
    raise AnsibleFilterError('enable_ipv6 muss ein boolescher Wert sein.')


def docker_network_ipam(item):
    """Return canonical IPAM entries; never include input values in errors."""
    if not isinstance(item, dict):
        raise AnsibleFilterError('Netzwerkdefinition muss ein Mapping sein.')
    result = []
    ipv6 = flag(item.get('enable_ipv6', False))
    if not ipv6 and (item.get('ipv6_subnet') or item.get('ipv6_gateway')):
        raise AnsibleFilterError('IPv6-IPAM gesetzt, aber enable_ipv6 ist nicht true.')
    for family, prefix in ((4, ''), (6, 'ipv6_')):
        if family == 6 and not ipv6:
            continue
        subnet_key = prefix + 'subnet'
        gateway_key = prefix + 'gateway'
        try:
            network = ip_network(item[subnet_key], strict=True)
            gateway = ip_address(item[gateway_key])
        except (KeyError, ValueError, TypeError):
            raise AnsibleFilterError(
                f'{subnet_key} und {gateway_key} muessen gueltig und explizit gesetzt sein.'
            ) from None
        if network.version != family or gateway.version != family or gateway not in network:
            raise AnsibleFilterError(f'{gateway_key} muss im passenden {subnet_key} liegen.')
        if gateway == network.network_address or (family == 4 and gateway == network.broadcast_address):
            raise AnsibleFilterError(f'{gateway_key} darf nicht Netz-/Broadcastadresse sein.')
        result.append({'subnet': str(network), 'gateway': str(gateway)})
    return result


class FilterModule:
    def filters(self):
        return {'docker_network_ipam': docker_network_ipam}
