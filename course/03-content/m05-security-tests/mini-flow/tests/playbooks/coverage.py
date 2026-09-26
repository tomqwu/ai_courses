"""Machine-readable coverage manifest for the mini-flow playbook (mirrors
SignUpFlow/tests/playbooks/coverage.py at lab scale).

`load_coverage_manifest` runs from `pytest_configure` (tests/conftest.py), so a manifest that
fails validation kills the run before a single test collects - the same mechanism as
SignUpFlow/tests/playbooks/plugin.py:37-45.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

PLAYBOOK_DIR = Path(__file__).resolve().parent
COVERAGE_MANIFEST_PATH = PLAYBOOK_DIR / "coverage.json"
FIXTURE_PATH = PLAYBOOK_DIR / "examples" / "food-bank.json"

FIXTURE_REQUIRED_KEYS = frozenset(
    {"id", "version", "workflow", "name", "event", "secondary_event", "critical_role", "roles", "drills"}
)
# The scenarios every mini-flow manifest must carry: three shared journeys, the fixture's drill, and
# the behavioural-eval row. MF-05 is `blocked` on purpose: the honest statuses exist so a scenario
# nothing tests yet can be admitted rather than dropped, and dropping it fails collection.
REQUIRED_SCENARIOS = frozenset({"MF-01", "MF-02", "MF-03", "PF-04", "MF-05"})
EXECUTABLE_TIERS = frozenset({"unit", "api", "integration", "e2e"})

ScenarioId = Annotated[str, Field(pattern=r"^[A-Z]{2}-[0-9]{2}$")]
Identifier = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]{0,63}$")]
Detail = Annotated[str, Field(min_length=1, max_length=300, pattern=r"\S")]
Tier = Literal["unit", "api", "integration", "e2e", "manual"]
CoverageStatus = Literal["automated", "partial", "manual", "blocked"]


class ScenarioCoverage(BaseModel):
    """Trace one stable scenario id to its operation, oracle, tiers, status and evidence."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    id: ScenarioId
    actor: Identifier | list[Identifier]
    precondition: Detail
    operation: Detail
    expected: Detail
    tiers: list[Tier] = Field(min_length=1)
    status: CoverageStatus
    evidence: list[Detail] = Field(min_length=1)


class CoverageManifest(BaseModel):
    """Every required scenario, each with an honest status."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    version: Literal[1]
    scenarios: list[ScenarioCoverage] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_ids(self) -> Self:
        ids = [scenario.id for scenario in self.scenarios]
        if len(ids) != len(set(ids)):
            raise ValueError("scenario IDs must be unique")
        return self

    @property
    def scenario_ids(self) -> set[str]:
        return {scenario.id for scenario in self.scenarios}


def load_fixture(path: Path = FIXTURE_PATH) -> dict:
    """Load the playbook fixture and check its shape (SignUpFlow/tests/playbooks/examples/food-bank.json + drills)."""
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Invalid playbook fixture {path}: {exc}") from exc
    missing = FIXTURE_REQUIRED_KEYS - set(fixture)
    if missing:
        raise ValueError(f"Invalid playbook fixture {path}: missing keys {sorted(missing)}")
    if not isinstance(fixture["roles"], dict) or not fixture["roles"]:
        raise ValueError(f"Invalid playbook fixture {path}: roles must be a non-empty headcount map")
    if fixture["critical_role"] not in fixture["roles"]:
        raise ValueError(f"Invalid playbook fixture {path}: critical_role must be one of the roles")
    return fixture


def load_coverage_manifest(path: Path = COVERAGE_MANIFEST_PATH, fixture: dict | None = None) -> CoverageManifest:
    """Load and validate the manifest before playbook tests collect."""
    try:
        manifest = CoverageManifest.model_validate_json(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise ValueError(f"Invalid playbook coverage manifest {path}: {exc}") from exc
    return manifest
