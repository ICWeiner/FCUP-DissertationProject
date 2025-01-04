from flask import Blueprint, render_template
from flask import current_app as app
from nornir import InitNornir
from nornir.core.filter import F
from nornir_lib.utils.gns3_api import get_project_id, get_project_nodes, start_project, gns3_to_yaml
from nornir_lib.modules.ping import PingLibrary
from flask_login import current_user, login_required

#TODO: FIX ABOVE IMPORTS

test_bp = Blueprint(
    'test_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@test_bp.route('/vm/<int:vm_id>/test/ping')
#@login_required
def ping(vm_id):#TODO: FINISH IMPLEMENTING PING TEST
    #ping_test(vm_id, 'test', 'pc1', '10.0.0.1')

    try:
        nr = InitNornir(config_file='config.yaml')
    except Exception as e:
        print(f'Failed to initialize Nornir: {str(e)}')
        exit(1)


    linux_hosts = nr.filter(F(name__startswith = str('up2')) & F(platform__eq = 'linux'))

    gns3_filename = 'test' #TODO: pass this as an argument

    results = ''

    for i in linux_hosts.inventory.hosts.items(): 
        
        node_ip = linux_hosts.inventory.hosts[i[0]].hostname 
        print(f'student ip is : {node_ip}')

        node_name = i[0] 
        print(f'student mec number is : {node_name}')

        project_id = get_project_id(node_ip, gns3_filename)

        nodes = get_project_nodes(node_ip, project_id) #Get info on given project's nodes

        gns3_to_yaml(node_ip, node_name, nodes) #Convert info into a format readable by nornir

        start_project(node_ip, project_id)

        config = f'{node_name}.yaml'
        ping_lib = PingLibrary(config)

        # Perform ping for a hostname (the full destination ip must be provided)
        results = ping_lib.command('pc1', '10.0.1.1') #TODO: pass these arguments as arguments instead of hard coding


    return f'<p>TEST RESULTS: <br> {results} </p>'