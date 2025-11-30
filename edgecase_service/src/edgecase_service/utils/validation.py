"""
Validation helpers.

These are intentionally incomplete and inconsistently used.
"""

from __future__ import annotations

import re


EMAIL_RE = re.compile(r"^[^@]+@[^@]+$")


def validate_email(email: str) -> None:
    """
    Raise ValueError if the email looks invalid.

    NOTE: This is a very rough check and does not handle many valid addresses.
    """
    if not EMAIL_RE.match(email):
        raise ValueError(f"invalid email: {email!r}")


def validate_non_empty(field: str, value: str) -> None:
    """
    Ensure the provided string is non-empty.

    TODO: Decide whether whitespace-only strings should be allowed.
    """
    if not value:
        raise ValueError(f"{field} must not be empty")

