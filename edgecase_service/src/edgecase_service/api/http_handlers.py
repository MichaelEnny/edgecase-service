from __future__ import annotations

from typing import Any, Dict, List

from ..repository import InMemoryRepository
from ..services.task_service import TaskService
from ..services.user_service import UserService


class Request:
    """
    Tiny stand-in for an HTTP request object.

    Only includes the fields we need for our tests.
    """

    def __init__(self, json: Dict[str, Any], user_id: str | None = None) -> None:
        self.json = json
        self.user_id = user_id


class Response:
    """
    Tiny stand-in for an HTTP response object.
    """

    def __init__(self, status_code: int, json: Dict[str, Any]) -> None:
        self.status_code = status_code
        self.json = json


class HttpApp:
    """
    Group of handler functions.

    This is *not* a real web server; it's just enough to enable unit tests
    and evaluation tasks around HTTP-style behavior.
    """

    def __init__(self, repo: InMemoryRepository | None = None) -> None:
        self.repo = repo or InMemoryRepository()
        self.user_service = UserService(self.repo)
        self.task_service = TaskService(self.repo)

    # NOTE: Handlers use slightly different conventions about errors and status codes.

    def create_user(self, req: Request) -> Response:
        email = req.json.get("email", "")
        # On error, we currently return 400 with a simple message.
        if not email:
            return Response(400, {"error": "email is required"})

        user = self.user_service.create_user(user_id=email, email=email)
        return Response(201, {"id": user.id, "email": user.email})

    def create_task(self, req: Request) -> Response:
        """
        Create a task for the current user.

        NOTE: This handler assumes req.user_id is populated and does not
        verify user existence.
        """
        if not req.user_id:
            # TODO: Decide whether this should be 401 or 403.
            return Response(400, {"error": "user_id missing"})

        title = req.json.get("title", "").strip()
        if not title:
            return Response(422, {"error": "title is required"})

        task = self.task_service.create_task(
            task_id=f"{req.user_id}:{title}",
            owner_id=req.user_id,
            title=title,
            description=req.json.get("description", ""),
        )
        return Response(
            201,
            {
                "id": task.id,
                "owner_id": task.owner_id,
                "title": task.title,
                "description": task.description,
            },
        )

    def list_my_tasks(self, req: Request) -> Response:
        if not req.user_id:
            return Response(401, {"error": "authentication required"})

        # NOTE: Page and page_size are accepted but not fully respected downstream.
        page = int(req.json.get("page", 1))
        page_size = req.json.get("page_size")
        page_size_int = int(page_size) if page_size is not None else None

        tasks = self.task_service.list_tasks_for_owner(
            owner_id=req.user_id,
            page=page,
            page_size=page_size_int,
        )
        items: List[Dict[str, Any]] = []
        for t in tasks:
            items.append(
                {
                    "id": t.id,
                    "title": t.title,
                    "is_completed": t.is_completed,
                }
            )
        return Response(200, {"items": items})

