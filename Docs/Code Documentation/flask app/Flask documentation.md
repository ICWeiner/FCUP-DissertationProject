# Flask - System for pratical evaluation of network administration 

Inside the folder containing the python code for the flask app you will find various folders.

```inventory```:
This folder contains various files pertinent to the functionality of the evaluation module __nornir_lib__ see its documentation for more details.  

```application```:
This folder contains the various [flask blueprints](https://flask.palletsprojects.com/en/stable/tutorial/views/) that contain the various different parts of the app.  
These blueprints are:  
    
- ```home```:
Contains the initial pages of the app.

- ```profile```:
Contains the various profile pages and functions.

- ```tests```:
Contains the methods that interface with nornir_lib to perform tests on the exercices.

- ```vm```:
Contains the methods that interface with proxmox to manage the work environments.



In the root of this folder you will find __wsgi.py__ which is the entry point for starting the entire flask app.

BEWARE that, in it's current state, the app will add ".." to it's PATH.

In the root of this folder, you will also find config.yaml which is also required by __nornir_lib__ .

Lastly you will find __config.py__ which is responsible for loading a .env located at the same level which must contain a set of values used in the app like:

- ```PROXMOX_HOST``` - The name or ip address of a ProxmoxVE node #NOTE: at this stage this project only supports working with a single node.
- ```PROXMOX_USER``` - A valid username to login on the specificied node e.g "exampleuser@pvenodename".
- ```PROXMOX_PASSWORD``` - The corresponding password for the given user.

