from time import sleep
import proxmox_api.proxmox_vm_actions as proxmox_vm_actions 
from proxmox_api.utils.proxmox_vm_ip_fetcher import get_ip, get_hostname
from . import utils
from . import proxmox_session
from gns3_api import gns3_actions
from gns3_api.utils import gns3_parser
from nornir_lib.modules.generic import GenericLibrary 


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
    return proxmox_vm_actions.check_vm_status( utils._get_proxmox_host(), session, vm_proxmox_id)

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

def create_new_template_vm(template_proxmox_id, hostname, path_to_gns3project, commands):#TODO: change sleeps to something more intelligent
    new_template_vm_proxmox_id = clone_vm(template_proxmox_id, hostname)

    while not vm_status(new_template_vm_proxmox_id):#poll vm until qemu-guest-agent is up
        sleep(5)
        start_vm(new_template_vm_proxmox_id)

    node_ip = get_vm_ip(new_template_vm_proxmox_id)

    gns3_project_id = gns3_actions.import_project(node_ip, path_to_gns3project)
    sleep(10)
    # the below code does not function as expected
    #while not gns3_actions.check_project(node_ip, gns3_project_id):
    #    sleep(5) #need to give a little time for gns3 to import the project

    
    if commands and commands is not None:#check if commands were provided
        print(f'COMMANDS: {commands}')
        gns3_nodes = gns3_actions.get_project_nodes(node_ip, gns3_project_id)

        gns3_parser.gns3_nodes_to_yaml(node_ip, hostname, gns3_nodes)

        gns3_actions.start_project(node_ip, gns3_project_id)
        sleep(20)
        
        config = f'{hostname}.yaml'
        generic_lib = GenericLibrary(config)
        generic_lib.set_command(commands[0])
        print('cheguei aki')
        results = generic_lib.command('r1', "doesnt matter")#Y U NO WORK
        print('e depois cheguei aki')
        print(f'COMMAND RESULTS: {results[1]}')


    while vm_status(new_template_vm_proxmox_id):#poll vm to make sure it is down and ready to convert into template
        sleep(5)
        stop_vm(new_template_vm_proxmox_id)

    template_vm(new_template_vm_proxmox_id)

    sleep(5) #TODO:how to wait in a smarter way for the template to be created?

    return new_template_vm_proxmox_id