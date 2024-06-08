from datetime import datetime, timezone

from pydantic import BaseModel, Field


class GradeFilmCreate(BaseModel):
    user_id: str
    film_id: str
    rating: int = Field(..., ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GradeFilmView(BaseModel):
    film_id: str
    rating_count: int
    rating_avg: float


class GradeReviewCreate(BaseModel):
    user_id: str
    review_id: str
    rating: int = Field(..., ge=0, le=10)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class GradeUpdate(BaseModel):
    rating: int = Field(..., ge=0, le=10)
