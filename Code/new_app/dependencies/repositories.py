from typing import Annotated
from fastapi import  Depends
from sqlmodel import Session
from ..repositories.user import UserRepository
from ..repositories.exercise import ExerciseRepository
from ..database import get_session

def _get_user_repository(db: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(db)

UserRepositoryDep = Annotated[UserRepository, Depends(_get_user_repository)]

def _get_exercise_repository(db: Session = Depends(get_session)) -> ExerciseRepository:
    return ExerciseRepository(db)

ExerciseRepositoryDep = Annotated[ExerciseRepository, Depends(_get_exercise_repository)]