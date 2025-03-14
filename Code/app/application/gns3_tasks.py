from gns3_api import gns3_actions
from gns3_api.utils import gns3_parser
from nornir_lib.modules.generic import GenericLibrary 
from time import sleep

def import_gns3_project(node_ip, path_to_gns3project):#TODO: decide if async or not 
    gns3_project_id = gns3_actions.import_project(node_ip, path_to_gns3project)
    sleep(10)
    return gns3_project_id

def run_gns3_commands(node_ip, gns3_project_id, hostname,  commands_by_hostname):#TODO: decide if async or not 
    """Execute provided commands on the GNS3 project"""
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
