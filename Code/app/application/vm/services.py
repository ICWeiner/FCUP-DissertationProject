from time import sleep
import proxmox_api.proxmox_vm_actions as proxmox_vm_actions 
from proxmox_api.utils.proxmox_vm_ip_fetcher import get_ip, get_hostname
from . import utils
from . import proxmox_session
from gns3_api import gns3_actions


def get_vm_ip(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    vm_ip = get_ip( utils._get_proxmox_host(), session, vm_proxmox_id)
    return vm_ip

def get_vm_hostname(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    vm_ip = get_hostname( utils._get_proxmox_host(), session, vm_proxmox_id)
    return vm_ip

def vm_status(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    return proxmox_vm_actions.status( utils._get_proxmox_host(), session, vm_proxmox_id)

def start_vm(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    return proxmox_vm_actions.start( utils._get_proxmox_host(), session, vm_proxmox_id)

def stop_vm(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    return proxmox_vm_actions.stop( utils._get_proxmox_host(), session, vm_proxmox_id)

def clone_vm(template_proxmox_id, hostname):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )

    clone_id = proxmox_vm_actions.get_free_id( utils._get_proxmox_host(), session)

    proxmox_vm_actions.create( utils._get_proxmox_host(), session, template_proxmox_id, clone_id, hostname)

    return clone_id

def template_vm(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    return proxmox_vm_actions.template( utils._get_proxmox_host(), session, vm_proxmox_id)

def create_new_template_vm(template_proxmox_id, hostname, path_to_gns3project):#TODO: change sleeps to something more intelligent
    new_template_vm_proxmox_id = clone_vm(template_proxmox_id, hostname)

    while not vm_status(new_template_vm_proxmox_id):
        sleep(30)
        start_vm(new_template_vm_proxmox_id)

    node_ip = get_vm_ip(new_template_vm_proxmox_id)

    gns3_actions.import_project(node_ip, path_to_gns3project)

    sleep(30)

    stop_vm(new_template_vm_proxmox_id)

    sleep(10)

    template_vm(new_template_vm_proxmox_id)

    sleep(30)

    return new_template_vm_proxmox_id