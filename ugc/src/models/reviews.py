from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    film_id: str
    author: str
    text: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReviewUpdate(BaseModel):
    text: str
