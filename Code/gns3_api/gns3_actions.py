import requests
import uuid

def check_project(node_ip, project_id):
    try:
        #GET request to get the project ID
        project_url = f'http://{node_ip}:3080/v2/projects/{project_id}'
        headers = {'accept': 'application/json'}
        response = requests.get(project_url, headers=headers)

        response.raise_for_status()

        if response.status_code != 200:
            print(f'No projects found for IP {node_ip} with project ID {project_id}')
            return False
        
        return True
    
    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def get_project_id(node_ip, project_name):
    try:
        #GET request to get the project ID
        project_url = f'http://{node_ip}:3080/v2/projects'
        headers = {'accept': 'application/json'}
        response = requests.get(project_url, headers=headers)

        response.raise_for_status()

        projects = response.json()
        if not projects:
            print(f'No projects found for IP {node_ip}')
            return False

        for project in projects:
            if project['name'] == project_name:
                return project['project_id']
    
    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def get_project_nodes(node_ip, project_id):    
    try:

        # GET request to get the project's related nodes parameters
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/nodes'
        response = requests.get(nodes_url, headers = headers)

        response.raise_for_status()

        nodes = response.json()  
        #Uncomment to save nodes in a json file      
        #with open(project_name + '.json', 'w') as file:
        #    json.dump(nodes, file, indent=4)
            
        return nodes

    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def start_project(node_ip, project_id):
    try:
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/open'
        response = requests.post(nodes_url, headers = headers)

        response.raise_for_status()

        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/nodes/start'
        response = requests.post(nodes_url, headers = headers)

        response.raise_for_status()

        return True
    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def export_project(node_ip, project_id, filename): #Filename is the name of the file obtained from the response
    try:
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/export'
        response = requests.get(nodes_url, headers = headers)

        response.raise_for_status()

        try:
            with open(filename, "wb") as f:
                f.write(response.content)
        except OSError as e:
            print(f"File error: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        return True

    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
        return False

def import_project(node_ip, filepath):
    try:
        headers = {'accept': 'application/json'}
        
        project_id = uuid.uuid4()
            
        fileobj = open(filepath, 'rb')

        filename = filepath.split("/")[-1]  

        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/import'

        response = requests.post(nodes_url, headers = headers , files = {"archive": (filename, fileobj)})

        response.raise_for_status()

        return project_id
    
    except OSError as e:
        print(f"File error: {e}")
    except AttributeError:
        print("Invalid response object: 'content' attribute missing")
    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
    return None