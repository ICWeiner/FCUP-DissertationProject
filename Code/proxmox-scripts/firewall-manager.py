import requests
import sys
import os
from shlex import quote
from re import search
from utils.connection import proxmox_connect
import utils.constants as constants
from utils.proxmox_vm_ip_fetcher import get_ip

def create_proxmox_vm_isolation_rule(first_vm_id, last_vm_id, allowed_vm_ip, session):
    data = {    
                'comment': 'Restrict student VMs from communicating with each other',
                'source': allowed_vm_ip,
                'action': 'ACCEPT',
                'enable': 1,
                'type': 'in',
            } 
    for current_vm_id in range(first_vm_id, last_vm_id + 1):# TODO:CONTINUAR AQUI, provavelmente 'data' esta mal
        response = session.post(f'{constants.baseuri}/nodes/{current_vm_id}/firewall/rules', data = data)
        print(response)


if __name__ == "__main__":
    
    session = proxmox_connect(constants.username, constants.password)

    student_vms = get_ip(300,301,session)

    teacher_vm = get_ip(800,800,session)

    teacher_vm_ip = teacher_vm[800][0]

    create_proxmox_vm_isolation_rule(300,301,teacher_vm, session)

