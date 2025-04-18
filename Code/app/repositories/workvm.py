from sqlmodel import Session, select
from app.models import WorkVm, TemplateVm, Exercise 
from app.repositories.base import BaseRepository
from typing import Optional, Union, List

class WorkVmRepository(BaseRepository):
    __entity_type__ = WorkVm

    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_proxmox_id(self, proxmox_id: int):
        """Given a proxmox VM id (not database related) return a WorkVm instance"""
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.proxmox_id == proxmox_id).first()
    
    # In your WorkVmRepository
    def find_by_user_id(self, user_id: int) -> List[WorkVm]:
        workvms = self.db.exec(
            select(WorkVm)
            .where(WorkVm.user_id == user_id)
        ).all()
        
        # Manually load relationships if needed
        for w in workvms:
            _ = w.templatevm  # Trigger lazy load
            if w.templatevm:
                _ = w.templatevm.exercise  # Trigger lazy load
        return workvms
    
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
    
    def check_if_user_owns_workvm_by_proxmox_id(self, user_id: int, proxmox_id: int) -> WorkVm | None:
        """Check if a user owns a WorkVm with given proxmox_id"""
        statement = select(WorkVm).where(
            (WorkVm.proxmox_id == proxmox_id) &
            (WorkVm.user_id == user_id)
        )
        return self.db.exec(statement).first()

