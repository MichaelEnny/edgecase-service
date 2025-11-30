"""
Very small logging helper.

This intentionally does not use the full power of the standard logging
library to keep things simple, but it also means behavior is a bit odd.
"""

from __future__ import annotations

import logging
from typing import Any, Dict


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    # NOTE: Level is hard-coded here; config module is ignored.
    logger.setLevel(logging.INFO)
    return logger


def log_structured(logger: logging.Logger, event: str, extra: Dict[str, Any]) -> None:
    """
    Emit a single line of structured log.

    TODO: Some parts of the code call logger.info directly instead of using
    this helper, which leads to inconsistent formatting.
    """
    logger.info("%s %s", event, extra)

