"""Lab M5 step 4 - the coverage manifest fails validation when a required scenario is removed.

Un-skip with `make step4`. On the shipped starter four tests are RED: `load_coverage_manifest`
in tests/playbooks/coverage.py parses the JSON shape and nothing else. It does not check
`REQUIRED_SCENARIOS`, does not check that every fixture drill has a manifest row, and
`ScenarioCoverage` has no status/tier coupling rule. The reference is
SignUpFlow/tests/playbooks/coverage.py:42-46 (coupling) and the required-scenario check that makes
"Removing a ... required scenario ... fails collection" true (SignUpFlow/docs/playbooks/README.md:84-87).

Once the loader is fixed, prove it live: delete the MF-03 row from tests/playbooks/coverage.json,
run `make lab-m5`, and watch collection die in conftest's pytest_configure. Restore it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.playbooks.coverage import COVERAGE_MANIFEST_PATH, load_coverage_manifest, load_fixture

pytestmark = pytest.mark.lab(step=4)


def _manifest() -> dict:
    return json.loads(COVERAGE_MANIFEST_PATH.read_text(encoding="utf-8"))


def _write(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "coverage.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def _without(data: dict, scenario_id: str) -> dict:
    data["scenarios"] = [row for row in data["scenarios"] if row["id"] != scenario_id]
    return data


def test_shipped_manifest_and_fixture_validate():
    manifest = load_coverage_manifest(fixture=load_fixture())
    assert {"MF-01", "MF-02", "MF-03", "PF-04"} <= manifest.scenario_ids


def test_removing_a_required_scenario_fails(tmp_path):
    """RED on the starter: the loader never looks at REQUIRED_SCENARIOS."""
    path = _write(tmp_path, _without(_manifest(), "MF-03"))
    with pytest.raises(ValueError, match="MF-03"):
        load_coverage_manifest(path, fixture=load_fixture())


def test_every_fixture_drill_needs_a_manifest_row(tmp_path):
    """RED on the starter: the fixture's PF-04 drill is not cross-checked against the manifest."""
    path = _write(tmp_path, _without(_manifest(), "PF-04"))
    with pytest.raises(ValueError, match="PF-04"):
        load_coverage_manifest(path, fixture=load_fixture())


def test_automated_status_requires_an_executable_tier(tmp_path):
    """RED on the starter: no coupling rule (SignUpFlow/tests/playbooks/coverage.py:42-44)."""
    data = _manifest()
    data["scenarios"][0].update(status="automated", tiers=["manual"])
    with pytest.raises(ValueError, match="executable tier"):
        load_coverage_manifest(_write(tmp_path, data))


def test_blocked_status_requires_the_manual_tier(tmp_path):
    """RED on the starter: a blocked row can pretend to be executable."""
    data = _manifest()
    data["scenarios"][0].update(status="blocked", tiers=["api"])
    with pytest.raises(ValueError, match="manual tier"):
        load_coverage_manifest(_write(tmp_path, data))


def test_unknown_status_is_still_rejected(tmp_path):
    data = _manifest()
    data["scenarios"][0]["status"] = "hopefully"
    with pytest.raises(ValueError):
        load_coverage_manifest(_write(tmp_path, data))
