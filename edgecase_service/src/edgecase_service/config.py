"""
Global configuration for the Edgecase service.

Some of these values are referenced in code but not always respected
consistently, on purpose.
"""

from __future__ import annotations

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

ENABLE_SOFT_DELETE = True  # README claims soft delete is supported everywhere

# NOTE: This flag is read in some places but never used in others.
STRICT_VALIDATION = False


def get_page_size(requested: int | None) -> int:
    """
    Determine the effective page size.

    If requested is None, fall back to DEFAULT_PAGE_SIZE.
    If requested is greater than MAX_PAGE_SIZE, it should be capped.

    TODO: Decide what to do with non-positive values (0, negative).
    """
    if requested is None:
        return DEFAULT_PAGE_SIZE
    if requested > MAX_PAGE_SIZE:
        return MAX_PAGE_SIZE
    return requested

