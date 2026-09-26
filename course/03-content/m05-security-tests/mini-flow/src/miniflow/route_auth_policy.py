"""Reviewed authentication policy for every mounted API operation.

Keyed by FastAPI operation name, like SignUpFlow/api/route_auth_policy.py. Three classes suffice
at lab scale (SignUpFlow uses five). A unit test compares this mapping with the live route table
so a new route cannot ship without an explicit classification - that test is Lab M5 step 3.
"""

PUBLIC_OPERATIONS = {
    "health_check",
    "signup",
    "login",
    "accept_invitation",
}

MEMBER_OPERATIONS = {
    "get_current_person",
    "list_people",
    "get_person",
    "list_events",
    "get_event",
}

ADMIN_OPERATIONS = {
    "create_invitation",
    "update_person",
    "create_event",
}

ROUTE_AUTH_POLICY = {
    **{name: "public" for name in PUBLIC_OPERATIONS},
    **{name: "member" for name in MEMBER_OPERATIONS},
    **{name: "admin" for name in ADMIN_OPERATIONS},
}
