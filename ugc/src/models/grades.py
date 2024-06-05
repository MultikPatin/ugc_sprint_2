from datetime import datetime, timezone
from uuid import UUID

from pydantic import Field, BaseModel


class GradeModel(BaseModel):
    user_id: UUID
    film_id: str
    rating: int = Field(..., ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
