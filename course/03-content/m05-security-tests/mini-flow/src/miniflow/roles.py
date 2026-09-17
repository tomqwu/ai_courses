"""Role policy: one permission role, any number of scheduling qualifications, one JSON array.

Mirrors SignUpFlow/api/roles.py. Permission roles are exactly one of `volunteer`/`admin`;
everything else in the array is a scheduling qualification (`usher`, `packer`, `coordinator`)
and must never be interpreted as a permission (SignUpFlow/AGENTS.md:60).
"""

from __future__ import annotations

import re
from collections.abc import Iterable

PERMISSION_ROLES = frozenset({"admin", "volunteer"})
QUALIFICATION_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


def normalize_roles(roles: Iterable[str]) -> list[str]:
    """Validate an admin-supplied role array and make the account access role explicit."""
    values = list(dict.fromkeys(value.strip().lower() for value in roles))
    permission_roles = [value for value in values if value in PERMISSION_ROLES]
    qualifications = [value for value in values if value not in PERMISSION_ROLES]
    if len(permission_roles) > 1:
        raise ValueError("Select exactly one account access role")
    for qualification in qualifications:
        if not QUALIFICATION_PATTERN.fullmatch(qualification):
            raise ValueError(
                "Qualifications must be lowercase identifiers using letters, numbers, and underscores"
            )
    return [permission_roles[0] if permission_roles else "volunteer", *qualifications]


def qualifications_of(roles: Iterable[str]) -> list[str]:
    """The scheduling half of the array - what the person *can do*, never what they *may do*."""
    return [role for role in roles if role not in PERMISSION_ROLES]
