from bunnet import init_bunnet
from pymongo import MongoClient

from src.core.config import settings
from src.db.collections import Favorite, Grade, Review


def get_mongo_client() -> MongoClient:
    return MongoClient(str(settings.mongodb.mongodb_uri))


class MongoDBInit:
    def __init__(self, mongodb_client: MongoClient):
        self.client = mongodb_client

    def create_collections(self):
        init_bunnet(database=self.client.ugc, document_models=[Grade, Review, Favorite])


def get_mongodb_init() -> MongoDBInit:
    return MongoDBInit(mongodb_client=get_mongo_client())
