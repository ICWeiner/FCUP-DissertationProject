import requests
import yaml
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
            return

        for project in projects:
            if project['name'] == project_name:
                return project['project_id']

        return
    
    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')

def get_project_nodes(node_ip, project_id):    
    try:

        # GET request to get the project's related nodes parameters
        headers = {'accept': 'application/json'}
        nodes_url = f'http://{node_ip}:3080/v2/projects/{project_id}/nodes'
        response = requests.get(nodes_url, headers=headers)

        response.raise_for_status()

        nodes = response.json()        
        #with open(project_name + '.json', 'w') as file:
        #    json.dump(nodes, file, indent=4)
            
        return nodes

    except requests.exceptions.RequestException as e:
        print(f'Error with IP {node_ip}: {e}')

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
            
def gns3_to_yaml(node_ip, node_name, gns3_obj):
    hosts = {}
    destination_folder = 'inventory/'
    for device in gns3_obj:
        # cloud, nat, ethernet_hub, ethernet_switch,
        # frame_relay_switch, atm_switch, docker, dynamips,
        # vpcs, traceng, virtualbox, vmware, iou, qemu
            
        if 'console' in device and device['console'] is not None:
            platform = None
            port = device['console']

            if device['node_type'] == 'vpcs':
                platform = 'vpcs'
            elif device['node_type'] in ('iou', 'dynamips'):
                if device['name'].startswith('R'):
                    platform = 'cisco_router'
                elif device['name'].startswith('SW'):
                    platform = 'cisco_switch'
            elif device['node_type'] in ('virtualbox', 'vmware', 'qemu', 'docker'):
                platform = 'linuxvm'
                options = device['properties'].get('options', '')
                port = int(options.split(':')[-1].split(',')[0])

            hostname = device['name'].lower()

            host = {
                'hostname': node_ip,
                'port': port,
                'groups': [platform]}

            if platform == 'linuxvm':
                host.update({
                    'username': 'ar',
                    'password': 'admredes23'}#TODO: Remove these hardcoded credentials
                )
            
            hosts[hostname] = host

        output_file = destination_folder + node_name
       
    with open(f'{output_file}.yaml', 'w') as yaml_file:
        yaml.dump(hosts, yaml_file, default_flow_style=False)
    print(f'{output_file}.yaml file has been created successfully.')