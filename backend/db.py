from sqlmodel import create_engine, SQLModel, Session
from config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine with connection pooling
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True,  # Test connections before using
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=settings.DEBUG,  # Log SQL queries in debug mode
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    engine = None


def create_db_and_tables():
    """Create all database tables."""
    if engine is None:
        logger.warning("Database engine not available, skipping table creation")
        return
    
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # Don't raise in serverless environment


def get_session():
    """
    Dependency for database session.
    Yields a session and ensures it's closed after use.
    """
    if engine is None:
        raise RuntimeError("Database engine not available")
    
    with Session(engine) as session:
        yield session
