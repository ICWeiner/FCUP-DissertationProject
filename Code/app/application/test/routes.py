from quart import Blueprint, render_template, request
from quart import current_app as app
from quart_login import current_user, login_required
from nornir import InitNornir
from nornir.core.filter import F
from gns3_api import gns3_actions
from gns3_api.utils.gns3_parser import gns3_nodes_to_yaml
from nornir_lib.modules.ping import PingLibrary
from nornir_lib.modules.traceroute import TracerouteLibrary 


#TODO: FIX ABOVE IMPORTS

test_bp = Blueprint(
    'test_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@test_bp.route('/vm/<int:vm_proxmox_id>/test/ping', methods=['POST'])
@login_required
def ping(vm_proxmox_id):#TODO: FINISH IMPLEMENTING PING TEST

    hostname = request.form.get('hostname')#TODO: not the best way of getting this info
    target = request.form.get('ip_address')

    gns3_filename = 'test' #TODO: pass this as an argument
        
    vm_ip = get_vm_ip(vm_proxmox_id)
    print(f'student ip is : {vm_ip}')

    vm_hostname = get_vm_hostname(vm_proxmox_id)
    print(f'student vm hostname is : {vm_hostname}')

    project_id = gns3_actions.get_project_id(vm_ip, gns3_filename)
    print(f'project id is : {project_id}')

    nodes = gns3_actions.get_project_nodes(vm_ip, project_id) #Get info on given project's nodes

    gns3_nodes_to_yaml(vm_ip, vm_hostname, nodes) #Convert info into a format readable by nornir

    gns3_actions.start_project(vm_ip, project_id)
    print('project started')

    config = f'{vm_hostname}.yaml'
    ping_lib = PingLibrary(config)
    print('ping library initialized')

    # Perform ping for a hostname (the full destination ip must be provided)
    results = ping_lib.command(hostname, target) #TODO: pass these arguments as arguments instead of hard coding
    print('ping command executed')


    return f'<p>TEST RESULTS: <br> {results} </p>'

@test_bp.route('/vm/<int:vm_proxmox_id>/test/traceroute', methods=['POST'])
@login_required
def traceroute(vm_proxmox_id):#TODO: FINISH IMPLEMENTING TRACEROUTE TEST

    hostname = request.form.get('hostname')#TODO: not the best way of getting this info
    target = request.form.get('ip_address')

    gns3_filename = 'test' #TODO: pass this as an argument
        
    vm_ip = get_vm_ip(vm_proxmox_id)
    print(f'student ip is : {vm_ip}')

    vm_hostname = get_vm_hostname(vm_proxmox_id)
    print(f'student vm hostname is : {vm_hostname}')

    project_id = gns3_actions.get_project_id(vm_ip, gns3_filename)
    print(f'project id is : {project_id}')

    nodes = gns3_actions.get_project_nodes(vm_ip, project_id) #Get info on given project's nodes

    gns3_to_yaml(vm_ip, vm_hostname, nodes) #Convert info into a format readable by nornir

    gns3_actions.start_project(vm_ip, project_id)
    print('project started')

    config = f'{vm_hostname}.yaml'
    traceroute_lib = TracerouteLibrary(config)
    print('traceroute library initialized')

    # Perform ping for a hostname (the full destination ip must be provided)
    results = traceroute_lib.command(hostname, target) #TODO: pass these arguments as arguments instead of hard coding
    print('traceroute command executed')


    return f'<p>TEST RESULTS: <br> {results} </p>'