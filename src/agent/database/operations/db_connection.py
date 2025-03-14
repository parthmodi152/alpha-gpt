"""
Database connection utilities for AlphaGPT
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from agent.database.models.base import Base


def get_db_url():
    """
    Generate PostgreSQL connection URL from environment variables

    Returns:
        Connection URL string for PostgreSQL
    """
    db_host = os.environ.get("POSTGRES_HOST", "localhost")
    db_port = os.environ.get("POSTGRES_PORT", "5432")
    db_name = os.environ.get("POSTGRES_DB", "alphagpt")
    db_user = os.environ.get("POSTGRES_USER", "postgres")
    db_password = os.environ.get("POSTGRES_PASSWORD", "postgres")

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_db_connection_params():
    """
    Get database connection parameters from environment variables

    Returns:
        Dictionary with connection parameters
    """
    return {
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": os.environ.get("POSTGRES_PORT", "5432"),
        "db": os.environ.get("POSTGRES_DB", "alphagpt"),
        "user": os.environ.get("POSTGRES_USER", "postgres"),
        "password": os.environ.get("POSTGRES_PASSWORD", "postgres"),
    }


def get_db_engine():
    """
    Create and return a SQLAlchemy engine using environment variables

    Returns:
        SQLAlchemy engine instance
    """
    db_url = get_db_url()
    return create_engine(db_url)


def get_session_factory(engine=None):
    """
    Get a sessionmaker for creating database sessions

    Args:
        engine: Optional SQLAlchemy engine

    Returns:
        SQLAlchemy sessionmaker
    """
    if engine is None:
        engine = get_db_engine()

    return sessionmaker(bind=engine)


def create_tables(engine=None):
    """
    Create all tables defined in the models

    Args:
        engine: Optional SQLAlchemy engine
    """
    if engine is None:
        engine = get_db_engine()

    Base.metadata.create_all(engine)
