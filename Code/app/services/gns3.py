from gns3_api import gns3_actions
from gns3_api.utils import gns3_parser
from time import sleep #TODO, change to async?

def import_gns3_project(node_ip, path_to_gns3project):#TODO: decide if async or not 
    gns3_project_id = gns3_actions.import_project(node_ip, path_to_gns3project)
    sleep(10) #GNS3 will immediately answer 200 OK , even though project has not actually finished importing
    return gns3_project_id

def setup_gns3_project(node_ip, gns3_project_id, node_hostname):#This function should be called before running nornir commands against a VM
    gns3_actions.start_project(node_ip, gns3_project_id)
    sleep(10)
    # Get project nodes information
    nodes = gns3_actions.get_project_nodes(node_ip, gns3_project_id)
    # Convert GNS3 nodes to YAML for Nornir processing
    gns3_config_filename = gns3_parser.gns3_nodes_to_yaml(node_ip, node_hostname, nodes)

    return gns3_config_filename
