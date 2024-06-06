from datetime import datetime, timezone
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
        return self.collection.find_one(condition).run()

    def find_all(self, user_id: str) -> list[Grade]:
        return self.collection.find({"user_id": user_id}).to_list()

    def create(self, data: dict) -> Grade:
        grade = Grade.model_validate(data)

        exist_document = self.find_one({"user_id": grade.user_id, "film_id": grade.film_id})
        if exist_document is not None:
            return exist_document

        return grade.create()

    @staticmethod
    def update(grade: Grade, rating: int) -> Grade:
        grade.rating = rating
        grade.timestamp = datetime.now(timezone.utc)
        grade.save_changes()

        return grade

    @staticmethod
    def delete(grade: Grade) -> None:
        grade.delete()


@inject
def get_grade_manager(client: Annotated[MongoClient, Depends(get_mongo_client)]):
    return GradeManager(client=client)
