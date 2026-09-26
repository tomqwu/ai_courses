"""The shipped playbook fixture and manifest load and reject the obviously malformed.

What the starter's validator does *not* yet catch (a removed required scenario, a drill with no
manifest row, a status that lies about its tier) is Lab M5 step 4: tests/test_lab4_manifest.py.
"""

from __future__ import annotations

import json

import pytest

from tests.playbooks.coverage import (
    COVERAGE_MANIFEST_PATH,
    FIXTURE_PATH,
    REQUIRED_SCENARIOS,
    load_coverage_manifest,
    load_fixture,
)


def test_fixture_has_the_food_bank_shape_plus_one_drill():
    fixture = load_fixture()
    assert fixture["id"] == "food-bank"
    assert fixture["roles"] == {"packer": 2, "coordinator": 1}
    assert fixture["critical_role"] == "coordinator"
    assert [drill["id"] for drill in fixture["drills"]] == ["PF-04"]


def test_shipped_manifest_validates_and_names_every_required_scenario():
    manifest = load_coverage_manifest(fixture=load_fixture())
    assert manifest.version == 1
    assert REQUIRED_SCENARIOS <= manifest.scenario_ids


def test_shipped_manifest_is_honest_about_what_is_not_proven():
    """At least one row admits it is not automated - the lab's honesty requirement."""
    statuses = {s.id: s.status for s in load_coverage_manifest().scenarios}
    assert any(status != "automated" for status in statuses.values())


def test_manifest_rejects_unknown_status(tmp_path):
    data = json.loads(COVERAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    data["scenarios"][0]["status"] = "probably-fine"
    path = tmp_path / "coverage.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid playbook coverage manifest"):
        load_coverage_manifest(path)


def test_manifest_rejects_duplicate_ids(tmp_path):
    data = json.loads(COVERAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    data["scenarios"].append(dict(data["scenarios"][0]))
    path = tmp_path / "coverage.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="unique"):
        load_coverage_manifest(path)


def test_fixture_rejects_a_critical_role_with_no_headcount(tmp_path):
    data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    data["critical_role"] = "chaplain"
    path = tmp_path / "food-bank.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="critical_role"):
        load_fixture(path)
