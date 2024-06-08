from datetime import datetime
from uuid import UUID, uuid4

from bunnet import Document, Indexed
from pydantic import Field


class Review(Document):
    id: UUID = Field(default_factory=uuid4)  # type:ignore
    film_id: Indexed(str, unique=False)  # type:ignore
    author: str
    text: str
    timestamp: datetime

    class Settings:
        name = "reviews"
        use_state_management = True
        state_management_save_previous = True


class FilmGrade(Document):
    user_id: str
    film_id: Indexed(str, unique=False)  # type:ignore
    rating: int
    timestamp: datetime

    class Settings:
        name = "films_grades"
        use_state_management = True
        state_management_save_previous = True


class ReviewGrade(Document):
    user_id: str
    review_id: Indexed(str, unique=False)  # type:ignore
    rating: int
    timestamp: datetime

    class Settings:
        name = "review_grades"
        use_state_management = True
        state_management_save_previous = True


class Favorite(Document):
    user_id: str
    film_id: Indexed(str, unique=False)  # type:ignore
    timestamp: datetime

    class Settings:
        name = "favorites"
        use_state_management = True
        state_management_save_previous = True
