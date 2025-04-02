from typing import List
from sqlmodel import Session, SQLModel

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
            for entity in entities:
                self.db.add(entity) 
            self.db.commit()  # Commit the transaction
            for entity in entities:
                self.db.refresh(entity)
        except Exception as e:
            self.db.rollback()  # Rollback in case of an error
            print(f"Error during batch save: {e}")
            raise  