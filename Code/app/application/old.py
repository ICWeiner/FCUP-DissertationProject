from flask import Flask, render_template, request, make_response
from proxmox.utils import constants as constants
from proxmox.utils.connection import proxmox_connect
from proxmox import proxmox_vm_actions, proxmox_vm_firewall
from proxmox.utils.proxmox_vm_ip_fetcher import get_ip


app = Flask(__name__)

app.config.from_object('config.Config')

@app.route('/')
@app.route("/home")
def hello():
    nav = [
        {'name': 'Start VM 300', 'url': 'http://localhost:5000/api/v1/vm/300/start'},
        {'name': 'Stop VM 301', 'url': 'http://localhost:5000/api/v1/vm/300/stop'}]
    
    return render_template('home.html',
        nav=nav,
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja.")

@app.route('/api/v1/vm/<int:vmid>/start')
def start_vm(vmid):
    session = proxmox_connect(constants.username,constants.password)
    proxmox_vm_actions.start(vmid,vmid,session)
    return f'<p>Starting VM with id {vmid} </p>'

@app.route('/api/v1/vm/<int:vmid>/stop')
def test_stop_vm(vmid):
    session = proxmox_connect(constants.username,constants.password)
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

@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(
        render_template("404.html"),
        404)

@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(
        render_template("400.html"),
        400
    )


@app.errorhandler(500)
def server_error():
    """Internal server error."""
    return make_response(
        render_template("500.html"),
        500
    )

'''@app.route('/api/v1/vm/start', methods = ['POST'])
def test_start_vm():
    if request.method != 'POST':
        return make_response('Malformed request', 400)
    headers = {"Content-Type": "application/json"}
    session = proxmox_connect(constants.username,constants.password)
    proxmox_vm_actions.start(300,301,session)
    return make_response('Starting VMs',200, headers)

@app.route('/api/v1/vm/stop', methods = ['POST'])
def test_stop_vm():
    if request.method != 'POST':
        return make_response('Malformed request', 400)
    headers = {"Content-Type": "application/json"}
    session = proxmox_connect(constants.username,constants.password)
    proxmox_vm_actions.stop(300,301,session)
    return make_response('Stopping VMs',200, headers)

@app.route('/api/v1/firewall/create', methods = ['POST'])
def test_start_firewall():
    if request.method != 'POST':
        return make_response('Malformed request', 400)
    headers = {"Content-Type": "application/json"}
    session = proxmox_connect(constants.username,constants.password)
    teacher_vm = get_ip(800,800,session)
    teacher_vm_ip = teacher_vm[800][0]
    proxmox_vm_firewall.create_proxmox_vm_isolation_rules(300, 301, teacher_vm_ip, session)
    return make_response('Creating firewall rules for VMs',200, headers)

@app.route('/api/v1/firewall/destroy', methods = ['POST'])
def test_stop_firewall():
    if request.method != 'POST':
        return make_response('Malformed request', 400)
    headers = {"Content-Type": "application/json"}
    session = proxmox_connect(constants.username,constants.password)
    proxmox_vm_firewall.delete_proxmox_vm_isolation_rules(300, 301, session)
    return make_response('Destroying firewall rules for VMs',200, headers)'''