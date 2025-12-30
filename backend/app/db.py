"""Database setup for the application."""

from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.base import Base


def get_database_url() -> str:
    """Return the database URL for SQLAlchemy."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://nebenkosten:nebenkosten@localhost:5432/nebenkosten",
    )


engine = create_engine(get_database_url(), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

__all__ = ["Base", "engine", "SessionLocal", "get_database_url"]
