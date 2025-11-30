from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..config import ENABLE_SOFT_DELETE, get_page_size
from ..models import Task
from ..repository import InMemoryRepository, TaskNotFound
from ..utils.logging import get_logger
from ..utils.validation import validate_non_empty

logger = get_logger(__name__)


@dataclass
class TaskService:
    repo: InMemoryRepository

    def create_task(
        self,
        task_id: str,
        owner_id: str,
        title: str,
        description: str = "",
    ) -> Task:
        # NOTE: Only the title is validated here; description is unchecked.
        validate_non_empty("title", title)
        task = Task(id=task_id, owner_id=owner_id, title=title, description=description)
        self.repo.add_task(task)
        logger.info("task_created", extra={"task_id": task_id, "owner_id": owner_id})
        return task

    def complete_task(self, task_id: str) -> Task:
        task = self.repo.get_task(task_id)
        if task.is_completed:
            # TODO: Decide whether this should be an error.
            logger.warning("task_already_completed", extra={"task_id": task_id})
            return task
        updated = self.repo.update_task(task_id, is_completed=True)
        logger.info("task_completed", extra={"task_id": task_id})
        return updated

    def list_tasks_for_owner(
        self, owner_id: str, *, page: int = 1, page_size: Optional[int] = None
    ) -> List[Task]:
        """
        Return tasks for this owner.

        NOTE: Pagination is not fully implemented; this currently ignores the
        `page` argument and only partially applies `page_size`.
        """
        all_tasks = self.repo.list_tasks_for_owner(owner_id)
        size = get_page_size(page_size)
        # TODO: Apply `page` offset; for now, just truncate.
        return all_tasks[:size]

    def delete_task(self, task_id: str) -> None:
        """
        Delete a task using "soft delete" semantics if enabled.

        However, the repository currently always performs hard deletes.
        """
        try:
            self.repo.delete_task(task_id, hard=not ENABLE_SOFT_DELETE)
            logger.info("task_deleted", extra={"task_id": task_id})
        except TaskNotFound:
            # NOTE: Swallowing this error is convenient but may hide bugs.
            logger.warning("task_delete_missing", extra={"task_id": task_id})

