# Flask - System for pratical evaluation of network administration 

## Interaction with ProxmoxVE

To interact with Proxmox, a series of endpoints were implemented that use functions imported from ```Code/proxmox```
Proxmox's API requires proper authentication for most of its endpoints and so to minimize the amount of times the user's credentials have to be sent, proxmox implements what is know as 'Ticket Cookie', hereafter refered to as a Ticket.
A Ticket can be acquired by sending a POST request to the correct endpoint, with the body containing valid user credentials.
This Ticket, by default, is valid for a period of 2 hours since being issued.
In an attempt to reduce the amount of requests sent, the Flask app will store the Ticket in memory for a period slightly shorter than its validicity.
To obtain this Ticket in the context of the flask app, please use the function ```get_proxmox_session``` found in ```utils.py``` under the ```vm``` blueprint.
This function will return a ```Session``` object with all required configurations needed by the proxmox library functions.