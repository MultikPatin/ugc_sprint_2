from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field


class GradeModel(BaseModel):
    user_id: UUID | None = None
    film_id: str
    rating: int = Field(..., ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
