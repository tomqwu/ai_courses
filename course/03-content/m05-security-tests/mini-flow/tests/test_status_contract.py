"""The status contract of SignUpFlow/docs/API_AUTHORIZATION.md:21-24, pinned by tests.

    invalid bearer token                        -> 401
    missing bearer token on a protected route   -> 403
    token whose tenant claim matches no active membership -> 401
"""

from __future__ import annotations

from datetime import timedelta

from miniflow.security import create_access_token
from tests.support import auth, invite, signup


def test_invalid_bearer_token_is_401(client):
    response = client.get("/api/people/me", headers=auth("not-a-jwt"))
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_missing_bearer_token_is_403(client):
    response = client.get("/api/people/me")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


def test_expired_token_is_401(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    stale = create_access_token(
        {"sub": admin.person_id, "org_id": admin.org_id}, expires_delta=timedelta(minutes=-1)
    )
    assert client.get("/api/people/me", headers=auth(stale)).status_code == 401


def test_token_without_tenant_claim_is_401(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    unbound = create_access_token({"sub": admin.person_id})
    assert client.get("/api/people/me", headers=auth(unbound)).status_code == 401


def test_token_with_mismatched_tenant_claim_is_401(client):
    """A valid signature is not enough: the reload is by id AND org_id AND active status."""
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    forged = create_access_token({"sub": grace.person_id, "org_id": tokyo.org_id})
    response = client.get("/api/people/me", headers=auth(forged))
    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"


def test_token_for_inactive_person_is_401(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    invitation = invite(client, admin, "pat@grace.example", ["volunteer"])
    not_yet_active = create_access_token({"sub": invitation["person_id"], "org_id": admin.org_id})
    assert client.get("/api/people/me", headers=auth(not_yet_active)).status_code == 401


def test_explicit_foreign_org_is_403(client):
    grace = signup(client, "Grace Church", "admin@grace.example")
    tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
    response = client.get(f"/api/organizations/{grace.org_id}/people", headers=tokyo.headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Access denied: not a member of this organization"


def test_guessed_person_id_inside_own_tenant_is_404(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    response = client.get("/api/people/00000000000000000000000000000000", headers=admin.headers)
    assert response.status_code == 404
