"""
Script to manage database migrations with Alembic.
Database model management and migrations.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd: list) -> int:
    """Run shell command."""
    return subprocess.run(cmd).returncode


def init_db():
    """Initialize database."""
    print("📦 Initializing database...")
    
    # Create tables
    from app.models.database import Base
    from sqlalchemy import create_engine
    from app.config.settings import get_settings
    
    settings = get_settings()
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database initialized!")


def create_migration(message: str):
    """Create new migration."""
    print(f"📝 Creating migration: {message}")
    
    cmd = [
        "alembic",
        "revision",
        "--autogenerate",
        "-m",
        message,
    ]
    
    return run_command(cmd)


def migrate_upgrade():
    """Apply migrations."""
    print("⬆️  Upgrading database...")
    
    cmd = ["alembic", "upgrade", "head"]
    return run_command(cmd)


def migrate_downgrade(revision: str = "-1"):
    """Downgrade migrations."""
    print(f"⬇️  Downgrading database to {revision}...")
    
    cmd = ["alembic", "downgrade", revision]
    return run_command(cmd)


def migrate_current():
    """Show current revision."""
    print("📍 Current database revision:")
    
    cmd = ["alembic", "current"]
    return run_command(cmd)


def migrate_history():
    """Show migration history."""
    print("📚 Migration history:")
    
    cmd = ["alembic", "history"]
    return run_command(cmd)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_db.py [init|create|upgrade|downgrade|current|history]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_db()
    elif command == "create" and len(sys.argv) > 2:
        create_migration(sys.argv[2])
    elif command == "upgrade":
        migrate_upgrade()
    elif command == "downgrade" and len(sys.argv) > 2:
        migrate_downgrade(sys.argv[2])
    elif command == "current":
        migrate_current()
    elif command == "history":
        migrate_history()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
