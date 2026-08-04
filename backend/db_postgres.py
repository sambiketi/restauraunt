import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env file")

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy instance for Flask
db = SQLAlchemy()

def get_session():
    """Get a database session"""
    return SessionLocal()

def get_engine():
    """Get the database engine"""
    return engine

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    return db
