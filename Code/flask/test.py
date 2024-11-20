from flask import Flask
from proxmox.utils import constants as constants
from proxmox.utils.connection import proxmox_connect
from proxmox import proxmox_vm_actions, proxmox_vm_firewall
from proxmox.utils.proxmox_vm_ip_fetcher import get_ip


app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/api/start')
def test_start_vm():
    session = proxmox_connect(constants.username,constants.password)
    proxmox_vm_actions.start(300,301,session)
    return '<p>Starting VMs 300 and 301</p>'

@app.route('/api/stop')
def test_stop_vm():
    session = proxmox_connect(constants.username,constants.password)
    proxmox_vm_actions.stop(300,301,session)
    return '<p>Stopping VMs 300 and 301</p>'

@app.route('/api/firewall/create')
def test_start_firewall():
    session = proxmox_connect(constants.username,constants.password)

    teacher_vm = get_ip(800,800,session)

    teacher_vm_ip = teacher_vm[800][0]

    proxmox_vm_firewall.create_proxmox_vm_isolation_rules(300, 301, teacher_vm_ip, session)

    return '<p>Creating firewall rules for VMs 300 and 301</p>'

@app.route('/api/firewall/destroy')
def test_stop_firewall():
    session = proxmox_connect(constants.username,constants.password)

    proxmox_vm_firewall.delete_proxmox_vm_isolation_rules(300, 301, session)

    return '<p>Destroying firewall rules for VMs 300 and 301</p>'