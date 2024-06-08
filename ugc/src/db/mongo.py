from bunnet import init_bunnet
from pymongo import MongoClient

from src.core.config import settings
from src.db.collections import Favorite, FilmGrade, Review, ReviewGrade


def get_mongo_client() -> MongoClient:
    return MongoClient(str(settings.mongodb.mongo_db_uri))


class MongoDBInit:
    def __init__(self, mongodb_client: MongoClient):
        self.client = mongodb_client

    def create_collections(self) -> None:
        init_bunnet(database=self.client.ugc, document_models=[Review, FilmGrade, ReviewGrade, Favorite])  # type:ignore


def get_mongodb_init() -> MongoDBInit:
    return MongoDBInit(mongodb_client=get_mongo_client())
