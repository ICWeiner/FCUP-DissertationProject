import os
from shlex import quote
import proxmox.utils.constants as constants
from proxmox.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri


def usage():
    print("""Usage: python vm_manager.py [OPTION]
          
          create <proxmox_host> <session> <template-id> <clone-id> <hostnames>    
          Clones the specified template VM with the given hostname.
          It then configures memory, CPU, disk size, enables QEMU guest agent and takes a snapshot.

          start <proxmox_host> <session> <vm-id> 
          Starts the specified VM.

          stop <proxmox_host> <session> <vm-id> 
          Stops the specified VM.

          destroy <proxmox_host> <session> <vm-id> 
          Destroys the specified VM.
        
          rollback <proxmox_host> <session> <vm-id> 
          Rolls back the specified VM to the initial snapshot taken after VM creation.

          <session> is created with the help of "connection" in utils/ 
          """)
    
def create(proxmox_host, session, template_id, clone_id, hostname):
    print("\nCreating virtual machine:\n")


    data = {
        'newid': clone_id,
        'name': hostname,
    } 

    response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{template_id}/clone', data = data)

    response.raise_for_status()

    print(f"{hostname} VM {clone_id} created.\n")

    
    print("""Finished Cloning VM.\n
          Creating initial snapshots\n""")


    data = {
        'snapname': f'initial_snap_{clone_id}',
        'description': f'Initial snapshot of VM {clone_id}',
    }
    response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{clone_id}/snapshot', data = data)

    response.raise_for_status()

    print("Finished snapshotting virtual machine\n")
    
    
def start(proxmox_host, session, vm_id):
    print("Starting virtual machines...\n")

    response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/status/current')

    if response.json()["data"]['qmpstatus'] == 'running':
        print(f'VM {vm_id} is already running.\n')
    elif response.status_code == 200:
        print(f"Starting virtual machine with ID {vm_id}\n")
        session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/status/start')
    else:
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not start VM {vm_id}')

    print("Done")

def stop(proxmox_host, session, vm_id):
    print("Stopping virtual machines...\n")

    response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/status/current')


    if response.json()["data"]['qmpstatus'] == 'stopped':
        print(f'VM {vm_id} is already stopped.\n')
    elif response.status_code == 200:
        print(f"Stopping virtual machine with ID {vm_id}\n")
        session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/status/stop')
    else: 
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not stop VM {vm_id}\n')

    print("Done")

def destroy(proxmox_host, session, vm_id):
    print("Destroying virtual machines...\n")


    response = session.delete(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}')

    if response.status_code == 200:
        print(f"Destroying virtual machine with ID {vm_id}\n")
    else:
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not destroy VM {vm_id}\n')

    print("Done")

def rollback(proxmox_host, session, vm_id):
    print("Rolling back virtual machines to initial state...\n")


    response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_id}/snapshot/initial_snap_{vm_id}/rollback')

    if response.status_code == 200:
        print(f"Rolling back virtual machine with ID {vm_id}\n")
    else:
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not destroy VM {vm_id}\n')
    print("Done")

