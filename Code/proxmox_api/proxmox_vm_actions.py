import httpx
import logging
import proxmox_api.utils.constants as constants
from proxmox_api.utils.proxmox_base_uri_generator import proxmox_base_uri


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
async def _aget_status(proxmox_host, session, vm_proxmox_id):
    response = await session.get(
        f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/current')
    return response


async def acheck_free_id(proxmox_host, session, id):
    try:
        response = await session.get(
            f'{proxmox_base_uri(proxmox_host)}/cluster/nextid',
            params = {'vmid': f'{id}'} 
            )

        if response.status_code == 200:
            print(f"Verified that VM ID {id} is free.")
            return True
        else:
            try:#Because the API returns 400 if the ID is not free
                response.raise_for_status()
            except httpx.HTTPStatusError as err:
                if response.status_code == 400:
                    print(f"VM ID {id} is not free.")
                    return False
                raise
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        print(f"Network error: {err}")
        return None
    except httpx.RequestError as err:
        print(f"An ambiguous exception occurred: {err}")
        raise

async def acreate(proxmox_host, session, template_id, clone_id, hostname):
    try:
        #VM creation
        response = await session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{template_id}/clone',
            data = {
                'newid': clone_id,
                'name': hostname,
                } 
            )

        response.raise_for_status()

        print(f"Sent clone request VM ID {template_id} into VM ID {clone_id} successfully.")

        # Remove protection flag from clone
        response = await session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{clone_id}/config',
            data = {
                'protection': 0,
                }
            )

        response.raise_for_status()

        print(f"Removed protection flag from VM ID {clone_id} successfully.")

        #VM initial snapshot creation, currently disabled
        '''
        response = await session.post(
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

    except (httpx.ConnectError, httpx.TimeoutException) as err:
        print(f"Network error: {err}")
        return False
    except httpx.RequestError as err:
        print(f"An ambiguous exception occurred: {err}")
        raise


    
async def acheck_vm_status(proxmox_host, session, vm_proxmox_id):
    try:
        response = await _aget_status(proxmox_host, session, vm_proxmox_id)
        response.raise_for_status()
        if response.json()["data"]['qmpstatus'] == 'running':
            #This checks if vm is running and qemu-agent is responding
            response = await session.post(
                f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/agent/ping'
                )
            if response.json()['data'] != None:
                logging.info(f"VM ID {vm_proxmox_id} is running and qemu-agent is responding.")
                return True
            logging.info(f"VM ID {vm_proxmox_id} is running but qemu-agent is not responding.")
        else:
            logging.info(f"VM ID {vm_proxmox_id} is not running.")
        return False
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

async def acheck_vm_is_template(proxmox_host, session, vm_proxmox_id):
    try:
        response = await _aget_status(proxmox_host, session, vm_proxmox_id)
        response.raise_for_status()
        if "template" in response.json()["data"] and response.json()["data"]['template'] == 1:
            #This checks if vm is running and qemu-agent is responding
            logging.info(f"VM ID {vm_proxmox_id} is a template VM.")
            return True
        else:
            logging.info(f"VM ID {vm_proxmox_id} is not a template VM.")
        return False
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise
    
async def astart(proxmox_host, session, vm_proxmox_id):
    try:
        response = await session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/start')
        response.raise_for_status()
        logging.info(f"Sent start request for VM ID {vm_proxmox_id}")
        return True
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise


async def astop(proxmox_host, session, vm_proxmox_id):
    try:
        response = await session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/status/stop')
        response.raise_for_status()
        logging.info(f"Sent stop request for VM ID {vm_proxmox_id}")
        return True
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise


async def atemplate(proxmox_host, session, vm_proxmox_id):
    try:
        response = await session.post(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}/template')
        response.raise_for_status()
        logging.info(f"Sent template request for VM ID {vm_proxmox_id}")
        return True
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise
    
async def adestroy(proxmox_host, session, vm_proxmox_id):
    try:
        response = await session.delete(
            f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}/qemu/{vm_proxmox_id}',
            params = {
                'destroy-unreferenced-disks': 1,
                }
            )
        response.raise_for_status()
        print(f"Sent destroy request for VM ID {vm_proxmox_id}")
        return True
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        print(f"Network error: {err}")
        return False
    except httpx.RequestError as err:
        print(f"An ambiguous exception occurred: {err}")
        raise
    