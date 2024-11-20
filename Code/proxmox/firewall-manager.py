from utils.connection import proxmox_connect
import utils.constants as constants
from utils.proxmox_vm_ip_fetcher import get_ip

def usage():
    print("""Usage: python vm_manager.py [OPTION]
          
          create_proxmox_vm_isolation_rules <first-vm-id> <last-vm-id> <allowed-vm-ip> <session>
          Activates the proxmox firewall at the datacenter, node and vm levels.
          Creates firewall rules to disable communication between "student" VMs, they may only
          communicate with the designated IP, typically the "teacher" VM.

          create_proxmox_vm_isolation_rules <first-vm-id> <last-vm-id> <allowed-vm-ip> <session>
          Deactivates the proxmox firewall at the datacenter, node and vm levels.
          Deletes firewall rules enabling full internet access and communication between VMs.
          """)

def _get_firewall_uri_list():    #Get list of all firewall activation uri's
    uri_list = [f'{constants.baseuri}/cluster/firewall/options',
                f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/firewall/options']
    #add more if you have more proxmoxhosts
    
    return uri_list


def create_proxmox_vm_isolation_rules(first_vm_id, last_vm_id, allowed_vm_ip, session):

    for uri in _get_firewall_uri_list:
        response = session.put(uri, data = {'enable':0})
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

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.put(f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/options',
                            data = {'enable':1})
        response.raise_for_status()

        firewall_rules = [firewall_rule_2, firewall_rule_1, firewall_rule_0]

        for rule in firewall_rules:
            response = session.post(f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/rules',
                                    data = rule)
            response.raise_for_status()

        print(response)
    
def delete_proxmox_vm_isolation_rules(first_vm_id, last_vm_id, session):

    for uri in _get_firewall_uri_list:
        response = session.put(uri, data = {'enable':0})
        response.raise_for_status()


    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.put(f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/options',
                            data = {'enable':0})
        response.raise_for_status()


        response = session.get(f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/rules')
        response.raise_for_status()

        number_of_rules = len(response.json()['data'])

        for i in range(number_of_rules): #Since the number of higher pos rules changes when deleting, we can always delete rule pos 0
            response = session.delete(f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/firewall/rules/0')
            response.raise_for_status()
        


if __name__ == "__main__":
    
    session = proxmox_connect(constants.username, constants.password)

    student_vms = get_ip(300,301,session)

    teacher_vm = get_ip(800,800,session)

    teacher_vm_ip = teacher_vm[800][0]


    #create_proxmox_vm_isolation_rules(300, 301, teacher_vm_ip, session)

    #delete_proxmox_vm_isolation_rules(300, 301, session)

