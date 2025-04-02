from pydantic import BaseModel
from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from gns3_api import gns3_actions
from gns3_api.utils import gns3_parser
from app.services import proxmox as proxmox_services
from nornir_lib.modules.ping import PingLibrary
from nornir_lib.modules.traceroute import TracerouteLibrary 

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

router = APIRouter(prefix="/vm",
                    tags=["vms"],
                    responses={404: {"description": "Not found"}})

templates = Jinja2Templates(directory=str(BASE_DIR / "templates/"))

class TestRequest(BaseModel):
    hostname: str
    ip_address: str

@router.post("/{vm_proxmox_id}/start")
async def start_vm(vm_proxmox_id: int):
    success = await proxmox_services.aset_vm_status(vm_proxmox_id, True)
    
    if success:
        return JSONResponse(content={"message": "VM started successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="Failed to start VM")
    
@router.post("/{vm_proxmox_id}/stop")
async def stop_vm(vm_proxmox_id: int):
    success = await proxmox_services.aset_vm_status(vm_proxmox_id, False)
    
    if success:
        return JSONResponse(content={"message": "VM stopped successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="Failed to stop VM")
    
@router.post("/{vm_proxmox_id}/destroy")
async def destroy_vm(vm_proxmox_id: int):
    success = await proxmox_services.adestroy_vm(vm_proxmox_id)
    
    if success:
        return JSONResponse(content={"message": "VM destroyed successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="Failed to destroy VM")
    
@router.post("/{vm_proxmox_id}/connect")
async def connect_vm(vm_proxmox_id: int):
    vm_ip = await proxmox_services.aget_vm_ip(vm_proxmox_id)
    
    if vm_ip:
        return RedirectResponse(url=f'http://{vm_ip}:3080/')
    else:
        raise HTTPException(status_code=500, detail="Failed to connect to VM")
    
@router.post("/{vm_proxmox_id}/firewall/create")
async def start_vm_firewall(vm_proxmox_id: int):
    success = await proxmox_services.acreate_firewall_rules(vm_proxmox_id, 800)#remove hardcoded 800 id, should be the id of the fastapi host
    
    if success:
        return JSONResponse(content={"message": "VM firewall created successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="Failed to create VM firewall")
    
@router.post("/{vm_proxmox_id}/firewall/destroy")
async def stop_vm_firewall(vm_proxmox_id: int):
    success = await proxmox_services.adestroy_firewall_rules(vm_proxmox_id)

    if success:
        return JSONResponse(content={"message": "VM firewall destroyed successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail="Failed to destroy VM firewall")

@router.post("/{vm_proxmox_id}/test/ping")
async def ping(vm_proxmox_id: int,
                data: Annotated[TestRequest, Form()],
                #current_user: CurrentUserDep,
               ):
    hostname = data.hostname  
    target = data.ip_address

    gns3_filename = "test"  # TODO: pass this as an argument
        
    vm_ip = await proxmox_services.aget_vm_ip(vm_proxmox_id)
    print(f"Student IP is: {vm_ip}")

    vm_hostname = await proxmox_services.aget_vm_hostname(vm_proxmox_id)
    print(f"Student VM hostname is: {vm_hostname}")

    project_id = gns3_actions.get_project_id(vm_ip, gns3_filename)
    print(f"Project ID is: {project_id}")

    nodes = gns3_actions.get_project_nodes(vm_ip, project_id)  # Get project nodes info

    gns3_parser.gns3_nodes_to_yaml(vm_ip, vm_hostname, nodes)  # Convert info for Nornir

    gns3_actions.start_project(vm_ip, project_id)
    print("Project started")

    config = f"{vm_hostname}.yaml"
    ping_lib = PingLibrary(config)
    print("Ping library initialized")

    # Perform ping for a hostname
    results = ping_lib.command(hostname, target)  # Now using arguments dynamically
    print("Ping command executed")

    return {"test_results": results}

@router.post("/{vm_proxmox_id}/test/traceroute")#The below code is a near copy of the ping route
async def traceroute(vm_proxmox_id: int,
                data: Annotated[TestRequest, Form()],
                #current_user: CurrentUserDep,
               ):

    hostname = data.hostname  # Now using Pydantic model
    target = data.ip_address

    gns3_filename = "test"  # TODO: pass this as an argument
        
    vm_ip = proxmox_services.aget_vm_ip(vm_proxmox_id)
    print(f"Student IP is: {vm_ip}")

    vm_hostname = proxmox_services.aget_vm_hostname(vm_proxmox_id)
    print(f"Student VM hostname is: {vm_hostname}")

    project_id = gns3_actions.get_project_id(vm_ip, gns3_filename)
    print(f"Project ID is: {project_id}")

    nodes = gns3_actions.get_project_nodes(vm_ip, project_id)  # Get project nodes info

    gns3_parser.gns3_nodes_to_yaml(vm_ip, vm_hostname, nodes)  # Convert info for Nornir

    gns3_actions.start_project(vm_ip, project_id)
    print("Project started")

    config = f"{vm_hostname}.yaml"
    traceroute_lib = TracerouteLibrary(config)
    print("Ping library initialized")

    # Perform traceroute for a hostname
    results = traceroute_lib.command(hostname, target)
    print("Traceroute command executed")

    return {"test_results": results}