import httpx
from fastapi import Depends
from typing import Annotated, Optional
from app.services import auth as auth_services
from app.services import proxmox_auth as proxmox_auth_services
from app.models import UserPublic, WorkVm


CurrentUserDep = Annotated[UserPublic, Depends(auth_services.get_current_user)]


PrivilegedUserDep = Annotated[UserPublic, Depends(auth_services.require_privileged_user)]


ValidateVmOwnershipDep = Annotated[WorkVm, Depends(auth_services.validate_vm_ownership)]


def _get_session_manager() -> proxmox_auth_services.ProxmoxSessionManager:
    return proxmox_auth_services.ProxmoxSessionManager()

ProxmoxSessionManagerDep = Annotated[proxmox_auth_services.ProxmoxSessionManager, Depends(_get_session_manager)]


async def _require_authenticated_session(
    user: UserPublic = CurrentUserDep,  # Your existing user dependency
    session_manager: proxmox_auth_services.ProxmoxSessionManager = ProxmoxSessionManagerDep
) -> Optional[httpx.AsyncClient]:
    session = await session_manager.get_session(user.username, user.realm)
    if session: return session

ProxmoxSessionDep = Annotated[httpx.AsyncClient, Depends(_require_authenticated_session)]

