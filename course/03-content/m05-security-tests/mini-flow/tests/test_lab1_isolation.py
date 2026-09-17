"""Lab M5 step 1 - cross-tenant read and write are denied, and the row is unchanged.

Un-skip with `make step1`. On the shipped starter two tests are RED: the events router loads
`Event` by primary key only (src/miniflow/routers/events.py, `get_event` and `update_event`), so a
foreign event is readable and writable with a perfectly valid token from another tenant. The
people router is the reference shape (`get_person_in_actor_org`); its tests are already green.

Status contract (SignUpFlow/docs/API_AUTHORIZATION.md:21-24): a guessed or foreign id looked up
inside the actor's tenant is 404 - never 403, which would confirm the row exists.
"""

from __future__ import annotations

import pytest

from tests.support import create_event, event_snapshot, invite_and_accept, person_snapshot, signup

pytestmark = pytest.mark.lab(step=1)


@pytest.fixture
def two_tenants(client):
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    tokyo_member = invite_and_accept(client, tokyo, "fan@tokyo.example", ["volunteer"])
    grace_event = create_event(client, grace, "Sunday rota")
    return grace, tokyo, tokyo_member, grace_event


def test_same_tenant_member_reads_own_event(client, two_tenants):
    grace, _, _, grace_event = two_tenants
    grace_member = invite_and_accept(client, grace, "pat@grace.example", ["volunteer"])
    response = client.get(f"/api/events/{grace_event['id']}", headers=grace_member.headers)
    assert response.status_code == 200


def test_foreign_member_cannot_read_foreign_event(client, two_tenants):
    """RED on the starter: returns 200 with Grace's row."""
    _, _, tokyo_member, grace_event = two_tenants
    response = client.get(f"/api/events/{grace_event['id']}", headers=tokyo_member.headers)
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Event not found"


def test_foreign_admin_patch_is_denied_and_row_unchanged(client, two_tenants):
    """RED on the starter: returns 200 AND Grace's row now reads 'stolen'."""
    _, tokyo, _, grace_event = two_tenants
    before = event_snapshot(grace_event["id"])

    response = client.patch(
        f"/api/events/{grace_event['id']}", json={"title": "stolen"}, headers=tokyo.headers
    )

    assert response.status_code == 404, response.text  # the contract
    assert event_snapshot(grace_event["id"]) == before  # the control: nothing was written


def test_foreign_member_cannot_read_foreign_person(client, two_tenants):
    grace, _, tokyo_member, _ = two_tenants
    response = client.get(f"/api/people/{grace.person_id}", headers=tokyo_member.headers)
    assert response.status_code == 404


def test_foreign_admin_patch_person_is_denied_and_row_unchanged(client, two_tenants):
    grace, tokyo, _, _ = two_tenants
    before = person_snapshot(grace.person_id)
    response = client.patch(
        f"/api/people/{grace.person_id}", json={"name": "stolen"}, headers=tokyo.headers
    )
    assert response.status_code == 404
    assert person_snapshot(grace.person_id) == before


def test_explicit_foreign_org_is_403_for_events(client, two_tenants):
    grace, _, tokyo_member, _ = two_tenants
    response = client.get(f"/api/organizations/{grace.org_id}/events", headers=tokyo_member.headers)
    assert response.status_code == 403
