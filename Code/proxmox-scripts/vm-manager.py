import subprocess
import sys
import os
from shlex import quote
from re import search

def usage():
    print("""Usage: python vm_manager.py [OPTION]
          
          create <template-id> <first-clone-id> <hostnames-list-file>    
          Clones the specified template VM for each hostname listed in a given file 
          and the starting ID number.
          It then configures memory, CPU, disk size, enables QEMU guest agent and takes a snapshot.

          start <first-vm-id> [last-vm-id]
          Starts the specified VMs.

          stop <first-vm-id> [last-vm-id]
          Stops the specified VMs.

          destroy <first-vm-id> [last-vm-id]
          Destroys the specified VMs.
        
          rollback <first-vm-id> [last-vm-id]
          Rolls back the specifiedVM to the initial snapshot taken after VM creation.

          get-ip <first-vm-id> [last-vm-id] <output-file>
          Retrieves the IP address of each running VM and saves the associated ID, hostname and 
          IP address to the specified file.
          """)
    
def create(template_id, first_clone_id, hostnames_file):
    if not os.path.exists(hostnames_file):
        print(f"Error: Hostnames list file '{hostnames_file}' does not exist.")
        return 1
    print("\nCreating virtual machines:\n")

    current_clone_id = first_clone_id

    with open(hostnames_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            hostname = quote(line.strip())

            subprocess.run(["qm", "clone", str(template_id), str(current_clone_id), "--name" , hostname, "--full", ">", "/dev/null"])

            print(f"{hostname} VM ({current_clone_id}) created.\n")

            subprocess.run(["qm", "set", str(current_clone_id), "--memory", "4096"])

            subprocess.run(["qm", "set", str(current_clone_id), "--sockets", "1", "--cores", "2", "--cpu", "cputype=kvm64"])

            subprocess.run(["qm", "resize", str(current_clone_id), "scsi0", "32G"])

            subprocess.run(["qm", "set", str(current_clone_id), "--agent", "enabled=1"])

            subprocess.run(["qm", "set", str(current_clone_id), "--net0", "virtio,bridge=vmbr0,firewall=1"])

            current_clone_id+=1

    print("""Finished creating VMs.\n
          Snapshotting virtual machines\n""")

    current_clone_id = first_clone_id

    with open(hostnames_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            hostname = quote(line.strip())

            subprocess.run(["qm", "snapshot", str(current_clone_id), "snap01", "--description", "Initial snapshot"])
            print(".\n")
            current_clone_id+=1
    print("Finished snapshotting virtual machines\n")
    
def start(first_vm_id, last_vm_id):
    print("Starting virtual machines...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        print(f"Starting virtual machine with ID {current_vm_id}\n")
        subprocess.run(["qm", "start", str(current_vm_id)])
    print("Done")

def stop(first_vm_id, last_vm_id):
    print("Stoping virtual machines...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        print(f"Stopping virtual machine with ID {current_vm_id}\n")
        subprocess.run(["qm", "stop", str(current_vm_id)])
    print("Done")

def destroy(first_vm_id, last_vm_id):
    print("Destroying virtual machines...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        print(f"Destroying virtual machine with ID {current_vm_id}\n")
        subprocess.run(["qm", "destroy", str(current_vm_id), ">", "/dev/null"])
    print("Done")

def rollback(first_vm_id, last_vm_id):
    print("Rolling back virtual machines to initial state...\n")

    for current_vm_id in range(first_vm_id, last_vm_id + 1):
        print(f"Rolling back virtual machine with ID {current_vm_id}\n")
        subprocess.run(["qm", "rollback", str(current_vm_id), "snap01", ">", "/dev/null"])
    print("Done")

def get_ip(first_vm_id, last_vm_id):
    def retrieve_hostname(vm_id):
        #retrieve hostname from vm config using the respective ID
        output = subprocess.run(["qm", "config", str(vm_id)], capture_output=True, text=True)
        for line in output.stdout.splitlines():
            if "name:" in line.lower():
                name = line.split(": ")[1]
                return name
        return None
    def retrieve_ip(vm_id):
        #retrieve ip from interface ens18
        output = subprocess.run(["qm", "guest", "exec", str(vm_id), "--", "ip", "-4", "addr", "show", "ens18"], capture_output=True, text=True)
        for line in output.stdout.splitlines():
            match = search(r"inet\s(\d+\.\d+\.\d+\.\d+)", line)
            if match:
                return match.group(1)
        return None
    
    print("Getting IP addresses\n")

    current_vm_id = first_vm_id
    with open("output.txt", "w") as file:
        for current_vm_id in last_vm_id:
            file.write(f"Hostname: {retrieve_hostname} IP: {retrieve_ip}\n")
    print("IP addresses saved to pmvmips.txt")
        
        
        

if __name__ == "__main__":
    args = sys.argv
    args_length = len(args)

    if args_length == 5 and args[1] == 'create':
        template_id = args[2]
        first_clone_id = args[3]
        hostnames_file = args[4]
        create(template_id, first_clone_id, hostnames_file)
    elif args_length > 2 and args_length < 6 :
        first_vm_id = int(args[2])
        last_vm_id = int(args[3]) if args_length == 4 else first_vm_id
        if args[1] == 'start':
            start(first_vm_id, last_vm_id)
        elif args[1] == 'stop':
            stop(first_vm_id, last_vm_id)
        elif args[1] == 'destroy':
            destroy(first_vm_id, last_vm_id)
        elif args[1] == 'rollback':
            rollback(first_vm_id, last_vm_id)
        elif args[1] == 'get-ip':
            output_file = args[4] if args_length == 5 else args[3]
            get_ip(first_vm_id, last_vm_id, output_file)
        else :
            usage()
    else:
        usage()
