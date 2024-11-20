import utils.constants as constants

def get_ip(first_vm_id, last_vm_id, session): #Returns a dictionary that uses the vm id as key, with the ip and hostname as elements of a list
    def retrieve_hostname(vm_id): #retrieve hostname from vm config using the respective ID
        response = session.get(f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/agent/get-host-name')

        if response.status_code != 200:
            print(f"VM with ID {current_vm_id} is not currently running\n")
            return None
        
        name = response.json()['data']['result']['host-name']
        return name
    
    def retrieve_ip(vm_id): #retrieve ip from interface ens18
        response = session.get(f'{constants.baseuri}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/agent/network-get-interfaces')

        if response.status_code != 200:        
            print(f"VM with ID {current_vm_id} is not currently running\n")
            return None
        ip = response.json()['data']['result'][1]['ip-addresses'][0]['ip-address']
        return ip
    
    print("Getting IP addresses\n")

    vms = {}

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        print(f"Retrieving IP address of virtual machine with ID {current_vm_id}\n")

        vm_ip = retrieve_ip(current_vm_id)
        vm_hostname = retrieve_hostname(current_vm_id)
        vms.update({current_vm_id: [vm_ip, vm_hostname]})

    return vms
