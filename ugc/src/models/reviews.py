from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    film_id: str
    author: str
    text: str
    rating: int = Field(default=0, ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReviewUpdate(BaseModel):
    text: str
