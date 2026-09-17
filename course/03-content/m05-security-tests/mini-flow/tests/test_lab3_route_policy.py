"""Lab M5 step 3 - the route policy is compared to the LIVE route table, and wiring is checked.

Un-skip with `make step3`. On the shipped starter one test is RED: `update_event` is mounted
(src/miniflow/routers/events.py) but never classified in src/miniflow/route_auth_policy.py.
The mechanism is SignUpFlow/tests/unit/test_api_route_auth_policy.py: set equality against the
app (missing + stale), then a walk of each route's dependency tree (miswired).

Once the policy is complete, prove the guard: miswire `create_event` to `get_current_user`, run
`make step3`, record the red, restore, record the green.
"""

from __future__ import annotations

import pytest
from fastapi.routing import APIRoute, RouteContext, iter_route_contexts

from miniflow.main import app
from miniflow.route_auth_policy import ROUTE_AUTH_POLICY

pytestmark = pytest.mark.lab(step=3)

ADMIN_DEPENDENCY = "get_current_admin_user"
MEMBER_DEPENDENCY = "get_current_user"


def _dependency_names(route: RouteContext) -> set[str]:
    names: set[str] = set()
    assert route.dependant is not None
    pending = list(route.dependant.dependencies)
    while pending:
        dependency = pending.pop()
        names.add(getattr(dependency.call, "__name__", str(dependency.call)))
        pending.extend(dependency.dependencies)
    return names


def _live_routes() -> dict[str, RouteContext]:
    return {
        route.name: route
        for route in iter_route_contexts(app.routes)
        if isinstance(route.original_route, APIRoute)
        and (route.path.startswith("/api") or route.path == "/health")
    }


def test_every_mounted_route_is_classified():
    """RED on the starter: {'update_event'} is mounted but unclassified."""
    missing = set(_live_routes()) - set(ROUTE_AUTH_POLICY)
    assert missing == set(), f"mounted but unclassified: {sorted(missing)}"


def test_policy_names_no_stale_routes():
    stale = set(ROUTE_AUTH_POLICY) - set(_live_routes())
    assert stale == set(), f"classified but not mounted: {sorted(stale)}"


def test_every_classified_route_is_wired_as_its_policy_says():
    """Miswire one admin route to get_current_user and this is the test that goes red."""
    live = _live_routes()
    for operation, policy in ROUTE_AUTH_POLICY.items():
        if operation not in live:
            continue  # reported by test_every_mounted_route_is_classified's sibling
        dependencies = _dependency_names(live[operation])
        if policy == "admin":
            assert ADMIN_DEPENDENCY in dependencies, operation
        elif policy == "member":
            assert MEMBER_DEPENDENCY in dependencies, operation
            assert ADMIN_DEPENDENCY not in dependencies, operation
        else:
            assert policy == "public", operation
            assert not dependencies & {MEMBER_DEPENDENCY, ADMIN_DEPENDENCY}, operation


def test_policy_uses_only_the_three_classes():
    assert set(ROUTE_AUTH_POLICY.values()) <= {"public", "member", "admin"}
