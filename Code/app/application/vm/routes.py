from flask import Blueprint, render_template
from flask import current_app as app
#from proxmox.utils.connection import proxmox_connect
#import proxmox.proxmox_vm_actions as proxmox_vm_actions

vm_bp = Blueprint(
    'vm_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@vm_bp.route('/vm/<int:vmid>/start')
def start_vm(vmid):
    session = proxmox_connect(app.config['PROXMOX_USER'],app.config['PROXMOX_USER'])
    proxmox_vm_actions.start(vmid,vmid,session)
    return f'<p>Starting VM with id {vmid} </p>'

@vm_bp.route('/vm/<int:vmid>/stop')
def test_stop_vm(vmid):
    session = proxmox_connect(app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    proxmox_vm_actions.stop(vmid,vmid,session)
    return f'<p>Stopping VM with id {vmid}</p>'

@app.route('/api/v1/firewall/create')
def test_start_firewall():
    session = proxmox_connect(constants.username,constants.password)

    teacher_vm = get_ip(800,800,session)

    teacher_vm_ip = teacher_vm[800][0]

    proxmox_vm_firewall.create_proxmox_vm_isolation_rules(300, 301, teacher_vm_ip, session)

    return '<p>Creating firewall rules for VMs 300 and 301</p>'

@app.route('/api/v1/firewall/destroy')
def test_stop_firewall():
    session = proxmox_connect(constants.username,constants.password)

    proxmox_vm_firewall.delete_proxmox_vm_isolation_rules(300, 301, session)

    return '<p>Destroying firewall rules for VMs 300 and 301</p>'