import requests
import constants

headers = { "Content-Type": "application/x-www-form-urlencoded"}

auth =   {
    "username": constants.username,
    "password": constants.password
}

response = requests.post("https://localhost:8006/api2/json/access/ticket", headers=headers , data=auth, verify=False) #proxmox node currently has a bad cert

print(response.content)

print(response)

print(response.json)

print(response.request)