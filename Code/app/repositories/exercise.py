from sqlmodel import Session
from app.models import Exercise
from app.repositories.base import BaseRepository

class ExerciseRepository(BaseRepository):
    __entity_type__ = Exercise

    def __init__(self, db: Session):
        super().__init__(db)

    #Add methods as needed specific to exercise querying

