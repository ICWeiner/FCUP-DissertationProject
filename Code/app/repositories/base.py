from typing import List
from sqlmodel import Session, SQLModel, delete

from logger.logger import get_logger

logger = get_logger(__name__)

class BaseRepository:
    __entity_type__: SQLModel = None  # This will be overridden by subclasses

    def __init__(self, db: Session):
        self.db = db

    def save(self, entity: SQLModel):
        """Add a new entity and commit the transaction."""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def find_by_id(self, id_: int):
        """Find an entity by its ID."""
        return self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).first()
    
    def find_by_ids(self, ids: List[int]):
        """Find multiple entities by their IDs. """
        if not ids:
            return []
            
        return (self.db.query(self.__entity_type__)
                .filter(self.__entity_type__.id.in_(ids))
                .all())

    def find_all(self):
        """Find all entities."""
        return self.db.query(self.__entity_type__).all()

    def delete_by_id(self, id_: int):
        """Delete an entity by its ID."""
        entity = self.db.query(self.__entity_type__).filter(self.__entity_type__.id == id_).first()
        if entity:
            self.db.delete(entity)
            self.db.commit()
        return entity
    
    def batch_save(self, entities: List[object]):
        """
        Save a list of entities to the database in a single batch.

        :param entities: List of entities to be saved.
        :return: None
        """
        if not entities:
            return  # Early return if no entities are passed
        
        try:
            # Bulk add all entities
            self.db.add_all(entities)
            self.db.commit()
            
            # Bulk refresh for better performance
            for entity in entities:
                self.db.refresh(entity)
                
            return entities
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Batch save failed: {str(e)}", exc_info=True)
            raise

    def batch_delete(self, entities: List[object]) -> int:
        """
        Delete a list of entities from the database in a single batch.

        :param entities: List of entities to be deleted.
        :return: None
        """
        if not entities:
            return 0
        try:
            ids_to_delete = [entity.id for entity in entities]
            stmt = delete(type(entities[0])).where(type(entities[0]).id.in_(ids_to_delete))
            result = self.db.execute(stmt)
            self.db.commit()
            return result.rowcount
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during batch delete: {e}")
            raise