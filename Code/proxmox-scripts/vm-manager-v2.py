import requests
import sys
import os
from shlex import quote
from re import search
from utils.connection import proxmox_connect

import utils.constants as constants

baseuri = ""

def usage():
    print("""Usage: python vm_manager.py [OPTION]
          
          create <template-id> <first-clone-id> <hostnames-list-file>    
          Clones the specified template VM for each hostname listed in a given file 
          and the starting ID number.
          It then configures memory, CPU, disk size, enables QEMU guest agent and takes a snapshot.

          start <first-vm-id> [last-vm-id]
          Starts the specified VMs.

          stop <first-vm-id> [last-vm-id]
          Stops the specified VMs.

          destroy <first-vm-id> [last-vm-id]
          Destroys the specified VMs.
        
          rollback <first-vm-id> [last-vm-id]
          Rolls back the specifiedVM to the initial snapshot taken after VM creation.

          get-ip <first-vm-id> [last-vm-id] <output-file>
          Retrieves the IP address of each running VM and saves the associated ID, hostname and 
          IP address to the specified file.
          """)
    
def create(template_id, first_clone_id, hostnames_file, session):
    if not os.path.exists(hostnames_file):
        print(f"Error: Hostnames list file '{hostnames_file}' does not exist.")
        return 1
    print("\nCreating virtual machines:\n")

    current_clone_id = first_clone_id

    with open(hostnames_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            hostname = quote(line.strip())

            data = {
                'newid': current_clone_id,
                'name': hostname,
            } 

            response = session.post(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{template_id}/clone', data = data)

            if response.status_code != 200:
                print(f'Unexpected HTTP status code {response.status_code}')
                continue

            print(f"{hostname} VM {current_clone_id} created.\n")

            current_clone_id = int(current_clone_id) + 1

    
    print("""Finished creating VMs.\n
          Creating initial snapshots\n""")

    current_clone_id = first_clone_id

    with open(hostnames_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            hostname = quote(line.strip())

            data = {
                'snapname': f'initial_snap_{current_clone_id}',
                'description': f'Initial snapshot of VM {current_clone_id}',
            }
            response = session.post(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_clone_id}/snapshot', data = data)

            if response.status_code != 200:
                print(f'Unexpected HTTP status code {response.status_code}')
                continue

            print(".\n")
            current_clone_id = int(current_clone_id) + 1

    print("Finished snapshotting virtual machines\n")
    
    
def start(first_vm_id, last_vm_id, session):
    print("Starting virtual machines...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.get(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/status/current')

        if response.json()["data"]['qmpstatus'] == 'running':
            print(f'VM {current_vm_id} is already running.\n')
        elif response.status_code == 200:
            print(f"Starting virtual machine with ID {current_vm_id}\n")
            session.post(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/status/start')
        else:
            print(f'Unexpected HTTP status code {response.status_code}')
            print(f'Error: Could not start VM {current_vm_id}')

    print("Done")

def stop(first_vm_id, last_vm_id, session):
    print("Stopping virtual machines...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.get(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/status/current')


        if response.json()["data"]['qmpstatus'] == 'stopped':
            print(f'VM {current_vm_id} is already stopped.\n')
        elif response.status_code == 200:
            print(f"Stopping virtual machine with ID {current_vm_id}\n")
            session.post(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/status/stop')
        else: 
            print(f'Unexpected HTTP status code {response.status_code}')
            print(f'Error: Could not stop VM {current_vm_id}\n')

    print("Done")

def destroy(first_vm_id, last_vm_id, session):
    print("Destroying virtual machines...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.delete(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}')

        if response.status_code == 200:
            print(f"Destroying virtual machine with ID {current_vm_id}\n")
        else:
            print(f'Unexpected HTTP status code {response.status_code}')
            print(f'Error: Could not destroy VM {current_vm_id}\n')

    print("Done")

def rollback(first_vm_id, last_vm_id, session):
    print("Rolling back virtual machines to initial state...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        response = session.post(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{current_vm_id}/snapshot/initial_snap_{current_vm_id}/rollback')

        if response.status_code == 200:
            print(f"Rolling back virtual machine with ID {current_vm_id}\n")
        else:
            print(f'Unexpected HTTP status code {response.status_code}')
            print(f'Error: Could not destroy VM {current_vm_id}\n')
    print("Done")

def get_ip(first_vm_id, last_vm_id, output_file, session):
    def retrieve_hostname(vm_id): #retrieve hostname from vm config using the respective ID
        response = session.get(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/agent/get-host-name')

        if response.status_code != 200:
            print(f"VM with ID {current_vm_id} is not currently running\n")
            return None
        
        name = response.json()['data']['result']['host-name'] #TODO: this doesnt seem to get the fullname...
        return name
    
    def retrieve_ip(vm_id): #retrieve ip from interface ens18
        response = session.get(f'{baseuri}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/agent/network-get-interfaces')

        if response.status_code != 200:        #output = []#subprocess.run(["qm", "config", str(vm_id)], capture_output=True, text=True)
            print(f"VM with ID {current_vm_id} is not currently running\n")
            return None
        ip = response.json()['data']['result'][1]['ip-addresses'][0]['ip-address']
        return ip
    
    print("Getting IP addresses\n")

    with open(output_file, "w") as file:
        for current_vm_id in range(first_vm_id, last_vm_id + 1):
            print(f"Retrieving IP address of virtual machine with ID {current_vm_id}\n")
            file.write(f"VM ID: {current_vm_id}  Hostname: {retrieve_hostname(current_vm_id)} IP: {retrieve_ip(current_vm_id)}\n")
    print(f"IP addresses saved to {output_file}\n")

    

if __name__ == "__main__":
    baseuri = f'https://{constants.proxmox_host}:8006/api2/json'

    args = sys.argv
    args_length = len(args)

    if args_length == 5 and args[1] == 'create':
        template_id = args[2]
        first_clone_id = args[3]
        hostnames_file = args[4]

        session = proxmox_connect(constants.proxmox_host, constants.username, constants.password)

        create(template_id, first_clone_id, hostnames_file, session)
    elif (args_length == 4 or args_length == 5) and args[1] == 'get-ip':
            first_vm_id = int(args[2])
            last_vm_id = int(args[3]) if args_length == 5 else first_vm_id
            output_file = args[4] if args_length == 5 else args[3]

            session = proxmox_connect(constants.proxmox_host, constants.username, constants.password)

            get_ip(first_vm_id, last_vm_id, output_file, session)
    elif args_length == 3 or args_length == 4 :
        first_vm_id = int(args[2])
        last_vm_id = int(args[3]) if args_length == 4 else first_vm_id

        session = proxmox_connect(constants.proxmox_host, constants.username, constants.password)

        if args[1] == 'start':
            start(first_vm_id, last_vm_id, session)
        elif args[1] == 'stop':
            stop(first_vm_id, last_vm_id, session)
        elif args[1] == 'destroy':
            destroy(first_vm_id, last_vm_id, session)
        elif args[1] == 'rollback':
            rollback(first_vm_id, last_vm_id, session)
        else :
            usage()
    else:
        usage()
