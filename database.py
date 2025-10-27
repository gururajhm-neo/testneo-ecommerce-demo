"""
Database configuration for E-commerce Testing API
Uses SQLite for simplicity and isolation
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - SQLite file in the same directory
DATABASE_URL = "sqlite:///./ecommerce.db"

# Create SQLite engine with proper configuration
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=True,  # Enable SQL logging for debugging
    pool_pre_ping=True,
    pool_recycle=300
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI.
    Creates a new session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize database by creating all tables.
    """
    Base.metadata.create_all(bind=engine)

def drop_db():
    """
    Drop all tables (for testing).
    """
    Base.metadata.drop_all(bind=engine)
