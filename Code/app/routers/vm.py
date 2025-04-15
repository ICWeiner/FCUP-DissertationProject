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