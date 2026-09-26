"""Three tables. Every person and every event row carries org_id (SignUpFlow/AGENTS.md:57)."""

from __future__ import annotations

import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from miniflow.db import Base


def new_id() -> str:
    return uuid.uuid4().hex


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(120))


class Person(Base):
    """One account. `roles` holds exactly one permission role plus any scheduling qualifications."""

    __tablename__ = "people"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str | None] = mapped_column(String(200), nullable=True)
    roles: Mapped[list[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(16), default="active")  # active | invited | inactive
    invitation_token: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=new_id)
    org_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    starts_at: Mapped[str] = mapped_column(String(32))  # ISO-8601, kept as text at lab scale
    role_slots: Mapped[dict[str, int]] = mapped_column(JSON, default=dict)  # {"packer": 2}
