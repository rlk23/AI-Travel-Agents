# database/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from . import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define generic type T
ModelType = TypeVar("ModelType", bound=models.Base)


class CRUDBase(Generic[ModelType]):
    """
    Base class that provides basic CRUD operations
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: uuid.UUID) -> Optional[ModelType]:
        """Get a record by ID"""
        return db.query(self.model).filter(self.model.get_id_field() == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record"""
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[Dict[str, Any], ModelType]
    ) -> ModelType:
        """Update an existing record"""
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            
            for field in update_data:
                if hasattr(db_obj, field):
                    setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating {self.model.__name__}: {e}")
            raise

    def delete(self, db: Session, *, id: uuid.UUID) -> ModelType:
        """Delete a record"""
        try:
            obj = db.query(self.model).get(id)
            db.delete(obj)
            db.commit()
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error deleting {self.model.__name__}: {e}")
            raise


# Example of how to create specific CRUD classes for models
class CRUDUser(CRUDBase[models.User]):
    """CRUD operations for User model"""
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[models.User]:
        """Get user by email"""
        return db.query(models.User).filter(models.User.email == email).first()
    
    def create_with_preferences(
        self, db: Session, *, user_data: Dict[str, Any], preferences: List[Dict[str, Any]] = None
    ) -> models.User:
        """Create a user with preferences"""
        try:
            db_user = models.User(**user_data)
            db.add(db_user)
            db.flush()
            
            if preferences:
                for pref in preferences:
                    db_pref = models.UserPreference(user_id=db_user.user_id, **pref)
                    db.add(db_pref)
            
            db.commit()
            db.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating user with preferences: {e}")
            raise


# Initialize CRUD objects
user = CRUDUser(models.User)
# Add more CRUD objects for other models as needed