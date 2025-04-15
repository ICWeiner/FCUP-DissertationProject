from sqlmodel import Session
from typing import Optional
from app.models import User, UserPublic
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    __entity_type__ = User

    def find_by_username(self, username: str) -> Optional[User]:
        """Returns full User entity with all relationships"""
        return self.db.query(self.__entity_type__)\
                     .filter(self.__entity_type__.username == username)\
                     .first()

    def find_by_email(self, email: str) -> Optional[User]:
        """Returns full User entity with all relationships"""
        return self.db.query(self.__entity_type__)\
                     .filter(self.__entity_type__.email == email)\
                     .first()

    def get_public(self, user: User) -> UserPublic:
        """Converts a User entity to UserPublic"""
        return UserPublic(
            id=user.id,
            username=user.username,
            email=user.email
        )