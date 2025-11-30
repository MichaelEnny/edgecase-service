import os
import sys
import unittest


# Make src/ importable when running tests directly.
TEST_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from edgecase_service.repository import InMemoryRepository  # type: ignore  # noqa: E402
from edgecase_service.services.user_service import (  # type: ignore  # noqa: E402
    UserService,
)


class UserServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = InMemoryRepository()
        self.service = UserService(self.repo)

    def test_create_user_valid_email(self) -> None:
        user = self.service.create_user("u1", "user@example.com")
        self.assertEqual("u1", user.id)
        self.assertEqual("user@example.com", user.email)

    def test_create_user_invalid_email_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_user("u2", "not-an-email")

    def test_ensure_user_exists_creates_without_validation(self) -> None:
        # NOTE: This documents the current (inconsistent) behavior.
        user = self.service.ensure_user_exists("invalid-email")
        self.assertEqual("invalid-email", user.id)


if __name__ == "__main__":
    unittest.main()

