from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class Favorite(Document):
    user_id: str
    film_id: Indexed(str, unique=False)  # type:ignore
    timestamp: datetime

    class Settings:
        name = "favorites"
        use_state_management = True


class Grade(Document):
    user_id: str
    film_id: str
    rating: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "grades"
        use_state_management = True


class Review(Document):
    id: UUID = Field(default_factory=uuid4)  # type:ignore
    film_id: Indexed(str, unique=False)  # type:ignore
    author: UUID
    text: str
    rating: int = Field(default=0, ge=0, le=10)
    timestamp: datetime

    class Settings:
        name = "reviews"
        use_state_management = True
