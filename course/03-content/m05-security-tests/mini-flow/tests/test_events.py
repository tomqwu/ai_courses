"""Events: happy paths and the denials the starter already gets right.

The cross-tenant event cases live in tests/test_lab1_isolation.py - they are Lab M5 step 1.
"""

from __future__ import annotations

from tests.support import create_event, invite_and_accept, signup


def test_admin_creates_event_in_own_org(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    event = create_event(client, admin)
    assert event["org_id"] == admin.org_id
    assert event["role_slots"] == {"packer": 2}


def test_member_lists_own_org_events(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    create_event(client, admin, "Preparation")
    create_event(client, admin, "Packing shift")
    response = client.get(f"/api/organizations/{admin.org_id}/events", headers=member.headers)
    assert response.status_code == 200
    assert [e["title"] for e in response.json()] == ["Preparation", "Packing shift"]


def test_foreign_org_event_list_is_403(client):
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    create_event(client, grace)
    response = client.get(f"/api/organizations/{grace.org_id}/events", headers=tokyo.headers)
    assert response.status_code == 403


def test_member_reads_own_event(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    event = create_event(client, admin)
    response = client.get(f"/api/events/{event['id']}", headers=member.headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Packing shift"


def test_absent_event_id_is_404(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    response = client.get("/api/events/00000000000000000000000000000000", headers=admin.headers)
    assert response.status_code == 404
    response = client.patch(
        "/api/events/00000000000000000000000000000000", json={"title": "x"}, headers=admin.headers
    )
    assert response.status_code == 404


def test_admin_updates_own_event(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    event = create_event(client, admin)
    response = client.patch(
        f"/api/events/{event['id']}", json={"title": "Packing shift (moved)"}, headers=admin.headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Packing shift (moved)"
    assert response.json()["role_slots"] == {"packer": 2}  # untouched fields survive a PATCH


def test_plain_volunteer_cannot_create_or_update_events_403(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    event = create_event(client, admin)
    created = client.post(
        f"/api/organizations/{admin.org_id}/events",
        json={"title": "Rogue", "starts_at": "2026-10-04T09:00:00"},
        headers=member.headers,
    )
    assert created.status_code == 403
    patched = client.patch(f"/api/events/{event['id']}", json={"title": "Rogue"}, headers=member.headers)
    assert patched.status_code == 403


def test_admin_cannot_create_event_in_foreign_org_403(client):
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    response = client.post(
        f"/api/organizations/{grace.org_id}/events",
        json={"title": "Planted", "starts_at": "2026-10-04T09:00:00"},
        headers=tokyo.headers,
    )
    assert response.status_code == 403
    assert client.get(f"/api/organizations/{grace.org_id}/events", headers=grace.headers).json() == []
