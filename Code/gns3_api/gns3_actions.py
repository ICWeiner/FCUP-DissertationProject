import httpx
import uuid

from typing import Optional

from gns3_api import decorators

from logger.logger import get_logger

logger = get_logger(__name__)


def _gns3_base_uri(node_ip):
    return f'http://{node_ip}:3080/v2'

@decorators.handle_network_errors
async def acheck_project(node_ip: str, project_id: str) -> bool:    
    logger.info(f"Checking existence of project {project_id} on {node_ip}")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}',
            headers={'accept': 'application/json'}
        )
    
    response.raise_for_status()
    return True

@decorators.handle_network_errors
async def aget_project_id(node_ip: str, project_name: str) -> Optional[str]:
    logger.info(f"Fetching project id of project {project_name} on {node_ip}.")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{_gns3_base_uri(node_ip)}/projects',
            headers={'accept': 'application/json'}
        )

    projects = response.json()
    if not projects:
        logger.error(f'No GNS3 projects found for IP {node_ip}')
        return None

    for project in projects:
        if project['name'] == project_name:
            return project['project_id']
    

@decorators.handle_network_errors
async def aget_project_nodes(node_ip, project_id) -> str:    
    logger.info(f"Getting nodes of project {project_id} on {node_ip}.")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/nodes',
            headers = {'accept': 'application/json'}
            )
        
    response.raise_for_status()

    nodes = response.json()  
    #Uncomment to save nodes in a json file      
    #with open(project_name + '.json', 'w') as file:
    #    json.dump(nodes, file, indent=4)
        
    return nodes

@decorators.handle_network_errors
async def start_project(node_ip, project_id) -> bool:
    logger.info(f"Opening project {project_id} on {node_ip}.")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/open',
            headers = {'accept': 'application/json'}
            )
        
    response.raise_for_status()

    response = httpx.post(
        f'{_gns3_base_uri(node_ip)}/projects/{project_id}/nodes/start',
        headers = {'accept': 'application/json'}
        )
    
    logger.info(f"Starting nodes of project {project_id} on {node_ip}.")

    response.raise_for_status()

    return True

@decorators.handle_network_errors
async def aexport_project(node_ip: str, project_id: str, filename: str) -> Optional[bool]:
    logger.info(f"Exporting project {project_id} on {node_ip}.")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/export',
            headers = {'accept': 'application/json'}
            )

    response.raise_for_status()

    try:
        with open(filename, "wb") as f:
            f.write(response.content)
    except OSError as err:
        logger.error(f"File error: {err}")
        return False
    except Exception as err:
        logger.error(f"An unexpected error occurred: {err}")
        return False
    return True


@decorators.handle_network_errors
async def aimport_project(node_ip: str, filepath:str):
    project_id = uuid.uuid4()

    try:
        fileobj = open(filepath, 'rb')
    except OSError as err:
        logger.error(f"OSError: {err}")
        return None
    except AttributeError as err:
        logger.error(f"Attribute error: {err}")
        return None

    filename = filepath.split("/")[-1] #Get the filename from the full path

    logger.info(f"Importing project {project_id} on {node_ip}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/import',
            headers = {'accept': 'application/json'},
            files = {"archive": (filename, fileobj)}
            )

    response.raise_for_status()

    return project_id


