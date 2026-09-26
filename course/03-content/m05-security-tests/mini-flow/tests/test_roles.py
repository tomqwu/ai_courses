"""Unit tests for the role vocabulary and password helpers (no HTTP, no database)."""

from __future__ import annotations

import pytest

from miniflow.roles import PERMISSION_ROLES, normalize_roles, qualifications_of
from miniflow.security import hash_password, verify_password


def test_permission_roles_are_exactly_two():
    assert PERMISSION_ROLES == {"admin", "volunteer"}


def test_normalize_defaults_to_volunteer_and_keeps_qualifications():
    assert normalize_roles(["usher", "greeter"]) == ["volunteer", "usher", "greeter"]


def test_normalize_puts_the_permission_role_first_and_deduplicates():
    assert normalize_roles(["usher", "admin", "usher"]) == ["admin", "usher"]


def test_normalize_rejects_two_permission_roles():
    with pytest.raises(ValueError, match="exactly one account access role"):
        normalize_roles(["volunteer", "admin"])


def test_normalize_rejects_non_identifier_qualifications():
    with pytest.raises(ValueError, match="lowercase identifiers"):
        normalize_roles(["volunteer", "Head Usher"])


def test_qualifications_of_strips_permission_roles():
    assert qualifications_of(["admin", "usher", "coach"]) == ["usher", "coach"]
    assert qualifications_of(["volunteer"]) == []


def test_password_roundtrip_and_salt():
    stored = hash_password("correct-horse-battery")
    assert stored != hash_password("correct-horse-battery")  # fresh salt every time
    assert verify_password("correct-horse-battery", stored)
    assert not verify_password("wrong", stored)
    assert not verify_password("anything", None)  # an invited account has no password yet
