# Proxmox API - System for pratical evaluation of network administration 

This library is responsible for interacting with the proxmoxVE API automating some steps of managing proxmoxVE such as turning on/off VM/container.
Returns boolean unless specified otherwise.
All of these will return False when boolean is expected and None when something else is expected in case of network errors.
Any other exceptions will be propagated and should be caught and treated by the caller.

```proxmox_vm_actions``` - contains the following methods:

        _get_status <proxmox_host> <session> <vm-id> 
        Queries the state of a VM.
        Does not do any check whatsoever, only returns the response.
        Mostly for DRY reasons as it is used a lot, should only be used by the functions in the same file.

        acheck_free_id <proxmox_host> <session> <id>
        Returns a VM/CT ID not currently in use.
        Does not reserve the ID so its only useful if ID is used right away.

        create <proxmox_host> <session> <template-id> <clone-id> <hostnames>    
        Clones the specified template VM with the given hostname.

        check_vm_status <proxmox_host> <session> <vm-id> 
        Checks if VM is up and qemu guest-agent is running.

        check_vm_is_template <proxmox_host> <session> <vm-id> 
        Checks if VM is in template format

        start <proxmox_host> <session> <vm-id> 
        Starts the specified VM.

        stop <proxmox_host> <session> <vm-id> 
        Stops the specified VM.

        template <proxmox_host> <session> <vm-id> 
        Transforms the specified VM into a template

        destroy <proxmox_host> <session> <vm-id> 
        Destroys the specified VM.

        <session> is created with the help of "connection" in utils/ 
        It must contain appropriate credentials for the proxmox cluster


```proxmox_vm_firewall``` - contains the following methods:

        create_proxmox_vm_isolation_rules <proxmox-host> <first-vm-id> <last-vm-id> <allowed-vm-ip> <session>
        Activates the proxmox firewall at the datacenter, node and vm levels.
        Creates firewall rules to disable communication between "student" VMs, they may only
        communicate with the designated IP, typically the "teacher" VM.

        delete_proxmox_vm_isolation_rules <proxmox-host> <first-vm-id> <last-vm-id> <allowed-vm-ip> <session>
        Deactivates the proxmox firewall at the datacenter, node and vm levels.
        Deletes firewall rules enabling full internet access and communication between VMs.

```utils``` - Contains various utilities such as:  
- ```connection.proxmox_connect```: Given the necessary data to connect and authenticate to a proxmoxVE node given [here](../flask%20app/Flask%20documentation.md#) returns an HTTP session with an authentication cookie that is valid for a certain period of time.
Check proxmoxVE authentication documentation for more details.
- ```proxmox_base_uri_generator```: Generates the base part of the uri for the proxmoxAPI.
- ```proxmox_vm_ip_fetcher```: Given a VM/container ID returns their current ip address or hostname.
