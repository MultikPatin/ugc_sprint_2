from datetime import datetime, timezone
from typing import Annotated, Any, Type

from bunnet import Document
from fast_depends import Depends, inject
from pymongo import MongoClient

from .collections import Favorite, Grade, Review
from .mongo import get_mongo_client


class BaseRepository:
    def __init__(self, client: MongoClient, collection: Type[Document]):
        self.client = client
        self.collection = collection

    def find_one(self, condition: dict[str, Any]) -> Document | None:
        return self.collection.find_one(condition).run()

    def find_all(self, condition: dict[str, Any] | None = None) -> list[Document]:
        if condition is not None:
            return self.collection.find(condition).to_list()
        return self.collection.find().to_list()

    def create(self, data: dict[str, Any]) -> Document:
        document = self.collection.model_validate(data)

        exist_document = self.find_one({"user_id": document.user_id, "film_id": document.film_id})
        if exist_document is not None:
            return exist_document

        return document.create()

    @staticmethod
    def delete(document: Document) -> None:
        document.delete()


class GradeRepository(BaseRepository):
    @staticmethod
    def update(grade: Document, rating: int) -> Document:
        grade.rating = rating
        grade.timestamp = datetime.now(timezone.utc)
        grade.save_changes()

        return grade


class FavoriteRepository(BaseRepository):
    pass


class ReviewRepository(BaseRepository):
    def create(self, data: dict[str, Any]) -> Document:
        document = self.collection.model_validate(data)

        exist_document = self.find_one({"author": document.author, "film_id": document.film_id})
        if exist_document is not None:
            return exist_document

        return document.create()

    @staticmethod
    def update(review: Document, text: str) -> Document:
        review.text = text
        review.timestamp = datetime.now(timezone.utc)
        review.save_changes()

        return review


@inject
def get_grade_repository(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> GradeRepository:
    return GradeRepository(client=client, collection=Grade)


@inject
def get_favorite_repository(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> FavoriteRepository:
    return FavoriteRepository(client=client, collection=Favorite)


@inject
def get_review_repository(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> ReviewRepository:
    return ReviewRepository(client=client, collection=Review)
