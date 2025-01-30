from flask import Blueprint, redirect, request, jsonify
from flask import current_app as app
from flask_login import login_required
import proxmox_api.proxmox_vm_actions as proxmox_vm_actions
import proxmox_api.proxmox_vm_firewall as proxmox_vm_firewall
from proxmox_api.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri
from .proxmox_session import get_proxmox_session
from . import utils
from . import services


vm_bp = Blueprint(
    'vm_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@vm_bp.route('/vm/<int:vm_id>/start', methods=['POST'])
@login_required
def start_vm(vm_id:int):
    if services.start_vm(vm_id): return jsonify(), 200
    else: return jsonify(), 500

@vm_bp.route('/vm/<int:vm_id>/stop', methods=['POST'])
@login_required
def stop_vm(vm_id:int):
    session = get_proxmox_session( *utils._get_proxmox_host_and_credentials())
    if proxmox_vm_actions.stop( utils._get_proxmox_host, session, vm_id): return jsonify(), 200 
    else: return jsonify(), 500

@vm_bp.route('/vm/<int:vm_id>/delete', methods=['POST'])
@login_required
def delete_vm(vm_id:int):
    session = get_proxmox_session( *utils._get_proxmox_host_and_credentials())
    if proxmox_vm_actions.destroy( utils._get_proxmox_host, session, vm_id): return jsonify(), 200
    else: return jsonify(), 500

@vm_bp.route('/vm/<int:vm_id>/connect', methods=['POST'])
@login_required
def connect(vm_id:int):
    vm_ip = services.get_vm_ip(vm_id)

    return redirect(f'http://{vm_ip}:3080/')

@vm_bp.route('/vm/<int:vm_id>/firewall/create', methods=['POST'])
@login_required
def start_firewall(vm_id:int):
    teacher_vm_ip = services.get_vm_ip(800)#TODO: 800 is the ID of the development 'teacher' vm, in the future this should come as an argument

    session = get_proxmox_session( *utils._get_proxmox_host_and_credentials())

    proxmox_vm_firewall.create_proxmox_vm_isolation_rules( utils._get_proxmox_host, vm_id, teacher_vm_ip, session)

    return jsonify(), 200

@vm_bp.route('/vm/<int:vm_id>/firewall/destroy', methods=['POST'])
@login_required
def stop_firewall(vm_id:int):
    session = get_proxmox_session( *utils._get_proxmox_host_and_credentials())

    proxmox_vm_firewall.delete_proxmox_vm_isolation_rules( utils._get_proxmox_host, vm_id, session)#TODO: REVIEW LOGIC TO APPLY TO THE VM THAT BELONGS TO THE GIVEN STUDENT

    return jsonify(), 200
