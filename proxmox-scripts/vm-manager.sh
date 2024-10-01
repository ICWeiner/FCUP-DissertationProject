#!/bin/bash

snaptx=$3

function usage () {
    echo
    echo "  - create virtual machines"
    echo "    ./vm-manager.sh create {template-id} {first-clone-id} {hostnames-list-file}"
    echo "  - destroy virtual machines"
    echo "    ./vm-manager.sh destroy {first-vm-id} {last-vm-id}"
    echo "  - start virtual machines"
    echo "    ./vm-manager.sh start {first-vm-id} {last-vm-id}"
    echo "  - stop virtual machines"
    echo "    ./vm-manager.sh stop {first-vm-id} {last-vm-id}"
    echo "  - rollback virtual machines"
    echo "    ./vm-manager.sh rollback {first-vm-id} {last-vm-id}"
    echo "  - get IP addresses of virtual machines"
    echo "    ./vm-manager.sh get-ip {first-vm-id} {last-vm-id} {output-file}"
    echo
}

case $1 in
    create)
        echo
        if [ ! -f "$4" ]; then
            echo "Error: Hostnames list file '$4' does not exist."
            exit 1
        fi

        echo
        echo -n "Creating virtual machines:"
        echo

        initial_id=$3  # Starting VM ID
        current_id=$initial_id

        # Read the hostnames from hosts.txt and create VMs
        while read -r hostname; do
            qm clone $2 ${current_id} --name ${hostname} --full > /dev/null 
            
            echo -n "${hostname} VM (${current_id})created."
            echo 
            
            # Set memory
            qm set ${current_id} --memory 4096

            # Set CPUs
            qm set ${current_id} --sockets 1 --cores 2 --cpu cputype=kvm64

            # Set disk size
            qm resize ${current_id} scsi0 32G

            # Enable QEMU Guest Agent
            qm set ${current_id} --agent enabled=1

            # Set networking
            qm set ${current_id} --net0 virtio,bridge=vmbr0,firewall=1

            # Increment VM ID for the next VM
            current_id=$((current_id + 1))
        done < $4
        echo " done."
        echo
        echo -n "Snapshotting virtual machines:"
        current_id=$initial_id  # Reset to the initial ID for snapshotting
        while read -r hostname; do
            qm snapshot ${current_id} snap01 --description "Initial snapshot."
            echo -n "."
            current_id=$((current_id + 1))
        done < hosts.txt
        echo " done."
        ;;


    destroy)
        echo
        echo -n "Destroying virtual machines:"
        for i in $(seq $2 $3); do
            qm destroy ${i} > /dev/null
            echo -n "."
        done
        echo " done."
        ;;
    start)
        echo
        echo -n "Starting virtual machines:"
        for i in $(seq $2 $3); do
            qm start ${i}
            echo -n "."
        done
        echo " done."
        ;;
    stop)
        echo
        echo -n "Stopping virtual machines:"
        for i in $(seq $2 $3); do
            qm stop ${i}
            echo -n "."
        done
        echo " done."
        ;;
    rollback)
        echo
        echo -n "Rolling back virtual machines:"
        for i in $(seq $2 $3); do
            qm rollback ${i} snap01 > /dev/null
            echo -n "."
        done
        echo " done."
        ;;
    get-ip)
        echo
        echo -n "Getting IP addresses:"
        for i in $(seq $2 $3); do
            hostname=$(qm config ${i} | grep -i name | awk -F ": " '{print $2}')
            ip=$(qm guest exec ${i} -- ip -4 addr show ens18 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
            echo "${i} ${hostname} ${ip}" >> $4
            echo -n "."
        done
        echo " done. IP addresses saved to pmvmips.txt."
        ;;
    *)
        usage
        ;;
esac