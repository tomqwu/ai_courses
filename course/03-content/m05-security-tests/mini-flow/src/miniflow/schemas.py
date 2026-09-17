"""Request/response models. Identity and tenant never come from these bodies."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Email = Annotated[str, Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", max_length=254)]


class SignupRequest(BaseModel):
    org_name: str = Field(min_length=1, max_length=120)
    name: str = Field(min_length=1, max_length=120)
    email: Email
    password: str = Field(min_length=8, max_length=72)


class LoginRequest(BaseModel):
    email: Email
    password: str


class AcceptInvitationRequest(BaseModel):
    token: str
    password: str = Field(min_length=8, max_length=72)


class TokenResponse(BaseModel):
    token: str
    person_id: str
    org_id: str


class PersonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    org_id: str
    email: str
    name: str
    roles: list[str]
    status: str


class InvitationCreate(BaseModel):
    email: Email
    name: str = Field(min_length=1, max_length=120)
    roles: list[str] = Field(default_factory=lambda: ["volunteer"])


class InvitationOut(BaseModel):
    person_id: str
    org_id: str
    email: str
    roles: list[str]
    status: str
    invitation_token: str


class PersonUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    roles: list[str] | None = None


class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    starts_at: str = Field(min_length=1, max_length=32)
    role_slots: dict[str, int] = Field(default_factory=dict)


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    starts_at: str | None = Field(default=None, min_length=1, max_length=32)
    role_slots: dict[str, int] | None = None


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    org_id: str
    title: str
    starts_at: str
    role_slots: dict[str, int]
