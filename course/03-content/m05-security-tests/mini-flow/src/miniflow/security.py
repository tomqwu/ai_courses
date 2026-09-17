"""JWT + password hashing (mirrors SignUpFlow/api/security.py at lab scale).

Tokens are HS256 with a 24h expiry and carry both `sub` (person id) and `org_id` - the
"Session And Tenant Binding" of SignUpFlow/docs/API_AUTHORIZATION.md. Passwords use stdlib
PBKDF2 so the starter has no compiled dependency; SignUpFlow uses bcrypt.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

SECRET_KEY = os.getenv("MINIFLOW_SECRET_KEY", "miniflow-dev-secret-change-me-before-any-deploy")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60
_PBKDF2_ROUNDS = 100_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _PBKDF2_ROUNDS)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


def verify_password(password: str, stored: str | None) -> bool:
    if not stored:
        return False
    _, salt, expected = stored.split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), _PBKDF2_ROUNDS)
    return hmac.compare_digest(digest.hex(), expected)


def create_access_token(claims: dict, expires_delta: timedelta | None = None) -> str:
    """Sign `claims` (callers pass `sub` and `org_id`) with an `exp` claim."""
    payload = dict(claims)
    payload["exp"] = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """Decode or raise 401 - an invalid bearer token is a credential failure, not a policy denial."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
