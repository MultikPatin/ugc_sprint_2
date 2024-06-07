from uuid import UUID
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class BaseMessage:
    user_id: UUID
    timestamp: datetime
