import uuid
from datetime import datetime, timezone
from typing import TypeVar

from pydantic import BaseModel, Field


class BaseEventModel(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ClickEvent(BaseEventModel):
    service: str = Field("Сервис фильмов")
    user: str = Field(default_factory=lambda: str(uuid.uuid4))
    entity_type: str
    entity: str
    action: str


class FavoriteEvent(BaseEventModel):
    user_id: str
    film_id: str
    action: str


class GradeFilmEvent(BaseEventModel):
    user_id: str
    film_id: str
    rating: int


class GradeReviewEvent(BaseEventModel):
    user_id: str
    review_id: str
    rating: int


class ReviewEvent(BaseEventModel):
    author: str
    film_id: str
    action: str


EM = TypeVar("EM", bound=BaseEventModel)
