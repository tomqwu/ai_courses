"""Bootstrap, login and invitation acceptance - the public routes, with real tokens."""

from __future__ import annotations

import jwt

from tests.support import PASSWORD, invite, invite_and_accept, signup


def test_health_is_public(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_signup_creates_org_and_first_admin(client):
    admin = signup(client, "Grace Church", "admin@grace.example")

    claims = jwt.decode(admin.token, options={"verify_signature": False})
    assert claims["sub"] == admin.person_id
    assert claims["org_id"] == admin.org_id  # the token is tenant-bound from the first request

    me = client.get("/api/people/me", headers=admin.headers)
    assert me.status_code == 200
    assert me.json()["roles"] == ["admin"]
    assert me.json()["org_id"] == admin.org_id


def test_signup_rejects_existing_email(client):
    signup(client, "Grace Church", "admin@grace.example")
    response = client.post(
        "/api/auth/signup",
        json={"org_name": "Other", "name": "X", "email": "admin@grace.example", "password": PASSWORD},
    )
    assert response.status_code == 409


def test_signup_validates_body(client):
    response = client.post(
        "/api/auth/signup",
        json={"org_name": "", "name": "X", "email": "not-an-email", "password": "short"},
    )
    assert response.status_code == 422


def test_login_returns_tenant_bound_token(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    response = client.post("/api/auth/login", json={"email": admin.email, "password": PASSWORD})
    assert response.status_code == 200
    claims = jwt.decode(response.json()["token"], options={"verify_signature": False})
    assert claims == {"sub": admin.person_id, "org_id": admin.org_id, "exp": claims["exp"]}


def test_login_wrong_password_is_401(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    response = client.post("/api/auth/login", json={"email": admin.email, "password": "wrong-wrong"})
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_invited_person_cannot_login_until_accepted(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    invitation = invite(client, admin, "pat@grace.example", ["volunteer"])
    assert invitation["status"] == "invited"

    denied = client.post("/api/auth/login", json={"email": "pat@grace.example", "password": PASSWORD})
    assert denied.status_code == 401

    accepted = client.post(
        "/api/auth/accept", json={"token": invitation["invitation_token"], "password": PASSWORD}
    )
    assert accepted.status_code == 200
    assert accepted.json()["org_id"] == admin.org_id

    allowed = client.post("/api/auth/login", json={"email": "pat@grace.example", "password": PASSWORD})
    assert allowed.status_code == 200


def test_invitation_token_is_single_use(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    invitation = invite(client, admin, "pat@grace.example", ["volunteer"])
    body = {"token": invitation["invitation_token"], "password": PASSWORD}
    assert client.post("/api/auth/accept", json=body).status_code == 200
    assert client.post("/api/auth/accept", json=body).status_code == 404


def test_unknown_invitation_token_is_404(client):
    response = client.post("/api/auth/accept", json={"token": "nope", "password": PASSWORD})
    assert response.status_code == 404


def test_accepted_member_lands_in_the_inviting_tenant(client):
    admin = signup(client, "Grace Church", "admin@grace.example")
    member = invite_and_accept(client, admin, "pat@grace.example", ["volunteer", "usher"])
    me = client.get("/api/people/me", headers=member.headers)
    assert me.status_code == 200
    assert me.json()["org_id"] == admin.org_id
    assert me.json()["roles"] == ["volunteer", "usher"]
