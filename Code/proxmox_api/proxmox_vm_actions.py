import requests
import logging
import proxmox_api.utils.constants as constants
from proxmox_api.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)


#Internal use only
def _get_status(proxmox_host, session, vm_proxmox_id):
    response = session.get(
        f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/current'
        )
    return response


def get_free_id(proxmox_host, session):
    try:
        response = session.get(
            f'{proxmox_base_uri(proxmox_host)}/cluster/nextid'
            )

        response.raise_for_status()

        free_id = response.json()['data']

        logging.info(f"Checked that VM ID {free_id} is free.")

        return free_id
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

def check_free_id(proxmox_host, session, id):
    try:
        response = session.get(
            f'{proxmox_base_uri(proxmox_host)}/cluster/nextid',
            params = {
                'vmid': f'{id}'
                }
            )

        if response.status_code == 200:
            logging.info(f"Verified that VM ID {id} is free.")
            return True
        else:
            try:#Because the API returns 400 if the ID is not free
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                if response.status_code == 400:
                    logging.info(f"VM ID {id} is not free.")
                    return False
                raise
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise
    

def create(proxmox_host, session, template_id, clone_id, hostname):
    try:
        #VM creation
        response = session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{template_id}/clone',
            data = {
                'newid': clone_id,
                'name': hostname,
                } 
            )

        response.raise_for_status()

        logging.info(f"Sent clone request VM ID {template_id} into VM ID {clone_id} successfully.")

        # Remove protection flag from clone

        response = session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{clone_id}/config',
            data = {
                'protection': 0,
                }
            )

        response.raise_for_status()

        logging.info(f"Removed protection flag from VM ID {clone_id} successfully.")


        #VM initial snapshot creation, currently disabled
        '''
        response = session.post(
        f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{clone_id}/snapshot',
            data = {
            'snapname': f'initial_snap_{clone_id}',
            'description': f'Initial snapshot of VM {clone_id}',
            }
        )

        response.raise_for_status()

        logging.info(f"Created initial snapshot of VM ID {clone_id} successfully.")
        '''

        return True

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return False
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

    
def check_vm_status(proxmox_host, session, vm_proxmox_id):
    try:
        response = _get_status(proxmox_host, session, vm_proxmox_id)
        response.raise_for_status()
        if response.json()["data"]['qmpstatus'] == 'running':
            #This checks if vm is running and qemu-agent is responding
            response = session.post(
                f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/agent/ping'
                )
            if response.json()['data'] != None:
                logging.info(f"VM ID {vm_proxmox_id} is running and qemu-agent is responding.")
                return True
            logging.info(f"VM ID {vm_proxmox_id} is running but qemu-agent is not responding.")
        else:
            logging.info(f"VM ID {vm_proxmox_id} is not running.")
        return False
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return False
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

    
def start(proxmox_host, session, vm_proxmox_id):
    try:
        response = session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/start'
            )
        response.raise_for_status()
        logging.info(f"Sent start request for VM ID {vm_proxmox_id}")
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return False
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise


def stop(proxmox_host, session, vm_proxmox_id):
    try:
        response = session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/stop'
            )
        response.raise_for_status()
        logging.info(f"Sent stop request for VM ID {vm_proxmox_id}")
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return False
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise


def template(proxmox_host, session, vm_proxmox_id):
    try:
        response = session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/template'
            )
        response.raise_for_status()
        logging.info(f"Sent template request for VM ID {vm_proxmox_id}")
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return False
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise


def destroy(proxmox_host, session, vm_proxmox_id):
    try:
        response = session.delete(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}',
            params = {
                'destroy-unreferenced-disks': 1,
                }
            )
        response.raise_for_status()
        logging.info(f"Sent destroy request for VM ID {vm_proxmox_id}")
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
        logging.error(f"Network error: {err}")
        return False
    except requests.exceptions.RequestException as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise
    
    