from nornir import InitNornir
from utils.gns3_api import get_project_id, get_project_nodes, start_project, gns3_to_yaml
from modules.ping import PingLibrary
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result

# Initialize Nornir
try:
    nr = InitNornir(config_file='config.yaml')
except Exception as e:
    print(f'Failed to initialize Nornir: {str(e)}')
    exit(1)

project_name = 'test'

linux_hosts = nr.filter(F(name__startswith='up2') & F(platform__eq='linux'))


for i in linux_hosts.inventory.hosts.items(): 
    
    node_ip = linux_hosts.inventory.hosts[i[0]].hostname 
    print(f'student ip is : {node_ip}')

    node_name = i[0] 
    print(f'student mec number is : {node_name}')

    project_id = get_project_id(node_ip, project_name)

    nodes = get_project_nodes(node_ip, project_id) #Get info on given project's nodes

    gns3_to_yaml(node_ip, node_name, nodes) #Convert info into a format readable by nornir

    start_project(node_ip, project_id)

    config = f'{node_name}.yaml'
    ping_lib = PingLibrary(config)

    # Perform ping for a hostname (the full destination ip must be provided)
    ping_results = ping_lib.command('pc1', '10.0.1.1')
    print('Ping Results:', ping_results)
    