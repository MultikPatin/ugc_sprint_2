import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class EventModel(BaseModel):
    service: str = Field("Сервис фильмов")
    user: str = Field(default_factory=lambda: str(uuid.uuid4))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    entity_type: str
    entity: str
    action: str
