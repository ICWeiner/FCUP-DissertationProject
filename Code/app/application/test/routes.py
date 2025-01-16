from flask import Blueprint, render_template
from flask import current_app as app
from flask_login import current_user, login_required
from nornir import InitNornir
from nornir.core.filter import F
from nornir_lib.utils.gns3_api import get_project_id, get_project_nodes, start_project, gns3_to_yaml
from nornir_lib.modules.ping import PingLibrary
from ..vm.routes import get_vm_ip, get_vm_hostname


#TODO: FIX ABOVE IMPORTS

test_bp = Blueprint(
    'test_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@test_bp.route('/vm/<int:vm_id>/test/ping', methods=['POST'])
#@login_required
def ping(vm_id):#TODO: FINISH IMPLEMENTING PING TEST

    gns3_filename = 'test' #TODO: pass this as an argument
        
    vm_ip = get_vm_ip(vm_id)
    print(f'student ip is : {vm_ip}')

    vm_hostname = get_vm_hostname(vm_id)
    print(f'student vm hostname is : {vm_hostname}')

    project_id = get_project_id(vm_ip, gns3_filename)
    print(f'project id is : {project_id}')

    nodes = get_project_nodes(vm_ip, project_id) #Get info on given project's nodes

    gns3_to_yaml(vm_ip, vm_hostname, nodes) #Convert info into a format readable by nornir

    start_project(vm_ip, project_id)
    print('project started')

    config = f'{vm_hostname}.yaml'
    ping_lib = PingLibrary(config)
    print('ping library initialized')

    # Perform ping for a hostname (the full destination ip must be provided)
    results = ping_lib.command('pc1', '10.0.1.2') #TODO: pass these arguments as arguments instead of hard coding
    print('ping command executed')


    return f'<p>TEST RESULTS: <br> {results} </p>'