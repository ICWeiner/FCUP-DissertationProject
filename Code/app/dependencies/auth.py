from fastapi import Depends
from typing import Annotated
from app.services import auth as auth_services
from app.models import UserPublic, WorkVm


CurrentUserDep = Annotated[UserPublic, Depends(auth_services.get_current_user)]


PrivilegedUserDep = Annotated[UserPublic, Depends(auth_services.require_privileged_user)]


ValidateVmOwnershipDep = Annotated[WorkVm, Depends(auth_services.validate_vm_ownership)]