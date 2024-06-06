from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ReviewModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    film_id: str
    author: UUID = Field(default_factory=uuid4)
    text: str
    rating: int = Field(default=0, ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
