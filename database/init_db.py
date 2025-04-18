# database/init_db.py
import os
import logging
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.exc import SQLAlchemyError

from .config import engine, DATABASE_URL
from .models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database with all tables"""
    try:
        # Create database if it doesn't exist
        if not database_exists(DATABASE_URL):
            logger.info(f"Creating database: {DATABASE_URL}")
            create_database(DATABASE_URL)
        
        # Create all tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        return True
    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    init_db()