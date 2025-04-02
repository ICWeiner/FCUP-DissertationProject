from fastapi import Depends
from typing import Annotated
from app.services import auth as auth_services
from app.models import UserPublic


CurrentUserDep = Annotated[UserPublic, Depends(auth_services.get_current_user)]