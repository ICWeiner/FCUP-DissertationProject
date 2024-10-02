import subprocess
import sys
import os
from shlex import quote

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

            subprocess.run(["qm", "clone", template_id, current_clone_id, "--name" , hostname, "--full", ">", "/dev/null"])

            print(f"{hostname} VM ({current_clone_id}) created.\n")

            # Set memory
            subprocess.run(["qm", "set", current_clone_id, "--memory", "4096"])

            # Set CPUs
            subprocess.run(["qm", "set", current_clone_id, "--sockets", "1", "--cores", "2", "--cpu", "cputype=kvm64"])

            # Set disk size
            subprocess.run(["qm", "resize", current_clone_id, "scsi0", "32G"])

            # Enable QEMU Guest Agent
            subprocess.run(["qm", "set", current_clone_id, "--agent", "enabled=1"])

            # Set networking
            subprocess.run(["qm", "set", current_clone_id, "--net0", "virtio,bridge=vmbr0,firewall=1"])

            current_clone_id+=1

    print("Finished creating VMs.\n")

    print("Snapshotting virtual machines\n")

    current_clone_id = first_clone_id

    with open(hostnames_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            hostname = quote(line.strip())

            subprocess.run(["qm", "snapshot", current_clone_id, "snap01", "--description", "Initial snapshot"])
            print(".\n")
            current_clone_id+=1
    print("Finished snapshotting virtual machines\n")
    

if __name__ == "__main__":
    args = sys.argv
    args_length = len(args)

    print(args)
    print(args[2])
    print(args_length)

    if args_length < 2:
        usage()
    elif args_length == 5 and args[1] == 'create':
        template_id = args[2]
        first_clone_id = args[3]
        hostnames_file = args[4]
        create(template_id, first_clone_id, hostnames_file)
    else:
        usage()