"""Shared FastAPI dependencies for authentication and authorization.

Mirrors SignUpFlow/api/dependencies.py: a tenant-bound credential reload (`get_current_user`),
the membership check (`verify_org_member`), the in-tenant lookup (`get_person_in_actor_org`)
and the admin gate (`get_current_admin_user`). Status semantics follow
SignUpFlow/docs/API_AUTHORIZATION.md:21-24:

    invalid bearer token                       -> 401
    missing bearer token on a protected route  -> 403 (documented, see below)
    explicit foreign organization              -> 403
    guessed id, looked up inside actor tenant  -> 404 whether foreign or absent
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from miniflow.db import get_db
from miniflow.models import Person
from miniflow.security import verify_token

# SignUpFlow documents HTTPBearer's historical 403 for a missing token and retains it on purpose
# (docs/API_AUTHORIZATION.md:21-24). Newer FastAPI releases - including the 0.141 line both repos
# pin - default to 401 instead. The starter pins the *documented* contract explicitly: the lesson
# is that a status code is a contract you write down and test, not a framework default you inherit.
security = HTTPBearer(auto_error=False)


def check_admin_permission(person: Person) -> bool:
    """Grant administrative access for the elevated account role."""
    roles = person.roles or []
    return any(role != "volunteer" for role in roles)


def verify_org_member(person: Person, org_id: str) -> None:
    """Verify the actor belongs to the organization named in the request - 403 otherwise."""
    if person.org_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: not a member of this organization",
        )


def get_person_in_actor_org(person_id: str, actor: Person, db: Session) -> Person:
    """Load a person only through the authenticated actor's tenant: foreign or absent -> 404."""
    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.org_id == actor.org_id)
        .first()
    )
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> Person:
    """Reload the person the token points at - by id AND tenant AND active status."""
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    payload = verify_token(credentials.credentials)

    person_id = payload.get("sub")
    token_org_id = payload.get("org_id")
    if not isinstance(person_id, str) or not isinstance(token_org_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    person = (
        db.query(Person)
        .filter(
            Person.id == person_id,
            Person.org_id == token_org_id,
            Person.status == "active",
        )
        .first()
    )
    if person is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return person


def get_current_admin_user(current_user: Person = Depends(get_current_user)) -> Person:
    """Authenticate, then require the admin permission role - 403 otherwise."""
    if not check_admin_permission(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user
