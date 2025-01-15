from flask import Blueprint, redirect, request, jsonify
from flask import current_app as app
from flask_login import login_required
import proxmox.proxmox_vm_actions as proxmox_vm_actions
import proxmox.proxmox_vm_firewall as proxmox_vm_firewall
from proxmox.utils.proxmox_vm_ip_fetcher import get_ip
from proxmox.utils.proxmox_base_uri_generator import proxmox_base_uri as proxmox_base_uri
from .proxmox_session import get_proxmox_session



vm_bp = Blueprint(
    'vm_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
#TODO: maybe jsonify is not the correct return for these functions

@vm_bp.route('/vm/<int:template_vm_id>/clone', methods=['POST'])
def create_vm(template_vm_id:int):

    data = request.get_json()

    if 'email' not in data:
        return jsonify(response = "Error: Missing email data.", status = 400)


    session = get_proxmox_session(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    clone_id = proxmox_vm_actions.get_free_id(app.config['PROXMOX_HOST'], session)
    
    hostname = f'gns3-{data["email"]}'

    proxmox_vm_actions.create(app.config['PROXMOX_HOST'], session, template_vm_id,clone_id, hostname)

    response = {'vm_id': clone_id,
                'hostname': hostname}

    return jsonify(response), 201

@vm_bp.route('/vm/<int:vm_id>/start', methods=['POST'])
#@login_required
def start_vm(vm_id:int):
    session = get_proxmox_session(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    proxmox_vm_actions.start(app.config['PROXMOX_HOST'], session, vm_id)
    return jsonify(), 200

@vm_bp.route('/vm/<int:vm_id>/stop', methods=['POST'])
#@login_required
def stop_vm(vm_id:int):
    session = get_proxmox_session(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    proxmox_vm_actions.stop(app.config['PROXMOX_HOST'], session, vm_id)
    return jsonify(), 200

@vm_bp.route('/vm/<int:vm_id>/connect', methods=['POST'])
def connect(vm_id:int):
    session = get_proxmox_session(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])
    vm_ip = get_ip(app.config['PROXMOX_HOST'], session, vm_id)

    return redirect(f'http://{vm_ip}:3080/')

#TODO: REVIEW LOGIC TO APPLY TO ALL VMS OR JUST ONE
@vm_bp.route('/vm/<int:vm_id>/firewall/create', methods=['POST'])
def start_firewall(vm_id:int):
    session = get_proxmox_session(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    teacher_vm = get_ip(app.config['PROXMOX_HOST'],session, 800)#TODO: REVIEW LOGIC TO APPLY TO THE VM THAT BELONGS TO THE GIVEN STUDENT

    teacher_vm_ip = teacher_vm[800][0]

    proxmox_vm_firewall.create_proxmox_vm_isolation_rules(app.config['PROXMOX_HOST'], vm_id, vm_id, teacher_vm_ip, session)

    return jsonify(), 200

#TODO: REVIEW LOGIC TO APPLY TO ALL VMS OR JUST ONE
@vm_bp.route('/vm/<int:vm_id>/firewall/destroy', methods=['POST'])
def stop_firewall(vm_id:int):
    session = get_proxmox_session(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    proxmox_vm_firewall.delete_proxmox_vm_isolation_rules(app.config['PROXMOX_HOST'], vm_id, vm_id, session)#TODO: REVIEW LOGIC TO APPLY TO THE VM THAT BELONGS TO THE GIVEN STUDENT

    return jsonify(), 200

def clone_vm(templatevm_proxmox_id, hostname):
    session = get_proxmox_session(app.config['PROXMOX_HOST'], app.config['PROXMOX_USER'],app.config['PROXMOX_PASSWORD'])

    clone_id = proxmox_vm_actions.get_free_id(app.config['PROXMOX_HOST'], session)

    proxmox_vm_actions.create(app.config['PROXMOX_HOST'], session, templatevm_proxmox_id, clone_id, hostname)

    return clone_id