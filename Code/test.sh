#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 {template-id} {new-vm-id}"
    exit 1
fi

# Assign arguments to variables
template_id=$1
new_vm_id=$2

# Clone the VM
qm clone $template_id $new_vm_id --name mac-test --full > /dev/null

# Set memory
qm set $new_vm_id --memory 4096 > /dev/null

# Set CPUs
qm set $new_vm_id --sockets 1 --cores 2 --cpu cputype=kvm64 > /dev/null

# Set disk size
qm resize $new_vm_id scsi0 32G > /dev/null

# Enable QEMU Guest Agent
qm set $new_vm_id --agent enabled=1 > /dev/null

# Generate a valid MAC address
fixed_prefix="02:42:ac:11"
mac_suffix=$(printf "%04X" $new_vm_id)
mac="${fixed_prefix}:00:${mac_suffix}"

# Set networking with the generated MAC address
qm set $new_vm_id --net0 virtio,bridge=vmbr1,firewall=1,macaddr=${mac} > /dev/null

echo "VM creation and configuration complete."