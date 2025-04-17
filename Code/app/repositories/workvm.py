from sqlmodel import Session
from app.models import WorkVm, Exercise
from app.repositories.base import BaseRepository
from typing import Optional, Union, List

class WorkVmRepository(BaseRepository):
    __entity_type__ = WorkVm

    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_proxmox_id(self, proxmox_id: int):
        """Given a proxmox VM id (not database related) return a WorkVm instance"""
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.proxmox_id == proxmox_id).first()
    
    def find_by_users_and_exercise(self,
        user_ids: Union[int, List[int]],  # Accept both single and multiple IDs
        exercise_id: int
    ) -> List[WorkVm]:
        """Flexible method to find WorkVMs for one or many users"""
        query = self.db.query(WorkVm).join(Exercise, WorkVm.templatevm_id == Exercise.templatevm_id)
        
        if isinstance(user_ids, list):
            query = query.filter(WorkVm.user_id.in_(user_ids))
        else:
            query = query.filter(WorkVm.user_id == user_ids)
            
        return query.filter(Exercise.id == exercise_id).all()

