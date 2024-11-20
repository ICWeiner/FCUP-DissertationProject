import requests
import proxmox.utils.constants as constants

def proxmox_connect(username, password):
    uri = f'{constants.baseuri}/access/ticket'
    
    headers = { "Content-Type": "application/x-www-form-urlencoded"}

    auth =   {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(uri, headers=headers , data=auth, verify=False)  #proxmox node currently has a bad cert
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

    response = session.get(f'{constants.baseuri}/nodes/pve1')

    return session