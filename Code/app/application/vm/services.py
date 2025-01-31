import proxmox_api.proxmox_vm_actions as proxmox_vm_actions 
from proxmox_api.utils.proxmox_vm_ip_fetcher import get_ip, get_hostname
from . import utils
from . import proxmox_session


def get_vm_ip(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    vm_ip = get_ip( utils._get_proxmox_host(), session, vm_proxmox_id)
    return vm_ip

def get_vm_hostname(vm_proxmox_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    vm_ip = get_hostname( utils._get_proxmox_host(), session, vm_proxmox_id)
    return vm_ip

def vm_status(vm_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    return proxmox_vm_actions.status( utils._get_proxmox_host(), session, vm_id)

def start_vm(vm_id):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )
    return proxmox_vm_actions.start( utils._get_proxmox_host(), session, vm_id)

def clone_vm(template_proxmox_id, hostname):
    session = proxmox_session.get_proxmox_session( *utils._get_proxmox_host_and_credentials() )

    clone_id = proxmox_vm_actions.get_free_id( utils._get_proxmox_host(), session)

    proxmox_vm_actions.create( utils._get_proxmox_host(), session, template_proxmox_id, clone_id, hostname)

    return clone_id

