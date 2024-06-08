from uuid import UUID
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReviewMessage:
    id: UUID
    film_id: UUID
    author: UUID
    text: str
    rating: int
    timestamp: datetime
