import httpx
import uuid
import logging

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to the console
    ]
)

def _gns3_base_uri(node_ip):
    return f'http://{node_ip}:3080/v2'

def check_project(node_ip, project_id):
    try:
        #GET request to get the project ID

        response = httpx.get(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}',
            headers = {'accept': 'application/json'}
            )
        
        logging.info(f"Checking existence of project {project_id} on {node_ip}.")

        response.raise_for_status()
        
        return True
    
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.HTTPStatusError as err:
        if response.status_code == 404:
            logging.info(f"GNS3 Project {project_id} not found on {node_ip}.")
            return False
        logging.error(f"HTTP error for IP {node_ip}: {err}")
        raise
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

def get_project_id(node_ip, project_name):
    try:
        #GET request to get the project ID

        response = httpx.get(
            f'{_gns3_base_uri(node_ip)}/projects',
            headers = {'accept': 'application/json'}
            )
        
        logging.info(f"Checking ID of project {project_name} on {node_ip}.")

        response.raise_for_status()

        projects = response.json()
        if not projects:
            logging.error(f'No GNS3 projects found for IP {node_ip}')
            return None

        for project in projects:
            if project['name'] == project_name:
                return project['project_id']
    
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return None
    except httpx.HTTPStatusError as err:
        if response.status_code == 404:
            logging.info(f"No GNS3 projects found on {node_ip}.")
            return None  
        logging.error(f"HTTP error for IP {node_ip}: {err}")
        raise  # Re-raise for other HTTP errors (500, etc.)
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

def get_project_nodes(node_ip, project_id):    
    try:
        # GET request to get the project's related nodes parameters
        response = httpx.get(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/nodes',
            headers = {'accept': 'application/json'}
            )
        
        logging.info(f"Getting nodes of project {project_id} on {node_ip}.")

        response.raise_for_status()

        nodes = response.json()  
        #Uncomment to save nodes in a json file      
        #with open(project_name + '.json', 'w') as file:
        #    json.dump(nodes, file, indent=4)
            
        return nodes

    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return None
    except httpx.HTTPStatusError as err:
        if response.status_code == 404:
            logging.info(f"GNS3 project {project_id} not found on {node_ip}.")
            return None
        logging.error(f"HTTP error for IP {node_ip}: {err}")
        raise
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

def start_project(node_ip, project_id):
    try:
        response = httpx.post(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/open',
            headers = {'accept': 'application/json'}
            )
        
        logging.info(f"Opening project {project_id} on {node_ip}.")

        response.raise_for_status()

        response = httpx.post(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/nodes/start',
            headers = {'accept': 'application/json'}
            )
        
        logging.info(f"Starting nodes of project {project_id} on {node_ip}.")

        response.raise_for_status()

        return True
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.HTTPStatusError as err:
        if response.status_code == 404:
            logging.info(f"GNS3 instance {project_id} not found on {node_ip}.")
            return False
        logging.error(f"HTTP error for IP {node_ip}: {err}")
        raise
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

def export_project(node_ip, project_id, filename): #Filename is the name of the file obtained from the response
    try:
        response = httpx.get(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/export',
            headers = {'accept': 'application/json'}
            )
        
        logging.info(f"Exporting project {project_id} on {node_ip}.")

        response.raise_for_status()

        try:
            with open(filename, "wb") as f:
                f.write(response.content)
        except OSError as err:
            print(f"File error: {err}")
            return False
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
            return False
        return True

    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return False
    except httpx.HTTPStatusError as err:
        if response.status_code == 404:
            logging.info(f"GNS3 project {project_id} not found on {node_ip}.")
            return False
        logging.error(f"HTTP error for IP {node_ip}: {err}")
        raise
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise

def import_project(node_ip, filepath):
    try:
        project_id = uuid.uuid4()
            
        fileobj = open(filepath, 'rb')

        filename = filepath.split("/")[-1] #Get the filename from the full path

        logging.info(f"Importing project {project_id} on {node_ip}")

        response = httpx.post(
            f'{_gns3_base_uri(node_ip)}/projects/{project_id}/import',
            headers = {'accept': 'application/json'},
            files = {"archive": (filename, fileobj)}
            )

        response.raise_for_status()

        return project_id
    
    except OSError as err:
        logging.error(f"OSError: {err}")
    except AttributeError as err:
        logging.error(f"Attribute error: {err}")
    except (httpx.ConnectError, httpx.TimeoutException) as err:
        logging.error(f"Network error: {err}")
        return None
    except httpx.HTTPStatusError as err:
        if response.status_code == 404:
            logging.info(f"GNS3 project {project_id} not found on {node_ip}.")
            return None
        logging.error(f"HTTP error for IP {node_ip}: {err}")
        raise
    except httpx.RequestError as err:
        logging.error(f"An ambiguous exception occurred: {err}")
        raise
    return None