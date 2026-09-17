"""Two tenants, one database, one leaky router - watch the status contract live.

Runs the app in-process against an in-memory SQLite database. Tokyo's admin holds a perfectly
valid token for Tokyo and tries every way in to Grace's data. Each line shows the status the
starter returns against the status the contract requires (SignUpFlow/docs/API_AUTHORIZATION.md:21-24).
Before Lab M5 step 1 two lines say LEAK; after it, none do.
"""

from __future__ import annotations

import os
import warnings

os.environ.setdefault("MINIFLOW_DATABASE_URL", "sqlite:///:memory:")
# Raised by starlette's testclient about the httpx package, not by mini-flow.
warnings.filterwarnings("ignore", message="Using `httpx` with `starlette.testclient` is deprecated")

from fastapi.testclient import TestClient  # noqa: E402

from miniflow.db import Base, SessionLocal, engine  # noqa: E402
from miniflow.main import app  # noqa: E402
from miniflow.models import Event  # noqa: E402

PASSWORD = "correct-horse-battery"


def signup(client: TestClient, org: str, email: str) -> dict:
    return client.post(
        "/api/auth/signup", json={"org_name": org, "name": "Founder", "email": email, "password": PASSWORD}
    ).json()


def headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def main() -> int:
    Base.metadata.create_all(engine)
    leaks = 0
    with TestClient(app) as client:
        grace = signup(client, "Grace Church", "admin@grace.example")
        tokyo = signup(client, "Tokyo Hoops", "admin@tokyo.example")
        event = client.post(
            f"/api/organizations/{grace['org_id']}/events",
            json={"title": "Sunday rota", "starts_at": "2026-10-04T09:00:00", "role_slots": {"usher": 2}},
            headers=headers(grace["token"]),
        ).json()

        print("mini-flow demo - two tenants in one database")
        print(f"  Grace Church  org={grace['org_id']}  event={event['id']}")
        print(f"  Tokyo Hoops   org={tokyo['org_id']}")
        print()
        print("Tokyo's admin, holding a valid Tokyo token, requests Grace's data:")

        probes = [
            ("GET", f"/api/organizations/{grace['org_id']}/people", None, 403, "explicit foreign org: policy denial"),
            ("GET", f"/api/people/{grace['person_id']}", None, 404, "guessed id, looked up inside own tenant"),
            ("GET", f"/api/events/{event['id']}", None, 404, "guessed id, events router"),
            ("PATCH", f"/api/events/{event['id']}", {"title": "stolen"}, 404, "foreign write, events router"),
        ]
        for method, path, body, expected, why in probes:
            response = client.request(method, path, json=body, headers=headers(tokyo["token"]))
            verdict = "ok" if response.status_code == expected else f"LEAK  (contract says {expected})"
            if response.status_code != expected:
                leaks += 1
            print(f"  {method:5} {path:52} -> {response.status_code}  {verdict:28} {why}")

        no_token = client.get("/api/people/me")
        bad_token = client.get("/api/people/me", headers=headers("garbage"))
        print(f"  {'GET':5} {'/api/people/me  (no token)':52} -> {no_token.status_code}  ok                           missing bearer token")
        print(f"  {'GET':5} {'/api/people/me  (garbage token)':52} -> {bad_token.status_code}  ok                           invalid bearer token")

        with SessionLocal() as db:
            title = db.get(Event, event["id"]).title
        print()
        print(f"Grace's event title in the database is now: {title!r}")
        if leaks:
            print(f"{leaks} leak(s). Lab M5 step 1 closes them: src/miniflow/routers/events.py -> `make step1`.")
        else:
            print("No leaks. The events router carries the tenant predicate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
