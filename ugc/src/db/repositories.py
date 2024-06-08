from datetime import datetime, timezone
from typing import Annotated, Any, Type

from bunnet import Document
from fast_depends import Depends, inject
from pymongo import MongoClient

from .collections import Favorite, FilmGrade, Review, ReviewGrade
from .mongo import get_mongo_client


class BaseRepository:
    def __init__(self, client: MongoClient, collection: Type[Document]):
        self.client = client
        self.collection = collection

    def get(self, document_id: Any) -> Document | None:
        document = self.collection.get(document_id)
        if document is None:
            return None
        return document.run()

    def find_one(self, condition: dict[str, Any]) -> Document | None:
        return self.collection.find_one(condition).run()

    def find_all(self, condition: dict[str, Any] | None = None) -> list[Document]:
        if condition is not None:
            return self.collection.find(condition).to_list()
        return self.collection.find().to_list()

    def create(self, data: dict[str, Any]) -> Document:
        document = self.collection.model_validate(data)
        return document.create()

    @staticmethod
    def delete(document: Document) -> None:
        document.delete()


class GradeRepository(BaseRepository):
    @staticmethod
    def update(grade: FilmGrade, rating: int) -> FilmGrade:
        grade.rating = rating
        grade.timestamp = datetime.now(timezone.utc)
        grade.save_changes()

        return grade


class FavoriteRepository(BaseRepository):
    pass


class ReviewRepository(BaseRepository):
    @staticmethod
    def update(review: Review, text: str) -> Review:
        review.text = text
        review.timestamp = datetime.now(timezone.utc)
        review.save_changes()

        return review


class ReviewGradeRepository(BaseRepository):
    @staticmethod
    def update(grade: ReviewGrade, rating: int) -> ReviewGrade:
        grade.rating = rating
        grade.timestamp = datetime.now(timezone.utc)
        grade.save_changes()

        return grade


@inject
def get_grade_repository(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> GradeRepository:
    return GradeRepository(client=client, collection=FilmGrade)


@inject
def get_favorite_repository(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> FavoriteRepository:
    return FavoriteRepository(client=client, collection=Favorite)


@inject
def get_review_repository(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> ReviewRepository:
    return ReviewRepository(client=client, collection=Review)


@inject
def get_review_grade_repository(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> ReviewGradeRepository:
    return ReviewGradeRepository(client=client, collection=ReviewGrade)
