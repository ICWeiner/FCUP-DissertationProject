import requests
from proxmox_api.utils.proxmox_base_uri_generator import proxmox_base_uri
import proxmox_api.utils.constants as constants


def proxmox_connect(proxmox_host, username, password):
    uri = f'{proxmox_base_uri(proxmox_host)}/access/ticket'
    
    headers = { "Content-Type": "application/x-www-form-urlencoded"}

    auth =   {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(uri, headers=headers , data=auth, verify=False)  #TODO:proxmox node currently has a bad cert
    except:
        print("Error: Failure during ticket request")
        exit(1)


    response.raise_for_status()

    try:
        response_data=response.json()
    except ValueError:
        print("Error: Failure during JSON parsing")
        exit(1)
        
    session = requests.Session()

    session.verify = False

    session.cookies.set("PVEAuthCookie", response_data["data"]["ticket"])

    session.headers.update({"CSRFPreventionToken": response_data["data"]["CSRFPreventionToken"]})  

    response = session.get(f'{proxmox_base_uri(proxmox_host)}/nodes/{constants.proxmox_node_name}')

    response.raise_for_status()

    return session