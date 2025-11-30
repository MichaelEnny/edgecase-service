"""
Very small in-memory "database" layer.

The goal here is to have just enough behavior to test reasoning,
not to be a perfect repository abstraction.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Dict, List, Optional

from .models import User, Task


class RepositoryError(Exception):
    pass


class UserNotFound(RepositoryError):
    pass


class TaskNotFound(RepositoryError):
    pass


class InMemoryRepository:
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}
        self._tasks: Dict[str, Task] = {}

    # --- user operations -------------------------------------------------

    def add_user(self, user: User) -> None:
        # NOTE: No duplicate email checks, on purpose.
        self._users[user.id] = user

    def get_user(self, user_id: str) -> User:
        try:
            return self._users[user_id]
        except KeyError as exc:
            raise UserNotFound(f"user {user_id!r} not found") from exc

    def find_user_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email.lower() == email.lower():
                return user
        return None

    # --- task operations -------------------------------------------------

    def add_task(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get_task(self, task_id: str) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as exc:
            raise TaskNotFound(f"task {task_id!r} not found") from exc

    def update_task(self, task_id: str, **fields) -> Task:
        task = self.get_task(task_id)
        # NOTE: No validation that fields are allowed.
        updated = replace(task, **fields)
        self._tasks[task_id] = updated
        return updated

    def list_tasks_for_owner(self, owner_id: str) -> List[Task]:
        # NOTE: This currently returns deleted tasks as well.
        return [t for t in self._tasks.values() if t.owner_id == owner_id]

    def delete_task(self, task_id: str, *, hard: bool = False) -> None:
        """
        Delete a task.

        If hard is True, remove it from the store.
        Otherwise, it should be a soft delete.

        TODO: Implementation currently does a hard delete regardless of config.
        """
        if hard:
            self._tasks.pop(task_id, None)
        else:
            # For now, we just also do a hard delete.
            # A soft-delete implementation would set deleted_at instead.
            self._tasks.pop(task_id, None)

