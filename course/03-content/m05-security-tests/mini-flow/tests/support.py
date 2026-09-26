"""Helpers shared by every test tier: real signups, real JWTs, real rows.

Nothing here mocks authentication. Every actor is created through the public API, every request
carries the bearer token the API issued, and row snapshots are read from a fresh session so a
test cannot be fooled by an object it already holds in memory.
"""

from __future__ import annotations

from dataclasses import dataclass

from fastapi.testclient import TestClient

from miniflow.db import SessionLocal
from miniflow.models import Event, Person

PASSWORD = "correct-horse-battery"


@dataclass(frozen=True)
class Actor:
    """One authenticated account: who they are, which tenant they belong to, and their token."""

    person_id: str
    org_id: str
    token: str
    email: str

    @property
    def headers(self) -> dict[str, str]:
        return auth(self.token)


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def signup(client: TestClient, org_name: str, email: str, name: str = "Founder") -> Actor:
    """Create an organization and its first admin through POST /api/auth/signup."""
    response = client.post(
        "/api/auth/signup",
        json={"org_name": org_name, "name": name, "email": email, "password": PASSWORD},
    )
    assert response.status_code == 201, response.text
    body = response.json()
    return Actor(person_id=body["person_id"], org_id=body["org_id"], token=body["token"], email=email)


def invite(client: TestClient, admin: Actor, email: str, roles: list[str], name: str = "Invitee") -> dict:
    """Admin-created invitation (the only way a second account enters a tenant)."""
    response = client.post(
        f"/api/organizations/{admin.org_id}/invitations",
        json={"email": email, "name": name, "roles": roles},
        headers=admin.headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


def invite_and_accept(client: TestClient, admin: Actor, email: str, roles: list[str]) -> Actor:
    """Invite, accept, and return the new member holding the token the API issued on acceptance."""
    invitation = invite(client, admin, email, roles)
    response = client.post(
        "/api/auth/accept", json={"token": invitation["invitation_token"], "password": PASSWORD}
    )
    assert response.status_code == 200, response.text
    body = response.json()
    return Actor(person_id=body["person_id"], org_id=body["org_id"], token=body["token"], email=email)


def create_event(client: TestClient, admin: Actor, title: str = "Packing shift") -> dict:
    response = client.post(
        f"/api/organizations/{admin.org_id}/events",
        json={"title": title, "starts_at": "2026-10-03T09:00:00", "role_slots": {"packer": 2}},
        headers=admin.headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


def event_snapshot(event_id: str) -> dict | None:
    """Read the event row from a fresh session - the before/after evidence for a denied write."""
    with SessionLocal() as db:
        row = db.get(Event, event_id)
        if row is None:
            return None
        return {"id": row.id, "org_id": row.org_id, "title": row.title, "starts_at": row.starts_at, "role_slots": dict(row.role_slots)}


def person_snapshot(person_id: str) -> dict | None:
    with SessionLocal() as db:
        row = db.get(Person, person_id)
        if row is None:
            return None
        return {"id": row.id, "org_id": row.org_id, "email": row.email, "name": row.name, "roles": list(row.roles), "status": row.status}
