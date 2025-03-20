from quart import Blueprint, redirect, request, jsonify
from quart import current_app as app
from quart_login import login_required
from .. import proxmox_tasks #because this is a package, we need to use .. to go up one level


vm_bp = Blueprint(
    'vm_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@vm_bp.route('/vm/<int:vm_proxmox_id>/start', methods=['POST'])
@login_required
async def start_vm(vm_proxmox_id:int):
    if await proxmox_tasks.aset_vm_status(vm_proxmox_id, True): return jsonify(), 200
    else: return jsonify(), 500

@vm_bp.route('/vm/<int:vm_proxmox_id>/stop', methods=['POST'])
@login_required
async def stop_vm(vm_proxmox_id:int):
    if await proxmox_tasks.aset_vm_status(vm_proxmox_id, False): return jsonify(), 200
    else: return jsonify(), 500

@vm_bp.route('/vm/<int:vm_proxmox_id>/delete', methods=['POST'])#TODO: make async
@login_required
async def delete_vm(vm_proxmox_id:int):
    if await proxmox_tasks.adestroy_vm(vm_proxmox_id): return jsonify(), 200
    else: return jsonify(), 500

@vm_bp.route('/vm/<int:vm_proxmox_id>/connect', methods=['POST'])
@login_required
async def connect(vm_proxmox_id:int):
    vm_ip = await proxmox_tasks.aget_vm_ip(vm_proxmox_id)

    return redirect(f'http://{vm_ip}:3080/')

@vm_bp.route('/vm/<int:vm_proxmox_id>/firewall/create', methods=['POST'])#TODO: make async
@login_required
async def start_firewall(vm_proxmox_id:int):
    if await proxmox_tasks.acreate_firewall_rules(vm_proxmox_id, 800): return jsonify(), 200#TODO: unhardcode teacher vm id
    else: return jsonify(), 500

@vm_bp.route('/vm/<int:vm_proxmox_id>/firewall/destroy', methods=['POST'])#TODO: make async
@login_required
async def stop_firewall(vm_proxmox_id:int):
    if await proxmox_tasks.adelete_firewall_rules(vm_proxmox_id): return jsonify(), 200
    else: return jsonify(), 500
