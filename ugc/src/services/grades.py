from typing import Annotated, Any

from fast_depends import Depends, inject
from pymongo import MongoClient

from src.db.collections import Grade
from src.db.mongo import get_mongo_client


class GradeManager:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = Grade

    def find_one(self, condition: dict[str, Any]) -> Grade | None:
        result = self.collection.find_one(condition).run()
        return result

    def create(self, data: dict) -> Grade:
        grade = Grade.model_validate(data)

        exist_document = self.find_one({"user_id": grade.user_id, "film_id": grade.film_id})
        if exist_document is not None:
            return exist_document

        return grade.create()

    def update(self, grade: Grade, rating: int) -> Grade:
        grade.rating = rating
        grade.save_changes()

        return grade


@inject
def get_grade_manager(client: Annotated[MongoClient, Depends(get_mongo_client)]):
    return GradeManager(client=client)
