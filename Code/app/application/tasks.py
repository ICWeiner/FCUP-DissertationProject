from time import sleep
import random
import proxmox_api.proxmox_vm_actions as proxmox_vm_actions 
from proxmox_api.utils.proxmox_vm_ip_fetcher import get_ip, get_hostname
from gns3_api import gns3_actions
from gns3_api.utils import gns3_parser
from nornir_lib.modules.generic import GenericLibrary 
import celery
import logging
import requests
from .vm import utils

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

@celery.shared_task(bind=True)
def celery_destroy_vm(self, vm_proxmox_id):
    session = utils._get_proxmox_session()
    try:
        return proxmox_vm_actions.destroy( utils._get_proxmox_host(), session, vm_proxmox_id)
    except Exception as err:
        logging.error(f"Error deleting VM: {err}")
        raise self.retry(exc=err, countdown=10)

@celery.shared_task(bind=True)
def celery_clone_vm(self, template_proxmox_id, hostname):
    session = utils._get_proxmox_session()

    clone_id = None
    try:

        while clone_id is None:
            id = random.randint(100, 999999999)
            if proxmox_vm_actions.check_free_id( utils._get_proxmox_host(), session, id): clone_id = id

        proxmox_vm_actions.create( utils._get_proxmox_host(), session, template_proxmox_id, clone_id, hostname)

    except Exception as err:
        logging.error(f"Error cloning VM: {err}")
        raise self.retry(exc=err, countdown=10)

    return clone_id

@celery.shared_task
def celery_set_vm_status(vm_proxmox_id, desired_status, max_retries=10, interval=5):
    session = utils._get_proxmox_session()
    try:
        action = ""
        if desired_status == True:
            proxmox_vm_actions.start( utils._get_proxmox_host(), session, vm_proxmox_id)
            action = "Power on"
        else:
            proxmox_vm_actions.stop( utils._get_proxmox_host(), session, vm_proxmox_id)
            action = "Power off"
        
        for _ in range(max_retries): 
            if utils.vm_status(vm_proxmox_id) == desired_status:
                return True
            sleep(interval)

        logging.warning(f"Timeout reached while waiting for VM {vm_proxmox_id} to {action}.")
        raise TimeoutError(f"VM {vm_proxmox_id} failed to {action}.")
    except requests.exceptions.RequestException as err:
        logging.error(f"Error setting VM status: {err}")
        return False

@celery.shared_task()
def celery_import_gns3_project(vm_proxmox_id, path_to_gns3project):
    session = utils._get_proxmox_session()
    node_ip = get_ip( utils._get_proxmox_host(), session, vm_proxmox_id)
    gns3_project_id = gns3_actions.import_project(node_ip, path_to_gns3project)
    sleep(10)
    return gns3_project_id

@celery.shared_task()
def celery_run_gns3_commands(gns3_project_id, vm_proxmox_id, hostname,  commands_by_hostname):
    """Execute provided commands on the GNS3 project"""
    node_ip = utils.get_vm_ip(vm_proxmox_id)
    gns3_nodes = gns3_actions.get_project_nodes(node_ip, gns3_project_id)
    gns3_parser.gns3_nodes_to_yaml(node_ip, hostname, gns3_nodes)

    gns3_actions.start_project(node_ip, gns3_project_id)
    sleep(10)

    config = f'{hostname}.yaml'
    generic_lib = GenericLibrary(config)

    for entry in commands_by_hostname:
        for command in entry["commands"]:
            generic_lib.set_command(command)
            generic_lib.command(entry["hostname"], "")

@celery.shared_task()
def celery_template_vm(vm_proxmox_id, max_retries=10, interval=5):
    session = utils._get_proxmox_session()
    try:
        if proxmox_vm_actions.template( utils._get_proxmox_host(), session, vm_proxmox_id):
            for _ in range(max_retries):
                if proxmox_vm_actions.check_vm_is_template( utils._get_proxmox_host(), session, vm_proxmox_id):
                    return True
                sleep(interval)
            raise TimeoutError(f"VM {vm_proxmox_id} failed to become a template.")
    except requests.exceptions.RequestException as err:
        logging.error(f"Error setting VM as template: {err}")
        return False
