import os
import sys
import unittest


# Make src/ importable when running tests directly.
TEST_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from edgecase_service.api.http_handlers import (  # type: ignore  # noqa: E402
    HttpApp,
    Request,
)
from edgecase_service.repository import InMemoryRepository  # type: ignore  # noqa: E402


class TaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InMemoryRepository()
        self.app = HttpApp(repo=self.repo)

    def test_create_task_happy_path(self) -> None:
        # First create a user.
        req_user = Request({"email": "owner@example.com"})
        res_user = self.app.create_user(req_user)
        self.assertEqual(201, res_user.status_code)

        # Now create a task for that user.
        owner_id = res_user.json["id"]
        req_task = Request({"title": "First task"}, user_id=owner_id)
        res_task = self.app.create_task(req_task)

        self.assertEqual(201, res_task.status_code)
        self.assertEqual("First task", res_task.json["title"])

    def test_create_task_requires_title(self) -> None:
        req = Request({"title": "   "}, user_id="someone")
        res = self.app.create_task(req)
        self.assertEqual(422, res.status_code)

    def test_list_my_tasks_respects_page_size_partially(self) -> None:
        owner_id = "owner@example.com"
        self.app.create_user(Request({"email": owner_id}))

        # Create several tasks.
        for i in range(10):
            self.app.create_task(
                Request({"title": f"Task {i+1}"}, user_id=owner_id)
            )

        # Ask for a small page size; tests only the truncation behavior,
        # not the page offset.
        req = Request({"page": 1, "page_size": 3}, user_id=owner_id)
        res = self.app.list_my_tasks(req)

        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(res.json["items"]))


if __name__ == "__main__":
    unittest.main()

