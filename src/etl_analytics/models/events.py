import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class EventMessage:
    service: str
    user: uuid
    timestamp: datetime
    entity_type: str
    entity: str
    action: str
