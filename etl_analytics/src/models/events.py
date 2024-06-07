from dataclasses import dataclass

from src.models.base import BaseMessage


@dataclass(frozen=True)
class EventMessage(BaseMessage):
    service: str
    entity_type: str
    entity: str
    action: str
