from uuid import UUID
from dataclasses import dataclass

from src.models.base import BaseMessage


@dataclass(frozen=True)
class FavoriteMessage(BaseMessage):
    film_id: UUID
