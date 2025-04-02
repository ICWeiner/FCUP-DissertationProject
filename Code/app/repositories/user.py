from sqlmodel import Session
from app.models import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    __entity_type__ = User

    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_username(self, username: str):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.username == username).first()

    def find_by_email(self, email: str):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.email == email).first()
