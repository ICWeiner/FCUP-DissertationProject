from typing import Annotated
from fastapi import  Depends
from sqlmodel import Session
from ..repositories.user import UserRepository
from ..database import get_session

def _get_user_repository(db: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(_get_user_repository)]