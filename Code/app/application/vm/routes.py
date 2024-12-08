from flask import Blueprint, render_template, redirect
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


@vm_bp.route('/vm/<int:vm_id>/start')
def start_vm(vm_id:int):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    proxmox_vm_actions.start(app.config['PROXMOX_HOST'], session, vm_id)
    return f'<p>Starting VM with id {vm_id} </p>'

@vm_bp.route('/vm/<int:vm_id>/stop')
def stop_vm(vm_id:int):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    proxmox_vm_actions.stop(app.config['PROXMOX_HOST'], session, vm_id)
    return f'<p>Stopping VM with id {vm_id}</p>'

@vm_bp.route('/vm/<int:vm_id>/connect')
def connect(vm_id:int):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    vm_ip = get_ip(app.config['PROXMOX_HOST'], session, vm_id)

    return redirect(f'http://{vm_ip}:3080/')

#TODO: REVIEW LOGIC TO APPLY TO ALL VMS OR JUST ONE
@vm_bp.route('/vm/<int:vm_id>/firewall/create')
def start_firewall(vm_id:int):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    teacher_vm = get_ip(app.config['PROXMOX_HOST'],session, 800)

    teacher_vm_ip = teacher_vm[800][0]

    proxmox_vm_firewall.create_proxmox_vm_isolation_rules(app.config['PROXMOX_HOST'], vm_id, vm_id, teacher_vm_ip, session)

    return '<p>Creating firewall rules for VMs 300 and 301</p>'

@vm_bp.route('/vm/<int:vm_id>/firewall/destroy')
def stop_firewall(vm_id:int):
    session = proxmox_connect(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    proxmox_vm_firewall.delete_proxmox_vm_isolation_rules(app.config['PROXMOX_HOST'], vm_id, vm_id, session)

    return '<p>Destroying firewall rules for VMs 300 and 301</p>'