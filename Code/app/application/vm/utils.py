from flask import current_app as app
from time import sleep
import proxmox_api.proxmox_vm_actions as proxmox_vm_actions 
from proxmox_api.utils.proxmox_vm_ip_fetcher import get_ip, get_hostname
from .. import proxmox_session
import logging

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

def _get_proxmox_host():
    return app.config['PROXMOX_HOST']

def _get_proxmox_credentials():
    return app.config['PROXMOX_USER'], app.config['PROXMOX_PASSWORD']

def _get_proxmox_host_and_credentials():
    return _get_proxmox_host(), *_get_proxmox_credentials()

def _get_proxmox_session():
    return proxmox_session.get_flask_proxmox_session( *_get_proxmox_host_and_credentials() )

def get_vm_ip(vm_proxmox_id):
    session = _get_proxmox_session()
    vm_ip = get_ip( _get_proxmox_host(), session, vm_proxmox_id)
    return vm_ip

def get_vm_hostname(vm_proxmox_id):
    session = _get_proxmox_session()
    vm_ip = get_hostname( _get_proxmox_host(), session, vm_proxmox_id)
    return vm_ip

def vm_status(vm_proxmox_id):
    session = _get_proxmox_session()
    return proxmox_vm_actions.check_vm_status( _get_proxmox_host(), session, vm_proxmox_id)

def start_vm(vm_proxmox_id):
    session = _get_proxmox_session()
    return proxmox_vm_actions.start( _get_proxmox_host(), session, vm_proxmox_id)

def stop_vm(vm_proxmox_id):
    session = _get_proxmox_session()
    return proxmox_vm_actions.stop( _get_proxmox_host(), session, vm_proxmox_id)