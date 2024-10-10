import requests
import constants

headers = { "Content-Type": "application/x-www-form-urlencoded"}

auth = (
    constants.username, constants.password
)

response = requests.post('https://localhost:8006/api2/json/access/ticket', headers=headers , auth=auth, verify=False) #proxmox node currently has a bad cert

print(response.content)