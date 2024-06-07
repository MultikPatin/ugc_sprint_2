from typing import Annotated, Any

from fast_depends import Depends, inject
from pymongo import MongoClient

from src.db.collections import Favorite
from src.db.mongo import get_mongo_client


class FavoriteManager:
    def __init__(self, client: MongoClient):
        self.client = client
        self.collection = Favorite

    def find_one(self, condition: dict[str, Any]) -> Favorite | None:
        return self.collection.find_one(condition).run()

    def find_all(self, user_id: str) -> list[Favorite]:
        return self.collection.find({"user_id": user_id}).to_list()

    def create(self, data: dict[str, Any]) -> Favorite:
        favorite = Favorite.model_validate(data)

        exist_document = self.find_one({"user_id": favorite.user_id, "film_id": favorite.film_id})
        if exist_document is not None:
            return exist_document

        return favorite.create()

    @staticmethod
    def delete(grade: Favorite) -> None:
        grade.delete()


@inject
def get_favorite_manager(client: Annotated[MongoClient, Depends(get_mongo_client)]) -> FavoriteManager:
    return FavoriteManager(client=client)
