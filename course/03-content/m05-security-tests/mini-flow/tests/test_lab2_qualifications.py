"""Lab M5 step 2 - a scheduling qualification confers no permission.

Un-skip with `make step2`. On the shipped starter four tests are RED:

* `check_admin_permission` in src/miniflow/dependencies.py grants admin to *any* role that is not
  `volunteer` - so `["volunteer", "usher"]` is an admin. The reference is
  SignUpFlow/api/dependencies.py:15-17: admin iff `"admin" in person.roles`.
* `normalize_roles` in src/miniflow/roles.py case-folds `"ADMIN"` into `admin` - it repairs an
  ambiguous input instead of refusing it (SignUpFlow/api/roles.py:49).

"Do not grant admin access merely because someone leads a ministry" - SignUpFlow/docs/playbooks/church.md:26.
"""

from __future__ import annotations

import pytest

from miniflow.roles import normalize_roles, qualifications_of
from tests.support import create_event, invite_and_accept, signup

pytestmark = pytest.mark.lab(step=2)


@pytest.fixture
def usher(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    return admin, invite_and_accept(client, admin, "usher@grace.example", ["volunteer", "usher"])


def test_usher_keeps_the_qualification_and_can_read(client, usher):
    admin, usher_actor = usher
    me = client.get("/api/people/me", headers=usher_actor.headers)
    assert me.json()["roles"] == ["volunteer", "usher"]
    listed = client.get(f"/api/organizations/{admin.org_id}/people", headers=usher_actor.headers)
    assert listed.status_code == 200


def test_usher_cannot_invite(client, usher):
    """RED on the starter: the invitation is created (201)."""
    admin, usher_actor = usher
    response = client.post(
        f"/api/organizations/{admin.org_id}/invitations",
        json={"email": "new@grace.example", "name": "New", "roles": ["volunteer"]},
        headers=usher_actor.headers,
    )
    assert response.status_code == 403, response.text  # not 404 (route exists), not 201
    assert response.json()["detail"] == "Admin access required"


def test_usher_cannot_create_event(client, usher):
    admin, usher_actor = usher
    response = client.post(
        f"/api/organizations/{admin.org_id}/events",
        json={"title": "Rogue", "starts_at": "2026-10-04T09:00:00"},
        headers=usher_actor.headers,
    )
    assert response.status_code == 403, response.text


def test_usher_cannot_promote_themselves(client, usher):
    """The privilege-escalation path: an usher patching their own roles to admin."""
    _, usher_actor = usher
    response = client.patch(
        f"/api/people/{usher_actor.person_id}", json={"roles": ["admin"]}, headers=usher_actor.headers
    )
    assert response.status_code == 403, response.text
    me = client.get("/api/people/me", headers=usher_actor.headers)
    assert me.json()["roles"] == ["volunteer", "usher"]


def test_uppercase_admin_is_ambiguous_not_repaired():
    """RED on the starter: normalize_roles(['ADMIN']) == ['admin']."""
    with pytest.raises(ValueError, match="ambiguous"):
        normalize_roles(["ADMIN"])


def test_qualification_vocabulary_never_overlaps_permissions():
    assert "admin" not in qualifications_of(normalize_roles(["admin", "usher"]))
    assert qualifications_of(normalize_roles(["coach", "usher"])) == ["coach", "usher"]


def test_real_admin_still_can_invite(client, usher):
    admin, _ = usher
    _ = create_event(client, admin)  # the admin gate must not become "nobody"
    response = client.post(
        f"/api/organizations/{admin.org_id}/invitations",
        json={"email": "new@grace.example", "name": "New", "roles": ["volunteer"]},
        headers=admin.headers,
    )
    assert response.status_code == 201
