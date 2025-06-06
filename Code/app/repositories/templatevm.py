from sqlmodel import Session
from app.models import TemplateVm
from app.repositories.base import BaseRepository

class TemplateVmRepository(BaseRepository):
    __entity_type__ = TemplateVm

    def __init__(self, db: Session):
        super().__init__(db)

    def find_by_proxmox_id(self, proxmox_id: int):
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.proxmox_id == proxmox_id).first()
    #Add methods as needed specific to exercise querying

