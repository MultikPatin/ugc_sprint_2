from typing import Annotated, Any

from fast_depends import inject, Depends
from pymongo import MongoClient

from src.db.collections import Grade
from src.db.mongo import get_mongo_client


class GradeManager:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = Grade

    def exist(self, condition: dict[str, Any]) -> Grade | None:
        result = self.collection.find_one(condition).run()
        return result

    def create(self, data: dict[str, Any]):
        document = self.collection(**data)

        exist_document = self.exist({"user_id": document.user_id, "film_id": document.film_id})
        if exist_document is not None:
            return exist_document

        return document.create()


@inject
def get_grade_manager(
        client: Annotated[MongoClient, Depends(get_mongo_client)]
):
    return GradeManager(client=client)
