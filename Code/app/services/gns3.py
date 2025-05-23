from gns3_api import gns3_actions
from gns3_api.utils import gns3_parser
import asyncio 

#TODO: these function might need retry mechanisms
async def import_gns3_project(node_ip: str, path_to_gns3project: str) -> str:
    gns3_project_id = await gns3_actions.aimport_project(node_ip, path_to_gns3project)

    await asyncio.sleep(10) #GNS3 will immediately answer 200 OK , even though project has not actually finished importing

    return gns3_project_id

async def setup_gns3_project(node_ip: str, gns3_project_id: str, node_hostname: str) -> str:#This function should be called before running nornir commands against a VM
    await gns3_actions.start_project(node_ip, gns3_project_id)

    await asyncio.sleep(10)

    # Get project nodes information
    nodes = await gns3_actions.aget_project_nodes(node_ip, gns3_project_id)
    
    # Convert GNS3 nodes to YAML for Nornir processing
    gns3_config_filename = gns3_parser.gns3_nodes_to_yaml(node_ip, node_hostname, nodes)

    return gns3_config_filename
