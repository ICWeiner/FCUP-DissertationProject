from typing import Annotated
from fastapi import  Depends
from sqlmodel import Session
from app.repositories.user import UserRepository
from app.repositories.exercise import ExerciseRepository
from app.repositories.workvm import WorkVmRepository
from app.repositories.templatevm import TemplateVmRepository
from app.database import get_session

def _get_user_repository(db: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(_get_user_repository)]

def _get_exercise_repository(db: Session = Depends(get_session)) -> ExerciseRepository:
    return ExerciseRepository(db)

ExerciseRepositoryDep = Annotated[ExerciseRepository, Depends(_get_exercise_repository)]



def _get_workvm_repository(db: Session = Depends(get_session)) -> WorkVmRepository:
    return WorkVmRepository(db)

WorkVmRepositoryDep = Annotated[WorkVmRepository, Depends(_get_workvm_repository)]

def _get_templatevm_repository(db: Session = Depends(get_session)) -> TemplateVmRepository:
    return TemplateVmRepository(db)

TemplateVmRepositoryDep = Annotated[TemplateVmRepository, Depends(_get_templatevm_repository)]