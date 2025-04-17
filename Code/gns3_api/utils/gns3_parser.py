import json
import yaml
import os

from logger.logger import get_logger

logger = get_logger(__name__)

def gns3_nodes_to_yaml(node_ip, node_name, gns3_devices):
    hosts = {}
    python_path = os.getenv("PYTHONPATH","../..")
    destination_folder = os.path.join(python_path, "inventory")
    for device in gns3_devices:
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

        output_file_path = os.path.join(destination_folder, f"{node_name}.yaml")
       
    with open(output_file_path, 'w') as yaml_file:
        yaml.dump(hosts, yaml_file, default_flow_style=False)
    logger.info(f'{output_file_path} file has been created successfully.')
    return output_file_path



#TODO: this code seems to never be used, should be removed?
# converts gns3 json file to yaml-type host file inventory
def parse_gns3_to_yaml(gns3_path, student_ip, student_mec, destination_folder):
    try:
        hosts = {}
        try:
            with open(gns3_path, 'r') as gns3_file:
                gns3_obj = json.load(gns3_file)
        except FileNotFoundError:
            logger.error(f"GNS3 file {gns3_path} not found.")
            return False
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from the file {gns3_path}.")
            return False

        for node in gns3_obj['topology']['nodes']:
            try:
                if 'console' in node and node['console'] is not None:
                    platform = None
                    port = node['console']

                    if node['name'].startswith('PC'):
                        platform = 'vpcs'
                    elif node['name'].startswith('R'):
                        platform = 'cisco_router'
                    elif node['name'].startswith('SW'):
                        platform = 'cisco_switch'
                    elif node['name'].startswith('Linux'):
                        platform = 'linuxvm'
                        options = node['properties'].get('options', '')
                        port = int(options.split(':')[-1].split(',')[0])

                    hostname = node['name'].lower()

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
                            'password': 'admredes23'#TODO: Remove these hardcoded credentials
                        }

                    hosts[hostname] = host
            except (KeyError, ValueError, AttributeError) as node_error:
                logger.error(f"Error processing node {node['name']}: {str(node_error)}")
                continue

        output_file = destination_folder + student_mec
        try:
            with open(f'{output_file}.yaml', 'w') as yaml_file:
                yaml.dump(hosts, yaml_file, default_flow_style=False)
            logger.info(f"{output_file}.yaml file has been created successfully.")
        except IOError:
            logger.error(f"Failed to write the inventory file {output_file}.yaml.")
            return False

        return True
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return False

# generates each student inventory from the gns3 folder
def generate_inventory(nornir_inventory):
    try:
        for i in nornir_inventory.inventory.hosts.items():
            # 'i' variable is a tuple: ('up20XXXXXX', Host: up20XXXXXX)
            student_ip = nornir_inventory.inventory.hosts[i[0]].hostname
            student_mec = i[0]
            
            gns3_path = "gns3/" + student_mec
            destination_folder = "inventory/"

            success = parse_gns3_to_yaml(gns3_path, student_ip, student_mec, destination_folder)
            if not success:
                logger.warning(f"Failed to create inventory for {student_mec}.")
    except Exception as e:
        logger.error(f"An error occurred during inventory generation: {str(e)}")

