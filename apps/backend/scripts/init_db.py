import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.database import engine
from app.models.user import Base
from alembic.config import Config
from alembic import command

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Run migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    print("Creating initial database...")
    init_db()
    print("Database initialization completed.") 