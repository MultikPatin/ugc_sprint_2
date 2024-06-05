from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field


class Favorite(Document):
    user_id: UUID = Field(default_factory=uuid4)
    film_id: Indexed(str, unique=False)  # type:ignore
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "favorites"
        use_state_management = True
