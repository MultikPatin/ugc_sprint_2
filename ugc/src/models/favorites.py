from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class FavoriteModel(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    film_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
