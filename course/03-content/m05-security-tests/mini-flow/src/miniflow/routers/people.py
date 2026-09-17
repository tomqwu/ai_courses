"""People: the reference router. Every query carries the tenant predicate."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from miniflow.db import get_db
from miniflow.dependencies import (
    get_current_admin_user,
    get_current_user,
    get_person_in_actor_org,
    verify_org_member,
)
from miniflow.models import Person
from miniflow.roles import normalize_roles
from miniflow.routers.auth import new_invitation_token
from miniflow.schemas import InvitationCreate, InvitationOut, PersonOut, PersonUpdate

router = APIRouter(prefix="/api", tags=["people"])


@router.get("/people/me", response_model=PersonOut)
def get_current_person(actor: Person = Depends(get_current_user)) -> Person:
    return actor


@router.get("/organizations/{org_id}/people", response_model=list[PersonOut])
def list_people(
    org_id: str,
    actor: Person = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Person]:
    verify_org_member(actor, org_id)
    return db.query(Person).filter(Person.org_id == org_id).order_by(Person.name).all()


@router.get("/people/{person_id}", response_model=PersonOut)
def get_person(
    person_id: str,
    actor: Person = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Person:
    return get_person_in_actor_org(person_id, actor, db)


@router.patch("/people/{person_id}", response_model=PersonOut)
def update_person(
    person_id: str,
    body: PersonUpdate,
    actor: Person = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Person:
    person = get_person_in_actor_org(person_id, actor, db)
    if body.name is not None:
        person.name = body.name
    if body.roles is not None:
        try:
            person.roles = normalize_roles(body.roles)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
            ) from exc
    db.commit()
    return person


@router.post(
    "/organizations/{org_id}/invitations",
    response_model=InvitationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_invitation(
    org_id: str,
    body: InvitationCreate,
    actor: Person = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> InvitationOut:
    verify_org_member(actor, org_id)
    if db.query(Person).filter(Person.email == body.email).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    try:
        roles = normalize_roles(body.roles)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)
        ) from exc
    person = Person(
        org_id=actor.org_id,
        email=body.email,
        name=body.name,
        roles=roles,
        status="invited",
        invitation_token=new_invitation_token(),
    )
    db.add(person)
    db.commit()
    return InvitationOut(
        person_id=person.id,
        org_id=person.org_id,
        email=person.email,
        roles=person.roles,
        status=person.status,
        invitation_token=person.invitation_token,
    )
