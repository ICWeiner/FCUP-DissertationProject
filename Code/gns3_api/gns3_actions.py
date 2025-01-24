import requests
import json

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

        return False
    
    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
        return False

def get_project_nodes(node_ip, project_id):    
    try:

        # GET request to get the project's related nodes parameters
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/nodes'
        response = requests.get(nodes_url, headers=headers)

        response.raise_for_status()

        nodes = response.json()  
        #Uncomment to save nodes in a json file      
        #with open(project_name + '.json', 'w') as file:
        #    json.dump(nodes, file, indent=4)
            
        return nodes

    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
        return False

def start_project(node_ip, project_id):
    try:
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/open'
        response = requests.post(nodes_url, headers=headers)

        response.raise_for_status()

        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/nodes/start'
        response = requests.post(nodes_url, headers=headers)

        response.raise_for_status()

        return True

    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
        return False

def export_project(node_ip, project_id):
    try:
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/export'
        response = requests.get(nodes_url, headers=headers)

        response.raise_for_status()

        return True

    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
        return False

def import_project(node_ip, project_id, file):
    try:
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/import'
        response = requests.post(nodes_url, headers=headers , files = file)

        response.raise_for_status()

        return True

    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')
        return False