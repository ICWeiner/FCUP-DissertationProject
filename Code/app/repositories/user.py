from sqlmodel import Session
from typing import Optional, List
from app.models import User, UserPublic, WorkVm, Exercise
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
    
    def get_users_for_exercise(self, exercise_id: int) -> List[User]:
        """Get users already enlisted in a given exercise"""
        return (self.db.query(User)
                .join(WorkVm, User.id == WorkVm.user_id)
                .join(Exercise, WorkVm.templatevm_id == Exercise.templatevm_id)
                .filter(Exercise.id == exercise_id)
                .all())

    def get_public(self, user: User) -> UserPublic:
        """Converts a User entity to UserPublic"""
        return UserPublic(
            id=user.id,
            username=user.username,
            email=user.email
        )