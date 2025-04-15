from sqlmodel import Session
from app.models import WorkVm, Exercise
from app.repositories.base import BaseRepository
from typing import Optional

class WorkVmRepository(BaseRepository):
    __entity_type__ = WorkVm

    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_proxmox_id(self, proxmox_id: int):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.proxmox_id == proxmox_id).first()
    
    def find_by_user_and_exercise(self, user_id: int, exercise_id: int) -> Optional[WorkVm]:
        return self.db.query(WorkVm)\
                    .join(Exercise, WorkVm.templatevm_id == Exercise.templatevm_id)\
                    .filter(
                        WorkVm.user_id == user_id,
                        Exercise.id == exercise_id
                    )\
                    .first()

