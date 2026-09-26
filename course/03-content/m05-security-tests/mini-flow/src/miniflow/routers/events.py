"""Events: the router added last."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from miniflow.db import get_db
from miniflow.dependencies import get_current_admin_user, get_current_user, verify_org_member
from miniflow.models import Event, Person
from miniflow.schemas import EventCreate, EventOut, EventUpdate

router = APIRouter(prefix="/api", tags=["events"])


@router.get("/organizations/{org_id}/events", response_model=list[EventOut])
def list_events(
    org_id: str,
    actor: Person = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Event]:
    verify_org_member(actor, org_id)
    return db.query(Event).filter(Event.org_id == org_id).order_by(Event.starts_at).all()


@router.post(
    "/organizations/{org_id}/events",
    response_model=EventOut,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    org_id: str,
    body: EventCreate,
    actor: Person = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Event:
    verify_org_member(actor, org_id)
    event = Event(org_id=actor.org_id, **body.model_dump())
    db.add(event)
    db.commit()
    return event


@router.get("/events/{event_id}", response_model=EventOut)
def get_event(
    event_id: str,
    actor: Person = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.patch("/events/{event_id}", response_model=EventOut)
def update_event(
    event_id: str,
    body: EventUpdate,
    actor: Person = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(event, field, value)
    db.commit()
    return event
