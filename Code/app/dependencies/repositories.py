from typing import Annotated, Type, TypeVar
from fastapi import  Depends
from sqlmodel import Session
from app.repositories.user import UserRepository
from app.repositories.exercise import ExerciseRepository
from app.repositories.workvm import WorkVmRepository
from app.repositories.templatevm import TemplateVmRepository
from app.database import get_session

T = TypeVar('T')  # Generic type for repositories

def get_repository(repo_class: Type[T]) -> T:
    def _get_repo(db: Session = Depends(get_session)) -> T:
        return repo_class(db)
    return Depends(_get_repo)


UserRepositoryDep = Annotated[UserRepository, get_repository(UserRepository)]


ExerciseRepositoryDep = Annotated[ExerciseRepository, get_repository(ExerciseRepository)]


WorkVmRepositoryDep = Annotated[WorkVmRepository, get_repository(WorkVmRepository)]


TemplateVmRepositoryDep = Annotated[TemplateVmRepository, get_repository(TemplateVmRepository)]