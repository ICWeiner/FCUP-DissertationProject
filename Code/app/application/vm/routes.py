from flask import Blueprint, render_template
from flask import current_app as app
from proxmox.utils.connection import proxmox_connect
from proxmox.utils.proxmox_vm_ip_fetcher import get_ip
import proxmox.proxmox_vm_actions as proxmox_vm_actions
import proxmox.proxmox_vm_firewall as proxmox_vm_firewall


vm_bp = Blueprint(
    'vm_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@vm_bp.route('/vm/<int:vmid>/start')
def start_vm(vmid):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    proxmox_vm_actions.start(app.config['PROXMOX_HOST'], vmid,vmid,session)
    return f'<p>Starting VM with id {vmid} </p>'

@vm_bp.route('/vm/<int:vmid>/stop')
def stop_vm(vmid):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    proxmox_vm_actions.stop(app.config['PROXMOX_HOST'], vmid,vmid,session)
    return f'<p>Stopping VM with id {vmid}</p>'

#TODO: REVIEW LOGIC TO APPLY TO ALL VMS OR JUST ONE
@vm_bp.route('/vm/<int:vmid>/firewall/create')
def start_firewall(vmid):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    teacher_vm = get_ip(app.config['PROXMOX_HOST'], 800,800,session)

    teacher_vm_ip = teacher_vm[800][0]

    proxmox_vm_firewall.create_proxmox_vm_isolation_rules(app.config['PROXMOX_HOST'], vmid, vmid, teacher_vm_ip, session)

    return '<p>Creating firewall rules for VMs 300 and 301</p>'

@vm_bp.route('/vm/<int:vmid>/firewall/destroy')
def stop_firewall(vmid):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    proxmox_vm_firewall.delete_proxmox_vm_isolation_rules(app.config['PROXMOX_HOST'], vmid, vmid, session)

    return '<p>Destroying firewall rules for VMs 300 and 301</p>'