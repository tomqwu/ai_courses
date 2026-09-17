"""Test configuration: one in-memory database, real JWTs, and the Lab M5 step gate.

Two things happen here that the lab depends on:

1. `pytest_configure` validates the playbook coverage manifest **before any test collects** -
   the mechanism of `SignUpFlow/tests/playbooks/plugin.py:37-45`. Once Lab M5 step 4 is done, a
   removed required scenario kills the whole run here, not in one test.
2. Tests marked `@pytest.mark.lab(step=N)` are the graded hooks. They are skipped unless
   `MINIFLOW_LAB_STEPS` names their step (`make step1`, `make lab-m5 STEPS=1,3`, ...). They are
   written against the *finished* app, so on the shipped starter each step is red when un-skipped.
"""

from __future__ import annotations

import os

# The app reads both at import time. Set them before anything imports `miniflow`.
os.environ.setdefault("MINIFLOW_DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("MINIFLOW_SECRET_KEY", "miniflow-test-secret-at-least-32-bytes-long")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from miniflow.db import Base, engine  # noqa: E402
from miniflow.main import app  # noqa: E402
from tests.playbooks.coverage import load_coverage_manifest, load_fixture  # noqa: E402

LAB_STEPS = {part.strip() for part in os.getenv("MINIFLOW_LAB_STEPS", "").split(",") if part.strip()}


def pytest_configure(config: pytest.Config) -> None:
    """Fail the run before collection when the manifest or fixture is invalid."""
    try:
        load_coverage_manifest(fixture=load_fixture())
    except ValueError as exc:
        raise pytest.UsageError(str(exc)) from exc


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip every lab hook whose step is not named in MINIFLOW_LAB_STEPS."""
    for item in items:
        marker = item.get_closest_marker("lab")
        if marker is None:
            continue
        step = str(marker.kwargs.get("step", marker.args[0] if marker.args else "?"))
        if step not in LAB_STEPS:
            item.add_marker(
                pytest.mark.skip(
                    reason=f"Lab M5 step {step} hook - run `make step{step}` to un-skip it"
                )
            )


@pytest.fixture(autouse=True)
def fresh_database() -> None:
    """Every test starts from empty tables on the shared in-memory engine."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
