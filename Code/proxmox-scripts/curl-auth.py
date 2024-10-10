import requests
import constants

headers = {
    'Authorization':f'PVEAPIToken={constants.username}!{constants.password}'
}


response = requests.get('https://localhost:8006/api2/json/nodes/pve1', headers=headers, verify=False) #proxmox node currently has a bad cert

print(response.json())