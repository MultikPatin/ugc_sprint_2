import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class EventModel(BaseModel):
    service: str = Field("Сервис фильмов")
    user: uuid.UUID | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    entity_type: str
    entity: str
    action: str
