"""People: the reference router. Every tenant path here is already correct in the starter."""

from __future__ import annotations

from tests.support import invite, invite_and_accept, person_snapshot, signup


def test_member_lists_own_org_people(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    response = client.get(f"/api/organizations/{admin.org_id}/people", headers=member.headers)
    assert response.status_code == 200
    assert {p["email"] for p in response.json()} == {admin.email, member.email}
    assert {p["org_id"] for p in response.json()} == {admin.org_id}


def test_member_reads_person_in_own_org(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    response = client.get(f"/api/people/{admin.person_id}", headers=member.headers)
    assert response.status_code == 200
    assert response.json()["email"] == admin.email


def test_foreign_person_id_is_404_not_403(client):
    """Looked up inside the actor's tenant, a foreign id and an absent id are indistinguishable."""
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    response = client.get(f"/api/people/{grace.person_id}", headers=tokyo.headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"


def test_foreign_admin_cannot_patch_person_and_row_is_unchanged(client):
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    before = person_snapshot(grace.person_id)

    response = client.patch(
        f"/api/people/{grace.person_id}", json={"name": "stolen"}, headers=tokyo.headers
    )

    assert response.status_code == 404
    assert person_snapshot(grace.person_id) == before


def test_admin_updates_name_and_roles(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    response = client.patch(
        f"/api/people/{member.person_id}",
        json={"name": "Pat Lee", "roles": ["usher", "volunteer", "usher"]},
        headers=admin.headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Pat Lee"
    assert response.json()["roles"] == ["volunteer", "usher"]  # permission role first, deduplicated


def test_two_permission_roles_are_rejected_422(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    response = client.patch(
        f"/api/people/{member.person_id}", json={"roles": ["volunteer", "admin"]}, headers=admin.headers
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Select exactly one account access role"


def test_admin_creates_invitation(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    invitation = invite(client, admin, "pat@grace.example", ["volunteer", "usher"])
    assert invitation["org_id"] == admin.org_id
    assert invitation["roles"] == ["volunteer", "usher"]
    assert invitation["status"] == "invited"
    assert len(invitation["invitation_token"]) >= 24


def test_invitation_with_bad_qualification_is_422(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    response = client.post(
        f"/api/organizations/{admin.org_id}/invitations",
        json={"email": "pat@grace.example", "name": "Pat", "roles": ["Head Usher"]},
        headers=admin.headers,
    )
    assert response.status_code == 422


def test_invitation_for_existing_email_is_409(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    response = client.post(
        f"/api/organizations/{admin.org_id}/invitations",
        json={"email": admin.email, "name": "Dup", "roles": ["volunteer"]},
        headers=admin.headers,
    )
    assert response.status_code == 409


def test_plain_volunteer_cannot_invite_403(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    response = client.post(
        f"/api/organizations/{admin.org_id}/invitations",
        json={"email": "new@grace.example", "name": "New", "roles": ["volunteer"]},
        headers=member.headers,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_plain_volunteer_cannot_update_person_403(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer"])
    response = client.patch(
        f"/api/people/{admin.person_id}", json={"name": "Nope"}, headers=member.headers
    )
    assert response.status_code == 403


def test_admin_cannot_invite_into_foreign_org_403(client):
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    response = client.post(
        f"/api/organizations/{grace.org_id}/invitations",
        json={"email": "spy@tokyo.example", "name": "Spy", "roles": ["volunteer"]},
        headers=tokyo.headers,
    )
    assert response.status_code == 403
