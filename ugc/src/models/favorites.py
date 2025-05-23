from datetime import datetime, timezone

from pydantic import BaseModel, Field


class FavoriteCreate(BaseModel):
    user_id: str
    film_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
