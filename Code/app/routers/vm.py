from pydantic import BaseModel

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from app.services import proxmox as proxmox_services
from app.dependencies.auth import ValidateVmOwnershipDep, CurrentUserDep

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
async def start_vm(
    vm_proxmox_id: int,
    current_user: CurrentUserDep,
    workvm: ValidateVmOwnershipDep
    ):
    
    success = await proxmox_services.aset_vm_status(current_user, vm_proxmox_id, True)
    
    if success:
        return {"message": "VM started successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to start VM"
            )
    
@router.post("/{vm_proxmox_id}/stop")
async def stop_vm(
    vm_proxmox_id: int,
    current_user: CurrentUserDep,
    workvm: ValidateVmOwnershipDep
    ):

    success = await proxmox_services.aset_vm_status(current_user, vm_proxmox_id, False)
    
    if success:
        return {"message": "VM stopped successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to stop VM"
            )
    
@router.post("/{vm_proxmox_id}/destroy")
async def destroy_vm(
    vm_proxmox_id: int,
    current_user: CurrentUserDep,
    workvm: ValidateVmOwnershipDep
    ):

    success = await proxmox_services.adestroy_vm(current_user, vm_proxmox_id)
    
    if success:
        return {"message": "VM destroyed successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to destroy VM"
            )
    
@router.post("/{vm_proxmox_id}/connect")
async def connect_vm(
    vm_proxmox_id: int,
    current_user: CurrentUserDep,
    workvm: ValidateVmOwnershipDep,
    request: Request
    ):

    vm_ip = await proxmox_services.aget_vm_ip(current_user, vm_proxmox_id)
    
    if vm_ip:
        response = RedirectResponse(
            url=f'http://{vm_ip}:3080/',
            status_code=303)
        response.headers["Access-Control-Allow-Origin"] = str(request.base_url)
        return response
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to VM"
            )
    
@router.post("/{vm_proxmox_id}/firewall/create")
async def start_vm_firewall(
    request: Request,
    vm_proxmox_id: int,
    current_user: CurrentUserDep,
    workvm: ValidateVmOwnershipDep
    ):

    client_ip = request.client.host
    success = await proxmox_services.acreate_firewall_rules(current_user, vm_proxmox_id, 800, client_ip)#remove hardcoded 800 id, should be the id of the fastapi host
    
    if success:
        return {"message": "VM firewall created successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to create VM firewall"
            )
    
@router.post("/{vm_proxmox_id}/firewall/destroy")
async def stop_vm_firewall(
    vm_proxmox_id: int,
    current_user: CurrentUserDep,
    workvm: ValidateVmOwnershipDep
    ):
    
    success = await proxmox_services.adestroy_firewall_rules(current_user, vm_proxmox_id)

    if success:
        return {"message": "VM firewall destroyed successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to destroy VM firewall"
            )