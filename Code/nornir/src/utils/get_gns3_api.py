import requests
import yaml
import json

def get_project(gns3_path, student_ip):    
    try:
        # First GET request to get the project ID
        project_url = f"http://{student_ip}:3080/v2/projects"
        headers = {"accept": "application/json"}
        response = requests.get(project_url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        projects = response.json()
        if not projects:
            print(f"No projects found for IP {student_ip}")
            return

        project_id = projects[0]['project_id']  # Assuming we need the first project's ID

        # Second GET request to get the project's related nodes parameters
        nodes_url = f"http://{student_ip}:3080/v2/projects/{project_id}/nodes"
        response = requests.get(nodes_url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        nodes = response.json()        
        with open(gns3_path + ".json", 'w') as file:
            json.dump(nodes, file, indent=4)
            
        print(f"Nodes parameters for project {project_id} on IP {student_ip}:")
        return nodes

    except requests.exceptions.RequestException as e:
        print(f"Error with IP {student_ip}: {e}")
            
def gns3_to_yaml(gns3_obj, student_ip, student_mec):
    hosts = {}
    destination_folder = "inventory/"
    for device in gns3_obj:
            
        if 'console' in device and device['console'] is not None:
            platform = None
            port = device['console']

            if device['name'].startswith('PC'):
                platform = 'vpcs'
            elif device['name'].startswith('R'):
                platform = 'cisco_router'
            elif device['name'].startswith('SW'):
                platform = 'cisco_switch'
            elif device['name'].startswith('Linux'):
                platform = 'linuxvm'
                options = device['properties'].get('options', '')
                port = int(options.split(':')[-1].split(',')[0])

            hostname = device['name'].lower()

            if platform != 'linuxvm':
                host = {
                    'hostname': student_ip,
                    'port': port,
                    'groups': [platform]
                }
            else:
                host = {
                    'hostname': student_ip,
                    'port': port,
                    'groups': [platform],
                    'username': 'ar',
                    'password': 'admredes23'
                }
            hosts[hostname] = host

        output_file = destination_folder + student_mec
       
    with open(f'{output_file}.yaml', 'w') as yaml_file:
        yaml.dump(hosts, yaml_file, default_flow_style=False)
    print(f"{output_file}.yaml file has been created successfully.")