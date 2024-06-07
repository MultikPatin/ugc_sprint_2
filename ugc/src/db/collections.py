from datetime import datetime

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
    film_id: Indexed(str, unique=False)  # type:ignore
    author: str
    text: str
    rating: int = Field(default=0, ge=0, le=10)
    timestamp: datetime

    class Settings:
        name = "reviews"
        use_state_management = True
        state_management_save_previous = True
