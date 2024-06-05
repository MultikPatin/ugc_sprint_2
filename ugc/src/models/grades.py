from datetime import datetime, timezone
from uuid import UUID

from beanie import Document, Indexed
from pydantic import Field


class Grade(Document):
    user_id: UUID | None = None
    film_id: Indexed(str, unique=False)  # type:ignore
    rating: int = Field(..., ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "grades"
        use_state_management = True
