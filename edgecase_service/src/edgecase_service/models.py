from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: str
    email: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Task:
    id: str
    owner_id: str
    title: str
    description: str = ""
    is_completed: bool = False
    # NOTE: README mentions soft-delete, but the model does not fully support it.
    deleted_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

