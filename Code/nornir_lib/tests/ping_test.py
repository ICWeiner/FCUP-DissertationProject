from nornir import InitNornir
from gns3_api import gns3_actions
from gns3_api.utils.gns3_parser import gns3_nodes_to_yaml
from nornir_lib.modules.ping import PingModule
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

# Initialize Nornir
def ping(target_vm, gns3_filename, command_host, command_target):
    try:
        nr = InitNornir(config_file='config.yaml')
    except Exception as e:
        print(f'Failed to initialize Nornir: {str(e)}')
        exit(1)


    linux_hosts = nr.filter(F(name__startswith = target_vm) & F(platform__eq = 'linux'))


    for i in linux_hosts.inventory.hosts.items(): 
        
        node_ip = linux_hosts.inventory.hosts[i[0]].hostname 
        print(f'student ip is : {node_ip}')

        node_name = i[0] 
        print(f'student mec number is : {node_name}')

        project_id = gns3_actions.get_project_id(node_ip, gns3_filename)

        nodes = gns3_actions.get_project_nodes(node_ip, project_id) #Get info on given project's nodes

        gns3_nodes_to_yaml(node_ip, node_name, nodes) #Convert info into a format readable by nornir

        gns3_actions.start_project(node_ip, project_id)

        config = f'{node_name}.yaml'
        ping_lib = PingModule(config)

        # Perform ping for a hostname (the full destination ip must be provided)
        ping_results = ping_lib.command(command_host, command_target)
        return ping_results
    