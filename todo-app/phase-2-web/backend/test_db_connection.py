#!/usr/bin/env python3
"""
Test script to verify database connection and table creation
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from sqlmodel import SQLModel, create_engine, text
    from models.user import User
    from models.task import Task

    # Get the database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        print("[ERROR] DATABASE_URL not found in environment variables")
        sys.exit(1)

    print(f"[SUCCESS] Using DATABASE_URL: {DATABASE_URL}")

    # Create engine
    engine = create_engine(DATABASE_URL, echo=True)

    print("[SUCCESS] Database engine created successfully")

    # Test connection
    with engine.connect() as conn:
        # Use SQLite-compatible query instead of PostgreSQL-specific one
        if 'sqlite' in DATABASE_URL:
            result = conn.execute(text("SELECT sqlite_version();"))
            version = result.fetchone()[0]
            print(f"[SUCCESS] Connected to SQLite database. Version: {version}")
        else:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"[SUCCESS] Connected to database. Version: {version[:50]}...")

    # Register all models and create tables
    print("\n[INFO] Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("[SUCCESS] Database tables created successfully!")

    # Check what tables were created
    with engine.connect() as conn:
        # Use SQLite-compatible query instead of PostgreSQL-specific one
        if 'sqlite' in DATABASE_URL:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]
        else:
            result = conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            )
            tables = [row[0] for row in result.fetchall()]

        print(f"[INFO] Tables in database: {tables}")

        # Check for expected tables (case-insensitive)
        table_names = [t.lower() for t in tables]
        if 'user' in table_names or 'users' in table_names:
            print("[SUCCESS] User table exists")
        else:
            print("[ERROR] User table does NOT exist")

        if 'task' in table_names or 'tasks' in table_names:
            print("[SUCCESS] Task table exists")
        else:
            print("[ERROR] Task table does NOT exist")

    print("\n[SUCCESS] Database setup completed successfully!")

except ImportError as e:
    print(f"[ERROR] ImportError: {e}")
    print("Make sure you have installed the required packages:")
    print("pip install sqlmodel python-dotenv asyncpg")

except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()