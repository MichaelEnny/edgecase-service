from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..models import User
from ..repository import InMemoryRepository, UserNotFound
from ..utils.validation import validate_email


@dataclass
class UserService:
    repo: InMemoryRepository

    def create_user(self, user_id: str, email: str) -> User:
        # NOTE: We validate email here but not in all code paths that create users.
        validate_email(email)
        user = User(id=user_id, email=email)
        self.repo.add_user(user)
        return user

    def get_user(self, user_id: str) -> User:
        return self.repo.get_user(user_id)

    def deactivate_user(self, user_id: str) -> User:
        user = self.repo.get_user(user_id)
        updated = User(
            id=user.id,
            email=user.email,
            is_active=False,
            created_at=user.created_at,
        )
        self.repo.add_user(updated)
        return updated

    def find_user_by_email(self, email: str) -> Optional[User]:
        # TODO: Should this validate the email format first?
        return self.repo.find_user_by_email(email)

    def ensure_user_exists(self, email: str) -> User:
        """
        Return the user with this email, creating one if needed.

        NOTE: This entry point does not currently validate email and
        may create invalid users, which conflicts with create_user.
        """
        existing = self.repo.find_user_by_email(email)
        if existing:
            return existing
        # No validation here, intentionally.
        user = User(id=email, email=email)
        self.repo.add_user(user)
        return user

    def safe_get_user(self, user_id: str) -> Optional[User]:
        """
        Return the user if it exists, otherwise None.

        This is used by some code paths that want to be forgiving.
        """
        try:
            return self.repo.get_user(user_id)
        except UserNotFound:
            return None

