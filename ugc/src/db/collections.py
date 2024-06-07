from datetime import datetime
from uuid import UUID, uuid4

from bunnet import Document, Indexed
from pydantic import Field


class Favorite(Document):
    user_id: str
    film_id: Indexed(str, unique=False)  # type:ignore
    timestamp: datetime

    class Settings:
        name = "favorites"
        use_state_management = True
        state_management_save_previous = True


class Grade(Document):
    user_id: str
    film_id: Indexed(str, unique=False)  # type:ignore
    rating: int
    timestamp: datetime

    class Settings:
        name = "grades"
        use_state_management = True
        state_management_save_previous = True


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
        state_management_save_previous = True
