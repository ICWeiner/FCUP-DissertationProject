import proxmox_api.utils.constants as constants
from proxmox_api.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri


def get_free_id(proxmox_host, session):
    response = session.get(f'{proxmox_base_uri(proxmox_host)}/cluster/nextid')

    response.raise_for_status()

    free_id = response.json()['data']

    return free_id
    
def create(proxmox_host, session, template_id, clone_id, hostname):

    #VM creation
    data = {
        'newid': clone_id,
        'name': hostname,
    } 

    response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{template_id}/clone', data = data)

    response.raise_for_status()

    # Remove protection flag from clone
    data = {
        'protection': 0,
    } 

    response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{clone_id}/config', data = data)

    response.raise_for_status()


    #VM initial snapshot creation
    data = {
        'snapname': f'initial_snap_{clone_id}',
        'description': f'Initial snapshot of VM {clone_id}',
    }

    #response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{clone_id}/snapshot', data = data)

    #response.raise_for_status()

    return True

#Internal use only
def _get_status(proxmox_host, session, vm_proxmox_id):
    response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/current')
    return response
    
def check_vm_status(proxmox_host, session, vm_proxmox_id):
    response = _get_status(proxmox_host, session, vm_proxmox_id)
    if response.json()["data"]['qmpstatus'] == 'running':
        #This checks if vm is running and qemu-agent is responding
        response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/agent/ping')
        if response.json()['data'] != None:
            return True
    return False
    
def start(proxmox_host, session, vm_proxmox_id):

    #Check VM status
    response = _get_status(proxmox_host, session, vm_proxmox_id)

    if response.json()["data"]['qmpstatus'] == 'running':
        print(f'VM {vm_proxmox_id} is already running.\n')
    elif response.status_code == 200:
        print(f"Starting virtual machine with ID {vm_proxmox_id}\n")
        session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/start')
    else:
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not start VM {vm_proxmox_id}')
        return False

    return True

def stop(proxmox_host, session, vm_proxmox_id):

    #Check VM status
    response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/current')

    if response.json()["data"]['qmpstatus'] == 'stopped':
        print(f'VM {vm_proxmox_id} is already stopped.\n')
    elif response.status_code == 200:
        print(f"Stopping virtual machine with ID {vm_proxmox_id}\n")
        session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/stop')
    else: 
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not stop VM {vm_proxmox_id}\n')
        return False


    return True

def template(proxmox_host, session, vm_proxmox_id):

    #Check VM status
    response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/template')

    if response.status_code == 200:
        print(f"Templating virtual machine with ID {vm_proxmox_id}\n")
    else:
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not template VM {vm_proxmox_id}\n')
        return False


    return True

def destroy(proxmox_host, session, vm_proxmox_id):

    #Check VM status
    response = session.delete(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}')

    if response.status_code == 200:
        print(f"Destroying virtual machine with ID {vm_proxmox_id}\n")
    else:
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not destroy VM {vm_proxmox_id}\n')
        return False


    return True

def rollback(proxmox_host, session, vm_proxmox_id):
    
    response = session.post(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/snapshot/initial_snap_{vm_proxmox_id}/rollback')

    if response.status_code == 200:
        print(f"Rolling back virtual machine with ID {vm_proxmox_id}\n")
    else:
        print(f'Unexpected HTTP status code {response.status_code}')
        print(f'Error: Could not destroy VM {vm_proxmox_id}\n')
        return False
    
    return True

