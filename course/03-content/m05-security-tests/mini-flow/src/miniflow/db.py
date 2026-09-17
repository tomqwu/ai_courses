"""Engine, session factory and the `get_db` dependency (mirrors SignUpFlow's api/database.py).

SQLite everywhere: a file for local runs, `sqlite:///:memory:` for the test suite and the demo
(tests/conftest.py and demo.py set MINIFLOW_DATABASE_URL before importing this module). The
database is real in every tier - mocking it in integration tests is a named anti-pattern in
SignUpFlow/AGENTS.md.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.getenv("MINIFLOW_DATABASE_URL", "sqlite:///./miniflow.db")


class Base(DeclarativeBase):
    """Declarative base shared by every model."""


def make_engine(url: str = DATABASE_URL) -> Engine:
    """Create an engine; an in-memory SQLite URL gets a StaticPool so every session sees one DB."""
    kwargs: dict = {"connect_args": {"check_same_thread": False}}
    if url.endswith(":memory:"):
        kwargs["poolclass"] = StaticPool
    return create_engine(url, **kwargs)


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """Yield one session per request; tests replace this via `app.dependency_overrides`."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
