"""
Database Migration Script for Phase III
Run this script to create the conversations and messages tables.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_migration():
    """Run the SQL migration script."""
    try:
        # Read SQL migration file
        migration_file = Path(__file__).parent / "001_add_chat_tables.sql"
        
        if not migration_file.exists():
            logger.error(f"Migration file not found: {migration_file}")
            return False
        
        with open(migration_file, 'r') as f:
            sql_script = f.read()
        
        # Connect to database
        logger.info(f"Connecting to database...")
        engine = create_engine(settings.DATABASE_URL)
        
        # Execute migration
        logger.info("Running migration...")
        with engine.connect() as conn:
            # Split by semicolons and execute each statement
            for statement in sql_script.split(';'):
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    conn.execute(text(statement))
                    conn.commit()
        
        logger.info("✅ Migration completed successfully!")
        logger.info("Tables created:")
        logger.info("  - conversations")
        logger.info("  - messages")
        logger.info("Indexes and triggers have been set up.")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
