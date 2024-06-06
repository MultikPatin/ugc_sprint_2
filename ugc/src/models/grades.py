from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class GradeCreate(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid4))
    film_id: str
    rating: int = Field(..., ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GradeUpdate(BaseModel):
    rating: int = Field(..., ge=0, le=10)
