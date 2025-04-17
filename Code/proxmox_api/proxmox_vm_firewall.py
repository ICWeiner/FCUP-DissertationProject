import httpx

import proxmox_api.utils.constants as constants

from proxmox_api import decorators
from proxmox_api.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri

from logger.logger import get_logger

logger = get_logger(__name__)

#TODO: Make arguments of all function be more in line with vm_actions
def _get_firewall_uri_list(proxmox_host: str):    #Get list of all firewall activation uri's
    uri_list = [f'{proxmox_base_uri(proxmox_host)}/cluster/firewall/options',
                f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/firewall/options']
    #add more if you have more proxmoxhosts
    
    return uri_list

@decorators.handle_network_errors
async def acreate_proxmox_vm_isolation_rules(proxmox_host: str, session: httpx.Client, vm_proxmox_id: str, allowed_vm_ip: str) -> bool:

    for uri in _get_firewall_uri_list(proxmox_host):
        response = await session.put(uri, data = {'enable':1})
        response.raise_for_status()

    firewall_rule_0 = {    
                'comment': 'VM accepts only packets from Teacher VM',
                'source': allowed_vm_ip,
                'action': 'ACCEPT',
                'enable': 1,
                'type': 'in',
            } 
    
    firewall_rule_1 = {    
                'comment': 'VM sends only packets to Teacher VM',
                'dest': allowed_vm_ip,
                'action': 'ACCEPT',
                'enable': 1,
                'type': 'out',
            }
    
    firewall_rule_2 = {    
                'comment': 'VM drops all other packets',
                'action': 'DROP',
                'enable': 1,
                'type': 'in',
            } 
    
    firewall_rule_3 = {    
                'comment': 'VM drops all other packets',
                'action': 'DROP',
                'enable': 1,
                'type': 'out',
            } 

    
    response = await session.put(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/firewall/options',
                        data = {'enable':1})
    response.raise_for_status()

    firewall_rules = [firewall_rule_3, firewall_rule_2, firewall_rule_1, firewall_rule_0]

    for rule in firewall_rules:
        response = await session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/firewall/rules',
                                data = rule)
        response.raise_for_status()

    return True
    
async def adelete_proxmox_vm_isolation_rules(proxmox_host: str, session: httpx.Client, vm_proxmox_id: str) -> bool:

    for uri in _get_firewall_uri_list(proxmox_host):
        response = await session.put(uri, data = {'enable':0})
        response.raise_for_status()

    response = await session.put(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/firewall/options',
                        data = {'enable':0})
    response.raise_for_status()


    response = await session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/firewall/rules')
    response.raise_for_status()

    number_of_rules = len(response.json()['data'])

    for i in range(number_of_rules): #Since the number of higher position rules changes when deleting, we can always delete rules in position 0, assuming we dont have a need for any other rules
        response = await session.delete(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/firewall/rules/0')
        response.raise_for_status()

    return True
        