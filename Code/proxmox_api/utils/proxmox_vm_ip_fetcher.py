import proxmox_api.utils.constants as constants
from proxmox_api.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri

def get_hostname(proxmox_host, session, vm_id): #retrieve hostname from vm config using the respective ID
    response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/agent/get-host-name')

    response.raise_for_status()
    
    name = response.json()['data']['result']['host-name']
    return name

def get_ip(proxmox_host, session, vm_id): #retrieve ip from interface ens18
    response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/agent/network-get-interfaces')

    response.raise_for_status()
    
    ip = response.json()['data']['result'][1]['ip-addresses'][0]['ip-address']
    return ip