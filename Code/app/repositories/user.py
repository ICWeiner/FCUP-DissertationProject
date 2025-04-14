from sqlmodel import Session
from typing import Optional
from app.models import User, UserPublic
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    __entity_type__ = User

    def __init__(self, db: Session):
        super().__init__(db)

    def _to_public(self, user: Optional[User]) -> Optional[UserPublic]:
        return UserPublic.from_orm(user) if user else None
    
    def find_by_username_for_auth(self, username: str) -> Optional[User]:
        """Special method only for authentication that returns full entity"""
        return self.db.query(self.__entity_type__)\
                     .filter(self.__entity_type__.username == username)\
                     .first()

    def find_by_username(self, username: str) -> Optional[UserPublic]:
        user = self.db.query(self.__entity_type__)\
                     .filter(self.__entity_type__.username == username)\
                     .first()
        return self._to_public(user)

    def find_by_email(self, email: str) -> Optional[UserPublic]:
        user = self.db.query(self.__entity_type__)\
                     .filter(self.__entity_type__.email == email)\
                     .first()
        return self._to_public(user)

    def find_by_id(self, id: int) -> Optional[UserPublic]:
        user = self.db.query(self.__entity_type__)\
                     .filter(self.__entity_type__.id == id)\
                     .first()
        return self._to_public(user)