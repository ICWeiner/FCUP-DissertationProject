# Nornir_lib - System for pratical evaluation of network administration 

This library is responsible for interacting with the proxmoxVE API automating some steps of managing proxmoxVE such as turning on/off VM/container

```proxmox_vm_actions``` - contains the following methods:

        create <proxmox_host> <session> <template-id> <clone-id> <hostnames>    
        Clones the specified template VM with the given hostname.
        It then configures memory, CPU, disk size, enables QEMU guest agent and takes a snapshot.

        start <proxmox_host> <session> <vm-id> 
        Starts the specified VM.

        stop <proxmox_host> <session> <vm-id> 
        Stops the specified VM.

        destroy <proxmox_host> <session> <vm-id> 
        Destroys the specified VM.

        rollback <proxmox_host> <session> <vm-id> 
        Rolls back the specified VM to the initial snapshot taken after VM creation.

        <session> is created with the help of "connection" in utils/ 

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
