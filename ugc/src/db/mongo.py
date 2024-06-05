from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings
from src.models.favorites import Favorite
from src.models.grades import Grade
from src.models.reviews import Review


def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(str(settings.mongodb.mongodb_uri))


class MongoDBInit:
    def __init__(self, mongodb_client: AsyncIOMotorClient):
        self.client = mongodb_client

    async def create_collections(self):
        await init_beanie(database=self.client.ugc, document_models=[Grade, Review, Favorite])


def get_mongodb_init() -> MongoDBInit:
    return MongoDBInit(mongodb_client=get_mongo_client())
