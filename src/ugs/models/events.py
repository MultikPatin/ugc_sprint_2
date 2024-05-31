import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class EventModel(BaseModel):
    service: str = Field("Сервис фильмов")
    user: uuid.UUID | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    entity_type: str
    entity: str
    action: str
