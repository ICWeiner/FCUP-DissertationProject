import proxmox.utils.constants as constants
from proxmox.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri


def usage():#TODO: Make arguments of all function be more in line with vm_actions
    print("""Usage: python vm_manager.py [OPTION]
          
          create_proxmox_vm_isolation_rules <proxmox-host> <first-vm-id> <last-vm-id> <allowed-vm-ip> <session>
          Activates the proxmox firewall at the datacenter, node and vm levels.
          Creates firewall rules to disable communication between "student" VMs, they may only
          communicate with the designated IP, typically the "teacher" VM.

          delete_proxmox_vm_isolation_rules <proxmox-host> <first-vm-id> <last-vm-id> <allowed-vm-ip> <session>
          Deactivates the proxmox firewall at the datacenter, node and vm levels.
          Deletes firewall rules enabling full internet access and communication between VMs.
          """)

def _get_firewall_uri_list(proxmox_host):    #Get list of all firewall activation uri's
    uri_list = [f'{proxmox_base_uri(proxmox_host)}/cluster/firewall/options',
                f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/firewall/options']
    #add more if you have more proxmoxhosts
    
    return uri_list


def create_proxmox_vm_isolation_rules(proxmox_host, first_vm_id, last_vm_id, allowed_vm_ip, session):

    for uri in _get_firewall_uri_list(proxmox_host):
        response = session.put(uri, data = {'enable':1})
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

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.put(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/options',
                            data = {'enable':1})
        response.raise_for_status()

        firewall_rules = [firewall_rule_3, firewall_rule_2, firewall_rule_1, firewall_rule_0]

        for rule in firewall_rules:
            response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/rules',
                                    data = rule)
            response.raise_for_status()

        print(response)
    
def delete_proxmox_vm_isolation_rules(proxmox_host, first_vm_id, last_vm_id, session):

    for uri in _get_firewall_uri_list(proxmox_host):
        response = session.put(uri, data = {'enable':0})
        response.raise_for_status()


    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.put(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/options',
                            data = {'enable':0})
        response.raise_for_status()


        response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/rules')
        response.raise_for_status()

        number_of_rules = len(response.json()['data'])

        for i in range(number_of_rules): #Since the number of higher pos rules changes when deleting, we can always delete rule pos 0
            response = session.delete(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/rules/0')
            response.raise_for_status()
        