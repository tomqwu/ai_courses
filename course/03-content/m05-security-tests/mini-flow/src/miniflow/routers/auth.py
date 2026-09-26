"""Bootstrap and login. Signup atomically creates an organization and its first admin; there is
no public join - every later account arrives through an admin-created invitation
(SignUpFlow/AGENTS.md:59)."""

from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from miniflow.db import get_db
from miniflow.models import Organization, Person
from miniflow.schemas import AcceptInvitationRequest, LoginRequest, SignupRequest, TokenResponse
from miniflow.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _token_for(person: Person) -> TokenResponse:
    token = create_access_token({"sub": person.id, "org_id": person.org_id})
    return TokenResponse(token=token, person_id=person.id, org_id=person.org_id)


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, db: Session = Depends(get_db)) -> TokenResponse:
    if db.query(Person).filter(Person.email == body.email).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    org = Organization(name=body.org_name)
    db.add(org)
    db.flush()
    person = Person(
        org_id=org.id,
        email=body.email,
        name=body.name,
        password_hash=hash_password(body.password),
        roles=["admin"],
        status="active",
    )
    db.add(person)
    db.commit()
    return _token_for(person)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    person = db.query(Person).filter(Person.email == body.email).first()
    if (
        person is None
        or person.status != "active"
        or not verify_password(body.password, person.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return _token_for(person)


@router.post("/accept", response_model=TokenResponse)
def accept_invitation(body: AcceptInvitationRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Single-use: the invitation token is cleared the moment the account becomes active."""
    person = (
        db.query(Person)
        .filter(Person.invitation_token == body.token, Person.status == "invited")
        .first()
    )
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")
    person.password_hash = hash_password(body.password)
    person.status = "active"
    person.invitation_token = None
    db.commit()
    return _token_for(person)


def new_invitation_token() -> str:
    return secrets.token_urlsafe(24)
